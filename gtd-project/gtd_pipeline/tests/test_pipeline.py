"""Verifiche sui moduli puri della pipeline.

    python -m gtd_pipeline.tests.test_pipeline

Nessun database, nessun modello addestrato, nessuna sorgente da 100 MB: tutto
cio' che viene provato qui e' funzione pura di un DataFrame. E' la proprieta'
che rende questi controlli eseguibili a ogni commit, ed e' la ragione per cui
'etl/' non importa SQLAlchemy.

Scritte con 'unittest' della libreria standard e non con pytest: una
dipendenza in meno da installare per far girare i test, che e' esattamente la
dipendenza che di solito manca sulla macchina di chi valuta il progetto.
"""

from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from ..audit import AuditLog, Level, Taxonomy
from ..etl.hierarchies import (
    ATTACK_MACRO, REGION_MACRO_AREA, TARGET_MACRO, WEAPON_MACRO,
    HierarchyResolver, resolve_parent_by_majority,
)
from ..etl.quality import DataQualityManager
from ..etl.sovereign import SovereignStateResolver
from ..models.base import BaseImputer, ImputationError
from ..models.zero_inflated import (
    DETERMINISTIC_LOWER_BOUND, ZERO_REGIME_THRESHOLD,
    ZeroInflatedCountRegressor, ZeroInflatedImputer,
)


# ==========================================================================
# Sorgente sintetica minima, con le anomalie che il cleaning deve trattare
# ==========================================================================
def sample_source(n: int = 6) -> pd.DataFrame:
    base = {
        "eventid": [1, 2, 3, 4, 5, 5],           # 5 duplicato
        "iyear": [1988, 1995, 2001, 1972, 2015, 2015],
        "imonth": [0, 7, 9, 3, 0, 0],            # 0 = mese ignoto
        "iday": [0, 15, 11, 0, 0, 0],
        "nkill": [3.0, np.nan, 2996.0, -99.0, 4.4, 4.4],
        "nkillter": [5.0, 1.0, 19.0, 0.0, 0.0, 0.0],   # 5 > nkill=3
        "nwound": [1.0, np.nan, 6000.0, 2.0, 0.0, 0.0],
        "nperps": [-99.0, 2.0, 19.0, np.nan, 1.0, 1.0],
        "propextent": [4, 1, 1, np.nan, 3, 3],   # 4 = Unknown su scala ordinale
        "propvalue": [0.0, 100.0, np.nan, 0.0, 0.0, 0.0],
        "property": [0, 1, 1, 0, 0, 0],
        "latitude": [0.0, 51.5, 40.7, 48.8, 33.5, 33.5],   # (0,0) = Null Island
        "longitude": [0.0, -0.1, -74.0, 2.3, 36.3, 36.3],
        "country": [603, 603, 217, 75, 200, 200],
        "country_txt": ["United Kingdom", "United Kingdom", "United States",
                        "West Germany (FRG)", "Syria", "Syria"],
        "region": [8, 8, 1, 8, 10, 10],
        "region_txt": ["Western Europe", "Western Europe", "North America",
                       "Western Europe", "Middle East & North Africa",
                       "Middle East & North Africa"],
        "natlty1": [604, 603, 217, 75, 200, 200],
        "natlty1_txt": ["Northern Ireland", "United Kingdom", "United States",
                        "Germany", "Syria", "Syria"],
        "specificity": [1, 1, 1, 1, 1, 1],
        "vicinity": [0, 0, 0, 0, 0, 0],
        "provstate": ["Ulster", "London", "NY", "Bayern", "Idlib", "Idlib"],
        "city": ["Belfast", "London", "New York", "Munich", "Idlib", "Idlib"],
        "gname": ["IRA", "IRA", "Al-Qaida", "RAF", "ISIL", "ISIL"],
        "gsubname": ["", "", "", "", "", ""],
        "claimed": [1, 0, 1, 1, 1, 1],
        "guncertain1": [0, 0, 0, 0, 0, 0],
        "doubtterr": [0, 0, 0, np.nan, 0, 0],
        "multiple": [0, 0, 1, np.nan, 0, 0],
        "crit1": [1, 1, 1, np.nan, 1, 1],
        "crit2": [1, 1, 1, 1, 1, 1],
        "crit3": [1, 1, 1, 1, 1, 1],
        "extended": [0, 0, 0, 0, 0, 0],
        "success": [1, 1, 1, 1, 1, 1],
        "suicide": [0, 0, 1, 0, 1, 1],
        "attacktype1": [3, 3, 4, 3, 2, 2],
        "attacktype1_txt": ["Bombing/Explosion", "Bombing/Explosion", "Hijacking",
                            "Bombing/Explosion", "Armed Assault", "Armed Assault"],
    }
    # slot armi: lo slot 1 contiene la coppia (sottotipo 7 = Grenade, tipo)
    # con UNA riga errata che lo attribuisce a Firearms (5) e le altre a
    # Explosives (6). E' la riproduzione in miniatura del difetto MIN().
    base |= {
        "weaptype1": [5, 6, 6, 6, 6, 6],
        "weaptype1_txt": ["Firearms", "Explosives", "Explosives", "Explosives",
                          "Explosives", "Explosives"],
        "weapsubtype1": [7, 7, 7, 7, 7, 7],
        "weapsubtype1_txt": ["Grenade"] * 6,
    }
    for i in (2, 3, 4):
        base |= {
            f"weaptype{i}": [np.nan] * 6, f"weaptype{i}_txt": [None] * 6,
            f"weapsubtype{i}": [np.nan] * 6, f"weapsubtype{i}_txt": [None] * 6,
        }
    base |= {
        "targtype1": [14, 14, 14, 2, 14, 14],
        "targtype1_txt": ["Private Citizens & Property"] * 3 + ["Government (General)"]
                         + ["Private Citizens & Property"] * 2,
        "targsubtype1": [68, 68, 68, 68, 68, 68],
        "targsubtype1_txt": ["Named Civilian"] * 6,
    }
    for i in (2, 3):
        base |= {
            f"targtype{i}": [np.nan] * 6, f"targtype{i}_txt": [None] * 6,
            f"targsubtype{i}": [np.nan] * 6, f"targsubtype{i}_txt": [None] * 6,
        }
    return pd.DataFrame(base).head(n)


