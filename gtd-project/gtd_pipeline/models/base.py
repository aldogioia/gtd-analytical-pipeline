"""Interfaccia astratta delle strategie di imputazione."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import pandas as pd

from ..logging_setup import get_logger

log = get_logger(__name__)


class ImputationError(RuntimeError):
    """Violazione del contratto da parte di una strategia di imputazione."""


class BaseImputer(ABC):
    """Contratto delle strategie di imputazione: run() lo verifica."""

    def __init__(self, targets: Sequence[str]) -> None:
        self.targets: tuple[str, ...] = tuple(targets)

    @abstractmethod
    def impute(self, df: pd.DataFrame) -> pd.DataFrame:
        """Stima i valori mancanti dei target e ne dichiara la provenienza."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Riga leggibile che identifica la strategia, per log e audit."""

    @staticmethod
    def flag_column(target: str) -> str:
        return f"is_{target}_imputed"

    def missing_counts(self, df: pd.DataFrame) -> dict[str, int]:
        return {
            t: int(df[t].isna().sum()) for t in self.targets if t in df.columns
        }

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Imputa e verifica il contratto. E' il punto d'ingresso della pipeline."""
        rows_before = len(df)
        missing_before = self.missing_counts(df)
        log.info("imputazione: %s", self.description)

        out = self.impute(df)

        self._validate_output(out, rows_before, missing_before)
        missing_after = self.missing_counts(out)
        for target in self.targets:
            if target not in missing_before:
                continue
            imputed = missing_before[target] - missing_after[target]
            log.info(
                "  %-8s mancanti %7d -> %7d  (%d imputati)",
                target, missing_before[target], missing_after[target], imputed,
            )
        return out

    def _validate_output(
        self, out: pd.DataFrame, rows_before: int, missing_before: dict[str, int]
    ) -> None:
        if not isinstance(out, pd.DataFrame):
            raise ImputationError(
                f"{type(self).__name__}.impute deve restituire un DataFrame, "
                f"ha restituito {type(out).__name__}"
            )
        if len(out) != rows_before:
            raise ImputationError(
                f"{type(self).__name__} ha cambiato il numero di righe "
                f"({rows_before} -> {len(out)}): l'imputazione riempie celle, "
                "non modifica la grana del fatto"
            )
        for target in self.targets:
            if target not in out.columns:
                continue
            flag = self.flag_column(target)
            if flag not in out.columns:
                raise ImputationError(
                    f"{type(self).__name__} non ha dichiarato la provenienza di "
                    f"'{target}': manca la colonna '{flag}'"
                )
            values = set(pd.unique(out[flag].dropna()))
            if not values <= {0, 1}:
                raise ImputationError(
                    f"il flag di provenienza '{flag}' contiene valori diversi da "
                    f"0 e 1: {sorted(values)[:5]}"
                )
            after = int(out[target].isna().sum())
            if after > missing_before.get(target, after):
                raise ImputationError(
                    f"{type(self).__name__} ha AUMENTATO i mancanti su '{target}' "
                    f"({missing_before[target]} -> {after})"
                )
