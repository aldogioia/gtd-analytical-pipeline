"""Punto di ingresso della pipeline GTD.

    python -m gtd_pipeline.main --help

Fasi: estrazione, data quality, gerarchie, imputazione, stati sovrani,
staging, reconciled database, ETL verso lo star schema, riconciliazione.

Modalita': (default) completa | --bootstrap ferma dopo lo staging |
--sql-only riesegue la sola parte SQL sul dato gia' in staging.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time

import pandas as pd
from sqlalchemy import text


from .audit import AuditLog
from .config import Settings
from .db.connection import DatabaseManager
from .db.loader import StagingLoader
from .db.sql_runner import SQLScriptRunner
from .etl.extract import SourceExtractor
from .etl.hierarchies import HierarchyResolver
from .etl.quality import DataQualityManager
from .etl.reconcile import Reconciler
from .etl.sovereign import SovereignStateResolver
from .logging_setup import get_logger, setup_logging
from .models.base import BaseImputer
from .models.noop import NoOpImputer
from .models.zero_inflated import ZeroInflatedImputer

log = get_logger(__name__)

# Prefisso delle tabelle di gerarchia in staging.
HIER_PREFIX = "hier_"


class Pipeline:
    """Orchestrazione delle fasi."""

    def __init__(self, settings: Settings, imputer: BaseImputer | None = None) -> None:
        self.settings = settings
        self.audit = AuditLog()
        self.db = DatabaseManager(settings.db)
        self.runner = SQLScriptRunner(self.db.engine)
        self.loader = StagingLoader(self.db.engine, settings.staging_schema)
        self._imputer = imputer


    def imputer(self) -> BaseImputer:
        """Strategia di imputazione, iniettabile dall'esterno."""
        if self._imputer is None:
            self._imputer = ZeroInflatedImputer(audit=self.audit)
        return self._imputer


    def transform(self, use_cache: bool = True) -> pd.DataFrame:
        """Fasi 1-5: dalla sorgente al DataFrame pronto per lo staging."""
        paths = self.settings.paths

        log.info("[1/9] estrazione")
        extractor = SourceExtractor(paths.source_xlsx, paths.parquet_cache, use_cache)
        df_raw = extractor.extract()

        log.info("[2/9] data quality")
        dq = DataQualityManager(df_raw, self.audit, self.settings.outlier_z_threshold)
        df_clean, report_before, report_after = dq.run()

        log.info("[3/9] gerarchie e macro-categorie")
        resolver = HierarchyResolver(self.audit)
        self.hierarchies = resolver.build(df_clean)
        resolver.assert_no_minority_parent()
        conflicts = resolver.conflict_report()
        if not conflicts.empty:
            paths.hierarchy_conflicts_csv.parent.mkdir(parents=True, exist_ok=True)
            conflicts.to_csv(paths.hierarchy_conflicts_csv, index=False)
            log.info("  conflitti di gerarchia scritti in %s", paths.hierarchy_conflicts_csv)

        log.info("[4/9] imputazione")
        df_imputed = self.imputer().run(df_clean)
        df_imputed = DataQualityManager.enforce_casualty_consistency(
            df_imputed, self.audit, "post_imputation_consistency"
        )

        log.info("[5/9] stati sovrani")
        sovereign = SovereignStateResolver(self.audit)
        df_final = sovereign.apply(df_imputed)
        self.sovereign_dim = sovereign.dimension()

        # Audit e report di qualita' su file
        paths.output_dir.mkdir(parents=True, exist_ok=True)
        self.audit.save(paths.audit_log_csv)
        pd.concat([report_before, report_after], ignore_index=True).to_csv(
            paths.quality_report_csv, index=False
        )
        log.info("  audit log: %s (%d voci)", paths.audit_log_csv, len(self.audit))
        return df_final


    def load_staging(self, df: pd.DataFrame) -> None:
        """Fase 6: il dato pulito e le gerarchie risolte entrano in staging."""
        log.info("[6/9] caricamento in staging")
        with self.db.engine.begin() as conn:
            conn.execute(text("DROP SCHEMA IF EXISTS staging CASCADE;"))
            conn.execute(text("DROP SCHEMA IF EXISTS rd CASCADE;"))
            conn.execute(text("DROP SCHEMA IF EXISTS dwh CASCADE;"))

        self.db.ensure_schema(self.settings.staging_schema)
        self.loader.load(df, "raw_gtd")
        self.loader.load(self.sovereign_dim, "dim_sovereign_state")
        self.loader.load_many(self.hierarchies, prefix=HIER_PREFIX)


    def run_sql(self) -> None:
        """Fasi 7-8: reconciled database e star schema."""
        paths = self.settings.paths
        log.info("[7/9] reconciled database")

        self.runner.execute_file(paths.ddl_reconciled)
        self.runner.execute_file(paths.ddl_warehouse)
        self.runner.execute_file(paths.hierarchy_levels)
        self.runner.execute_file(paths.populate_hierarchies)
        self.runner.execute_file(paths.populate_reconciled)

        log.info("[8/9] ETL verso il data warehouse")
        self.runner.execute_file(paths.etl_warehouse)
        self.runner.execute_file(paths.propagate_levels)


    def reconcile(self) -> bool:
        log.info("[9/9] riconciliazione")
        _, ok = Reconciler(self.db.engine).run()
        return ok


    def run(self, bootstrap: bool = False, sql_only: bool = False, use_cache: bool = True) -> bool:
        started = time.perf_counter()
        self.db.check_connection()

        if not sql_only:
            df_final = self.transform(use_cache=use_cache)
            self.load_staging(df_final)

            summary = self.audit.summary()
            if not summary.empty:
                log.info("--- AUDIT LOG (sintesi) ---")
                for _, row in summary.iterrows():
                    log.info(
                        "  %-14s %-20s %3d operazioni, %s righe",
                        row["Taxonomy_Level"], row["Taxonomy_Type"],
                        row["Operazioni"], f"{int(row['Righe_Toccate'] or 0):,}",
                    )

            if bootstrap:
                log.info("bootstrap completato: staging.raw_gtd e pronto.")
                return True

        self.run_sql()
        ok = self.reconcile()
        log.info("pipeline completata in %.1f s", time.perf_counter() - started)
        return ok

    def close(self) -> None:
        self.db.dispose()


# CLI
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gtd_pipeline",
        description="Pipeline ETL del Global Terrorism Database (Fase 2).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--bootstrap", action="store_true",
        help="ferma la pipeline dopo lo staging e salta l'imputazione",
    )
    parser.add_argument(
        "--sql-only", action="store_true",
        help="riesegue solo la parte SQL e la riconciliazione sul dato gia' in staging",
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="ignora la cache Parquet e rilegge la sorgente Excel",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="log di livello DEBUG")
    parser.add_argument("--log-file", type=str, default=None, help="scrive anche su file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings()
    setup_logging(
        logging.DEBUG if args.verbose else logging.INFO,
        settings.paths.root / args.log_file if args.log_file else None,
    )
    log.info("configurazione:\n%s", settings.describe())

    if args.bootstrap and args.sql_only:
        log.error("--bootstrap e --sql-only sono incompatibili")
        return 2

    imputer = NoOpImputer() if args.bootstrap else None
    pipeline = Pipeline(settings, imputer=imputer)
    try:
        ok = pipeline.run(
            bootstrap=args.bootstrap, sql_only=args.sql_only, use_cache=not args.no_cache
        )
    except Exception:
        log.exception("pipeline interrotta da un errore")
        return 1
    finally:
        pipeline.close()

    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
