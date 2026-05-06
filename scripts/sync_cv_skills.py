#!/usr/bin/env python3
"""
sync_cv_skills.py — Adds missing skills to both CV .docx files:
  1. Adds Python · C# / .NET to the Automation & Scripting line
  2. Adds AI & Productivity line before the Professional Development section

Uses zipfile + XML string manipulation (no external dependencies).
"""
import os, zipfile
from pathlib import Path

BASE    = Path(__file__).parent.parent
CV_DIR  = BASE / "cv-documents"
CV_EN   = CV_DIR / "CV_Filipe_Fernandes_EN.docx"
CV_PT   = CV_DIR / "CV_Filipe_Fernandes_PT.docx"


def update_docx(path: Path, replacements: list[tuple[str, str]], label: str):
    """Apply a list of (old, new) string replacements to word/document.xml."""
    with zipfile.ZipFile(path, 'r') as z:
        names = z.namelist()
        files = {name: z.read(name) for name in names}

    xml = files['word/document.xml'].decode('utf-8')

    for old, new in replacements:
        if old not in xml:
            print(f"  WARNING [{label}]: anchor not found — {old[:60]!r}")
            continue
        xml = xml.replace(old, new, 1)
        print(f"  ✓ [{label}] applied: {old[:60]!r}")

    files['word/document.xml'] = xml.encode('utf-8')

    tmp = str(path) + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for name in names:
            z_out.writestr(name, files[name])

    os.replace(tmp, str(path))


# ── Skill line XML template (matches existing formatting) ─────────────────────
def skill_line(para_id: str, category: str, items: str) -> str:
    return (
        f'<w:p w14:paraId="{para_id}" w14:textId="77777777" w:rsidR="004C0F7F" w:rsidRDefault="004C0F7F">'
        f'<w:pPr><w:spacing w:after="44"/></w:pPr>'
        f'<w:r><w:rPr><w:b/><w:bCs/><w:color w:val="1F4E79"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>'
        f'<w:t xml:space="preserve">{category}:  </w:t></w:r>'
        f'<w:r><w:rPr><w:color w:val="1A1A1A"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>'
        f'<w:t>{items}</w:t></w:r>'
        f'</w:p>'
    )


# ── EN changes ────────────────────────────────────────────────────────────────
AI_LINE_EN = skill_line(
    "AA000001",
    "AI &amp; Productivity",
    "Claude  \u00b7  ChatGPT  \u00b7  GitHub Copilot  \u00b7  AI-assisted Scripting  \u00b7  Prompt Engineering  \u00b7  Workflow Automation with LLMs",
)

# Anchor: the <w:pBdr> paragraph that starts "PROFESSIONAL DEVELOPMENT"
PROF_DEV_ANCHOR_EN = '<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="6" w:color="1F4E79"/></w:pBdr><w:spacing w:before="200" w:after="100"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/><w:color w:val="1F4E79"/></w:rPr><w:t>PROFESSIONAL DEVELOPMENT</w:t>'

EN_REPLACEMENTS = [
    # 1. Add Python · C# / .NET to Automation & Scripting
    (
        '<w:t>PowerShell  \u00b7  Bash  \u00b7  Ansible</w:t></w:r></w:p><w:p w14:paraId="5A109BF0"',
        '<w:t>PowerShell  \u00b7  Bash  \u00b7  Ansible  \u00b7  Python  \u00b7  C# / .NET</w:t></w:r></w:p><w:p w14:paraId="5A109BF0"',
    ),
    # 2. Insert AI & Productivity line before PROFESSIONAL DEVELOPMENT
    (
        PROF_DEV_ANCHOR_EN,
        AI_LINE_EN + PROF_DEV_ANCHOR_EN,
    ),
]


# ── PT changes ────────────────────────────────────────────────────────────────
AI_LINE_PT = skill_line(
    "BB000001",
    "IA &amp; Produtividade",
    "Claude  \u00b7  ChatGPT  \u00b7  GitHub Copilot  \u00b7  Scripting assistido por IA  \u00b7  Prompt Engineering  \u00b7  Automa\u00e7\u00e3o de fluxos com LLMs",
)

PROF_DEV_ANCHOR_PT = '<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="6" w:color="1F4E79"/></w:pBdr><w:spacing w:before="200" w:after="100"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/><w:color w:val="1F4E79"/></w:rPr><w:t>DESENVOLVIMENTO PROFISSIONAL</w:t>'

PT_REPLACEMENTS = [
    # 1. Add Python · C# / .NET to Automação & Scripting
    (
        '<w:t>PowerShell  \u00b7  Bash  \u00b7  Ansible</w:t></w:r></w:p><w:p w14:paraId="08F1A95A"',
        '<w:t>PowerShell  \u00b7  Bash  \u00b7  Ansible  \u00b7  Python  \u00b7  C# / .NET</w:t></w:r></w:p><w:p w14:paraId="08F1A95A"',
    ),
    # 2. Insert IA & Produtividade line before DESENVOLVIMENTO PROFISSIONAL
    (
        PROF_DEV_ANCHOR_PT,
        AI_LINE_PT + PROF_DEV_ANCHOR_PT,
    ),
]


# ── Run ───────────────────────────────────────────────────────────────────────
print("Updating EN CV...")
update_docx(CV_EN, EN_REPLACEMENTS, "EN")

print("\nUpdating PT CV...")
update_docx(CV_PT, PT_REPLACEMENTS, "PT")

print("\nDone. Open the .docx files to verify formatting, then export to PDF.")