# ==========================================================================
class TestAuditLog(unittest.TestCase):
    def test_taxonomy_is_an_enum(self):
        """Livello e tipo non sono stringhe libere: una grafia diversa
        spariva dal raggruppamento della sintesi."""
        audit = AuditLog()
        with self.assertRaises(ValueError):
            audit.log("s", "Instance level", Taxonomy.MISSING, "c", "a", "r")

    def test_summary_groups(self):
        audit = AuditLog()
        audit.log("s", Level.INSTANCE, Taxonomy.MISSING, "c", "a", "r", rows_affected=3)
        audit.log("s", Level.INSTANCE, Taxonomy.MISSING, "d", "a", "r", rows_affected=4)
        summary = audit.summary()
        self.assertEqual(len(summary), 1)
        self.assertEqual(int(summary.iloc[0]["Righe_Toccate"]), 7)


class TestDataQuality(unittest.TestCase):
    def setUp(self):
        self.audit = AuditLog()
        self.df, _, _ = DataQualityManager(sample_source(), self.audit).run()

    def test_duplicate_removed_on_natural_key(self):
        self.assertEqual(len(self.df), 5)
        self.assertTrue(self.df["eventid"].is_unique)

    def test_sentinels_become_nan(self):
        """-99 e' un codice di ignoto, non un conteggio negativo."""
        self.assertTrue(pd.isna(self.df.loc[self.df.eventid == 4, "nkill"].iloc[0]))
        self.assertTrue(pd.isna(self.df.loc[self.df.eventid == 1, "nperps"].iloc[0]))

    def test_ordinal_unknown_removed(self):
        """propextent=4 significa Unknown su una scala dove 1 e' il massimo."""
        self.assertTrue(pd.isna(self.df.loc[self.df.eventid == 1, "propextent"].iloc[0]))

    def test_null_island_removed(self):
        row = self.df.loc[self.df.eventid == 1]
        self.assertTrue(pd.isna(row["latitude"].iloc[0]))
        self.assertTrue(pd.isna(row["longitude"].iloc[0]))

    def test_date_precision_tracked(self):
        row = self.df.loc[self.df.eventid == 1].iloc[0]
        self.assertEqual(row["date_precision"], "year")
        self.assertEqual(row["imonth"], 7)      # midpoint dell'anno
        self.assertEqual(row["iday"], 1)
        self.assertTrue(row["is_approximate_date"])

    def test_casualty_consistency(self):
        """nkillter non puo' eccedere nkill."""
        row = self.df.loc[self.df.eventid == 1].iloc[0]
        self.assertLessEqual(row["nkillter"], row["nkill"])

    def test_structural_missing_preserved(self):
        """doubtterr pre-1998 resta NaN: imputarlo creerebbe un artefatto."""
        self.assertTrue(pd.isna(self.df.loc[self.df.eventid == 4, "doubtterr"].iloc[0]))

    def test_crit_filled_with_zero(self):
        self.assertEqual(self.df.loc[self.df.eventid == 4, "crit1"].iloc[0], 0)

    def test_no_rows_dropped_for_outliers(self):
        """Gli eventi estremi del GTD sono reali: si segnalano, non si eliminano."""
        self.assertIn("report_outliers", set(self.audit.to_frame()["Step"]))
        self.assertEqual(len(self.df), 5)


