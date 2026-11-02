"""Matrice di design e serializzazione dei modelli di imputazione."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Sequence

import joblib
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.metrics import normalized_mutual_info_score

from ..logging_setup import get_logger

log = get_logger(__name__)

BUNDLE_VERSION = "7.0"

# Target studiati, e quelli effettivamente imputati in produzione.
TARGETS = ("nkill", "nwound")
IMPUTED_TARGETS = ("nkill",)

VALID_ENCODINGS = ("onehot", "native")
OTHER_LEVEL = "Other"

# Classificate per semantica di dominio, non per dtype.
CATEGORICAL_FEATURES = [
    "region", "attacktype1", "weaptype1", "targtype1",
    "weapsubtype1", "targsubtype1", "propextent", "specificity",
]
BINARY_FEATURES = [
    "suicide", "multiple", "success", "extended", "property",
    "crit1", "crit2", "crit3", "vicinity", "guncertain1",
]
CONTINUOUS_FEATURES = ["nperps", "iyear"]
RAW_FEATURES = CATEGORICAL_FEATURES + BINARY_FEATURES + CONTINUOUS_FEATURES

# Le binarie sono codificate come le categoriche: il mancante resta una riga
# di zeri.
ENCODED_FEATURES = CATEGORICAL_FEATURES + BINARY_FEATURES

WINSOR_QUANTILE = 0.995
DEFAULT_MIN_FREQUENCY = 0.005

# Feature selection dinamica
MIN_COMPLETENESS = 0.85       # quota minima di valori noti per usare una feature
REDUNDANCY_THRESHOLD = 0.90   # oltre questa associazione ne sopravvive una sola
SELECTION_SAMPLE = 30_000     # righe campionate per stimare le associazioni
MI_BINS = 20                  # bin per discretizzare le continue prima della MI
MI_TIE_TOLERANCE = 0.05       # sotto questo scarto la MI non discrimina


# Nomi delle colonne
def source_variable(feature_name: str) -> str:
    """Risale dalla colonna della matrice alla variabile di origine."""
    for source in sorted(ENCODED_FEATURES, key=len, reverse=True):
        if feature_name.startswith(source + "_"):
            return source
    return feature_name


def aggregate_importance(importances, feature_names) -> pd.Series:
    """Somma le importance delle dummy appartenenti alla stessa variabile."""
    series = pd.Series(np.asarray(importances, dtype=float), index=list(feature_names))
    return (
        series.groupby(series.index.map(source_variable))
        .sum()
        .sort_values(ascending=False)
    )


# Matrice di design
def _as_level_string(series: pd.Series) -> pd.Series:
    """Normalizza una categorica a stringa in modo deterministico."""
    return pd.to_numeric(series, errors="coerce").round().astype("Int64").astype("string")


# Feature selection: completezza, ridondanza, informazione mutua
def _nominal_codes(series: pd.Series) -> np.ndarray:
    """Codici interi di una nominale, con i mancanti a -1."""
    return pd.factorize(series, use_na_sentinel=True)[0]


def _ordinal_codes(series: pd.Series, bins: int = MI_BINS) -> np.ndarray:
    """Discretizza una continua in quantili, per poterla usare con la MI."""
    numeric = pd.to_numeric(series, errors="coerce")
    try:
        return pd.qcut(numeric, q=bins, duplicates="drop").cat.codes.to_numpy()
    except (ValueError, IndexError):
        return _nominal_codes(numeric)


def _codes(series: pd.Series, continuous: bool) -> np.ndarray:
    return _ordinal_codes(series) if continuous else _nominal_codes(series)


def cramers_v(a: pd.Series, b: pd.Series) -> float:
    """Associazione fra due nominali, corretta per il bias da molti livelli."""
    table = pd.crosstab(_nominal_codes(a), _nominal_codes(b))
    if min(table.shape) < 2:
        return 0.0
    n = float(table.to_numpy().sum())
    chi2 = float(chi2_contingency(table, correction=False)[0])
    rows, cols = table.shape
    phi2 = max(0.0, chi2 / n - (cols - 1) * (rows - 1) / (n - 1))
    rows_c = rows - (rows - 1) ** 2 / (n - 1)
    cols_c = cols - (cols - 1) ** 2 / (n - 1)
    denominator = min(rows_c - 1, cols_c - 1)
    return float(np.sqrt(phi2 / denominator)) if denominator > 0 else 0.0


def _pearson(a: pd.Series, b: pd.Series) -> float:
    return pd.to_numeric(a, errors="coerce").corr(pd.to_numeric(b, errors="coerce"))


def target_mutual_information(feature: pd.Series, y_codes: np.ndarray, continuous: bool) -> float:
    """NMI fra una feature e il target discretizzato."""
    return float(normalized_mutual_info_score(y_codes, _codes(feature, continuous)))


def filter_by_completeness(
    df: pd.DataFrame, candidates: Sequence[str], threshold: float = MIN_COMPLETENESS
) -> list[str]:
    """Tiene le sole feature con almeno 'threshold' di valori noti."""
    kept: list[str] = []
    for col in candidates:
        completeness = float(df[col].notna().mean())
        if completeness >= threshold:
            kept.append(col)
        else:
            log.info(
                "  scartata per completezza: %-14s %5.1f%% noti (soglia %.0f%%)",
                col, 100 * completeness, 100 * threshold,
            )
    return kept


def drop_redundant(
    df: pd.DataFrame,
    features: Sequence[str],
    y: pd.Series,
    threshold: float = REDUNDANCY_THRESHOLD,
    sample: int = SELECTION_SAMPLE,
    random_state: int = 42,
) -> list[str]:
    """Di ogni coppia ridondante tiene la feature piu' informativa sul target.

    Pearson fra continue, V di Cramer fra nominali.
    """
    if len(df) > sample:
        df = df.sample(sample, random_state=random_state)
        y = y.loc[df.index]

    continuous = [c for c in features if c in CONTINUOUS_FEATURES]
    nominal = [c for c in features if c in ENCODED_FEATURES]
    y_codes = _ordinal_codes(y)
    strength = {c: target_mutual_information(df[c], y_codes, c in set(continuous))
                for c in features}

    dropped: set[str] = set()

    def scan(columns: Sequence[str], measure) -> None:
        for i, first in enumerate(columns):
            for second in columns[i + 1:]:
                if first in dropped or second in dropped:
                    continue
                # Colonna costante: l'associazione non e' definita
                if df[first].nunique(dropna=True) < 2 or df[second].nunique(dropna=True) < 2:
                    continue
                value = measure(df[first], df[second])
                if not np.isfinite(value) or abs(value) < threshold:
                    continue

                best = max(strength[first], strength[second])
                gap = abs(strength[first] - strength[second]) / best if best > 0 else 0.0
                if gap > MI_TIE_TOLERANCE:
                    loser = first if strength[first] < strength[second] else second
                    reason = "MI"
                else:
                    loser = (first if df[first].nunique(dropna=True)
                             <= df[second].nunique(dropna=True) else second)
                    reason = "granularita'"

                keeper = second if loser == first else first
                dropped.add(loser)
                log.info(
                    "  scartata per ridondanza: %-14s ~ %-14s (%.3f) | MI %.4f contro "
                    "%.4f, decide %s",
                    loser, keeper, abs(value), strength[loser], strength[keeper], reason,
                )

    scan(nominal, cramers_v)
    scan(continuous, _pearson)
    return [c for c in features if c not in dropped]


def fit_preprocessing(
    df: pd.DataFrame,
    y,
    encoding: str = "onehot",
    min_frequency: float = DEFAULT_MIN_FREQUENCY,
    min_completeness: float = MIN_COMPLETENESS,
    redundancy_threshold: float = REDUNDANCY_THRESHOLD,
    selection_sample: int = SELECTION_SAMPLE,
    random_state: int = 42,
) -> dict:
    """Seleziona le feature e stima mediane, cap e livelli sul solo training set."""

    if encoding not in VALID_ENCODINGS:
        raise ValueError(f"encoding non valido: {encoding}")

    target = y if isinstance(y, pd.Series) else pd.Series(np.asarray(y), index=df.index)
    target = target.reindex(df.index)

    candidates = [c for c in RAW_FEATURES if c in df.columns]
    survivors = filter_by_completeness(df, candidates, min_completeness)
    selected = drop_redundant(
        df, survivors, target, redundancy_threshold, selection_sample, random_state
    )
    if not selected:
        raise ValueError(
            "nessuna feature ha superato la selezione: allentare min_completeness "
            f"({min_completeness:.2f}) o redundancy_threshold ({redundancy_threshold:.2f})"
        )
    log.info(
        "  feature selection: %d candidate -> %d selezionate (%s)",
        len(candidates), len(selected), ", ".join(selected),
    )

    params = {
        "encoding": encoding,
        "min_frequency": float(min_frequency),
        "selected_features": list(selected),
        "medians": {},
        "winsor_caps": {},
        "categories": {},
    }

    n = len(df)
    for col in selected:
        if col in CONTINUOUS_FEATURES:
            series = pd.to_numeric(df[col], errors="coerce")
            params["medians"][col] = float(series.median())
            params["winsor_caps"][col] = float(series.quantile(WINSOR_QUANTILE))
        elif col in ENCODED_FEATURES:
            frequencies = _as_level_string(df[col]).value_counts(dropna=True) / max(n, 1)
            kept = frequencies[frequencies >= min_frequency].index.tolist()
            params["categories"][col] = sorted(kept) + [OTHER_LEVEL]
    return params


def build_design_matrix(
    df: pd.DataFrame,
    preprocessing: dict,
    feature_names: list[str] | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Costruisce la matrice di design con i parametri congelati in training."""

    encoding = preprocessing.get("encoding", "onehot")
    categories = preprocessing.get("categories", {})

    # Solo le feature superstiti alla selezione: il resto viene ignorato
    selected = preprocessing.get("selected_features") or RAW_FEATURES
    available = [c for c in selected if c in df.columns]
    absent = [c for c in selected if c not in df.columns]
    work = df[available].copy()

    # Continue: winsorizzazione, indicatore di mancanza, riempimento con la mediana
    for col in CONTINUOUS_FEATURES:
        if col not in work.columns:
            continue
        series = pd.to_numeric(work[col], errors="coerce")
        work[f"{col}_is_missing"] = series.isna().astype("int8")
        cap = preprocessing.get("winsor_caps", {}).get(col)
        if cap is not None:
            series = series.clip(upper=cap)
        median = preprocessing.get("medians", {}).get(col)
        work[col] = series.fillna(median) if median is not None else series

    # Categoriche: livelli congelati, i rari finiscono in "Other"
    to_encode = [c for c in ENCODED_FEATURES if c in work.columns]
    grouped_counts = {}
    for col in to_encode:
        levels = _as_level_string(work[col])
        allowed = categories.get(col)
        if allowed is not None:
            known = set(allowed) - {OTHER_LEVEL}
            rare = levels.notna() & ~levels.isin(known)
            grouped_counts[col] = int(rare.sum())
            levels = levels.mask(rare, OTHER_LEVEL)
        work[col] = levels

    # Codifica
    if encoding == "onehot":
        X = pd.get_dummies(work, columns=to_encode, dummy_na=False, dtype="int8")
    elif encoding == "native":
        X = work.copy()
        for col in to_encode:
            allowed = categories.get(col) or sorted(work[col].dropna().unique().tolist())
            X[col] = pd.Categorical(work[col], categories=allowed)
    else:
        raise ValueError(f"encoding non valido: {encoding}")

    # Riallineamento allo schema di training
    info = {
        "missing_columns": [],
        "unseen_columns": [],
        "grouped_into_other": grouped_counts,
        "missing_features": absent,
    }
    if feature_names is not None:
        info["missing_columns"] = sorted(set(feature_names) - set(X.columns))
        info["unseen_columns"] = sorted(set(X.columns) - set(feature_names))
        if encoding == "onehot":
            X = X.reindex(columns=feature_names, fill_value=0)
        else:
            if info["missing_columns"]:
                raise ValueError(
                    f"Codifica nativa: colonne assenti in inferenza {info['missing_columns']}"
                )
            X = X[feature_names]
    return X, info



