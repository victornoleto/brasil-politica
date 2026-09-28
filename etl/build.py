"""Builds web/public/data/*.json: the party composition of each institution per year.

Unit: seat-equivalent-year. Someone who held the office for half the year counts as 0.5.
The weighted mean of the coordinates happens in the front end, because the user edits weights and coordinates.
"""
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import yaml

from tse import tse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
OUT = ROOT / "web" / "public" / "data"
YEARS = range(1994, 2027)
TODAY = date.today()

ALIASES = yaml.safe_load((DATA / "aliases.yaml").read_text())["aliases"]
LEGISLATURES = {  # number -> (start, end)
    n: (date(1991 + 4 * (n - 49), 2, 1), date(1995 + 4 * (n - 49), 1, 31)) for n in range(49, 58)
}


def canon(acronym):
    if not acronym:
        return "NO_PARTY"
    acronym = acronym.strip()
    return ALIASES.get(acronym, acronym)


def d(s):
    return date.fromisoformat(s[:10]) if s else None


def as_list(x):
    return x if isinstance(x, list) else ([x] if x else [])


# ---------- Presidency ----------
def presidency():
    for p in yaml.safe_load((DATA / "presidents.yaml").read_text()):
        party = p["party"] or p.get("reference_party")
        end = p["end"] or TODAY
        yield ("presidency", p["name"], canon(party), p["start"], end)


# ---------- Chamber of Deputies ----------
def chamber():
    """Intervals in office, from each deputy's history.

    Legislatures without any dated "in office" event (old API) use the fallback:
    the party from the legislature's member list, for the whole legislature.
    """
    with_history = set()
    for f in sorted((RAW / "chamber" / "history").glob("*.json")):
        dep = f.stem
        events = defaultdict(list)
        for e in json.loads(f.read_text()):
            if e["situacao"] is None:  # synthetic "start of legislature" row, fake date
                continue
            events[e["idLegislatura"]].append(e)
        for leg, evs in events.items():
            if leg not in LEGISLATURES:
                continue
            leg_start, leg_end = LEGISLATURES[leg]
            evs.sort(key=lambda e: e["dataHora"])
            for cur, nxt in zip(evs, evs[1:] + [None]):
                if cur["situacao"] != "Exercício":
                    continue
                start = max(d(cur["dataHora"]), leg_start)
                end = min((d(nxt["dataHora"]) - timedelta(days=1)) if nxt else leg_end, leg_end, TODAY)
                if end >= start:
                    with_history.add((dep, leg))
                    yield ("chamber", dep, canon(cur["siglaPartido"]), start, end)

    for leg, (leg_start, leg_end) in LEGISLATURES.items():
        rows = json.loads((RAW / "chamber" / f"members_leg{leg}.json").read_text())
        missing = {}
        for x in rows:
            dep = str(x["id"])
            if (dep, leg) not in with_history:
                missing.setdefault(dep, x["siglaPartido"])
        # legislature without any history: incumbents + substitutes count for the whole legislature,
        # so rescale to 513 seats. With partial history, the missing ones get weight 1.
        has_history = any(l == leg for _, l in with_history)
        weight = 1 if has_history else 513 / len(missing)
        if missing:
            print(f"chamber leg {leg}: {len(missing)} deputies without history (weight {weight:.2f})")
        for dep, acronym in missing.items():
            yield ("chamber", dep, canon(acronym), leg_start, min(leg_end, TODAY), weight)


# ---------- Senate ----------
def senate_list_parties():
    """{(code, legislature): acronym} from the per-legislature lists; fallback when affiliations have no dates."""
    out = {}
    for leg in LEGISLATURES:
        body = json.loads((RAW / "senate" / f"members_leg{leg}.json").read_text())
        for p in as_list(body["ListaParlamentarLegislatura"]["Parlamentares"]["Parlamentar"]):
            ident = p["IdentificacaoParlamentar"]
            if ident.get("SiglaPartidoParlamentar"):
                out[(ident["CodigoParlamentar"], leg)] = ident["SiglaPartidoParlamentar"]
    return out


def legislature_of(day):
    return next((n for n, (s, e) in LEGISLATURES.items() if s <= day <= e), None)


def nearest_list_acronym(lists, code, day):
    """Acronym in the day's legislature or, if the senator is not listed there, in the nearest one where they are."""
    target = legislature_of(day) or (49 if day < LEGISLATURES[49][0] else 57)
    for leg in sorted(LEGISLATURES, key=lambda n: abs(n - target)):
        if (code, leg) in lists:
            return lists[(code, leg)]
    return None


