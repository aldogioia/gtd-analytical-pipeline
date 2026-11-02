"""Esporta lo schema a stella in CSV, una tabella per file.

Le query stanno in sql/export.sql, un blocco per tabella preceduto da
'--@table: <nome>'.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from gtd_pipeline.config import Settings
from gtd_pipeline.db.connection import DatabaseManager

EXPORT_SUBDIR = "dwh_export"

# Convenzione italiana
CSV_SEP = ";"
CSV_DECIMAL = ","

_TABLE_DIRECTIVE = re.compile(r"^\s*--\s*@table:\s*(\w+)\s*$", re.MULTILINE)


def parse_export_script(script: str) -> dict[str, str]:
    """Spezza sql/export.sql in una query per tabella."""
    matches = list(_TABLE_DIRECTIVE.finditer(script))
    if not matches:
        raise ValueError("nessuna direttiva --@table trovata in sql/export.sql")

    queries: dict[str, str] = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(script)
        body = script[match.end():end].strip().rstrip(";").strip()
        if not body:
            raise ValueError(f"blocco vuoto per la tabella {match.group(1)}")
        queries[match.group(1)] = body
    return queries


def export_star_schema() -> None:
    settings = Settings()
    db = DatabaseManager(settings.db)

    script = (settings.paths.sql_dir / "export.sql").read_text(encoding="utf-8")
    queries = parse_export_script(script)

    output_dir = settings.paths.output_dir / EXPORT_SUBDIR
    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    try:
        with db.engine.connect() as conn:
            for table, query in queries.items():
                df = pd.read_sql_query(text(query), conn).convert_dtypes()
                path = output_dir / f"{table}.csv"
                df.to_csv(path, index=False, sep=CSV_SEP, decimal=CSV_DECIMAL)
                total += len(df)
                print(f"  {table:<22} {len(df):>9,} righe  {len(df.columns):>3} colonne  -> {path}")
    finally:
        db.dispose()

    print(f"\n{len(queries)} tabelle estratte, {total:,} righe complessive in {output_dir}")


def main() -> int:
    export_star_schema()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
