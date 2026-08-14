#!/usr/bin/env python3
"""Fetch the Aizenbud et al. supplement from public article mirrors.

This is a provenance helper, not part of the frozen V22 regression.  It tries the
final PNAS/PMC supplement first and the older preprint supplement as a fallback,
then extracts text so Figure S5 / Table S1 can be audited without manual browser
copying.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

URLS = [
    (
        "final_pmc",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC13367794/bin/"
        "pnas.2533168123.sapp.pdf",
    ),
    (
        "final_pnas",
        "https://www.pnas.org/doi/suppl/10.1073/pnas.2533168123/"
        "suppl_file/pnas.2533168123.sapp.pdf",
    ),
    (
        "preprint_pmc",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11702691/bin/"
        "NIHPP2024.12.17.628883V2-supplement-1.pdf",
    ),
]


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "GeometricNeuronV22 provenance audit"})
    with urlopen(req, timeout=60) as r:
        payload = r.read()
        ctype = r.headers.get("content-type", "")
    if not payload.startswith(b"%PDF"):
        raise RuntimeError(f"not a PDF ({ctype!r}, first bytes={payload[:30]!r})")
    return payload


def extract_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("pip install pypdf") from exc
    reader = PdfReader(str(pdf_path))
    chunks = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"\n===== PDF PAGE {i} =====\n{text}")
    return "\n".join(chunks)


def context(text: str, needles: list[str], radius: int = 1800) -> dict[str, list[str]]:
    lower = text.lower()
    out: dict[str, list[str]] = {}
    for needle in needles:
        n = needle.lower()
        hits = []
        start = 0
        while True:
            i = lower.find(n, start)
            if i < 0:
                break
            lo = max(0, i - radius)
            hi = min(len(text), i + len(needle) + radius)
            hits.append(text[lo:hi])
            start = i + len(n)
        out[needle] = hits
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    attempts = []
    payload = None
    chosen_name = None
    chosen_url = None
    for name, url in URLS:
        try:
            payload = fetch(url)
            chosen_name, chosen_url = name, url
            attempts.append({"name": name, "url": url, "status": "ok", "bytes": len(payload)})
            break
        except Exception as exc:  # provenance receipt should preserve failed routes too
            attempts.append({"name": name, "url": url, "status": "failed", "error": repr(exc)})

    receipt = {"attempts": attempts, "chosen": chosen_name, "url": chosen_url}
    (args.out_dir / "fetch_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    if payload is None:
        raise SystemExit("all supplement download routes failed")

    pdf_path = args.out_dir / "aizenbud_supplement.pdf"
    pdf_path.write_bytes(payload)
    text = extract_text(pdf_path)
    (args.out_dir / "aizenbud_supplement.txt").write_text(text, encoding="utf-8")

    needles = [
        "Figure S5",
        "Fig. S5",
        "Table S1",
        "rat type synapses",
        "rat-type synapses",
        "0.022",
    ]
    ctx = context(text, needles)
    (args.out_dir / "interesting_context.json").write_text(
        json.dumps(ctx, indent=2), encoding="utf-8"
    )

    print(json.dumps(receipt, indent=2))
    for needle, hits in ctx.items():
        print(f"{needle!r}: {len(hits)} hits")


if __name__ == "__main__":
    main()