class TestMajorityResolution(unittest.TestCase):
    def test_majority_wins_over_min(self):
        """Il cuore della correzione: il padre e' il piu' osservato, non il
        codice minore. Con MIN() il sottotipo 7 finirebbe sotto il tipo 5."""
        pairs = pd.DataFrame({
            "child": [7, 7, 7, 7, 7],
            "parent": [5, 6, 6, 6, 6],       # 5 e' minore, 6 e' maggioritario
            "label": ["Grenade"] * 5,
        })
        res = resolve_parent_by_majority(pairs, "child", "parent", "label")
        self.assertEqual(int(res.mapping.loc[0, "parent"]), 6)
        self.assertEqual(res.dissenting, 1)
        self.assertEqual(int(res.mapping.loc[0, "support"]), 4)

    def test_tie_broken_on_lower_id_deterministically(self):
        """A parita' vince l'id minore: il caricamento deve essere ripetibile."""
        pairs = pd.DataFrame({"child": [1, 1], "parent": [9, 4], "label": ["x", "x"]})
        first = resolve_parent_by_majority(pairs, "child", "parent", "label")
        second = resolve_parent_by_majority(pairs.iloc[::-1], "child", "parent", "label")
        self.assertEqual(int(first.mapping.loc[0, "parent"]), 4)
        self.assertEqual(
            int(first.mapping.loc[0, "parent"]), int(second.mapping.loc[0, "parent"])
        )

    def test_conflicts_are_reported_not_hidden(self):
        pairs = pd.DataFrame({"child": [7, 7, 7], "parent": [5, 6, 6], "label": ["g"] * 3})
        res = resolve_parent_by_majority(pairs, "child", "parent", "label")
        self.assertFalse(res.conflicts.empty)
        self.assertEqual(set(res.conflicts["child_id"]), {7})

    def test_invalid_codes_excluded(self):
        pairs = pd.DataFrame({"child": [1, 1, -9], "parent": [-99, 3, 3], "label": ["a"] * 3})
        res = resolve_parent_by_majority(pairs, "child", "parent", "label")
        self.assertEqual(len(res.mapping), 1)
        self.assertEqual(int(res.mapping.loc[0, "parent"]), 3)


