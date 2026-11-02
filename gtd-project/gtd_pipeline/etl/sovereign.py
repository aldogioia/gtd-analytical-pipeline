"""Livello gerarchico stato sovrano sopra paese e nazionalita', con SCD di tipo 2.

Serve a calcolare correttamente 'is_transnational': nel GTD il paese
dell'attentato e la nazionalita' del bersaglio non usano lo stesso livello
(un solo membro 'United Kingdom' da un lato, tre dall'altro), e per la Germania
la mappa cambia con la riunificazione del 1990. Da qui la storicizzazione.
"""

from __future__ import annotations

import pandas as pd

from ..audit import AuditLog, Level, Taxonomy
from ..logging_setup import get_logger

log = get_logger(__name__)


class SovereignStateResolver:
    """Risolve i membri geografici nel loro stato sovrano all'anno dell'evento."""

    REUNIFICATION_YEAR = 1990   # 3 ottobre 1990; la grana del fatto e' l'anno
    OPEN_END = 9999             # convenzione per "versione corrente"

    # (membro, stato_sovrano, valido_da, valido_a, tipo_scd, nota)
    MAPPING = [
        ("Great Britain", "United Kingdom", 1970, OPEN_END, 1,
         "Nazionalita GTD interna al Regno Unito"),
        ("Northern Ireland", "United Kingdom", 1970, OPEN_END, 1,
         "Nazionalita GTD interna al Regno Unito"),
        ("United Kingdom", "United Kingdom", 1970, OPEN_END, 1,
         "Membro coincidente con lo stato sovrano"),
        ("West Germany (FRG)", "West Germany (FRG)", 1970, REUNIFICATION_YEAR - 1, 2,
         "Stato sovrano autonomo fino alla riunificazione"),
        ("West Germany (FRG)", "Germany", REUNIFICATION_YEAR, OPEN_END, 2,
         "Confluita nella Germania riunificata"),
        ("East Germany (GDR)", "East Germany (GDR)", 1970, REUNIFICATION_YEAR - 1, 2,
         "Stato sovrano autonomo fino alla riunificazione"),
        ("East Germany (GDR)", "Germany", REUNIFICATION_YEAR, OPEN_END, 2,
         "Confluita nella Germania riunificata"),
        # Demonimo pre-riunificazione: non e' uno stato, si risolve sul
        # territorio dell'attentato.
        ("Germany", None, 1970, REUNIFICATION_YEAR - 1, 2,
         "Demonimo, non uno stato sovrano: si risolve sul territorio dell attentato"),
        ("Germany", "Germany", REUNIFICATION_YEAR, OPEN_END, 2,
         "Germania riunificata"),
    ]

    UK_MEMBERS = ("Great Britain", "Northern Ireland", "United Kingdom")
    GERMAN_STATES_PRE = ("West Germany (FRG)", "East Germany (GDR)")
    GERMAN_DEMONYM = "Germany"

    def __init__(self, audit: AuditLog | None = None) -> None:
        self.audit = audit

    def dimension(self) -> pd.DataFrame:
        """La dimensione conforme, pronta per 'staging.dim_sovereign_state'."""
        rows = pd.DataFrame(
            self.MAPPING,
            columns=["member", "sovereign_state", "valid_from", "valid_to", "scd_type", "note"],
        )
        rows["is_current"] = (rows["valid_to"] == self.OPEN_END).astype(int)

        # sovereign_state nullo: la risoluzione e' delegata al territorio
        # dell'evento.
        rows["resolve_on"] = rows["sovereign_state"].isna().map({True: "territory", False: ""})
        return rows

    def resolve(self, member, year: int, territory=None):
        """Risolve un membro nel suo stato sovrano all'anno dell'evento.

        'territory' serve solo al demonimo tedesco pre-riunificazione.
        """
        if pd.isna(member):
            return member
        if member in self.UK_MEMBERS:
            return "United Kingdom"
        if member in self.GERMAN_STATES_PRE:
            return "Germany" if year >= self.REUNIFICATION_YEAR else member
        if member == self.GERMAN_DEMONYM:
            if year >= self.REUNIFICATION_YEAR:
                return "Germany"
            return territory if territory in self.GERMAN_STATES_PRE else "Germany"
        return member

    def apply(
        self,
        df: pd.DataFrame,
        country_col: str = "country_txt",
        natlty_col: str = "natlty1_txt",
        year_col: str = "iyear",
    ) -> pd.DataFrame:
        """Aggiunge le colonne risolte e il flag transnazionale corretto.

        Il flag grezzo resta in 'is_transnational_raw': la differenza fra i due
        e' essa stessa un risultato.
        """
        out = df.copy()
        years = out[year_col].astype("Int64")

        out["country_sovereign"] = [
            self.resolve(c, y if pd.notna(y) else -1)
            for c, y in zip(out[country_col], years)
        ]
        out["target_nat_sovereign"] = [
            self.resolve(t, y if pd.notna(y) else -1, territory=c)
            for t, c, y in zip(out[natlty_col], out[country_col], years)
        ]

        unknown = out[natlty_col].isna() | (out[natlty_col] == "Unknown")
        raw = (~unknown) & (out[country_col] != out[natlty_col])
        sov = (~unknown) & (out["country_sovereign"] != out["target_nat_sovereign"])

        out["is_transnational_raw"] = raw.astype(int)
        out["is_transnational"] = sov.astype(int)

        corrected = int((raw & ~sov).sum())
        if self.audit is not None:
            self.audit.log(
                "sovereign_state", Level.SCHEMA, Taxonomy.GRANULARITY, "is_transnational",
                "Riclassificazione del flag al livello stato sovrano (SCD di tipo 2)",
                "I due ruoli di dim_country usavano livelli di gerarchia diversi: il "
                "confronto produceva falsi positivi fra membri del medesimo stato "
                "sovrano alla data dell evento",
                rows_affected=corrected, domain_rule="Integrita' relazionale - paese dell'evento / nazionalita' del bersaglio",
            )
        log.info(
            "stati sovrani risolti: %s attentati riclassificati da transnazionali a domestici",
            f"{corrected:,}",
        )
        return out
