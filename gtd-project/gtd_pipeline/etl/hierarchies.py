"""Risoluzione delle gerarchie e delle macro-categorie.

Unica fonte di verita' per il livello *_macro e per il padre di ogni
sottotipo. La pipeline esegue questo modulo in fase di cleaning e materializza
il risultato in 'staging.hier_*'; l'SQL del reconciled database si limita a
leggerlo, quindi nessuna regola di dominio vive dentro l'SQL.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..audit import AuditLog, Level, Taxonomy
from ..logging_setup import get_logger

log = get_logger(__name__)

# Codici che nella sorgente significano ignoto o errore di codifica e non
# sono membri della gerarchia.
INVALID_CODES = (-1, -9, -99)

# Chiave surrogata convenzionale del membro Unknown, in ogni gerarchia.
UNKNOWN_ID = -1
UNKNOWN_LABEL = "Unknown"


# Funzioni di raggruppamento: il livello *_macro
# Sono funzioni totali sui codici di dominio: ogni membro ha esattamente un
# padre, e i codici non elencati ricadono nel membro residuo dichiarato.

ATTACK_MACRO: dict[int, str] = {
    1: "Against Persons",        # Assassination
    2: "Against Persons",        # Armed Assault
    8: "Against Persons",        # Unarmed Assault
    3: "Explosive or Property",  # Bombing/Explosion
    7: "Explosive or Property",  # Facility/Infrastructure Attack
    4: "Hostage Related",        # Hijacking
    5: "Hostage Related",        # Hostage Taking (Barricade Incident)
    6: "Hostage Related",        # Hostage Taking (Kidnapping)
    9: "Unknown",
}
ATTACK_MACRO_DEFAULT = "Unknown"

WEAPON_MACRO: dict[int, str] = {
    1: "CBRN", 2: "CBRN", 3: "CBRN", 4: "CBRN",            # bio, chim, radio, nucl
    5: "Conventional", 6: "Conventional",                   # firearms, explosives
    8: "Conventional", 9: "Conventional",                   # incendiary, melee
    7: "Other", 10: "Other", 11: "Other", 12: "Other",      # falsi, veicoli, sabotaggio
    13: "Unknown",
}
WEAPON_MACRO_DEFAULT = "Unknown"

TARGET_MACRO: dict[int, str] = {
    2: "State and Security", 3: "State and Security",
    4: "State and Security", 7: "State and Security",
    5: "Civilian and Society", 8: "Civilian and Society",
    10: "Civilian and Society", 12: "Civilian and Society",
    14: "Civilian and Society", 15: "Civilian and Society",
    18: "Civilian and Society",
    1: "Economic",
    6: "Infrastructure and Transport", 9: "Infrastructure and Transport",
    11: "Infrastructure and Transport", 16: "Infrastructure and Transport",
    19: "Infrastructure and Transport", 21: "Infrastructure and Transport",
    17: "Armed Non State Actors", 22: "Armed Non State Actors",
    # 13 e 20 sono elencati invece di ricadere nel default: cosi' il test sul
    # dominio si accorge se la sorgente introduce un codice nuovo.
    13: "Other or Unknown",
    20: "Other or Unknown",
}
TARGET_MACRO_DEFAULT = "Other or Unknown"

# Macro-area geografica
# Le 12 regioni GTD raggruppate in 6 macro-aree: dodici categorie non sono
# distinguibili dal colore, sei lo sono.
REGION_MACRO_AREA: dict[int, str] = {
    10: "Medio Oriente e Nord Africa",
    6: "Asia meridionale",
    11: "Africa subsahariana",
    3: "America Latina",          # South America
    2: "America Latina",          # Central America & Caribbean
    8: "Europa e Nord America",   # Western Europe
    9: "Europa e Nord America",   # Eastern Europe
    1: "Europa e Nord America",   # North America
    5: "Asia orientale e Oceania",  # Southeast Asia
    4: "Asia orientale e Oceania",  # East Asia
    7: "Asia orientale e Oceania",  # Central Asia
    12: "Asia orientale e Oceania",  # Australasia & Oceania
}
REGION_MACRO_DEFAULT = "Unknown"

# Gruppo narrativo d'arma
# Aggregazione diversa da weapon_macro: risponde alla domanda "con che cosa e'
# stato fatto materialmente l'attentato". Tre soli gruppi, per leggibilita'
# del colore.
WEAPON_GROUP: dict[int, str] = {6: "Esplosivi", 5: "Armi da fuoco"}
WEAPON_GROUP_DEFAULT = "Altre armi"


def _map_total(codes: pd.Series, mapping: dict[int, str], default: str) -> pd.Series:
    """Applica una funzione di raggruppamento totale.

    Il fillna copre i codici non elencati: senza, un codice nuovo darebbe NULL
    e romperebbe il NOT NULL della colonna *_macro molto lontano dalla causa.
    """
    return codes.map(mapping).fillna(default)


# Risoluzione del padre per maggioranza
@dataclass
class ParentResolution:
    """Esito della risoluzione di una gerarchia a due livelli."""

    mapping: pd.DataFrame          # child_id, parent_id, support, label
    conflicts: pd.DataFrame        # membri con piu' di un padre osservato
    observations: int              # coppie (figlio, padre) osservate
    dissenting: int                # osservazioni non allineate al maggioritario

    @property
    def dissent_rate(self) -> float:
        return self.dissenting / self.observations if self.observations else 0.0


def resolve_parent_by_majority(
    pairs: pd.DataFrame,
    child_col: str,
    parent_col: str,
    label_col: str | None = None,
) -> ParentResolution:
    """Assegna a ogni figlio il padre con cui la sorgente lo associa piu' spesso.

    Le parita' si risolvono sull'id minore: serve una regola deterministica,
    altrimenti due esecuzioni sugli stessi dati danno warehouse diversi.
    """
    valid = pairs.dropna(subset=[child_col, parent_col]).copy()
    valid = valid[
        ~valid[child_col].isin(INVALID_CODES) & ~valid[parent_col].isin(INVALID_CODES)
    ]
    valid[child_col] = valid[child_col].astype(int)
    valid[parent_col] = valid[parent_col].astype(int)

    counts = (
        valid.groupby([child_col, parent_col], as_index=False)
        .size()
        .rename(columns={"size": "support"})
    )

    # Prima il piu' osservato, a parita' l'id minore.
    counts = counts.sort_values(
        [child_col, "support", parent_col], ascending=[True, False, True]
    )
    winners = counts.drop_duplicates(subset=child_col, keep="first").reset_index(drop=True)

    totals = counts.groupby(child_col, as_index=False)["support"].sum()
    totals = totals.rename(columns={"support": "total"})
    winners = winners.merge(totals, on=child_col)
    winners["dissenting"] = winners["total"] - winners["support"]

    # Membri con piu' di un padre osservato. I nomi delle colonne sono
    # normalizzati a child_id / parent_id: i consumatori sono generici sulle
    # tre gerarchie.
    multi = counts[child_col].duplicated(keep=False)
    conflicts = counts[multi].merge(
        winners[[child_col, parent_col]].rename(columns={parent_col: "assigned_parent"}),
        on=child_col,
        how="left",
    )
    conflicts["is_assigned"] = conflicts[parent_col] == conflicts["assigned_parent"]
    conflicts = conflicts.rename(
        columns={child_col: "child_id", parent_col: "parent_id"}
    )[["child_id", "parent_id", "support", "assigned_parent", "is_assigned"]]

    # Anche l'etichetta per maggioranza: la sorgente scrive lo stesso codice
    # con grafie leggermente diverse.
    if label_col is not None and label_col in valid.columns:
        labels = (
            valid.dropna(subset=[label_col])
            .groupby([child_col, label_col], as_index=False)
            .size()
            .sort_values([child_col, "size", label_col], ascending=[True, False, True])
            .drop_duplicates(subset=child_col, keep="first")[[child_col, label_col]]
        )
        winners = winners.merge(labels, on=child_col, how="left")
        winners[label_col] = winners[label_col].fillna(UNKNOWN_LABEL)

    return ParentResolution(
        mapping=winners,
        conflicts=conflicts,
        observations=int(counts["support"].sum()),
        dissenting=int(winners["dissenting"].sum()),
    )


def _majority_label(frame: pd.DataFrame, key: str, label: str) -> pd.DataFrame:
    """Etichetta di un membro senza padre da risolvere (tipi, regioni, paesi)."""
    valid = frame.dropna(subset=[key]).copy()
    valid = valid[~valid[key].isin(INVALID_CODES)]
    valid[key] = valid[key].astype(int)
    valid[label] = valid[label].astype("string").str.strip()
    out = (
        valid.dropna(subset=[label])
        .groupby([key, label], as_index=False)
        .size()
        .sort_values([key, "size", label], ascending=[True, False, True])
        .drop_duplicates(subset=key, keep="first")[[key, label]]
        .reset_index(drop=True)
    )
    return out


# Il risolutore
class HierarchyResolver:
    """Produce i DataFrame pronti per 'staging.hier_*'.

    Ogni gerarchia include il membro Unknown (id -1), che permette al warehouse
    di rappresentare l'ignoto senza NULL sulle chiavi esterne.
    """

    # Slot della sorgente da cui si raccolgono le coppie osservate.
    WEAPON_SLOTS = range(1, 5)
    TARGET_SLOTS = range(1, 4)

    def __init__(self, audit: AuditLog, strict: bool = True) -> None:
        self.audit = audit
        self.strict = strict
        self.resolutions: dict[str, ParentResolution] = {}

    @staticmethod
    def _stack(df: pd.DataFrame, columns: list[tuple[str, ...]], names: list[str]) -> pd.DataFrame:
        """Impila piu' gruppi di colonne (gli slot) in un'unica tabella lunga."""
        blocks = []
        for group in columns:
            if not all(col in df.columns for col in group):
                continue
            block = df.loc[:, list(group)].copy()
            block.columns = names
            blocks.append(block)
        if not blocks:
            return pd.DataFrame(columns=names)
        out = pd.concat(blocks, ignore_index=True)
        for col in names:
            if col.endswith("_id"):
                out[col] = pd.to_numeric(out[col], errors="coerce")
        return out

    def build(self, df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        """Costruisce tutte le tabelle di gerarchia dal dato pulito.

        I tipi vanno risolti prima dei sottotipi: il segnaposto Not Specified
        va creato per ogni tipo, altrimenti un evento con tipo ma senza
        sottotipo perde la riga di bridge.
        """
        log.info("risoluzione delle gerarchie e delle macro-categorie")
        weapon_types = self._weapon_types(df)
        target_types = self._target_types(df)
        tables = {
            "region": self._regions(df),
            "country": self._countries(df),
            "attack_type": self._attack_types(df),
            "weapon_type": weapon_types,
            "weapon_subtype": self._weapon_subtypes(df, weapon_types),
            "target_type": target_types,
            "target_subtype": self._target_subtypes(df, target_types),
        }
        self._audit_conflicts()
        for name, table in tables.items():
            log.info("  %-16s %4d membri", name, len(table))
        return tables

    # Geografia
    def _regions(self, df: pd.DataFrame) -> pd.DataFrame:
        labels = _majority_label(df[["region", "region_txt"]].copy(), "region", "region_txt")
        labels = labels.rename(columns={"region": "region_id", "region_txt": "region_name"})
        labels["macro_area"] = _map_total(
            labels["region_id"], REGION_MACRO_AREA, REGION_MACRO_DEFAULT
        )
        unknown = pd.DataFrame(
            [{"region_id": UNKNOWN_ID, "region_name": UNKNOWN_LABEL,
              "macro_area": REGION_MACRO_DEFAULT}]
        )
        return pd.concat([unknown, labels], ignore_index=True)

    def _countries(self, df: pd.DataFrame) -> pd.DataFrame:
        """Paesi come unione fra paese dell'attentato e nazionalita' del bersaglio.

        Sono due ruoli della stessa dimensione, e il GTD usa come nazionalita'
        18 codici che non compaiono mai come paese: senza l'unione la FK
        'natlty_id' di 'rd.event' verrebbe violata. Quei 18 non hanno una
        regione osservata e vanno sul membro Unknown.
        """
        as_country = df[["country", "region", "country_txt"]].copy()
        as_country.columns = ["country_id", "region_id", "country_name"]

        as_nationality = df[["natlty1", "natlty1_txt"]].copy()
        as_nationality.columns = ["country_id", "country_name"]
        as_nationality["region_id"] = np.nan

        pairs = pd.concat(
            [as_country, as_nationality[["country_id", "region_id", "country_name"]]],
            ignore_index=True,
        )

        # La risoluzione del padre lavora sulle sole coppie con regione nota.
        resolution = resolve_parent_by_majority(
            pairs, "country_id", "region_id", "country_name"
        )
        self.resolutions["country"] = resolution
        table = resolution.mapping[["country_id", "country_name", "region_id"]].copy()

        # I membri visti solo come nazionalita': nessuna regione osservata.
        known = set(table["country_id"])
        orphans = _majority_label(
            pairs[~pairs["country_id"].isin(known)][["country_id", "country_name"]].copy(),
            "country_id", "country_name",
        )
        if not orphans.empty:
            orphans["region_id"] = UNKNOWN_ID
            log.info(
                "  country: %d membri presenti solo come nazionalita del bersaglio, "
                "agganciati alla regione Unknown", len(orphans),
            )
            self.audit.log(
                "resolve_hierarchies", Level.SCHEMA, Taxonomy.STRUCTURAL_MISSING, "country",
                "Membri geografici senza regione osservata agganciati al membro Unknown",
                "dim_country e una role-playing dimension: il GTD usa alcuni codici solo "
                "come nazionalita del bersaglio, mai come paese dell attentato. Quei "
                "membri devono esistere nella dimensione, altrimenti la chiave esterna "
                "natlty_id non e soddisfacibile, ma non hanno una regione nota",
                rows_affected=len(orphans),
                domain_rule="Integrita' referenziale - nazionalita' del bersaglio",
            )
            table = pd.concat([table, orphans], ignore_index=True)

        unknown = pd.DataFrame(
            [{"country_id": UNKNOWN_ID, "country_name": UNKNOWN_LABEL,
              "region_id": UNKNOWN_ID}]
        )
        return pd.concat([unknown, table], ignore_index=True)

    # Tipo di attacco
    def _attack_types(self, df: pd.DataFrame) -> pd.DataFrame:
        labels = _majority_label(
            df[["attacktype1", "attacktype1_txt"]].copy(), "attacktype1", "attacktype1_txt"
        )
        labels = labels.rename(
            columns={"attacktype1": "attacktype_id", "attacktype1_txt": "attack_name"}
        )
        labels["attack_macro"] = _map_total(
            labels["attacktype_id"], ATTACK_MACRO, ATTACK_MACRO_DEFAULT
        )
        unknown = pd.DataFrame(
            [{"attacktype_id": UNKNOWN_ID, "attack_name": UNKNOWN_LABEL,
              "attack_macro": UNKNOWN_LABEL}]
        )
        return pd.concat([unknown, labels], ignore_index=True)

    # Armi
    def _weapon_pairs(self, df: pd.DataFrame) -> pd.DataFrame:
        groups = [
            (f"weapsubtype{i}", f"weaptype{i}", f"weapsubtype{i}_txt", f"weaptype{i}_txt")
            for i in self.WEAPON_SLOTS
        ]
        return self._stack(
            df, groups, ["weapsubtype_id", "weaptype_id", "subtype_name", "type_name"]
        )

    def _weapon_types(self, df: pd.DataFrame) -> pd.DataFrame:
        pairs = self._weapon_pairs(df)
        labels = _majority_label(
            pairs[["weaptype_id", "type_name"]].copy(), "weaptype_id", "type_name"
        )
        labels = labels.rename(columns={"type_name": "weapon_name"})
        labels["weapon_macro"] = _map_total(
            labels["weaptype_id"], WEAPON_MACRO, WEAPON_MACRO_DEFAULT
        )
        labels["weapon_group"] = _map_total(
            labels["weaptype_id"], WEAPON_GROUP, WEAPON_GROUP_DEFAULT
        )
        unknown = pd.DataFrame(
            [{"weaptype_id": UNKNOWN_ID, "weapon_name": UNKNOWN_LABEL,
              "weapon_macro": UNKNOWN_LABEL, "weapon_group": WEAPON_GROUP_DEFAULT}]
        )
        return pd.concat([unknown, labels], ignore_index=True)

    def _weapon_subtypes(self, df: pd.DataFrame, weapon_types: pd.DataFrame) -> pd.DataFrame:
        pairs = self._weapon_pairs(df)
        resolution = resolve_parent_by_majority(
            pairs, "weapsubtype_id", "weaptype_id", "subtype_name"
        )
        self.resolutions["weapon_subtype"] = resolution
        table = resolution.mapping[["weapsubtype_id", "subtype_name", "weaptype_id"]].copy()
        table.columns = ["weapsubtype_id", "weapon_subtype_name", "weaptype_id"]

        placeholders = self._placeholders(
            weapon_types, "weaptype_id", "weapsubtype_id", "weapon_subtype_name"
        )
        unknown = pd.DataFrame(
            [{"weapsubtype_id": UNKNOWN_ID, "weapon_subtype_name": UNKNOWN_LABEL,
              "weaptype_id": UNKNOWN_ID}]
        )
        return pd.concat([unknown, table, placeholders], ignore_index=True)

    @staticmethod
    def _placeholders(
        types: pd.DataFrame, parent_key: str, child_key: str, child_label: str
    ) -> pd.DataFrame:
        """Sottotipo convenzionale Not Specified, uno per ogni tipo.

        L'id e' 9000 + id_del_tipo: una regola aritmetica, non una sequenza,
        cosi' la chiave resta stabile fra due caricamenti.
        """
        parents = [p for p in sorted(types[parent_key].unique()) if p != UNKNOWN_ID]
        return pd.DataFrame(
            [{child_key: 9000 + int(p), child_label: "Not Specified", parent_key: int(p)}
             for p in parents]
        )

    # Bersagli
    def _target_pairs(self, df: pd.DataFrame) -> pd.DataFrame:
        groups = [
            (f"targsubtype{i}", f"targtype{i}", f"targsubtype{i}_txt", f"targtype{i}_txt")
            for i in self.TARGET_SLOTS
        ]
        return self._stack(
            df, groups, ["targsubtype_id", "targtype_id", "subtype_name", "type_name"]
        )

    def _target_types(self, df: pd.DataFrame) -> pd.DataFrame:
        pairs = self._target_pairs(df)
        labels = _majority_label(
            pairs[["targtype_id", "type_name"]].copy(), "targtype_id", "type_name"
        )
        labels = labels.rename(columns={"type_name": "target_name"})
        labels["target_macro"] = _map_total(
            labels["targtype_id"], TARGET_MACRO, TARGET_MACRO_DEFAULT
        )
        unknown = pd.DataFrame(
            [{"targtype_id": UNKNOWN_ID, "target_name": UNKNOWN_LABEL,
              "target_macro": UNKNOWN_LABEL}]
        )
        return pd.concat([unknown, labels], ignore_index=True)

    def _target_subtypes(self, df: pd.DataFrame, target_types: pd.DataFrame) -> pd.DataFrame:
        pairs = self._target_pairs(df)
        resolution = resolve_parent_by_majority(
            pairs, "targsubtype_id", "targtype_id", "subtype_name"
        )
        self.resolutions["target_subtype"] = resolution
        table = resolution.mapping[["targsubtype_id", "subtype_name", "targtype_id"]].copy()
        table.columns = ["targsubtype_id", "target_subtype_name", "targtype_id"]
        placeholders = self._placeholders(
            target_types, "targtype_id", "targsubtype_id", "target_subtype_name"
        )
        unknown = pd.DataFrame(
            [{"targsubtype_id": UNKNOWN_ID, "target_subtype_name": UNKNOWN_LABEL,
              "targtype_id": UNKNOWN_ID}]
        )
        return pd.concat([unknown, table, placeholders], ignore_index=True)

    # Presidio sui conflitti
    def conflict_report(self) -> pd.DataFrame:
        frames = []
        for name, res in self.resolutions.items():
            if res.conflicts.empty:
                continue
            block = res.conflicts.copy()
            block.insert(0, "hierarchy", name)
            frames.append(block)
        if not frames:
            return pd.DataFrame(
                columns=["hierarchy", "child_id", "parent_id", "support",
                         "assigned_parent", "is_assigned"]
            )
        return pd.concat(frames, ignore_index=True)

    def _audit_conflicts(self) -> None:
        for name, res in self.resolutions.items():
            n_conflicting = int(res.conflicts["child_id"].nunique()) if not res.conflicts.empty else 0
            if n_conflicting == 0:
                continue
            self.audit.log(
                "resolve_hierarchies",
                Level.SCHEMA,
                Taxonomy.INCONSISTENT,
                name,
                "Padre risolto per maggioranza delle osservazioni",
                "La chiave primaria del figlio dichiara una dipendenza funzionale verso il "
                "padre che la sorgente viola su una minoranza di righe. Il criterio "
                "precedente, MIN(parent_id), sceglieva in base all ordinamento arbitrario "
                "dei codici e su cinque sottotipi esplosivi assegnava il padre sbagliato. "
                f"Osservazioni: {res.observations}, dissenzienti: {res.dissenting} "
                f"({res.dissent_rate:.4%}), membri ambigui: {n_conflicting}",
                rows_affected=res.dissenting,
                domain_rule="Integrita' relazionale - dipendenze funzionali nelle gerarchie",
            )
            log.info(
                "  %-16s %d membri ambigui, %d osservazioni dissenzienti su %d (%.4f%%)",
                name, n_conflicting, res.dissenting, res.observations,
                100 * res.dissent_rate,
            )

    def assert_no_minority_parent(self) -> None:
        """Ferma il caricamento se un membro ha ricevuto un padre minoritario."""
        offenders: list[str] = []
        for name, res in self.resolutions.items():
            if res.conflicts.empty:
                continue
            best = (
                res.conflicts.sort_values(["child_id", "support"], ascending=[True, False])
                .drop_duplicates("child_id", keep="first")
            )
            minority = best[~best["is_assigned"]]
            offenders += [f"{name} #{int(c)}" for c in minority["child_id"]]
        if offenders and self.strict:
            raise ValueError(
                "Gerarchia incoerente: "
                f"{len(offenders)} membri hanno ricevuto un padre MINORITARIO nella "
                f"sorgente -> {', '.join(offenders)}"
            )
        if offenders:
            log.warning("padre minoritario su %d membri (strict disattivato)", len(offenders))
