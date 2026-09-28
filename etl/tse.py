"""Governors and state/district deputies elected, from the TSE consulta_cand_YYYY.zip files.

Put the ZIPs in data/raw/tse/ (manual download: the TSE CDN blocks automated access).
Limitation: the party at election time counts for the whole mandate (no party switches, no vices who took over).
"""
import io
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "tse"
ELECTIONS = [1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]
OFFICES = {3: "governors", 7: "assemblies", 8: "assemblies"}  # 8 = district deputy (DF)
COLS = ["ANO_ELEICAO", "CD_CARGO", "NR_TURNO", "SG_UF", "SG_PARTIDO", "SQ_CANDIDATO", "DS_SIT_TOT_TURNO",
        "CD_TIPO_ELEICAO", "DT_ELEICAO"]
SPECIAL = "1"  # CD_TIPO_ELEICAO: 1 = special (supplementary) election, 2 = regular


def elected(year):
    zpath = RAW / f"consulta_cand_{year}.zip"
    if not zpath.exists():
        return None
    parts = []
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():
            # one CSV per state + aggregated _BR and _BRASIL files (which duplicate everything); use only the per-state ones
            if not name.lower().endswith(".csv") or name.upper().endswith(("_BR.CSV", "_BRASIL.CSV")):
                continue
            with z.open(name) as f:
                df = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep=";", usecols=COLS, dtype=str)
            parts.append(df)
    df = pd.concat(parts, ignore_index=True)
    df["CD_CARGO"] = df["CD_CARGO"].astype(int)
    df["NR_TURNO"] = df["NR_TURNO"].astype(int)
    df = df[df["CD_CARGO"].isin(OFFICES)]
    status = df["DS_SIT_TOT_TURNO"].str.upper()
    df = df[status.str.startswith("ELEITO") | (status == "MÉDIA")]
    # a governor elected in the runoff also appears in round 1 as "2º TURNO"; keep the last elected row.
    # SQ_CANDIDATO is only unique within the state in some years (2002, 2006), so the key includes state and office.
    df = df.sort_values("NR_TURNO").drop_duplicates(["SG_UF", "CD_CARGO", "SQ_CANDIDATO"], keep="last")
    return df


def tse():
    """Intervals (institution, person, raw_party, start, end) — the caller applies canon().

    Special governor election (e.g. AM 2017, TO 2018): the winner takes office on the election date
    and the previous governor's term ends the day before.
    """
    for year in ELECTIONS:
        df = elected(year)
        if df is None:
            print(f"tse: missing consulta_cand_{year}.zip")
            continue
        gov_end = date(year + 4, 12, 31)
        for r in df[df["CD_CARGO"] != 3].itertuples():
            yield ("assemblies", r.SQ_CANDIDATO, r.SG_PARTIDO, date(year + 1, 2, 1), date(year + 5, 1, 31))
        for uf, g in df[df["CD_CARGO"] == 3].groupby("SG_UF"):
            inaugurations = sorted(
                (pd.to_datetime(r.DT_ELEICAO, dayfirst=True).date() if r.CD_TIPO_ELEICAO == SPECIAL
                 else date(year + 1, 1, 1), r.SQ_CANDIDATO, r.SG_PARTIDO)
                for r in g.itertuples()
            )
            for (start, sq, party), nxt in zip(inaugurations, inaugurations[1:] + [None]):
                yield ("governors", sq, party, start, nxt[0] - timedelta(days=1) if nxt else gov_end)
