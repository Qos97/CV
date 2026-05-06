#!/usr/bin/env python3
"""
check_cv.py — Verifies that CV .docx files contain the same information as content.json.

Checks per language (EN / PT):
  - Job: company, role, period
  - Each bullet point
  - Each skill item

Usage:
    python3 scripts/check_cv.py
"""
import json, re, sys, zipfile
from pathlib import Path

BASE     = Path(__file__).parent.parent
CONTENT  = BASE / "content.json"
CV_DIR   = BASE / "cv-documents"
CV_FILES = {
    "en": CV_DIR / "CV_Filipe_Fernandes_EN.docx",
    "pt": CV_DIR / "CV_Filipe_Fernandes_PT.docx",
}


# ── Extract plain text from docx ─────────────────────────────────────────────

def extract_text(docx_path: Path) -> str:
    """Extract all text from a .docx by concatenating <w:t> elements."""
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    # Collect all <w:t> content; preserve spaces
    tokens = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml, re.DOTALL)
    text = " ".join(tokens)
    # Normalise whitespace
    text = re.sub(r'\s+', ' ', text)
    return text


def normalise(s: str) -> str:
    """Lowercase + collapse whitespace for loose matching."""
    return re.sub(r'\s+', ' ', s.lower().strip())


def check(label: str, value: str, docx_text: str) -> bool:
    """Return True if value is found in docx_text (case-insensitive)."""
    return normalise(value) in normalise(docx_text)


# ── Main ─────────────────────────────────────────────────────────────────────

with open(CONTENT, encoding="utf-8") as f:
    content = json.load(f)

total_checks = 0
total_missing = 0

for lang, docx_path in CV_FILES.items():
    print(f"\n{'='*60}")
    print(f"  {lang.upper()} — {docx_path.name}")
    print(f"{'='*60}")

    if not docx_path.exists():
        print(f"  ERROR: file not found — {docx_path}")
        total_missing += 1
        continue

    docx_text = extract_text(docx_path)
    data = content[lang]
    missing = []

    # ── Experience ───────────────────────────────────────────────────────────
    print("\n  [Experience]")
    for job in data["experience"]["jobs"]:
        header = f"{job['company']} | {job['role']} | {job['period']}"
        fields = [
            ("company", job["company"]),
            ("role",    job["role"]),
            ("period",  job["period"]),
        ]
        job_ok = True
        for field, value in fields:
            total_checks += 1
            found = check(field, value, docx_text)
            if not found:
                missing.append(f"[{job['company']}] {field}: {value!r}")
                job_ok = False

        status = "✓" if job_ok else "✗"
        print(f"    {status} {header}")

        for bullet in job.get("bullets", []):
            total_checks += 1
            # Use first 60 chars as anchor to avoid false negatives from minor diffs
            anchor = bullet[:60]
            found = check("bullet", anchor, docx_text)
            mark = "  ✓" if found else "  ✗"
            if not found:
                missing.append(f"[{job['company']}] bullet: {bullet[:80]}...")
            print(f"      {mark} {bullet[:80]}{'...' if len(bullet) > 80 else ''}")

    # ── Skills ───────────────────────────────────────────────────────────────
    print("\n  [Skills]")
    skill_missing = []
    for group in data["skills"]["groups"]:
        for item in group["items"]:
            total_checks += 1
            found = check("skill", item, docx_text)
            if not found:
                skill_missing.append(f"{group['category']} › {item}")
                missing.append(f"[Skills] {group['category']} › {item}")

    if skill_missing:
        print(f"    ✗ {len(skill_missing)} skill(s) not found in docx:")
        for s in skill_missing:
            print(f"      - {s}")
    else:
        skill_count = sum(len(g["items"]) for g in data["skills"]["groups"])
        print(f"    ✓ All {skill_count} skills present")

    # ── Summary ──────────────────────────────────────────────────────────────
    total_missing += len(missing)
    print(f"\n  {'─'*56}")
    if missing:
        print(f"  MISSING ({len(missing)} items):")
        for m in missing:
            print(f"    ✗ {m}")
    else:
        print(f"  All checks passed.")

# ── Final ─────────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  Total checks : {total_checks}")
print(f"  Missing      : {total_missing}")
print(f"{'='*60}\n")

sys.exit(1 if total_missing > 0 else 0)
