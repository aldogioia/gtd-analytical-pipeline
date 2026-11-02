"""Addestra e valuta il modello hurdle a due stadi, un modello per target."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from gtd_pipeline.config import Settings
from gtd_pipeline.db.connection import DatabaseManager
from gtd_pipeline.logging_setup import get_logger
from gtd_pipeline.models import gtd_ml
from gtd_pipeline.models.zero_inflated import (
    DETERMINISTIC_LOWER_BOUND, ZeroInflatedCountRegressor,
)

log = get_logger(__name__)


# Configurazione e criteri di accettazione
RANDOM_STATE: int = 42
HOLDOUT_SIZE: float = 0.20
ENCODING: str = "native"
MIN_FREQUENCY: float = gtd_ml.DEFAULT_MIN_FREQUENCY

MIN_BASELINE_GAIN_PCT: float = 10.0
MAX_ABS_TOTAL_BIAS_PCT: float = 15.0
MIN_ZERO_RECALL: float = 0.60

# Iperparametri del secondo stadio. nkill usa i default (Poisson). Per nwound
# la sovradispersione rende la Poisson mal specificata: si passa a Tweedie 1,5,
# con alberi piu' piccoli perche' il secondo stadio vede solo le righe positive.
REGRESSOR_KWARGS: dict[str, dict[str, Any]] = {
    "nkill": {},
    "nwound": {
        "objective": "tweedie",
        "tweedie_variance_power": 1.5,
        "num_leaves": 31,
        "min_child_samples": 100,
    },
}

CLASSIFIER_KWARGS: dict[str, dict[str, Any]] = {
    "nkill": {},
    "nwound": {},
}


# Setup dei dati
@dataclass(frozen=True)
class TargetSplit:
    """Partizione di un target, con il preprocessing congelato necessario a
    ricostruire la matrice di design al ricaricamento."""

    target: str
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: np.ndarray
    y_test: np.ndarray
    preprocessing: dict
    floor_test: np.ndarray

    @property
    def feature_names(self) -> list[str]:
        return list(self.X_train.columns)


def load_clean_dataset(settings: Settings) -> pd.DataFrame:
    """Legge i dati gia' sottoposti a Data Quality, da PostgreSQL o da cache."""
    columns = sorted(
        set(gtd_ml.RAW_FEATURES)
        | set(gtd_ml.TARGETS)
        | set(DETERMINISTIC_LOWER_BOUND.values())   # colonne dei vincoli a priori
    )
    query = f"SELECT {', '.join(columns)} FROM {settings.staging_schema}.raw_gtd"

    try:
        with DatabaseManager(settings.db) as db:
            frame = pd.read_sql_query(query, db.engine)
        log.info("caricate %s righe da %s.raw_gtd", f"{len(frame):,}", settings.staging_schema)
        return frame
    except Exception as exc:                                  # noqa: BLE001
        log.warning("lettura da PostgreSQL non riuscita: %s", exc)

    fallback = settings.paths.output_dir / "gtd_clean.parquet"
    if fallback.exists():
        log.info("fallback su %s", fallback)
        return pd.read_parquet(fallback)

    raise SystemExit(
        "Nessuna sorgente disponibile.\n"
        f"Atteso {settings.staging_schema}.raw_gtd su PostgreSQL, oppure {fallback}.\n"
        "Esegui prima la pipeline in modalita' bootstrap per produrre lo staging pulito."
    )


def get_train_test_data(target_col: str, df: pd.DataFrame) -> TargetSplit:
    """Partiziona e costruisce le matrici di design per un target.

    Il preprocessing e' stimato solo sul training set: stimarlo su tutto
    sarebbe una fuga di informazione dal test.
    """
    support = df.dropna(subset=[target_col])
    raw_train, raw_test = train_test_split(
        support, test_size=HOLDOUT_SIZE, random_state=RANDOM_STATE
    )

    preprocessing = gtd_ml.fit_preprocessing(
        raw_train, raw_train[target_col], encoding=ENCODING, min_frequency=MIN_FREQUENCY
    )
    X_train, _ = gtd_ml.build_design_matrix(raw_train, preprocessing)
    X_test, _ = gtd_ml.build_design_matrix(
        raw_test, preprocessing, list(X_train.columns)
    )

    y_train = raw_train[target_col].to_numpy(dtype=float)
    y_test = raw_test[target_col].to_numpy(dtype=float)

    log.info(
        "[%s] training %s righe | holdout %s righe | %d colonne | zeri %.1f%%",
        target_col, f"{len(X_train):,}", f"{len(X_test):,}",
        X_train.shape[1], 100 * float((y_train == 0).mean()),
    )
    bound_col = DETERMINISTIC_LOWER_BOUND.get(target_col)
    floor_test = (
        pd.to_numeric(raw_test[bound_col], errors="coerce").fillna(0.0).clip(lower=0.0)
        .to_numpy(dtype=float)
        if bound_col and bound_col in raw_test.columns
        else np.zeros(len(raw_test), dtype=float)
    )

    return TargetSplit(
        target_col, X_train, X_test, y_train, y_test, preprocessing, floor_test
    )


