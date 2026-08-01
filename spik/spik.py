"""Spiken: utlovat.se genom ImmersaDocs befintliga grant-profil.

Syftet är inte att bli snyggt. Syftet är att med minsta möjliga insats ta
reda på exakt var ImmersaDocs tar slut när man matar den med ett register i
stället för med dokument — och att göra det utan att ändra en enda rad i
ImmersaDocs.

Ingenting här är en produkt. Det är en mätning.

Körs så här:

    python spik/spik.py

Kräver `pydantic` och att ImmersaDocs ligger bredvid (se IMMERSADOCS_ROT).
"""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

HÄR = Path(__file__).resolve().parent
RESULTAT = HÄR / "resultat"

# ImmersaDocs importeras från sin egen källkatalog. Vi installerar den inte
# och vi ändrar den inte — spiken ska kunna köras mot vilken version som helst.
IMMERSADOCS_ROT = Path(os.environ.get("IMMERSADOCS_ROT", "/home/user/ImmersaDocs"))
sys.path.insert(0, str(IMMERSADOCS_ROT / "packages" / "spatial-grammar" / "src"))
sys.path.insert(0, str(IMMERSADOCS_ROT / "packages" / "backend" / "src"))

from spatial_grammar.profiles import load_profiles  # noqa: E402
from spatial_grammar.spatial_mapper import SpatialMapper  # noqa: E402

API = "https://utlovat.se/api/v1"
HV_API = "https://utlovat.se/handlingsvagen/api/hv"

# Kategori → kod. Koden är godtycklig; motorn läser bara siffran före punkten
# och slår upp den i profilens arttabell.
KATEGORI_KOD = {
    "välfärd": "1",
    "utbildning": "2",
    "skatter": "3",
    "klimat-miljö": "4",
    "migration": "5",
    "rättsväsende": "6",
    "försvar": "7",
    "infrastruktur": "8",
    "övrigt": "9",
}

# Handlingsvågens dom → mognadstal. Motorn kallar fältet `trl` och förväntar
# sig 1–9; vi använder det som en ordnad mognadsskala, inget annat.
DOM_MOGNAD = {
    "agerat_i_linje": 9,
    "bade_och": 5,
    "agerat_emot": 3,
    "ingen_handling_annu": 1,
}


# Sajten ligger bakom Cloudflare, som nekar `Python-urllib` rakt av. En egen,
# ärlig användaragent räcker — vi utger oss inte för att vara en webbläsare.
ANVÄNDARAGENT = "storleksordningen-spik/0.1 (+https://github.com/bambapappa/storleksordningen)"


