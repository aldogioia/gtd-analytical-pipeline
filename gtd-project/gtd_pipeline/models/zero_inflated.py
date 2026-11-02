"""Imputer: modello hurdle a due stadi per conteggi zero-inflated."""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor

from ..audit import AuditLog, Level, Taxonomy
from ..logging_setup import get_logger
from . import gtd_ml
from .base import BaseImputer

log = get_logger(__name__)

DEFAULT_CLASSIFIER_PARAMS: dict[str, Any] = {
    "objective": "binary",
    "n_estimators": 400,
    "learning_rate": 0.05,
    "num_leaves": 63,
    "min_child_samples": 50,
    "n_jobs": -1,
    "verbose": -1,
}

DEFAULT_REGRESSOR_PARAMS: dict[str, Any] = {
    "objective": "poisson",
    "n_estimators": 600,
    "learning_rate": 0.05,
    "num_leaves": 63,
    "min_child_samples": 50,
    "n_jobs": -1,
    "verbose": -1,
}


# Soglia oltre la quale il primo stadio dichiara il regime a zero vittime.
# Non e' 0,5: l'errore non e' simmetrico. Azzerare un evento con vittime costa
# al totale molto piu' che attribuire una vittima a un evento incruento, e la
# misura finisce in un warehouse dove viene letta aggregata. A 0,40 lo zero si
# dichiara solo quando il classificatore e' convinto; il prezzo e' una zero
# recall piu' bassa, misurata e accettata in train_hurdle_models.py.
ZERO_REGIME_THRESHOLD: float = 0.40

# Scarto massimo fra la somma delle stime continue e quella delle discretizzate.
# Vale una unita' perche' e' l'invariante garantito dal metodo dei resti
# maggiori: se salta e' un difetto del codice, non un effetto dei dati.
MAX_ROUNDING_DRIFT_UNITS: float = 1.0

# Vincoli a priori. Chiave: target imputato; valore: colonna che per regola di
# dominio ne e' un limite inferiore certo. Un evento con attentatori morti
# accertati non puo' stare nel regime a zero vittime.
DETERMINISTIC_LOWER_BOUND: dict[str, str] = {"nkill": "nkillter"}

class NotFittedError(RuntimeError):
    """predict invocato prima di fit."""