# Metriche
def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Metriche sulla scala originale del conteggio.

    MAE: errore sul singolo record. Bias totale: errore che si accumula nelle
    aggregazioni. Zero recall: eventi incruenti trasformati in eventi con vittime.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.shape != y_pred.shape:
        raise ValueError(f"forme diverse: {y_true.shape} contro {y_pred.shape}")

    total_true = float(y_true.sum())
    zeros = y_true == 0
    n_zeros = int(zeros.sum())

    return {
        "mae": float(np.abs(y_true - y_pred).mean()),
        # RMSE non e' un criterio di accettazione: serve a leggere la
        # sovradispersione, se cresce molto piu' del MAE la coda domina.
        "rmse": float(np.sqrt(((y_true - y_pred) ** 2).mean())),
        "total_bias_pct": (
            float(100.0 * (y_pred.sum() - total_true) / total_true)
            if total_true > 0 else float("nan")
        ),
        "zero_recall": (
            float(((y_pred == 0) & zeros).sum() / n_zeros)
            if n_zeros else float("nan")
        ),
        "pred_zero_share": float((y_pred == 0).mean()),
    }


def baseline_mae(y_train: np.ndarray, y_test: np.ndarray) -> float:
    """MAE del predittore costante alla mediana del training set."""
    return float(np.abs(y_test - np.median(y_train)).mean())


def assess(metrics: dict[str, float], gain_pct: float) -> tuple[bool, str]:
    """Applica i tre criteri dichiarati e motiva l'esito."""
    failures: list[str] = []
    if not gain_pct >= MIN_BASELINE_GAIN_PCT:
        failures.append(f"guadagno {gain_pct:+.1f}% < {MIN_BASELINE_GAIN_PCT:.0f}%")
    if not abs(metrics["total_bias_pct"]) <= MAX_ABS_TOTAL_BIAS_PCT:
        failures.append(
            f"bias {metrics['total_bias_pct']:+.1f}% oltre "
            f"±{MAX_ABS_TOTAL_BIAS_PCT:.0f}%"
        )
    if not metrics["zero_recall"] >= MIN_ZERO_RECALL:
        failures.append(
            f"zero recall {metrics['zero_recall']:.3f} < {MIN_ZERO_RECALL:.2f}"
        )
    return (not failures), ("; ".join(failures) if failures else "tutti i criteri superati")


# Addestramento e valutazione
def train_and_evaluate(
    split: TargetSplit,
    classifier_kwargs: dict[str, Any] | None = None,
    regressor_kwargs: dict[str, Any] | None = None,
) -> tuple[ZeroInflatedCountRegressor, dict[str, float]]:
    """Addestra il modello a due stadi e lo valuta sull'holdout."""
    log.info("[%s] addestramento del modello a due stadi", split.target)

    model = ZeroInflatedCountRegressor(
        classifier_kwargs=classifier_kwargs,
        regressor_kwargs=regressor_kwargs,
        random_state=RANDOM_STATE,
    )
    model.fit(split.X_train, split.y_train)

    # Stessi vincoli a priori della produzione: valutare un predittore diverso
    # da quello che si adotta darebbe metriche non informative.
    predictions = model.predict(
        split.X_test,
        force_positive=split.floor_test > 0,
        lower_bound=split.floor_test,
    )
    metrics = evaluate_predictions(split.y_test, predictions)
    metrics["baseline_mae"] = baseline_mae(split.y_train, split.y_test)
    metrics["gain_vs_baseline_pct"] = float(
        100.0 * (1.0 - metrics["mae"] / metrics["baseline_mae"])
    )
    metrics["n_test"] = float(len(split.y_test))

    adoptable, reason = assess(metrics, metrics["gain_vs_baseline_pct"])
    metrics["adoptable"] = float(adoptable)
    metrics["reason"] = reason

    log.info(
        "[%s] MAE %.4f (baseline %.4f, %+.1f%%) | bias %+.2f%% | zero recall %.3f",
        split.target, metrics["mae"], metrics["baseline_mae"],
        metrics["gain_vs_baseline_pct"], metrics["total_bias_pct"],
        metrics["zero_recall"],
    )
    return model, metrics


