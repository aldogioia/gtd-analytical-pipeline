"""Lettura della sorgente Excel, con cache Parquet (--no-cache la ignora)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..logging_setup import get_logger

log = get_logger(__name__)


class SourceExtractor:
    """Legge il GTD dalla sorgente Excel, con cache Parquet opzionale."""

    # Elenco esplicito: la sorgente ha 135 colonne, qui ne servono ~70.
    COLUMNS = [
        # identificativo, tempo, esiti
        "eventid", "iyear", "imonth", "iday", "extended", "multiple",
        "success", "suicide", "nkill", "nkillter", "nwound",
        "property", "propextent", "propvalue", "nperps",
        # localizzazione
        "country", "country_txt", "region", "region_txt", "provstate", "city",
        "latitude", "longitude", "specificity", "vicinity",
        # perpetratore e affidabilita'
        "gname", "gsubname", "claimed", "guncertain1", "doubtterr",
        "crit1", "crit2", "crit3",
        # modalita' di attacco (primaria)
        "attacktype1", "attacktype1_txt",
        # armi: tutti gli slot
        "weaptype1", "weaptype1_txt", "weapsubtype1", "weapsubtype1_txt",
        "weaptype2", "weaptype2_txt", "weapsubtype2", "weapsubtype2_txt",
        "weaptype3", "weaptype3_txt", "weapsubtype3", "weapsubtype3_txt",
        "weaptype4", "weaptype4_txt", "weapsubtype4", "weapsubtype4_txt",
        # bersagli: tutti gli slot
        "targtype1", "targtype1_txt", "targsubtype1", "targsubtype1_txt",
        "targtype2", "targtype2_txt", "targsubtype2", "targsubtype2_txt",
        "targtype3", "targtype3_txt", "targsubtype3", "targsubtype3_txt",
        # nazionalita' del bersaglio
        "natlty1", "natlty1_txt",
    ]

    def __init__(
        self,
        source: Path,
        cache: Path | None = None,
        use_cache: bool = True,
    ) -> None:
        self.source = Path(source)
        self.cache = Path(cache) if cache else None
        self.use_cache = use_cache

    def extract(self) -> pd.DataFrame:
        if self.use_cache and self.cache and self.cache.exists():
            log.info("lettura da cache Parquet: %s", self.cache)
            df = pd.read_parquet(self.cache)
            self._check_columns(df)
            log.info("  righe: %s | colonne: %d", f"{len(df):,}", df.shape[1])
            return df

        if not self.source.exists():
            raise FileNotFoundError(
                f"Sorgente non trovata: {self.source}. Imposta GTD_SOURCE oppure "
                "passa --source."
            )
        log.info("lettura del file Excel sorgente (lenta, verra messa in cache): %s", self.source)
        df = pd.read_excel(self.source, usecols=self.COLUMNS)
        self._check_columns(df)
        log.info("  righe: %s | colonne: %d", f"{len(df):,}", df.shape[1])
        self._write_cache(df)
        return df

    def _write_cache(self, df: pd.DataFrame) -> None:
        if not self.cache:
            return
        try:
            self.cache.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(self.cache, index=False)
            log.info("  cache scritta in %s", self.cache)
        except Exception as exc:
            log.warning("  cache Parquet non disponibile (%s), si prosegue senza", exc)

    def _check_columns(self, df: pd.DataFrame) -> None:
        """Fallisce subito se la sorgente ha cambiato schema."""
        missing = [c for c in self.COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(
                f"La sorgente non contiene {len(missing)} colonne attese: {missing[:10]}"
            )