# Stimatore a due stadi
class ZeroInflatedCountRegressor:
    """Classificatore di zeri + regressore di conteggi sui soli positivi."""

    def __init__(
        self,
        classifier_kwargs: dict[str, Any] | None = None,
        regressor_kwargs: dict[str, Any] | None = None,
        random_state: int = 42,
    ) -> None:
        # Copia prima dell'update, per non mutare i default fra istanze.
        classifier_params = {**DEFAULT_CLASSIFIER_PARAMS, "random_state": random_state}
        classifier_params.update(classifier_kwargs or {})

        regressor_params = {**DEFAULT_REGRESSOR_PARAMS, "random_state": random_state}
        regressor_params.update(regressor_kwargs or {})

        self.classifier: LGBMClassifier = LGBMClassifier(**classifier_params)
        self.regressor: LGBMRegressor = LGBMRegressor(**regressor_params)

        self.random_state = random_state
        self.feature_names_: list[str] | None = None
        self.zero_rate_: float | None = None
        self.positive_mean_: float | None = None
        self._degenerate_all_zero: bool = False
        self._degenerate_no_zero: bool = False
        self._fitted: bool = False
        # Esito dell'ultima discretizzazione, per l'audit log.
        self.last_discretization_: dict[str, float] | None = None

    def fit(
        self, X: pd.DataFrame, y: np.ndarray | pd.Series
    ) -> "ZeroInflatedCountRegressor":
        y = np.asarray(y, dtype=float)
        if len(X) != len(y):
            raise ValueError(f"X e y hanno lunghezze diverse: {len(X)} contro {len(y)}")
        if np.isnan(y).any():
            raise ValueError("y contiene valori mancanti: filtrarli prima di addestrare")

        self.feature_names_ = list(X.columns)

        # Stadio 1: la classe positiva e' "conteggio uguale a zero"
        y_zero = (y == 0).astype(int)
        self.zero_rate_ = float(y_zero.mean())

        # Casi degeneri: classificatore a una sola classe, o nessuna riga positiva
        self._degenerate_all_zero = bool(y_zero.all())
        self._degenerate_no_zero = bool(not y_zero.any())
        if not (self._degenerate_all_zero or self._degenerate_no_zero):
            self.classifier.fit(X, y_zero)

        # Stadio 2: solo le righe con almeno una vittima
        positive = y > 0
        if positive.any():
            self.regressor.fit(X.loc[positive], y[positive])
            self.positive_mean_ = float(y[positive].mean())
        else:
            self.positive_mean_ = 0.0

        log.info(
            "  due stadi: %d righe, %.1f%% zeri, %d righe positive (media %.2f)",
            len(y), 100 * self.zero_rate_, int(positive.sum()), self.positive_mean_,
        )
        self._fitted = True
        return self

    def predict_zero_probability(self, X: pd.DataFrame) -> np.ndarray:
        self._check_fitted()
        if self._degenerate_all_zero:
            return np.ones(len(X), dtype=float)
        if self._degenerate_no_zero:
            return np.zeros(len(X), dtype=float)

        classes = list(self.classifier.classes_)
        return np.asarray(
            self.classifier.predict_proba(X)[:, classes.index(1)], dtype=float
        )

    def predict_positive_count(self, X: pd.DataFrame) -> np.ndarray:
        self._check_fitted()
        if self.positive_mean_ == 0.0:
            return np.zeros(len(X), dtype=float)
        return np.clip(np.asarray(self.regressor.predict(X), dtype=float), 0.0, None)

    def predict_expected(
        self,
        X: pd.DataFrame,
        *,
        force_positive: np.ndarray | pd.Series | None = None,
        lower_bound: np.ndarray | pd.Series | None = None,
    ) -> np.ndarray:
        """Stima continua di E[Y]: 0 nel regime a zero, altrimenti E[Y | Y > 0].

        'force_positive' fa scavalcare il primo stadio alle righe per cui il
        dominio esclude gia' lo zero; 'lower_bound' tronca dal basso la stima.
        """
        self._check_fitted()
        self._check_columns(X)

        n = len(X)
        forced = self._as_vector(force_positive, n, default=0.0).astype(bool)
        floor = self._as_vector(lower_bound, n, default=0.0)

        # Le righe vincolate non passano dal primo stadio: la probabilita' di
        # zero e' posta a zero per definizione, non stimata.
        p_zero = np.where(forced, 0.0, self.predict_zero_probability(X))
        expected = np.where(
            p_zero >= ZERO_REGIME_THRESHOLD, 0.0, self.predict_positive_count(X)
        )
        return np.maximum(np.clip(expected, 0.0, None), np.clip(floor, 0.0, None))

    def discretize(
        self, continuous: np.ndarray, tolerance: float = MAX_ROUNDING_DRIFT_UNITS
    ) -> tuple[np.ndarray, dict[str, float]]:
        """Porta la stima continua sull'intero conservando il totale.

        Metodo dei resti maggiori: parte intera piu' una unita' alle righe con
        il resto piu' grande. Troncare sottostima gli aggregati, arrotondare a
        0,5 e' non distorto solo con resti simmetrici — qui non lo sono. Cosi'
        lo scarto sul totale resta sotto l'unita' per costruzione. Lo scarto
        effettivo e' comunque restituito.
        """
        values = np.clip(np.asarray(continuous, dtype=float), 0.0, None)
        integers = np.floor(values).astype(np.int64)
        remainders = values - integers

        # Quante unita' restano da distribuire dopo la parte intera.
        to_assign = int(np.rint(remainders.sum()))
        if to_assign > 0:
            # Ordine stabile: resto decrescente, e a parita' indice crescente.
            winners = np.argsort(-remainders, kind="stable")[:to_assign]
            integers[winners] += 1

        sum_continuous = float(values.sum())
        sum_discrete = float(integers.sum())
        drift = sum_discrete - sum_continuous
        drift_pct = 100.0 * drift / sum_continuous if sum_continuous > 0 else 0.0

        report = {
            "sum_continuous": sum_continuous,
            "sum_discrete": sum_discrete,
            "drift": drift,
            "drift_pct": drift_pct,
            "within_tolerance": float(abs(drift) < tolerance),
        }
        message = (
            "  discretizzazione: somma continua %.2f -> intera %d "
            "(scarto %+.2f unita', %+.4f%%)"
        )
        if report["within_tolerance"]:
            log.info(message, sum_continuous, int(sum_discrete), drift, drift_pct)
        else:
            log.warning(
                message + " OLTRE l invariante di %.1f unita'",
                sum_continuous, int(sum_discrete), drift, drift_pct, tolerance,
            )
        return integers, report

    def predict(
        self,
        X: pd.DataFrame,
        *,
        force_positive: np.ndarray | pd.Series | None = None,
        lower_bound: np.ndarray | pd.Series | None = None,
    ) -> np.ndarray:
        """Stima INTERA, pronta per la tabella di staging e per il fatto."""
        continuous = self.predict_expected(
            X, force_positive=force_positive, lower_bound=lower_bound
        )
        integers, report = self.discretize(continuous)
        self.last_discretization_ = report
        return integers

    @staticmethod
    def _as_vector(
        values: np.ndarray | pd.Series | None, n: int, default: float
    ) -> np.ndarray:
        """Normalizza un vincolo opzionale a un vettore denso di lunghezza n."""
        if values is None:
            return np.full(n, default, dtype=float)
        array = np.asarray(
            values.to_numpy() if isinstance(values, pd.Series) else values, dtype=float
        )
        if array.shape != (n,):
            raise ValueError(
                f"vincolo di lunghezza {array.shape} incompatibile con {n} righe"
            )
        return np.nan_to_num(array, nan=default)

    def _check_fitted(self) -> None:
        if not self._fitted:
            raise NotFittedError(f"{type(self).__name__}: chiamare fit() prima di predict()")

    def _check_columns(self, X: pd.DataFrame) -> None:
        if self.feature_names_ is None or list(X.columns) == self.feature_names_:
            return
        missing = sorted(set(self.feature_names_) - set(X.columns))
        raise ValueError(
            f"matrice di design disallineata: {len(missing)} colonne assenti {missing[:5]}"
        )

    def __repr__(self) -> str:
        state = "addestrato" if self._fitted else "non addestrato"
        objective = self.regressor.get_params().get("objective")
        return f"ZeroInflatedCountRegressor({objective}, {state})"


