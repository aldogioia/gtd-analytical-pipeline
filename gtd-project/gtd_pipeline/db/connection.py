"""Connessione a PostgreSQL. Unico modulo che importa SQLAlchemy."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine

from ..config import DatabaseSettings
from ..logging_setup import get_logger

log = get_logger(__name__)


class DatabaseManager:
    """Incapsula la creazione dell'engine e le operazioni di schema."""

    def __init__(self, settings: DatabaseSettings, echo: bool = False) -> None:
        self.settings = settings
        # pool_pre_ping: il cleaning dura minuti e il server puo' chiudere
        # la connessione nel frattempo.
        self.engine: Engine = create_engine(
            settings.url, echo=echo, pool_pre_ping=True, future=True
        )
        if settings.uses_default_password:
            log.warning(
                "GTD_DB_PASSWORD non impostata: connessione senza password. "
                "Configura l’autenticazione tramite variabili d’ambiente."
            )

    def check_connection(self) -> str:
        """Verifica la connessione e restituisce la versione del server."""
        with self.engine.connect() as conn:
            version = conn.execute(text("SELECT version()")).scalar_one()
        log.info("connesso a %s", str(version).split(" on ")[0])
        return str(version)

    def ensure_schema(self, schema: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        log.info("schema '%s' disponibile", schema)

    @contextmanager
    def begin(self) -> Iterator[Connection]:
        with self.engine.begin() as conn:
            yield conn

    def dispose(self) -> None:
        self.engine.dispose()

    def __enter__(self) -> "DatabaseManager":
        return self

    def __exit__(self, *exc_info) -> None:
        self.dispose()
