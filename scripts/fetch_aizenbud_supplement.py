#!/usr/bin/env python3
"""Fetch the Aizenbud et al. supplement from public article mirrors.

This is a provenance helper, not part of the frozen V22 regression. PMC moved its
article datasets to a new per-version AWS structure in 2026, so that official
cloud route is tried first. Older OA-package and direct URLs remain as fallbacks
and their failures are retained in the receipt.
"""
from __future__ import annotations

import argparse
import io
import json
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote
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
S3_HTTPS = "https://pmc-oa-opendata.s3.amazonaws.com"


def read_url(url: str) -> tuple[bytes, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=90) as r:
        return r.read(), r.headers.get("content-type", "")


def fetch_pdf(url: str) -> bytes:
    payload, ctype = read_url(url)
    if not payload.startswith(b"%PDF"):
        raise RuntimeError(f"not a PDF ({ctype!r}, first bytes={payload[:30]!r})")
    return payload


def s3_keys_for_pmcid(pmcid: str) -> list[str]:
    # New 2026 PMC AWS layout is versioned: PMC12345678.1/<objects>.
    url = f"{S3_HTTPS}/?list-type=2&prefix={quote(pmcid + '.', safe='')}"
    payload, _ = read_url(url)
    root = ET.fromstring(payload)
    keys = []
    for el in root.iter():
        if el.tag.rsplit("}", 1)[-1] == "Key" and el.text:
            keys.append(el.text)
    return keys


def _supplement_score(key: str) -> int:
    base = Path(key).name.lower()
    score = 0
    if base == "pnas.2533168123.sapp.pdf":
        score = 100
    elif "supplement" in base and base.endswith(".pdf"):
        score = 90
    elif "sapp" in base and base.endswith(".pdf"):
        score = 85
    elif base.endswith(".pdf") and ("suppl" in base or "supp" in base):
        score = 80
    elif base.endswith(".pdf") and ("-s0" in base or "_s0" in base):
        score = 60
    # Main article PDFs in the new layout are usually PMCID.version.pdf.
    if base.startswith("pmc") and base.endswith(".pdf"):
        score = min(score, 5)
    return score


def fetch_from_pmc_s3(pmcid: str) -> tuple[bytes, dict]:
    keys = s3_keys_for_pmcid(pmcid)
    ranked = sorted(
        ((_supplement_score(key), key) for key in keys),
        key=lambda x: (-x[0], x[1]),
    )
    ranked = [(score, key) for score, key in ranked if score > 0]
    if not ranked:
        raise RuntimeError(f"no supplement-looking PDF under AWS prefix; keys={keys!r}")

    failures = []
    for score, key in ranked:
        url = f"{S3_HTTPS}/{quote(key, safe='/._-')}"
        try:
            payload = fetch_pdf(url)
            return payload, {
                "pmcid": pmcid,
                "s3_key": key,
                "s3_url": url,
                "candidate_score": score,
                "prefix_keys": keys,
            }
        except Exception as exc:
            failures.append({"key": key, "url": url, "error": repr(exc)})
    raise RuntimeError(f"AWS candidates failed; failures={failures!r}; keys={keys!r}")


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
        candidates = sorted(
            ((_supplement_score(m.name), m) for m in members),
            key=lambda x: (-x[0], x[1].name),
        )
        candidates = [(score, member) for score, member in candidates if score > 0]
        if not candidates:
            raise RuntimeError(f"no supplement PDF in OA package; files={names}")
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
    source_receipt = None

    for pmcid in PMC_IDS:
        try:
            payload, source_receipt = fetch_from_pmc_s3(pmcid)
            chosen_name = f"{pmcid}_aws"
            chosen_url = source_receipt["s3_url"]
            attempts.append({"name": chosen_name, "status": "ok", "bytes": len(payload)})
            break
        except Exception as exc:
            attempts.append({"name": f"{pmcid}_aws", "status": "failed", "error": repr(exc)})

    if payload is None:
        for pmcid in PMC_IDS:
            try:
                payload, source_receipt = fetch_from_pmc_package(pmcid)
                chosen_name = f"{pmcid}_oa_package"
                chosen_url = source_receipt["oa_url"]
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
        "source": source_receipt,
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
