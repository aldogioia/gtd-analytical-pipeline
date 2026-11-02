"""Registro delle operazioni di pulizia, classificate secondo Rahm & Do (2000)."""

from __future__ import annotations

import enum
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd


class Level(str, enum.Enum):
    SCHEMA = "Schema Level"
    INSTANCE = "Instance Level"


class Taxonomy(str, enum.Enum):
    MISSING = "Missing Value"
    STRUCTURAL_MISSING = "Structural Missing"
    NOISY = "Noisy Data"
    INCONSISTENT = "Inconsistent Value"
    DUPLICATE = "Duplicate"
    OUTLIER = "Outlier"
    GRANULARITY = "Granularity"


@dataclass
class AuditEntry:
    entry_id: int
    timestamp: str
    phase: str
    step: str
    taxonomy_level: str
    taxonomy_type: str
    column: str
    action: str
    rows_affected: int | None
    rows_before: int | None
    rows_after: int | None
    reason: str
    domain_rule: str


class AuditLog:
    """Accumula le voci e le materializza in CSV."""

    COLUMNS = [
        "Entry_ID", "Timestamp", "Phase", "Step", "Taxonomy_Level", "Taxonomy_Type",
        "Column", "Action", "Rows_Affected", "Rows_Before", "Rows_After",
        "Reason", "Domain_Rule",
    ]

    def __init__(self, phase: str = "Phase 2 - Data Management") -> None:
        self.phase = phase
        self._entries: list[AuditEntry] = []

    def log(
        self,
        step: str,
        level: Level,
        taxonomy: Taxonomy,
        column: str,
        action: str,
        reason: str,
        rows_affected: int | None = None,
        rows_before: int | None = None,
        rows_after: int | None = None,
        domain_rule: str = "",
    ) -> "AuditLog":
        self._entries.append(
            AuditEntry(
                entry_id=len(self._entries) + 1,
                timestamp=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                phase=self.phase,
                step=step,
                taxonomy_level=Level(level).value,
                taxonomy_type=Taxonomy(taxonomy).value,
                column=column,
                action=action,
                rows_affected=rows_affected,
                rows_before=rows_before,
                rows_after=rows_after,
                reason=reason,
                domain_rule=domain_rule,
            )
        )
        return self

    def __len__(self) -> int:
        return len(self._entries)

    def to_frame(self) -> pd.DataFrame:
        if not self._entries:
            return pd.DataFrame(columns=self.COLUMNS)
        frame = pd.DataFrame([asdict(e) for e in self._entries])
        frame.columns = self.COLUMNS
        return frame

    def save(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.to_frame().to_csv(path, index=False)
        return path

    def summary(self) -> pd.DataFrame:
        frame = self.to_frame()
        if frame.empty:
            return frame
        return (
            frame.groupby(["Taxonomy_Level", "Taxonomy_Type"], as_index=False)
            .agg(Operazioni=("Entry_ID", "count"), Righe_Toccate=("Rows_Affected", "sum"))
        )
