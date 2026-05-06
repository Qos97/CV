#!/usr/bin/env python3
"""
Adds new Sendit bullets to both EN and PT CV DOCX files.
Uses zipfile + string manipulation to avoid needing python-docx.
"""
import zipfile
import shutil
import os

# ─── Templates ────────────────────────────────────────────────────────────────

BULLET_TEMPLATE = (
    '<w:p>'
    '<w:pPr>'
    '<w:pStyle w:val="ListParagraph"/>'
    '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>'
    '<w:spacing w:after="30"/>'
    '</w:pPr>'
    '<w:r>'
    '<w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri"/>'
    '<w:color w:val="1A1A1A"/>'
    '<w:sz w:val="19"/>'
    '<w:szCs w:val="19"/>'
    '</w:rPr>'
    '<w:t xml:space="preserve">{text}</w:t>'
    '</w:r>'
    '</w:p>'
)

def make_bullet(text):
    return BULLET_TEMPLATE.format(text=text)

# ─── New bullets ──────────────────────────────────────────────────────────────

EN_BULLETS = [
    make_bullet(
        "Automated Exchange Online user lifecycle via PowerShell: full offboarding "
        "(Distribution Lists, M365 Groups, Shared Mailboxes, RBAC, mailbox delegations), "
        "permission/group membership cloning, and scheduled report uploads to SharePoint via PnP and Graph API"
    ),
    make_bullet(
        "Developed containerised video compression service (C#/.NET, Docker): downloads MP4s "
        "from SharePoint via Graph API, compresses with FFmpeg (H.264/CRF28), re-uploads to "
        "SharePoint on a 2-hour cycle with automated Office 365 email alerting on failure"
    ),
    make_bullet(
        "Built internal IT self-service portal (ASP.NET 8 MVC, Windows Authentication, IIS): AD user creation "
        "with configurable OUs, password reset/unlock, group management, password age tracking, and Exchange Online "
        "Distribution List management via Graph API — eliminating helpdesk dependency on PowerShell/MMC"
    ),
]

PT_BULLETS = [
    make_bullet(
        "Automatizou ciclo de vida de utilizadores Exchange Online via PowerShell: offboarding "
        "completo (Distribution Lists, M365 Groups, Shared Mailboxes, RBAC, delegações), "
        "clonagem de grupos e permissões, e upload automático de relatórios para SharePoint via PnP e Graph API"
    ),
    make_bullet(
        "Desenvolveu serviço de compressão de vídeo containerizado (C#/.NET, Docker): download de "
        "MP4s do SharePoint via Graph API, compressão com FFmpeg (H.264/CRF28), re-upload automático "
        "em ciclo de 2 horas com alertas por email Office 365 em caso de erro"
    ),
    make_bullet(
        "Construiu portal interno IT de self-service (ASP.NET 8 MVC, Windows Authentication, IIS): criação de "
        "utilizadores AD com OUs configuráveis, reset/desbloqueio de passwords, gestão de grupos, tracking de "
        "idade de password e gestão de Distribution Lists Exchange Online via Graph API"
    ),
]

# ─── Insertion anchor: insert BEFORE the Azure AD bullet ──────────────────────
# We insert just BEFORE the "Manage Hybrid Azure AD" bullet (EN) / "Gestão de Hybrid Azure AD" (PT)
# so related automation topics are grouped.

EN_ANCHOR = "Manage Hybrid Azure AD, Active Directory"
PT_ANCHOR = "Gestão de Hybrid Azure AD, Active Directory"

# ─── Processing function ───────────────────────────────────────────────────────

def update_docx(src_path, anchor_text, new_bullets):
    # Read existing DOCX
    with zipfile.ZipFile(src_path, 'r') as z:
        names = z.namelist()
        files = {}
        for name in names:
            files[name] = z.read(name)

    doc_xml = files['word/document.xml'].decode('utf-8')

    # Find the <w:p> element that contains anchor_text
    # We'll find the start of the paragraph containing the anchor
    anchor_idx = doc_xml.find(anchor_text)
    if anchor_idx == -1:
        print(f"ERROR: anchor '{anchor_text}' not found in {src_path}")
        return False

    # Walk backwards to find the start of the <w:p> tag
    para_start = doc_xml.rfind('<w:p>', 0, anchor_idx)
    if para_start == -1:
        print(f"ERROR: could not find <w:p> before anchor in {src_path}")
        return False

    # Insert new bullets just before this paragraph
    insertion = ''.join(new_bullets)
    new_xml = doc_xml[:para_start] + insertion + doc_xml[para_start:]

    # Write back to DOCX
    files['word/document.xml'] = new_xml.encode('utf-8')

    # Save to a temp file, then replace original
    tmp_path = src_path + '.tmp'
    with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for name in names:
            z_out.writestr(name, files[name])

    os.replace(tmp_path, src_path)
    print(f"Updated: {src_path}")
    return True


# ─── Run ──────────────────────────────────────────────────────────────────────

base = '/mnt/c/Users/filip/OneDrive/Documentos/CV/cv-documents'

ok_en = update_docx(f'{base}/CV_Filipe_Fernandes_EN.docx', EN_ANCHOR, EN_BULLETS)
ok_pt = update_docx(f'{base}/CV_Filipe_Fernandes_PT.docx', PT_ANCHOR, PT_BULLETS)

if ok_en and ok_pt:
    print("\nDone. Both CVs updated successfully.")
    print("Convert to PDF:")
    print("  soffice --headless --convert-to pdf CV_Filipe_Fernandes_EN.docx --outdir .")
    print("  soffice --headless --convert-to pdf CV_Filipe_Fernandes_PT.docx --outdir .")
