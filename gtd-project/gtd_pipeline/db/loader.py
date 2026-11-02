"""Caricamento di DataFrame in staging, via COPY con fallback su to_sql."""

from __future__ import annotations

import io

import pandas as pd
from sqlalchemy.engine import Engine

from ..logging_setup import get_logger

log = get_logger(__name__)

# Marcatore NULL di COPY: una stringa vuota sarebbe indistinguibile da un
# testo vuoto legittimo.
NULL_MARKER = "\\N"


class StagingLoader:
    """Carica DataFrame nello schema di staging."""

    def __init__(self, engine: Engine, schema: str = "staging") -> None:
        self.engine = engine
        self.schema = schema

    def load(self, df: pd.DataFrame, table: str, if_exists: str = "replace") -> int:
        """Crea la tabella e vi carica il DataFrame."""
        # head(0) crea la tabella lasciando inferire i tipi: lo staging accoglie
        # il dato com'e', la tipizzazione forte e' nel DDL del reconciled.
        df.head(0).to_sql(
            table, con=self.engine, schema=self.schema, if_exists=if_exists, index=False
        )
        try:
            rows = self._copy(df, table)
            log.info("  %s righe caricate in %s.%s via COPY", f"{rows:,}", self.schema, table)
            return rows
        except Exception as exc:
            log.warning("  COPY non riuscito (%s), fallback su to_sql", exc)
            df.to_sql(
                table, con=self.engine, schema=self.schema, if_exists="replace",
                index=False, method="multi", chunksize=500,
            )
            log.info("  %s righe caricate in %s.%s via to_sql", f"{len(df):,}", self.schema, table)
            return len(df)

    def _copy(self, df: pd.DataFrame, table: str) -> int:
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False, sep="\t", na_rep=NULL_MARKER)
        buffer.seek(0)

        connection = self.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.copy_expert(
                f"COPY {self.schema}.{table} FROM STDIN "
                f"WITH (FORMAT csv, DELIMITER E'\\t', NULL '{NULL_MARKER}')",
                buffer,
            )
            connection.commit()
            return len(df)
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def load_many(self, tables: dict[str, pd.DataFrame], prefix: str = "") -> dict[str, int]:
        """Carica piu' tabelle, restituendo le righe caricate per ciascuna."""
        return {name: self.load(frame, f"{prefix}{name}") for name, frame in tables.items()}
