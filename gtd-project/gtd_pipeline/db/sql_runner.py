"""Esecuzione degli script SQL del progetto."""

from __future__ import annotations

import re
from pathlib import Path

from sqlalchemy.engine import Engine

from ..logging_setup import get_logger

log = get_logger(__name__)

# Apertura/chiusura di un blocco dollar-quoted: $$ oppure $tag$
_DOLLAR_TAG = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)?\$")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_LINE_COMMENT = re.compile(r"--[^\n]*")


def _scan_quoted(script: str, start: int, quote: str) -> int:
    """Indice successivo alla chiusura di un letterale o identificatore."""
    i, n = start + 1, len(script)
    while i < n:
        if script[i] == quote:
            # Apice raddoppiato: escape, non chiusura
            if i + 1 < n and script[i + 1] == quote:
                i += 2
                continue
            return i + 1
        i += 1
    return n


def _has_code(statement: str) -> bool:
    """Vero se resta qualcosa dopo aver tolto i commenti."""
    without = _BLOCK_COMMENT.sub(" ", statement)
    return bool(_LINE_COMMENT.sub(" ", without).strip())


class SQLScriptRunner:
    """Esegue file SQL in transazione, con errori localizzati."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @staticmethod
    def split_statements(script: str) -> list[str]:
        """Separa gli statement sul ';' di primo livello.

        I ';' dentro commenti, stringhe, identificatori quotati e blocchi
        $$...$$ non contano.
        """
        statements: list[str] = []
        buffer: list[str] = []
        i, n = 0, len(script)

        while i < n:
            # Commento di riga
            if script.startswith("--", i):
                end = script.find("\n", i)
                end = n if end < 0 else end

            # Commento a blocco, annidabile in PostgreSQL
            elif script.startswith("/*", i):
                end, depth = i + 2, 1
                while end < n and depth:
                    if script.startswith("/*", end):
                        depth, end = depth + 1, end + 2
                    elif script.startswith("*/", end):
                        depth, end = depth - 1, end + 2
                    else:
                        end += 1

            # Letterale fra apici singoli
            elif script[i] == "'":
                end = _scan_quoted(script, i, "'")

            # Identificatore fra virgolette
            elif script[i] == '"':
                end = _scan_quoted(script, i, '"')

            # Blocco dollar-quoted: consumato per intero, ';' interni inclusi
            elif script[i] == "$" and (match := _DOLLAR_TAG.match(script, i)):
                tag = match.group(0)
                close = script.find(tag, match.end())
                end = n if close < 0 else close + len(tag)

            # Terminatore di statement
            elif script[i] == ";":
                statements.append("".join(buffer))
                buffer = []
                i += 1
                continue

            else:
                buffer.append(script[i])
                i += 1
                continue

            buffer.append(script[i:end])
            i = end

        statements.append("".join(buffer))
        return [s.strip() for s in statements if _has_code(s)]

    def execute_file(self, path: Path) -> int:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Script SQL non trovato: {path}")
        statements = self.split_statements(path.read_text(encoding="utf-8"))

        with self.engine.begin() as conn:
            for index, statement in enumerate(statements, 1):
                try:
                    # Cursore grezzo: evita che SQLAlchemy interpreti ':=' e '%'.
                    raw_conn = conn.connection
                    cursor = raw_conn.cursor()
                    try:
                        cursor.execute(statement)
                    finally:
                        cursor.close()
                except Exception:
                    log.error("errore nello statement %d di %s", index, path.name)
                    log.error("  %s", statement[:400].replace("\n", "\n  "))
                    raise
        log.info("  %3d statement eseguiti da %s", len(statements), path.name)
        return len(statements)

    def execute_files(self, *paths: Path) -> int:
        return sum(self.execute_file(p) for p in paths)
