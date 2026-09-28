"""Downloads federal deputies per legislature (Câmara API) into data/raw/chamber/."""
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

API = "https://dadosabertos.camara.leg.br/api/v2"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "chamber"
LEGISLATURES = range(49, 58)  # 1991–2027 covers 1994–2026


def get_all(url, params):
    """Follows the API pagination to the end."""
    out, params = [], {**params, "itens": 100, "pagina": 1}
    while True:
        r = requests.get(url, params=params, headers={"Accept": "application/json"}, timeout=60)
        r.raise_for_status()
        body = r.json()
        out.extend(body["dados"])
        if not any(l["rel"] == "next" for l in body["links"]):
            return out
        params["pagina"] += 1
        time.sleep(0.2)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for leg in LEGISLATURES:
        rows = get_all(f"{API}/deputados", {"idLegislatura": leg})
        (RAW / f"members_leg{leg}.json").write_text(json.dumps(rows, ensure_ascii=False))
        print(leg, len(rows), "rows", len({r["id"] for r in rows}), "deputies")
    fetch_histories()


def fetch_histories():
    """History (taking office, leave, party switch) of each deputy; cached by id."""
    ids = set()
    for leg in LEGISLATURES:
        ids |= {r["id"] for r in json.loads((RAW / f"members_leg{leg}.json").read_text())}
    out = RAW / "history"
    out.mkdir(exist_ok=True)
    pending = sorted(i for i in ids if not (out / f"{i}.json").exists())
    print(len(ids), "deputies;", len(pending), "histories to download", flush=True)

    def download(dep_id):
        for attempt in range(3):
            try:
                r = requests.get(f"{API}/deputados/{dep_id}/historico",
                                 headers={"Accept": "application/json"}, timeout=60)
                r.raise_for_status()
                (out / f"{dep_id}.json").write_text(json.dumps(r.json()["dados"], ensure_ascii=False))
                return
            except requests.RequestException:
                time.sleep(5 * (attempt + 1))
        print("failed", dep_id, flush=True)

    with ThreadPoolExecutor(max_workers=4) as pool:
        for n, _ in enumerate(pool.map(download, pending), 1):
            if n % 200 == 0:
                print(n, "/", len(pending), flush=True)


if __name__ == "__main__":
    main()