class TestHierarchyResolver(unittest.TestCase):
    def setUp(self):
        self.audit = AuditLog()
        df, _, _ = DataQualityManager(sample_source(), self.audit).run()
        self.resolver = HierarchyResolver(self.audit)
        self.tables = self.resolver.build(df)

    def test_grenade_lands_under_explosives(self):
        ws, wt = self.tables["weapon_subtype"], self.tables["weapon_type"]
        parent = ws.loc[ws.weapsubtype_id == 7, "weaptype_id"].iloc[0]
        name = wt.loc[wt.weaptype_id == parent, "weapon_name"].iloc[0]
        self.assertEqual(name, "Explosives")

    def test_macro_maps_are_total_functions(self):
        """Nessun membro puo' restare senza macro: la colonna e' NOT NULL."""
        for table, col in [("attack_type", "attack_macro"), ("weapon_type", "weapon_macro"),
                           ("target_type", "target_macro"), ("region", "macro_area")]:
            with self.subTest(table=table):
                self.assertTrue(self.tables[table][col].notna().all())
                self.assertTrue((self.tables[table][col].str.len() > 0).all())

    def test_unknown_member_in_every_hierarchy(self):
        keys = {
            "region": "region_id", "country": "country_id", "attack_type": "attacktype_id",
            "weapon_type": "weaptype_id", "weapon_subtype": "weapsubtype_id",
            "target_type": "targtype_id", "target_subtype": "targsubtype_id",
        }
        for table, key in keys.items():
            with self.subTest(table=table):
                self.assertIn(-1, set(self.tables[table][key]))
                self.assertTrue(self.tables[table][key].is_unique)

    def test_not_specified_placeholder_per_type(self):
        """Senza, un evento con tipo ma non sottotipo perde la riga di bridge."""
        wt, ws = self.tables["weapon_type"], self.tables["weapon_subtype"]
        expected = set(wt.loc[wt.weaptype_id != -1, "weaptype_id"])
        got = set(ws.loc[ws.weapon_subtype_name == "Not Specified", "weaptype_id"])
        self.assertEqual(expected, got)

    def test_nationality_only_countries_are_present(self):
        """dim_country e' role-playing: i codici usati solo come nazionalita'
        devono esistere, altrimenti la FK natlty_id non e' soddisfacibile."""
        countries = set(self.tables["country"]["country_id"])
        self.assertIn(604, countries)   # Northern Ireland, mai paese ospite
        orphan = self.tables["country"]
        self.assertEqual(int(orphan.loc[orphan.country_id == 604, "region_id"].iloc[0]), -1)

    def test_macro_area_covers_all_twelve_regions(self):
        self.assertEqual(len(REGION_MACRO_AREA), 12)
        self.assertEqual(len(set(REGION_MACRO_AREA.values())), 6)

    def test_macro_maps_cover_the_declared_domain(self):
        self.assertEqual(set(ATTACK_MACRO) , set(range(1, 10)))
        self.assertEqual(set(WEAPON_MACRO), set(range(1, 14)))
        self.assertEqual(set(TARGET_MACRO), set(range(1, 23)))


class TestSovereignState(unittest.TestCase):
    def setUp(self):
        self.r = SovereignStateResolver()

    def test_uk_members_collapse(self):
        for member in ("Great Britain", "Northern Ireland", "United Kingdom"):
            self.assertEqual(self.r.resolve(member, 1988), "United Kingdom")

    def test_germany_is_scd_type_2(self):
        """La stessa coppia da' esito diverso a seconda dell'anno: e' cio'
        che distingue il tipo 2 dal tipo 1."""
        self.assertEqual(self.r.resolve("West Germany (FRG)", 1988), "West Germany (FRG)")
        self.assertEqual(self.r.resolve("West Germany (FRG)", 1995), "Germany")
        self.assertNotEqual(
            self.r.resolve("East Germany (GDR)", 1988),
            self.r.resolve("West Germany (FRG)", 1988),
        )
        self.assertEqual(
            self.r.resolve("East Germany (GDR)", 1995),
            self.r.resolve("West Germany (FRG)", 1995),
        )

    def test_demonym_resolves_on_territory(self):
        """Prima del 1990 Germany non e' uno stato ma un demonimo."""
        self.assertEqual(
            self.r.resolve("Germany", 1988, territory="West Germany (FRG)"),
            "West Germany (FRG)",
        )
        self.assertEqual(self.r.resolve("Germany", 1995, territory="Italy"), "Germany")

    def test_raw_flag_is_preserved(self):
        audit = AuditLog()
        df, _, _ = DataQualityManager(sample_source(), audit).run()
        out = SovereignStateResolver(audit).apply(df)
        self.assertIn("is_transnational_raw", out.columns)
        # evento 1: United Kingdom -> Northern Ireland, falso positivo
        row = out.loc[out.eventid == 1].iloc[0]
        self.assertEqual(row["is_transnational_raw"], 1)
        self.assertEqual(row["is_transnational"], 0)



# Il contratto dell'interfaccia astratta
class _DropsRows(BaseImputer):
    description = "strategia che viola il contratto scartando righe"

    def impute(self, df):
        out = df.dropna(subset=list(self.targets)).copy()
        for t in self.targets:
            out[self.flag_column(t)] = 0
        return out


class _ForgetsFlag(BaseImputer):
    description = "strategia che non dichiara la provenienza"

    def impute(self, df):
        out = df.copy()
        for t in self.targets:
            out[t] = out[t].fillna(0)
        return out


class _Median(BaseImputer):
    """Strategia alternativa legittima: dimostra che aggiungerne una non
    richiede di toccare la pipeline."""

    description = "mediana costante"

    def impute(self, df):
        out = df.copy()
        for t in self.targets:
            flag = self.flag_column(t)
            out[flag] = out[t].isna().astype(int)
            out[t] = out[t].fillna(out[t].median())
        return out


