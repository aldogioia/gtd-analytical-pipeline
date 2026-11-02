"""Percorsi, credenziali e parametri della pipeline.

Ogni valore ha un default per lo sviluppo locale e si sovrascrive con una
variabile d'ambiente.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return default if value is None or value == "" else value


@dataclass(frozen=True)
class DatabaseSettings:
    """Coordinate di PostgreSQL."""

    user: str = field(default_factory=lambda: _env("GTD_DB_USER", "postgres"))
    password: str = field(default_factory=lambda: _env("GTD_DB_PASSWORD", ""))
    host: str = field(default_factory=lambda: _env("GTD_DB_HOST", "localhost"))
    port: str = field(default_factory=lambda: _env("GTD_DB_PORT", "5432"))
    name: str = field(default_factory=lambda: _env("GTD_DB_NAME", "data_warehouse_project"))

    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.user}:{quote_plus(self.password)}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    @property
    def uses_default_password(self) -> bool:
        return os.environ.get("GTD_DB_PASSWORD") in (None, "")


@dataclass(frozen=True)
class PathSettings:
    """Percorsi di ingresso e uscita, tutti relativi alla radice del progetto."""

    root: Path = PROJECT_ROOT

    @property
    def source_xlsx(self) -> Path:
        return self.root / _env("GTD_SOURCE", "dataset/globalterrorismdb_0522dist.xlsx")

    @property
    def parquet_cache(self) -> Path:
        return self.root / _env("GTD_CACHE", "dataset/gtd_raw.parquet")

    @property
    def model_dir(self) -> Path:
        return self.root / _env("GTD_MODEL_DIR", "models")

    @property
    def output_dir(self) -> Path:
        return self.root / _env("GTD_OUTPUT_DIR", "dataset")

    @property
    def sql_dir(self) -> Path:
        return self.root / "sql"

    # Script SQL, nell'ordine in cui la pipeline li esegue.
    @property
    def ddl_reconciled(self) -> Path:
        return self.sql_dir / "reconciled_database.sql"

    @property
    def ddl_warehouse(self) -> Path:
        return self.sql_dir / "data_warehouse.sql"

    @property
    def populate_hierarchies(self) -> Path:
        return self.sql_dir / "populate_rd_hierarchies.sql"

    @property
    def populate_reconciled(self) -> Path:
        return self.sql_dir / "populate_rd.sql"

    @property
    def hierarchy_levels(self) -> Path:
        return self.sql_dir / "hierarchy_levels.sql"

    @property
    def etl_warehouse(self) -> Path:
        return self.sql_dir / "etl_queries.sql"

    @property
    def propagate_levels(self) -> Path:
        return self.sql_dir / "propagate_hierarchy_levels.sql"

    @property
    def audit_log_csv(self) -> Path:
        return self.output_dir / "audit_log.csv"

    @property
    def quality_report_csv(self) -> Path:
        return self.output_dir / "data_quality_report.csv"

    @property
    def hierarchy_conflicts_csv(self) -> Path:
        return self.output_dir / "hierarchy_conflicts.csv"


@dataclass(frozen=True)
class Settings:
    """Configurazione completa della pipeline."""

    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    paths: PathSettings = field(default_factory=PathSettings)

    staging_schema: str = "staging"

    # Soglia dello z-score robusto su MAD oltre la quale un evento e' segnalato.
    outlier_z_threshold: float = 10.0

    def describe(self) -> str:
        return (
            f"database  {self.db.user}@{self.db.host}:{self.db.port}/{self.db.name}\n"
            f"sorgente  {self.paths.source_xlsx}\n"
            f"cache     {self.paths.parquet_cache}\n"
            f"modelli   {self.paths.model_dir}\n"
            f"sql       {self.paths.sql_dir}"
        )
