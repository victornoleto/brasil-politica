"""Downloads senators (list per legislature, mandates/terms in office and party affiliations) into data/raw/senate/."""
import json
import time
from pathlib import Path

import requests

API = "https://legis.senado.leg.br/dadosabertos"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "senate"
LEGISLATURES = range(49, 58)
ENDPOINTS = {"mandates": "mandatos", "affiliations": "filiacoes"}  # local dir -> API resource


def get(path):
    for attempt in range(3):
        try:
            r = requests.get(f"{API}/{path}.json", timeout=60)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"failed: {path}")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    codes = set()
    for leg in LEGISLATURES:
        body = get(f"senador/lista/legislatura/{leg}")
        (RAW / f"members_leg{leg}.json").write_text(json.dumps(body, ensure_ascii=False))
        parl = body["ListaParlamentarLegislatura"]["Parlamentares"]["Parlamentar"]
        codes |= {p["IdentificacaoParlamentar"]["CodigoParlamentar"] for p in parl}
        print(leg, len(parl), "senators")

    for sub in ENDPOINTS:
        (RAW / sub).mkdir(exist_ok=True)
    pending = [c for c in sorted(codes) if not (RAW / "affiliations" / f"{c}.json").exists()]
    print(len(codes), "senators;", len(pending), "to download")
    for n, code in enumerate(pending, 1):
        for sub, resource in ENDPOINTS.items():
            (RAW / sub / f"{code}.json").write_text(json.dumps(get(f"senador/{code}/{resource}"), ensure_ascii=False))
        if n % 100 == 0:
            print(n, "/", len(pending), flush=True)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