# Strategia di imputazione della pipeline
class ZeroInflatedImputer(BaseImputer):
    """Imputa i conteggi mancanti addestrando un modello a due stadi per target."""

    def __init__(
        self,
        targets: Sequence[str] = gtd_ml.IMPUTED_TARGETS,
        audit: AuditLog | None = None,
        *,
        classifier_kwargs: dict[str, Any] | None = None,
        regressor_kwargs: dict[str, Any] | None = None,
        declared_targets: Sequence[str] = gtd_ml.TARGETS,
        min_frequency: float = gtd_ml.DEFAULT_MIN_FREQUENCY,
        min_completeness: float = gtd_ml.MIN_COMPLETENESS,
        redundancy_threshold: float = gtd_ml.REDUNDANCY_THRESHOLD,
        encoding: str = "native",
        random_state: int = 42,
    ) -> None:
        super().__init__(targets)
        self.audit = audit
        self.declared_targets = tuple(declared_targets)
        self.classifier_kwargs = classifier_kwargs
        self.regressor_kwargs = regressor_kwargs
        self.min_frequency = min_frequency
        self.min_completeness = min_completeness
        self.redundancy_threshold = redundancy_threshold
        self.encoding = encoding
        self.random_state = random_state

        self.models_: dict[str, ZeroInflatedCountRegressor] = {}
        self.preprocessing_: dict[str, dict] = {}

    @property
    def description(self) -> str:
        objective = (self.regressor_kwargs or {}).get(
            "objective", DEFAULT_REGRESSOR_PARAMS["objective"]
        )
        return (
            f"modello a due stadi (classificatore zero + regressore "
            f"'{objective}') su {', '.join(self.targets)}"
        )

    def impute(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for target in self.targets:
            out = self._impute_target(out, target)
        self._declare_not_imputed(out)
        return out

    def _impute_target(self, df: pd.DataFrame, target: str) -> pd.DataFrame:
        flag = self.flag_column(target)
        df[flag] = 0

        if target not in df.columns:
            return df

        mask = df[target].isna()
        n_missing = int(mask.sum())
        if not n_missing:
            self._log_audit(target, "Nessuna imputazione necessaria", "Colonna gia completa", 0)
            return df

        observed = df.loc[~mask]
        if observed.empty:
            self._log_audit(
                target,
                "Imputazione non applicata: nessuna riga osservata",
                "Senza osservazioni il modello non e addestrabile",
                n_missing,
            )
            return df

        # Solo righe osservate: il target serve a dirimere le feature ridondanti.
        preprocessing = gtd_ml.fit_preprocessing(
            observed,
            observed[target],
            encoding=self.encoding,
            min_frequency=self.min_frequency,
            min_completeness=self.min_completeness,
            redundancy_threshold=self.redundancy_threshold,
            random_state=self.random_state,
        )
        X_train, _ = gtd_ml.build_design_matrix(observed, preprocessing)
        X_missing, info = gtd_ml.build_design_matrix(
            df.loc[mask], preprocessing, list(X_train.columns)
        )

        if info["missing_columns"] or info["unseen_columns"]:
            self._log_audit(
                target,
                "Scostamento fra schema di addestramento e schema di inferenza",
                f"Colonne attese e assenti: {info['missing_columns'][:10]} | "
                f"Colonne osservate e non viste: {info['unseen_columns'][:10]}",
                n_missing,
                level=Level.SCHEMA,
                taxonomy=Taxonomy.INCONSISTENT,
            )

        model = ZeroInflatedCountRegressor(
            classifier_kwargs=self.classifier_kwargs,
            regressor_kwargs=self.regressor_kwargs,
            random_state=self.random_state,
        )
        model.fit(X_train, observed[target].to_numpy(dtype=float))

        # Le righe per cui il dominio esclude gia' lo zero scavalcano il primo
        # stadio. Il training non ne risente: nkillter <= nkill e' imposto a
        # monte, quindi fra le osservate non esiste y = 0 con limite positivo.
        floor = self._deterministic_floor(df.loc[mask], target)
        forced = floor > 0

        df.loc[mask, target] = model.predict(
            X_missing, force_positive=forced.to_numpy(), lower_bound=floor.to_numpy()
        )
        df.loc[mask, flag] = 1

        self.models_[target] = model
        self.preprocessing_[target] = preprocessing

        n_forced = int(forced.sum())
        bound_col = DETERMINISTIC_LOWER_BOUND.get(target)
        drift = model.last_discretization_ or {}
        prior_note = (
            f"{n_forced} record con {bound_col} > 0 hanno saltato il primo stadio "
            f"(P(zero) nulla per regola di dominio) e sono stati troncati dal basso "
            f"a {bound_col}. "
            if bound_col and n_forced else ""
        )
        self._log_audit(
            target,
            "Imputazione con modello a due stadi (hurdle)",
            "Un classificatore riconosce gli zeri strutturali, un regressore per "
            "conteggi stima la gravita sui soli eventi con vittime. "
            + prior_note
            + "La stima continua e discretizzata all intero con il metodo dei resti "
            "maggiori, che conserva il totale "
            f"(scarto {drift.get('drift', 0.0):+.2f} unita, "
            f"{drift.get('drift_pct', 0.0):+.4f}%). Il mancante e MNAR e la "
            f"provenance e tracciata da {flag}",
            n_missing,
        )
        return df

    def _deterministic_floor(self, rows: pd.DataFrame, target: str) -> pd.Series:
        """Limite inferiore certo per ciascuna riga da imputare.

        Vale zero dove il vincolo non si applica o la colonna di riferimento e'
        essa stessa mancante: un vincolo ignoto non e' un vincolo nullo, ma in
        assenza di informazione il limite inferiore degenera a zero e la stima
        resta interamente affidata al modello.
        """
        column = DETERMINISTIC_LOWER_BOUND.get(target)
        if column is None or column not in rows.columns:
            return pd.Series(0.0, index=rows.index, dtype=float)
        return pd.to_numeric(rows[column], errors="coerce").fillna(0.0).clip(lower=0.0)

    def _declare_not_imputed(self, df: pd.DataFrame) -> None:
        """Flag a zero per i target studiati ma non imputati."""
        for target in self.declared_targets:
            flag = self.flag_column(target)
            if flag not in df.columns:
                df[flag] = 0

    def _log_audit(
        self,
        target: str,
        action: str,
        rationale: str,
        rows_affected: int,
        level: Level = Level.INSTANCE,
        taxonomy: Taxonomy = Taxonomy.MISSING,
    ) -> None:
        if self.audit is None:
            return
        self.audit.log(
            "ml_imputation", level, taxonomy, target, action, rationale,
            rows_affected=rows_affected,
            domain_rule="Regola di dominio - totale delle vittime",
        )
