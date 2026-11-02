"""Strategia che non imputa nulla, usata da --bootstrap."""

from __future__ import annotations

from typing import Sequence

import pandas as pd

from . import gtd_ml
from .base import BaseImputer


class NoOpImputer(BaseImputer):
    """Lascia i mancanti dove sono, ma scrive comunque i flag di provenienza."""

    def __init__(self, targets: Sequence[str] = gtd_ml.TARGETS) -> None:
        super().__init__(targets)

    @property
    def description(self) -> str:
        return "nessuna imputazione (bootstrap)"

    def impute(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for target in self.targets:
            out[self.flag_column(target)] = 0
        return out