def hämta(url: str) -> dict:
    begäran = urllib.request.Request(url, headers={"User-Agent": ANVÄNDARAGENT})
    with urllib.request.urlopen(begäran, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


@dataclass
class Löfte:
    """Ett löfte klätt som en bidragsansökan.

    Fältnamnen är ImmersaDocs, inte våra. Motorn väljer profil genom att
    titta efter attributet `requestedAmount`, så ett vanligt objekt med rätt
    namn går rakt igenom grant-profilen utan att någon kod behöver ändras.
    """

    projectTitle: str
    abstract: str
    fundingBody: str
    requestedAmount: float
    totalProjectCost: float
    durationMonths: int
    fordClassification: str | None
    trl: int | None
    workPackages: list = field(default_factory=list)
    consortiumPartners: list = field(default_factory=list)
    sdgMapping: list = field(default_factory=list)
    acronym: str | None = None


def total_msek(löfte: dict) -> float:
    """Summan för mandatperioden, samma regel som sajten använder (R1)."""
    kostnad = löfte["cost"]
    return kostnad["msek_base"] * (4 if kostnad["period"] == "per_ar" else 1)


def main() -> int:
    RESULTAT.mkdir(exist_ok=True)

    print("Hämtar publika data …")
    löften = hämta(f"{API}/promises.json")["data"]
    partier = {p["code"]: p for p in hämta(f"{API}/parties.json")["data"]}
    hv = hämta(f"{HV_API}/summary.json")
    print(f"  {len(löften)} löften, {len(partier)} partier, "
          f"{len(hv.get('loften', []))} rader i Handlingsvågens rutnät")

    # Handlingsvågens dom per (löfte, parti). Vi tar partiets egen dom om den
    # finns — annars står löftet utan handling.
    dom_per_löfte: dict[str, str] = {}
    for rad in hv.get("loften", []):
        celler = rad.get("celler") or {}
        for parti, cell in celler.items():
            status = (cell or {}).get("status")
            if status and status != "ingen_handling_annu":
                dom_per_löfte[rad["id"]] = status
                break
    print(f"  {len(dom_per_löfte)} löften har en dom som inte är 'ingen handling ännu'")

    profiler = load_profiles(HÄR / "profil-utlovat.json")
    motor = SpatialMapper(profiles=profiler)

    scener: list[dict] = []
    kraschade: list[dict] = []
    kopplingar_per_löfte = {r["id"]: r.get("n_kopplingar", 0) for r in hv.get("loften", [])}

    # Delade löften: alla som bär samma group_id hör ihop.
    grupp_medlemmar: dict[str, list[str]] = {}
    for l in löften:
        if l.get("group_id"):
            grupp_medlemmar.setdefault(l["group_id"], []).append(l["id"])

    for l in löften:
        parti_kod = l["parties"][0]
        parti = partier.get(parti_kod, {})
        belopp = total_msek(l)
        syskon = [x for x in grupp_medlemmar.get(l.get("group_id") or "", []) if x != l["id"]]

        doc = Löfte(
            projectTitle=l["title"],
            abstract=l["quote"],
            fundingBody=parti.get("name", parti_kod),
            requestedAmount=belopp,
            totalProjectCost=l["cost"]["msek_high"] * (4 if l["cost"]["period"] == "per_ar" else 1),
            durationMonths=48 if l["cost"]["period"] == "per_ar" else 12,
            fordClassification=KATEGORI_KOD.get(l["category"]),
            trl=DOM_MOGNAD.get(dom_per_löfte.get(l["id"], "ingen_handling_annu")),
            workPackages=[None] * kopplingar_per_löfte.get(l["id"], 0),
            consortiumPartners=syskon,
            acronym=l["id"],
        )

        try:
            scen = motor.map_document(doc)
        except Exception as fel:  # noqa: BLE001 — vi vill räkna felen, inte dölja dem
            kraschade.append({
                "id": l["id"],
                "parti": parti_kod,
                "kategori": l["category"],
                "msek_base": l["cost"]["msek_base"],
                "typ": type(fel).__name__,
                "fel": str(fel),
            })
            continue

        scener.append(json.loads(scen.model_dump_json()))

    # ---- determinism: samma indata två gånger ska ge samma utdata ----
    andra_varvet = []
    for l in löften:
        parti_kod = l["parties"][0]
        belopp = total_msek(l)
        if belopp <= 0:
            continue
        syskon = [x for x in grupp_medlemmar.get(l.get("group_id") or "", []) if x != l["id"]]
        doc = Löfte(
            projectTitle=l["title"],
            abstract=l["quote"],
            fundingBody=partier.get(parti_kod, {}).get("name", parti_kod),
            requestedAmount=belopp,
            totalProjectCost=l["cost"]["msek_high"] * (4 if l["cost"]["period"] == "per_ar" else 1),
            durationMonths=48 if l["cost"]["period"] == "per_ar" else 12,
            fordClassification=KATEGORI_KOD.get(l["category"]),
            trl=DOM_MOGNAD.get(dom_per_löfte.get(l["id"], "ingen_handling_annu")),
            workPackages=[None] * kopplingar_per_löfte.get(l["id"], 0),
            consortiumPartners=syskon,
            acronym=l["id"],
        )
        andra_varvet.append(json.loads(motor.map_document(doc).model_dump_json()))
    deterministisk = andra_varvet == scener

    # ---- rapport ----
    höjder = [s["tree"]["height"] for s in scener]
    rapport = {
        "körd": "spik/spik.py",
        "källa": {"api": API, "hv_api": HV_API},
        "in": {
            "löften": len(löften),
            "partier": len(partier),
        },
        "ut": {
            "scener": len(scener),
            "kraschade": len(kraschade),
        },
        "deterministisk": deterministisk,
        "höjd": {
            "min": min(höjder) if höjder else None,
            "max": max(höjder) if höjder else None,
            "spann_tiopotenser": (max(höjder) - min(höjder)) if höjder else None,
        },
        "biom": dict(Counter(s["biome"] for s in scener).most_common()),
        "art": dict(Counter(s["tree"]["species"] for s in scener).most_common()),
        "fas": dict(Counter(s["tree"]["phase"] for s in scener).most_common()),
        "grenar": dict(Counter(s["tree"]["branch_count"] for s in scener).most_common(8)),
        "kraschorsaker": dict(Counter(k["fel"].split(",")[0] for k in kraschade).most_common(3)),
    }

    (RESULTAT / "scener.json").write_text(
        json.dumps(scener, ensure_ascii=False, indent=2), encoding="utf-8")
    (RESULTAT / "kraschade.json").write_text(
        json.dumps(kraschade, ensure_ascii=False, indent=2), encoding="utf-8")
    (RESULTAT / "rapport.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 68)
    print(f"  {len(scener)} av {len(löften)} löften gick genom motorn")
    print(f"  {len(kraschade)} kraschade")
    print(f"  deterministisk: {'ja' if deterministisk else 'NEJ'}")
    if höjder:
        print(f"  höjd: {min(höjder):.2f} … {max(höjder):.2f}"
              f"  ({max(höjder) - min(höjder):.2f} tiopotenser)")
    print("=" * 68)
    for nyckel in ("biom", "art", "fas"):
        print(f"\n  {nyckel}:")
        for k, v in rapport[nyckel].items():
            print(f"    {k:<16} {v:>4}")
    if kraschade:
        print(f"\n  kraschorsaker:")
        for k, v in rapport["kraschorsaker"].items():
            print(f"    {v:>4}  {k}")
    print(f"\nSkrivet till {RESULTAT}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