# Serializzazione
def save_model(
    model: ZeroInflatedCountRegressor,
    split: TargetSplit,
    metrics: dict[str, float],
    model_dir: Path,
) -> Path:
    """Salva lo stimatore nudo. Il ricaricamento richiede zero_inflated importabile."""
    model_dir.mkdir(parents=True, exist_ok=True)
    path = Path(gtd_ml.bundle_path(str(model_dir), split.target))

    serialisable = {k: v for k, v in metrics.items() if not isinstance(v, str)}
    gtd_ml.save_bundle(
        path=str(path),
        target=split.target,
        model_type="hurdle_lgbm",
        estimator=model,
        feature_names=split.feature_names,
        preprocessing=split.preprocessing,
        validation_metrics=serialisable,
        training_rows=len(split.y_train),
        best_params={
            "classifier": model.classifier.get_params(),
            "regressor": model.regressor.get_params(),
        },
        source_file="staging.raw_gtd (post Data Quality)",
        notes=(
            f"Modello hurdle a due stadi, codifica {ENCODING}, "
            f"{len(split.feature_names)} colonne. "
            f"Esito dei criteri di accettazione: {metrics.get('reason', 'n/d')}."
        ),
    )
    log.info("[%s] bundle salvato in %s", split.target, path)
    return path


# Report finale
def build_report(results: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Tabella riassuntiva, una riga per target."""
    rows = []
    for target, m in results.items():
        rows.append({
            "target": target,
            "n_test": int(m["n_test"]),
            "MAE": round(m["mae"], 4),
            "MAE baseline": round(m["baseline_mae"], 4),
            "guadagno %": round(m["gain_vs_baseline_pct"], 1),
            "RMSE": round(m["rmse"], 3),
            "bias totale %": round(m["total_bias_pct"], 2),
            "zero recall": round(m["zero_recall"], 3),
            "quota zeri predetti": round(m["pred_zero_share"], 3),
            "esito": "ADOTTABILE" if m["adoptable"] else "NON adottabile",
        })
    return pd.DataFrame(rows).set_index("target")


def print_report(report: pd.DataFrame, results: dict[str, dict[str, float]]) -> None:
    print(
        f"Criteri: guadagno sul baseline >= {MIN_BASELINE_GAIN_PCT:.0f}%, "
        f"|bias totale| <= {MAX_ABS_TOTAL_BIAS_PCT:.0f}%, "
        f"zero recall >= {MIN_ZERO_RECALL:.2f}\n"
    )
    print(report.to_string())
    print(f"\nMotivazione dell'esito, per target:")
    for target, m in results.items():
        print(f"  {target:8s} {m.get('reason', 'n/d')}")


# Orchestrazione
def run(targets: Sequence[str], save: bool, model_dir: Path) -> pd.DataFrame:
    settings = Settings()
    df = load_clean_dataset(settings)

    results: dict[str, dict[str, float]] = {}
    for target in targets:
        split = get_train_test_data(target, df)
        model, metrics = train_and_evaluate(
            split,
            classifier_kwargs=CLASSIFIER_KWARGS.get(target),
            regressor_kwargs=REGRESSOR_KWARGS.get(target),
        )
        results[target] = metrics
        if save:
            save_model(model, split, metrics, model_dir)

    report = build_report(results)
    print_report(report, results)

    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--targets", nargs="+", default=list(gtd_ml.TARGETS),
        help="target da addestrare (default: nkill nwound)",
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="valuta senza serializzare i bundle",
    )
    parser.add_argument(
        "--model-dir", type=Path, default=None,
        help=f"cartella dei bundle (default: {Settings().paths.model_dir})",
    )
    args = parser.parse_args(argv)

    model_dir = args.model_dir or (Settings().paths.model_dir)
    run(targets=args.targets, save=not args.no_save, model_dir=model_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