class TestImputerContract(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"nkill": [1.0, np.nan, 3.0, np.nan]})

    def test_cannot_instantiate_the_abstract_base(self):
        with self.assertRaises(TypeError):
            BaseImputer(["nkill"])       # metodi astratti non implementati

    def test_dropping_rows_is_rejected(self):
        with self.assertRaises(ImputationError) as ctx:
            _DropsRows(["nkill"]).run(self.df)
        self.assertIn("numero di righe", str(ctx.exception))

    def test_missing_provenance_flag_is_rejected(self):
        with self.assertRaises(ImputationError) as ctx:
            _ForgetsFlag(["nkill"]).run(self.df)
        self.assertIn("provenienza", str(ctx.exception))

    def test_a_conforming_strategy_passes(self):
        out = _Median(["nkill"]).run(self.df)
        self.assertEqual(len(out), len(self.df))
        self.assertEqual(int(out["nkill"].isna().sum()), 0)
        self.assertEqual(list(out["is_nkill_imputed"]), [0, 1, 0, 1])

    def test_not_imputing_is_allowed(self):
        """Una strategia puo' legittimamente non imputare: e' il caso di
        nwound, dove nessun modello batte il baseline a mediana costante."""

        class Abstain(BaseImputer):
            description = "non imputa"

            def impute(self, df):
                out = df.copy()
                for t in self.targets:
                    out[self.flag_column(t)] = 0
                return out

        out = Abstain(["nkill"]).run(self.df)
        self.assertEqual(int(out["nkill"].isna().sum()), 2)



# Regole di predizione del modello a due stadi
# Nessun addestramento: i due stadi sono sostituiti da stub deterministici,
# cosi' che a essere provata sia la LOGICA di combinazione — vincolo a priori,
# limite inferiore, discretizzazione — e non LightGBM.

class _StubTwoStage(ZeroInflatedCountRegressor):
    """Due stadi a esito fissato, per isolare le regole di combinazione."""

    def __init__(self, p_zero: float, positive_count: float) -> None:
        super().__init__()
        self._p_zero = p_zero
        self._positive_count = positive_count
        self._fitted = True
        self.feature_names_ = None

    def predict_zero_probability(self, X):
        return np.full(len(X), self._p_zero, dtype=float)

    def predict_positive_count(self, X):
        return np.full(len(X), self._positive_count, dtype=float)