# Serializzazione
_REQUIRED_KEYS = {
    "bundle_version", "target", "model_type", "estimator", "feature_names",
    "preprocessing", "trained_at", "training_rows", "validation_metrics",
}


def save_bundle(
    path: str,
    target: str,
    model_type: str,
    estimator,
    feature_names,
    preprocessing: dict,
    validation_metrics: dict,
    training_rows: int,
    best_params: dict | None = None,
    source_file: str = "",
    notes: str = "",
) -> str:
    """Salva lo stimatore cosi' com'e', senza incapsularlo."""
    if not hasattr(estimator, "predict"):
        raise ValueError("lo stimatore non espone predict()")
    if preprocessing.get("encoding") not in VALID_ENCODINGS:
        raise ValueError("preprocessing privo di una codifica valida")

    bundle = {
        "bundle_version": BUNDLE_VERSION,
        "target": target,
        "model_type": model_type,
        "estimator": estimator,
        "feature_names": list(feature_names),
        "preprocessing": preprocessing,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "training_rows": int(training_rows),
        "validation_metrics": validation_metrics,
        "best_params": best_params or {},
        "source_file": source_file,
        "notes": notes,
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    joblib.dump(bundle, path, compress=3)
    return path


def load_bundle(path: str) -> dict:
    """Carica un bundle e ne verifica versione e chiavi obbligatorie."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Bundle non trovato: {path}")
    bundle = joblib.load(path)

    missing = _REQUIRED_KEYS - set(bundle)
    if missing:
        raise ValueError(f"Bundle {path} non conforme, chiavi mancanti: {sorted(missing)}")
    if bundle["bundle_version"] != BUNDLE_VERSION:
        raise ValueError(
            f"Bundle {path} versione {bundle['bundle_version']}, atteso {BUNDLE_VERSION}"
        )
    if not hasattr(bundle["estimator"], "predict"):
        raise ValueError(f"Bundle {path}: lo stimatore non espone predict()")
    return bundle


def bundle_path(model_dir: str, target: str) -> str:
    return os.path.join(model_dir, f"imputer_{target}.joblib")