def senate():
    lists = senate_list_parties()
    for f in sorted((RAW / "senate" / "mandates").glob("*.json")):
        code = f.stem
        aff_path = RAW / "senate" / "affiliations" / f.name
        if not aff_path.exists():
            print("warning: senator without downloaded affiliations", code)
            continue
        parl = json.loads(f.read_text())["MandatoParlamentar"]["Parlamentar"]
        aff_body = json.loads(aff_path.read_text())
        affiliations = [
            (d(x.get("DataFiliacao")), d(x.get("DataDesfiliacao")), x["Partido"]["SiglaPartido"])
            for x in as_list(aff_body["FiliacaoParlamentar"]["Parlamentar"].get("Filiacoes", {}).get("Filiacao"))
            if x["Partido"].get("SiglaPartido")  # old records without an acronym
        ]
        affiliations.sort(key=lambda t: t[0] or date.min)
        # old affiliation without an end date (e.g. ARENA, UDN) ends when the next one starts
        affiliations = [
            (start, end or (nxt[0] - timedelta(days=1) if nxt and nxt[0] else None), s)
            for (start, end, s), nxt in zip(affiliations, affiliations[1:] + [None])
        ]
        undated = not any(start for start, _, _ in affiliations)
        for m in as_list(parl.get("Mandatos", {}).get("Mandato")):
            terms = [(d(ex["DataInicio"]), d(ex.get("DataFim")) or TODAY)
                     for ex in as_list((m.get("Exercicios") or {}).get("Exercicio"))]
            if not terms and m.get("DescricaoParticipacao") == "Titular":
                # old mandates (e.g. elected in 1986) come without terms in office: assume the whole mandate
                second = m.get("SegundaLegislaturaDoMandato") or m["PrimeiraLegislaturaDoMandato"]
                terms = [(d(m["PrimeiraLegislaturaDoMandato"]["DataInicio"]), min(d(second["DataFim"]), TODAY))]
            for start, end in terms:
                # split the term at the affiliation change dates
                cuts = sorted({start, *(aff[0] for aff in affiliations if aff[0] and start < aff[0] <= end)})
                for a, b in zip(cuts, cuts[1:] + [end + timedelta(days=1)]):
                    if undated:  # undated affiliations come in arbitrary order: use the legislature list
                        # no acronym in the list: the API sorts affiliations from newest to oldest
                        acronym = nearest_list_acronym(lists, code, a) or (affiliations[0][2] if affiliations else None)
                    else:
                        acronym = party_on(affiliations, a)
                    yield ("senate", code, canon(acronym), a, b - timedelta(days=1))


def party_on(affiliations, day):
    active = [s for start, end, s in affiliations if (start is None or start <= day) and (end is None or end >= day)]
    if active:
        return active[-1]
    future = [s for start, _, s in affiliations if start and start > day]  # affiliation recorded after taking office
    return future[0] if future else None


# ---------- Governors and State Assemblies (TSE) ----------
def state_level():
    for inst, person, acronym, start, end in tse():
        if start <= TODAY:
            yield (inst, person, canon(acronym), start, min(end, TODAY))


# ---------- Aggregation ----------
def composition(intervals):
    """{institution: {year: {party: seat_equivalents}}}"""
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for inst, _person, party, start, end, *rest in intervals:
        weight = rest[0] if rest else 1
        for year in YEARS:
            a, b = max(start, date(year, 1, 1)), min(end, date(year, 12, 31))
            if b >= a:
                # current year: divide by the days elapsed so far, not by the whole year
                year_days = (min(date(year, 12, 31), TODAY) - date(year, 1, 1)).days + 1
                out[inst][year][party] += weight * ((b - a).days + 1) / year_days
    return out


def main():
    intervals = [*presidency(), *chamber(), *senate(), *state_level()]
    comp = composition(intervals)
    OUT.mkdir(parents=True, exist_ok=True)
    rounded = {
        inst: {year: {p: round(v, 3) for p, v in sorted(ps.items(), key=lambda kv: -kv[1])} for year, ps in years.items()}
        for inst, years in comp.items()
    }
    (OUT / "composition.json").write_text(json.dumps(rounded, ensure_ascii=False))
    (OUT / "parties.json").write_text(
        json.dumps(yaml.safe_load((DATA / "parties.yaml").read_text())["parties"], ensure_ascii=False)
    )
    for inst, years in sorted(comp.items()):
        print(inst, {y: round(sum(p.values()), 1) for y, p in sorted(years.items()) if y % 4 == 3})
    return comp


if __name__ == "__main__":
    main()