class TestTwoStagePredictionRules(unittest.TestCase):
    def setUp(self):
        self.X = pd.DataFrame({"f": [0, 1, 2, 3]})

    def test_zero_regime_applies_without_prior(self):
        model = _StubTwoStage(p_zero=0.99, positive_count=3.4)
        self.assertEqual(list(model.predict(self.X)), [0, 0, 0, 0])

    def test_known_perpetrator_deaths_bypass_the_zero_regime(self):
        """nkillter > 0 esclude logicamente il regime a zero vittime."""
        model = _StubTwoStage(p_zero=0.99, positive_count=3.4)
        forced = np.array([True, True, False, False])
        out = model.predict(self.X, force_positive=forced)
        self.assertTrue((out[:2] > 0).all())      # saltano il primo stadio
        self.assertTrue((out[2:] == 0).all())     # le altre no

    def test_lower_bound_is_never_violated(self):
        model = _StubTwoStage(p_zero=0.0, positive_count=2.0)
        floor = np.array([0.0, 5.0, 9.0, np.nan])
        out = model.predict(self.X, lower_bound=floor)
        self.assertEqual(list(out), [2, 5, 9, 2])

    def test_threshold_is_the_declared_constant(self):
        below = _StubTwoStage(p_zero=ZERO_REGIME_THRESHOLD - 0.01, positive_count=4.0)
        at = _StubTwoStage(p_zero=ZERO_REGIME_THRESHOLD, positive_count=4.0)
        self.assertEqual(list(below.predict(self.X)), [4, 4, 4, 4])
        self.assertEqual(list(at.predict(self.X)), [0, 0, 0, 0])

    def test_discretization_conserves_the_total(self):
        """Il metodo dei resti maggiori conserva il totale; il troncamento no."""
        model = _StubTwoStage(p_zero=0.0, positive_count=0.0)
        continuous = np.array([0.5, 1.5, 2.5, 3.5, 1.4, 1.6])
        integers, report = model.discretize(continuous)
        self.assertEqual(report["sum_continuous"], 11.0)
        self.assertEqual(report["sum_discrete"], 11.0)
        self.assertAlmostEqual(report["drift"], 0.0)
        self.assertEqual(report["within_tolerance"], 1.0)
        # ogni riga resta a distanza inferiore a uno dalla propria stima
        self.assertTrue((np.abs(integers - continuous) < 1).all())
        # il troncamento avrebbe perso tre unita'
        self.assertEqual(float(np.trunc(continuous).sum()), 8.0)

    def test_discretization_drift_stays_below_one_unit(self):
        """Proprieta' per costruzione, provata su resti asimmetrici."""
        model = _StubTwoStage(p_zero=0.0, positive_count=0.0)
        rng = np.random.default_rng(3)
        continuous = rng.gamma(shape=1.2, scale=0.6, size=5000)
        _, report = model.discretize(continuous)
        self.assertLess(abs(report["drift"]), 1.0)
        self.assertEqual(report["within_tolerance"], 1.0)

    def test_discretization_is_deterministic_on_ties(self):
        model = _StubTwoStage(p_zero=0.0, positive_count=0.0)
        continuous = np.array([0.5, 0.5, 0.5, 0.5])
        first, _ = model.discretize(continuous)
        second, _ = model.discretize(continuous)
        self.assertEqual(list(first), list(second))
        self.assertEqual(int(first.sum()), 2)

    def test_predictions_are_integers_and_deterministic(self):
        model = _StubTwoStage(p_zero=0.1, positive_count=2.7)
        first = model.predict(self.X, lower_bound=np.array([0.0, 4.0, 0.0, 0.0]))
        second = model.predict(self.X, lower_bound=np.array([0.0, 4.0, 0.0, 0.0]))
        self.assertTrue(np.issubdtype(first.dtype, np.integer))
        self.assertEqual(list(first), list(second))

    def test_a_constraint_of_the_wrong_length_is_refused(self):
        model = _StubTwoStage(p_zero=0.1, positive_count=1.0)
        with self.assertRaises(ValueError):
            model.predict(self.X, lower_bound=np.array([1.0, 2.0]))


class TestDeterministicFloor(unittest.TestCase):
    def setUp(self):
        self.imputer = ZeroInflatedImputer(audit=None)

    def test_floor_reads_the_declared_column(self):
        self.assertEqual(DETERMINISTIC_LOWER_BOUND["nkill"], "nkillter")
        rows = pd.DataFrame({"nkillter": [3.0, np.nan, 0.0, -1.0]})
        floor = self.imputer._deterministic_floor(rows, "nkill")
        self.assertEqual(list(floor), [3.0, 0.0, 0.0, 0.0])

    def test_floor_degenerates_to_zero_without_the_column(self):
        rows = pd.DataFrame({"altro": [1, 2]})
        floor = self.imputer._deterministic_floor(rows, "nkill")
        self.assertEqual(list(floor), [0.0, 0.0])

    def test_no_floor_declared_for_nwound(self):
        rows = pd.DataFrame({"nkillter": [7.0, 7.0]})
        self.assertEqual(list(self.imputer._deterministic_floor(rows, "nwound")), [0.0, 0.0])


class TestEtlIsDatabaseFree(unittest.TestCase):
    def test_transform_modules_do_not_import_sqlalchemy(self):
        """Proprieta' architetturale, non stilistica: e' cio' che rende questi
        test eseguibili senza un database in piedi."""
        import ast
        import pathlib

        etl = pathlib.Path(__file__).resolve().parent.parent / "etl"
        offenders = []
        for path in etl.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                # gli import dentro una funzione sono deliberati e ammessi
                if isinstance(node, (ast.Import, ast.ImportFrom)) and _is_module_level(tree, node):
                    name = getattr(node, "module", None) or ""
                    names = [a.name for a in node.names]
                    if "sqlalchemy" in name or any("sqlalchemy" in n for n in names):
                        offenders.append(path.name)
        self.assertEqual(offenders, [])


def _is_module_level(tree: "ast.Module", target: "ast.AST") -> bool:
    import ast
    for node in tree.body:
        if node is target:
            return True
        if isinstance(node, ast.If):        # blocchi TYPE_CHECKING
            for sub in node.body:
                if sub is target:
                    return False
    return False


if __name__ == "__main__":
    unittest.main(verbosity=2)
