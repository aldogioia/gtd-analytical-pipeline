"""Controlli di riconciliazione fra staging, reconciled database e warehouse.

Ogni controllo ha un valore atteso: se anche uno solo fallisce la pipeline
esce con codice diverso da zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import pandas as pd

from ..logging_setup import get_logger

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

log = get_logger(__name__)


@dataclass(frozen=True)
class Check:
    """Un controllo di riconciliazione."""

    label: str
    query: str
    # Predicato sul valore osservato; se None il controllo e' solo informativo.
    expect: Callable[[int, dict[str, int]], bool] | None = None
    explain: str = ""


CHECKS: tuple[Check, ...] = (
    Check("righe staging", "SELECT COUNT(*) FROM staging.raw_gtd"),
    Check("righe rd.event", "SELECT COUNT(*) FROM rd.event"),
    Check(
        "righe dwh.fact_event", "SELECT COUNT(*) FROM dwh.fact_event",
        lambda v, r: v == r["righe rd.event"],
        "il fatto ha la stessa grana dell'evento riconciliato: un evento, una riga",
    ),
    Check("fatti su dim_time Unknown", "SELECT COUNT(*) FROM dwh.fact_event WHERE date_sk = -1"),
    Check("fatti su dim_group Unknown", "SELECT COUNT(*) FROM dwh.fact_event WHERE group_sk = -1"),
    Check(
        "eventi senza bridge arma",
        "SELECT COUNT(*) FROM dwh.fact_event f WHERE NOT EXISTS "
        "(SELECT 1 FROM dwh.bridge_event_weapon b WHERE b.event_sk = f.event_sk)",
        lambda v, r: v == 0,
        "ogni evento deve avere almeno una riga di bridge, altrimenti sparisce "
        "dalle viste per arma",
    ),
    Check(
        "eventi senza bridge bersaglio",
        "SELECT COUNT(*) FROM dwh.fact_event f WHERE NOT EXISTS "
        "(SELECT 1 FROM dwh.bridge_event_target b WHERE b.event_sk = f.event_sk)",
        lambda v, r: v == 0,
        "ogni evento deve avere almeno una riga di bridge, altrimenti sparisce "
        "dalle viste per bersaglio",
    ),
    Check(
        "eventi senza arco arma primario",
        "SELECT COUNT(*) FROM dwh.fact_event f WHERE NOT EXISTS "
        "(SELECT 1 FROM dwh.bridge_event_weapon b "
        "WHERE b.event_sk = f.event_sk AND b.is_primary)",
        lambda v, r: v == 0,
        "l'attribuzione univoca si regge sul filtro is_primary: un evento privo "
        "di arco primario sparirebbe dalle analisi per arma",
    ),
    Check(
        "eventi con piu' di un arco arma primario",
        "SELECT COUNT(*) FROM (SELECT event_sk FROM dwh.bridge_event_weapon "
        "WHERE is_primary GROUP BY event_sk HAVING COUNT(*) > 1) t",
        lambda v, r: v == 0,
        "l'arco primario deve essere unico, altrimenti il filtro is_primary "
        "reintroduce il fan-out che deve neutralizzare",
    ),
    Check(
        "eventi senza arco bersaglio primario",
        "SELECT COUNT(*) FROM dwh.fact_event f WHERE NOT EXISTS "
        "(SELECT 1 FROM dwh.bridge_event_target b "
        "WHERE b.event_sk = f.event_sk AND b.is_primary)",
        lambda v, r: v == 0,
        "stessa proposizione sul ponte dei bersagli",
    ),
    Check(
        "eventi con piu' di un arco bersaglio primario",
        "SELECT COUNT(*) FROM (SELECT event_sk FROM dwh.bridge_event_target "
        "WHERE is_primary GROUP BY event_sk HAVING COUNT(*) > 1) t",
        lambda v, r: v == 0,
        "stessa proposizione sul ponte dei bersagli",
    ),
    Check("vittime totali rd", "SELECT COALESCE(SUM(nkill), 0) FROM rd.event"),
    Check(
        "vittime totali dwh", "SELECT COALESCE(SUM(nkill), 0) FROM dwh.fact_event",
        lambda v, r: v == r["vittime totali rd"],
        "nessuna vittima persa o duplicata nel passaggio allo star schema",
    ),
    Check(
        "vittime totali via arco primario",
        "SELECT COALESCE(SUM(f.nkill), 0) FROM dwh.fact_event f "
        "JOIN dwh.bridge_event_weapon b ON b.event_sk = f.event_sk AND b.is_primary "
        "JOIN dwh.bridge_event_target t ON t.event_sk = f.event_sk AND t.is_primary",
        lambda v, r: v == r["vittime totali dwh"],
        "attraversare ENTRAMBE le bridge filtrando is_primary conserva i totali: "
        "e' la proprieta' che sostituisce le misure allocate",
    ),
    # Controlli sulle gerarchie risolte in Python.
    Check(
        "sottotipi d'arma senza padre valido",
        "SELECT COUNT(*) FROM rd.weapon_subtype ws LEFT JOIN rd.weapon_type wt "
        "ON wt.weaptype_id = ws.weaptype_id WHERE wt.weaptype_id IS NULL",
        lambda v, r: v == 0,
        "integrita' referenziale della gerarchia arma dopo la risoluzione per maggioranza",
    ),
    Check(
        "sottotipi di bersaglio senza padre valido",
        "SELECT COUNT(*) FROM rd.target_subtype ts LEFT JOIN rd.target_type tt "
        "ON tt.targtype_id = ts.targtype_id WHERE tt.targtype_id IS NULL",
        lambda v, r: v == 0,
        "integrita' referenziale della gerarchia bersaglio",
    ),
    Check(
        "sottotipi esplosivi sotto Firearms",
        "SELECT COUNT(*) FROM rd.weapon_subtype ws JOIN rd.weapon_type wt "
        "ON wt.weaptype_id = ws.weaptype_id "
        "WHERE ws.weapsubtype_id IN (7, 8, 11, 16, 17) AND wt.weapon_name <> 'Explosives'",
        lambda v, r: v == 0,
        "regressione del difetto MIN(): Grenade, Landmine, Projectile, Unknown e Other "
        "Explosive Type devono stare sotto Explosives",
    ),
)


class Reconciler:
    """Esegue i controlli e produce il verdetto."""

    def __init__(self, engine: "Engine", checks: tuple[Check, ...] = CHECKS) -> None:
        self.engine = engine
        self.checks = checks

    def run(self) -> tuple[pd.DataFrame, bool]:
        from sqlalchemy import text

        values: dict[str, int] = {}
        with self.engine.connect() as conn:
            for check in self.checks:
                values[check.label] = conn.execute(text(check.query)).scalar()

        rows = []
        ok = True
        for check in self.checks:
            observed = values[check.label]
            if check.expect is None:
                verdict = "-"
            else:
                passed = bool(check.expect(observed, values))
                ok &= passed
                verdict = "OK" if passed else "FALLITO"
            rows.append({
                "Controllo": check.label,
                "Valore": observed,
                "Esito": verdict,
                "Perche": check.explain,
            })

        report = pd.DataFrame(rows)
        log.info("--- RICONCILIAZIONE ---")
        for _, row in report.iterrows():
            log.info("  %-6s %-42s %s", row["Esito"], row["Controllo"], _fmt(row["Valore"]))
        log.info("esito complessivo: %s", "OK" if ok else "DISALLINEAMENTO DA INVESTIGARE")
        return report, ok


def _fmt(value) -> str:
    """Formatta il valore osservato senza mai far fallire il report."""
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "n/d" if value is None else str(value)
