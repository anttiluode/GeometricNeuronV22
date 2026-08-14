#!/usr/bin/env python3
"""Fetch the Aizenbud et al. supplement from public article mirrors.

This is a provenance helper, not part of the frozen V22 regression. Direct
article-bin URLs are brittle, especially during PMC's 2026 dataset migration, so
we also query the official PMC Open Access service and inspect the complete OA
article package for the supplement.
"""
from __future__ import annotations

import argparse
import io
import json
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import Request, urlopen

DIRECT_URLS = [
    (
        "final_pmc_direct",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC13367794/bin/"
        "pnas.2533168123.sapp.pdf",
    ),
    (
        "final_pnas_direct",
        "https://www.pnas.org/doi/suppl/10.1073/pnas.2533168123/"
        "suppl_file/pnas.2533168123.sapp.pdf",
    ),
    (
        "preprint_pmc_direct",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11702691/bin/"
        "NIHPP2024.12.17.628883V2-supplement-1.pdf",
    ),
]

PMC_IDS = ["PMC13367794", "PMC11702691"]
USER_AGENT = "GeometricNeuronV22 provenance audit; public reproducibility check"


def read_url(url: str) -> tuple[bytes, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=90) as r:
        return r.read(), r.headers.get("content-type", "")


def fetch_pdf(url: str) -> bytes:
    payload, ctype = read_url(url)
    if not payload.startswith(b"%PDF"):
        raise RuntimeError(f"not a PDF ({ctype!r}, first bytes={payload[:30]!r})")
    return payload


def https_from_ftp(url: str) -> str:
    prefix = "ftp://ftp.ncbi.nlm.nih.gov/"
    if url.startswith(prefix):
        return "https://ftp.ncbi.nlm.nih.gov/" + url[len(prefix):]
    return url


def pmc_oa_links(pmcid: str) -> list[tuple[str, str]]:
    api = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}"
    payload, _ = read_url(api)
    root = ET.fromstring(payload)
    links: list[tuple[str, str]] = []
    for link in root.findall(".//link"):
        fmt = link.attrib.get("format", "")
        href = link.attrib.get("href", "")
        if href:
            links.append((fmt, https_from_ftp(href)))
    return links


def supplement_from_tgz(payload: bytes) -> tuple[bytes, str, list[str]]:
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile()]
        names = [m.name for m in members]
        candidates = []
        for member in members:
            base = Path(member.name).name.lower()
            score = 0
            if base == "pnas.2533168123.sapp.pdf":
                score = 100
            elif "supplement" in base and base.endswith(".pdf"):
                score = 80
            elif "sapp" in base and base.endswith(".pdf"):
                score = 70
            elif base.endswith(".pdf") and ("suppl" in base or "supp" in base):
                score = 60
            if score:
                candidates.append((score, member))
        if not candidates:
            raise RuntimeError(f"no supplement PDF in OA package; files={names}")
        candidates.sort(key=lambda x: (-x[0], x[1].name))
        chosen = candidates[0][1]
        fh = tf.extractfile(chosen)
        if fh is None:
            raise RuntimeError(f"unable to read {chosen.name}")
        pdf = fh.read()
        if not pdf.startswith(b"%PDF"):
            raise RuntimeError(f"package member {chosen.name} is not a PDF")
        return pdf, chosen.name, names


def fetch_from_pmc_package(pmcid: str) -> tuple[bytes, dict]:
    links = pmc_oa_links(pmcid)
    failures = []
    for fmt, url in sorted(links, key=lambda x: 0 if x[0] == "tgz" else 1):
        if fmt != "tgz":
            continue
        try:
            payload, ctype = read_url(url)
            pdf, member, names = supplement_from_tgz(payload)
            return pdf, {
                "pmcid": pmcid,
                "oa_format": fmt,
                "oa_url": url,
                "content_type": ctype,
                "package_bytes": len(payload),
                "supplement_member": member,
                "package_files": names,
            }
        except Exception as exc:
            failures.append({"format": fmt, "url": url, "error": repr(exc)})
    raise RuntimeError(f"OA package retrieval failed; links={links!r}; failures={failures!r}")


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
    package_receipt = None

    # Official OA packages first: less dependent on front-end URL layout.
    for pmcid in PMC_IDS:
        try:
            payload, package_receipt = fetch_from_pmc_package(pmcid)
            chosen_name = f"{pmcid}_oa_package"
            chosen_url = package_receipt["oa_url"]
            attempts.append({"name": chosen_name, "status": "ok", "bytes": len(payload)})
            break
        except Exception as exc:
            attempts.append({"name": f"{pmcid}_oa_package", "status": "failed", "error": repr(exc)})

    if payload is None:
        for name, url in DIRECT_URLS:
            try:
                payload = fetch_pdf(url)
                chosen_name, chosen_url = name, url
                attempts.append({"name": name, "url": url, "status": "ok", "bytes": len(payload)})
                break
            except Exception as exc:
                attempts.append({"name": name, "url": url, "status": "failed", "error": repr(exc)})

    receipt = {
        "attempts": attempts,
        "chosen": chosen_name,
        "url": chosen_url,
        "package": package_receipt,
    }
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
        "functional complexity index",
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
