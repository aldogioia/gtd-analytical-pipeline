"""Profilazione e pulizia del dataset GTD."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..audit import AuditLog, Level, Taxonomy
from ..logging_setup import get_logger

log = get_logger(__name__)


class DataQualityManager:
    """Ogni intervento e' registrato nell'audit log."""

    # Sentinelle di non risposta, diverse per famiglia di colonne.
    _COUNTS = ["nkill", "nkillter", "nwound", "nperps", "propvalue"]
    _FLAGS = ["property", "vicinity", "claimed", "guncertain1", "doubtterr"]
    _CODES = (
        ["region", "country", "natlty1", "specificity", "propextent", "attacktype1"]
        + [f"weaptype{i}" for i in range(1, 5)]
        + [f"weapsubtype{i}" for i in range(1, 5)]
        + [f"targtype{i}" for i in range(1, 4)]
        + [f"targsubtype{i}" for i in range(1, 4)]
    )

    SENTINELS = (
        {c: [-99] for c in _COUNTS}
        | {c: [-9] for c in _FLAGS}
        | {c: [-9, -99] for c in _CODES}
    )

    # 'Unknown' previsti dal dominio: sono membri legittimi, non vanno rimossi.
    IN_DOMAIN_UNKNOWN = {"attacktype1": 9, "weaptype1": 13, "targtype1": 20}

    # 'Unknown' dentro una scala ordinale: a NaN, altrimenti l'ordinamento
    # lo leggerebbe come il livello piu' grave.
    ORDINAL_UNKNOWN = {"propextent": [4]}

    # Raccolti solo dopo il 1997: la loro assenza prima non e' un errore.
    POST_1997_FIELDS = ["multiple", "doubtterr"]

    # Binarie il cui zero significa "no oppure nessuna indicazione".
    BINARY_FILL_ZERO = ["crit1", "crit2", "crit3"]

    BINARY_COLS = [
        "suicide", "multiple", "success", "extended", "property", "crit1", "crit2",
        "crit3", "vicinity", "guncertain1", "claimed", "doubtterr",
    ]

    # Domini da codebook, usati per la metrica di validita'.
    DOMAINS = {
        "iyear": (1970, 2021), "imonth": (0, 12), "iday": (0, 31),
        "latitude": (-90, 90), "longitude": (-180, 180),
        "specificity": (1, 5), "propextent": (1, 4),
        "region": (1, 12), "attacktype1": (1, 9),
        "weaptype1": (1, 13), "targtype1": (1, 22),
        "nkill": (0, None), "nkillter": (0, None), "nwound": (0, None),
        "nperps": (0, None), "propvalue": (0, None),
        "success": {0, 1}, "suicide": {0, 1}, "extended": {0, 1},
        "multiple": {0, 1}, "property": {0, 1}, "vicinity": {0, 1},
        "crit1": {0, 1}, "crit2": {0, 1}, "crit3": {0, 1},
        "claimed": {0, 1}, "guncertain1": {0, 1}, "doubtterr": {0, 1},
    }

    def __init__(self, df: pd.DataFrame, audit: AuditLog, outlier_z: float = 10.0) -> None:
        self.df = df.copy()
        self.audit = audit
        self.outlier_z = outlier_z
        self.assessments: dict[str, pd.DataFrame] = {}

    def assess(self, stage: str) -> pd.DataFrame:
        """Profilazione: completezza, validita' rispetto al dominio, unicita'."""
        n = len(self.df)
        rows = []
        for col in self.df.columns:
            series = self.df[col]
            non_null = int(series.notna().sum())
            validity = np.nan
            domain = self.DOMAINS.get(col)
            if domain is not None and non_null:
                numeric = pd.to_numeric(series, errors="coerce")
                if isinstance(domain, set):
                    valid = numeric.isin(domain)
                else:
                    low, high = domain
                    valid = numeric.ge(low) if high is None else numeric.between(low, high)
                validity = float((valid & numeric.notna()).sum()) / non_null
            rows.append({
                "Stage": stage,
                "Feature": col,
                "Dtype": str(series.dtype),
                "Completeness_%": round(100 * non_null / n, 2) if n else np.nan,
                "Validity_%": round(100 * validity, 2) if validity == validity else "-",
                "Unique": int(series.nunique(dropna=True)),
            })
        report = pd.DataFrame(rows)
        self.assessments[stage] = report
        return report

    def check_uniqueness(self) -> "DataQualityManager":
        """eventid e' la chiave naturale del fatto: deve essere unica."""
        before = len(self.df)
        duplicated = int(self.df["eventid"].duplicated().sum())
        if duplicated:
            self.df = self.df.drop_duplicates(subset="eventid", keep="first")
            self.audit.log(
                "check_uniqueness", Level.SCHEMA, Taxonomy.DUPLICATE, "eventid",
                "Rimozione duplicati sulla chiave naturale",
                "eventid identifica univocamente l incidente e diventa dimensione "
                "degenere nel DW",
                rows_affected=duplicated, rows_before=before, rows_after=len(self.df),
                domain_rule="Regola di dominio - identificativo univoco dell'evento",
            )
        return self

    def clean_sentinels(self) -> "DataQualityManager":
        """Mappa a NaN i codici di errore, colonna per colonna."""
        for col, codes in self.SENTINELS.items():
            if col not in self.df.columns:
                continue
            numeric = pd.to_numeric(self.df[col], errors="coerce")
            mask = numeric.isin(codes)
            count = int(mask.sum())
            if count:
                self.df[col] = numeric.mask(mask)
                self.audit.log(
                    "clean_sentinels", Level.INSTANCE, Taxonomy.NOISY, col,
                    f"Sostituzione dei codici {codes} con NaN",
                    "Codici sentinella di ignoto: trattarli come valori numerici ne "
                    "falserebbe medie, correlazioni e ordinamenti",
                    rows_affected=count, domain_rule="Regola di dominio - sentinelle di non risposta",
                )
        return self

    def normalize_domains(self) -> "DataQualityManager":
        """Riconduce al dominio dichiarato i valori fuori scala."""
        # 1. codici Unknown dentro una scala ordinale
        for col, codes in self.ORDINAL_UNKNOWN.items():
            if col not in self.df.columns:
                continue
            numeric = pd.to_numeric(self.df[col], errors="coerce")
            mask = numeric.isin(codes)
            count = int(mask.sum())
            if count:
                self.df[col] = numeric.mask(mask)
                self.audit.log(
                    "normalize_domains", Level.INSTANCE, Taxonomy.INCONSISTENT, col,
                    f"Codici {codes} riportati a NaN",
                    "propextent e ordinale (1 catastrofico -> 3 minore): il codice 4 "
                    "significa Unknown e verrebbe altrimenti letto come massima gravita",
                    rows_affected=count,
                    domain_rule="Regola di dominio - scala ordinale del danno materiale",
                )

        # 2. valori fuori dominio
        for col, domain in self.DOMAINS.items():
            if col not in self.df.columns or isinstance(domain, set):
                continue
            low, high = domain
            numeric = pd.to_numeric(self.df[col], errors="coerce")
            invalid = ~numeric.between(low, high if high is not None else np.inf)
            invalid &= numeric.notna()
            count = int(invalid.sum())
            if count:
                self.df[col] = numeric.mask(invalid)
                self.audit.log(
                    "normalize_domains", Level.INSTANCE, Taxonomy.INCONSISTENT, col,
                    f"Valori fuori dal dominio [{low}, {high}] riportati a NaN",
                    "Il valore cade fuori dal dominio ammesso dalla specifica della variabile",
                    rows_affected=count,
                    domain_rule="Regola di dominio - intervallo ammesso della variabile",
                )

        # 3. Null Island
        if {"latitude", "longitude"} <= set(self.df.columns):
            null_island = (self.df["latitude"] == 0) & (self.df["longitude"] == 0)
            count = int(null_island.sum())
            if count:
                self.df.loc[null_island, ["latitude", "longitude"]] = np.nan
                self.audit.log(
                    "normalize_domains", Level.INSTANCE, Taxonomy.INCONSISTENT,
                    "latitude/longitude", "Coordinate (0, 0) riportate a NaN",
                    "La coppia (0,0) e una posizione reale nel Golfo di Guinea: "
                    "conservarla genererebbe un cluster fittizio di attentati sulla mappa",
                    rows_affected=count, domain_rule="Vincolo di dominio - localizzazione dell'evento",
                )
        return self

    def resolve_dates(self) -> "DataQualityManager":
        """Ricostruisce la data completa tracciandone la precisione."""
        month = pd.to_numeric(self.df["imonth"], errors="coerce").replace(0, np.nan)
        day = pd.to_numeric(self.df["iday"], errors="coerce").replace(0, np.nan)

        precision = np.where(month.isna(), "year", np.where(day.isna(), "month", "day"))
        self.df["date_precision"] = precision
        self.df["is_approximate_date"] = precision != "day"

        # midpoint: mese ignoto -> 1 luglio, giorno ignoto -> giorno 15
        month_filled = month.fillna(7)
        day_filled = day.where(month.notna(), 1).fillna(15)

        self.df["imonth"] = month_filled.astype("int16")
        self.df["iday"] = day_filled.astype("int16")

        self.df["full_date"] = pd.to_datetime(
            dict(
                year=pd.to_numeric(self.df["iyear"], errors="coerce").astype("int16"),
                month=self.df["imonth"],
                day=self.df["iday"],
            ),
            errors="coerce",
        )

        for level, label in (("year", "mese e giorno ignoti"), ("month", "giorno ignoto")):
            count = int((precision == level).sum())
            if count:
                self.audit.log(
                    "resolve_dates", Level.INSTANCE, Taxonomy.MISSING, "imonth/iday",
                    f"Midpoint imputation ({label})",
                    "La codifica di dominio assegna 0 al mese o al giorno non determinati. Si "
                    "adotta il punto medio del periodo e si traccia la precisione in "
                    "date_precision",
                    rows_affected=count, domain_rule="Regola di dominio - data dell'evento",
                )

        unparsed = int(self.df["full_date"].isna().sum())
        if unparsed:
            self.audit.log(
                "resolve_dates", Level.INSTANCE, Taxonomy.INCONSISTENT, "full_date",
                "Date non interpretabili lasciate a NaT",
                "Combinazioni giorno/mese inesistenti nel calendario. Il DW le associa "
                "al membro Unknown di dim_time",
                rows_affected=unparsed, domain_rule="Regola di dominio - data dell'evento",
            )
        return self

    def flag_structural_missing(self) -> "DataQualityManager":
        """Distingue il mancante strutturale da quello accidentale."""
        for col in self.POST_1997_FIELDS:
            if col not in self.df.columns:
                continue
            pre_1997 = (self.df["iyear"] < 1998) & self.df[col].isna()
            count = int(pre_1997.sum())
            if count:
                self.audit.log(
                    "flag_structural_missing", Level.INSTANCE,
                    Taxonomy.STRUCTURAL_MISSING, col,
                    "Mancante conservato come NaN, nessuna imputazione",
                    "La variabile e rilevata sistematicamente solo "
                    "dopo il 1997: imputare 0 creerebbe un artefatto temporale nelle "
                    "serie storiche",
                    rows_affected=count,
                    domain_rule="Regola di dominio - copertura temporale della rilevazione",
                )
        return self

    def handle_binaries(self) -> "DataQualityManager":
        """Riempie con 0 solo le binarie per cui la regola di dominio lo autorizza."""
        for col in self.BINARY_FILL_ZERO:
            if col not in self.df.columns:
                continue
            count = int(self.df[col].isna().sum())
            if count:
                self.df[col] = self.df[col].fillna(0)
                self.audit.log(
                    "handle_binaries", Level.INSTANCE, Taxonomy.MISSING, col,
                    "Riempimento con 0",
                    'La regola di dominio definisce lo 0 come "criterio non soddisfatto OPPURE '
                    'nessuna indicazione che lo sia": il riempimento e semanticamente '
                    "corretto",
                    rows_affected=count, domain_rule="Regola di dominio - criteri di inclusione",
                )

        preserved = [
            c for c in self.BINARY_COLS
            if c not in self.BINARY_FILL_ZERO
            and c in self.df.columns
            and self.df[c].isna().any()
        ]
        if preserved:
            self.audit.log(
                "handle_binaries", Level.INSTANCE, Taxonomy.MISSING, ", ".join(preserved),
                "Mancanti conservati come NaN",
                "Nessuna regola di dominio autorizza ad assumere il valore 0. "
                "Il mancante e materializzato come Unknown nella junk dimension dim_quality",
                rows_affected=int(self.df[preserved].isna().any(axis=1).sum()),
                domain_rule="Regola di dominio - assenza di un default ammesso",
            )
        return self

    def enforce_consistency(self) -> "DataQualityManager":
        """Vincoli di integrita' semantica fra colonne."""
        self.df = self.enforce_casualty_consistency(self.df, self.audit, "enforce_consistency")

        # I conteggi frazionari sono ammessi: un totale cumulato puo' essere
        # ripartito fra piu' incidenti collegati.
        for col in ["nkill", "nkillter", "nwound"]:
            if col not in self.df.columns:
                continue
            numeric = pd.to_numeric(self.df[col], errors="coerce")
            fractional = numeric.notna() & (numeric % 1 != 0)
            count = int(fractional.sum())
            if count:
                self.df[col] = numeric.round()
                self.audit.log(
                    "enforce_consistency", Level.INSTANCE, Taxonomy.INCONSISTENT, col,
                    "Arrotondamento dei conteggi frazionari",
                    "La regola di dominio ammette valori frazionari quando un totale cumulato "
                    "viene ripartito su piu incidenti collegati. Il data warehouse "
                    "richiede pero conteggi interi: la misura e un conteggio di "
                    "persone, e come tale deve restare un numero naturale",
                    rows_affected=count,
                    domain_rule="Regola di dominio - conteggi di vittime interi",
                )

        # propvalue valorizzato ma property dichiarato assente
        if {"propvalue", "property"} <= set(self.df.columns):
            conflict = (self.df["propvalue"] > 0) & (self.df["property"] == 0)
            count = int(conflict.sum())
            if count:
                self.audit.log(
                    "enforce_consistency", Level.INSTANCE, Taxonomy.INCONSISTENT,
                    "propvalue/property",
                    "Incoerenza rilevata e tracciata, valori conservati",
                    "La regola di dominio valorizza propvalue solo se property = Yes. I casi "
                    "residui sono segnalati ma non corretti, per non distruggere "
                    "informazione economica",
                    rows_affected=count, domain_rule="Vincolo di coerenza - propvalue / property",
                )

        # Da calcolare prima dell'imputazione, altrimenti il flag e' falsato.
        if "nkillter" in self.df.columns:
            self.df["nkillter_reported"] = self.df["nkillter"].notna().astype("int8")
        return self

    @staticmethod
    def enforce_casualty_consistency(
        df: pd.DataFrame, audit: AuditLog, step: str
    ) -> pd.DataFrame:
        """nkillter <= nkill. Va riapplicata anche dopo l'imputazione."""
        if not {"nkill", "nkillter"} <= set(df.columns):
            return df
        both = df["nkill"].notna() & df["nkillter"].notna()
        violation = both & (df["nkillter"] > df["nkill"])
        count = int(violation.sum())
        if count:
            df.loc[violation, "nkillter"] = df.loc[violation, "nkill"]
            audit.log(
                step, Level.INSTANCE, Taxonomy.INCONSISTENT, "nkillter",
                "Troncamento di nkillter al valore di nkill",
                "La regola di dominio definisce nkill come comprensivo delle vittime e degli "
                "attentatori: nkillter non puo eccederlo",
                rows_affected=count,
                domain_rule="Vincolo di coerenza - nkillter <= nkill",
            )
        return df

    def report_outliers(self) -> "DataQualityManager":
        """Segnala gli outlier SENZA eliminare righe."""
        for col in ["nperps", "nkill", "nwound"]:
            if col not in self.df.columns:
                continue
            numeric = pd.to_numeric(self.df[col], errors="coerce")
            median = numeric.median()
            mad = (numeric - median).abs().median()
            if not mad or pd.isna(mad):
                continue
            score = (numeric - median).abs() / (1.4826 * mad)
            count = int((score > self.outlier_z).sum())
            if count:
                self.audit.log(
                    "report_outliers", Level.INSTANCE, Taxonomy.OUTLIER, col,
                    "Outlier segnalati, nessuna riga eliminata",
                    "Si adotta lo z-score robusto su MAD invece della deviazione "
                    "standard, che e essa stessa inflazionata dagli outlier. Gli eventi "
                    "estremi del GTD sono reali (es. 11 settembre 2001): eliminarli "
                    "falserebbe i conteggi del DW",
                    rows_affected=count, domain_rule="Scelta metodologica - trattamento degli outlier",
                )
        return self

    def run(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        log.info("data quality: assessment e cleaning su %d righe", len(self.df))
        report_before = self.assess("pre-cleaning")
        (
            self.check_uniqueness()
            .clean_sentinels()
            .normalize_domains()
            .resolve_dates()
            .flag_structural_missing()
            .handle_binaries()
            .enforce_consistency()
            .report_outliers()
        )
        report_after = self.assess("post-cleaning")
        log.info("  righe dopo il cleaning: %d | voci di audit: %d", len(self.df), len(self.audit))
        return self.df, report_before, report_after
