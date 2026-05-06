#!/usr/bin/env python3
"""
Fixes UserPortal bullet placement.
Removes the wrongly-placed bullet and re-inserts it after the Video Compression bullet.
"""
import zipfile, os, re

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

BULLETS = {
    'en': {
        'text': (
            "Built internal IT self-service portal (ASP.NET 8 MVC, Windows Authentication, IIS): AD user creation "
            "with configurable OUs, password reset/unlock, group management, password age tracking, and Exchange Online "
            "Distribution List management via Graph API \u2014 eliminating helpdesk dependency on PowerShell/MMC"
        ),
        # Insert AFTER this text (end of its paragraph)
        'after_anchor': "re-uploads to SharePoint on a 2-hour cycle with automated Office 365 email alerting on failure",
    },
    'pt': {
        'text': (
            "Construiu portal interno IT de self-service (ASP.NET 8 MVC, Windows Authentication, IIS): cria\u00e7\u00e3o de "
            "utilizadores AD com OUs configur\u00e1veis, reset/desbloqueio de passwords, gest\u00e3o de grupos, tracking de "
            "idade de password e gest\u00e3o de Distribution Lists Exchange Online via Graph API"
        ),
        'after_anchor': "re-upload autom\u00e1tico em ciclo de 2 horas com alertas por email Office 365 em caso de erro",
    },
}

FILES = {
    'en': '/mnt/c/Users/filip/OneDrive/Documentos/CV/cv-documents/CV_Filipe_Fernandes_EN.docx',
    'pt': '/mnt/c/Users/filip/OneDrive/Documentos/CV/cv-documents/CV_Filipe_Fernandes_PT.docx',
}

def fix(lang):
    path = FILES[lang]
    info = BULLETS[lang]
    bullet_text = info['text']
    after_anchor = info['after_anchor']

    with zipfile.ZipFile(path, 'r') as z:
        names = z.namelist()
        files = {n: z.read(n) for n in names}

    xml = files['word/document.xml'].decode('utf-8')

    # Step 1: Remove existing wrongly-placed bullet (full <w:p>...</w:p> containing the text)
    wrong_idx = xml.find(bullet_text)
    if wrong_idx != -1:
        para_start = xml.rfind('<w:p>', 0, wrong_idx)
        para_end = xml.find('</w:p>', wrong_idx) + len('</w:p>')
        xml = xml[:para_start] + xml[para_end:]
        print(f"  [{lang.upper()}] Removed wrong bullet at pos {wrong_idx}")
    else:
        print(f"  [{lang.upper()}] Wrong bullet not found — skipping removal")

    # Step 2: Find the after_anchor and insert the new bullet after that paragraph
    anchor_idx = xml.find(after_anchor)
    if anchor_idx == -1:
        print(f"  [{lang.upper()}] ERROR: after_anchor not found"); return

    # Find end of the paragraph containing the anchor
    para_end = xml.find('</w:p>', anchor_idx) + len('</w:p>')
    new_bullet = BULLET_TEMPLATE.format(text=bullet_text)
    xml = xml[:para_end] + new_bullet + xml[para_end:]
    print(f"  [{lang.upper()}] Inserted bullet after anchor at pos {anchor_idx}")

    files['word/document.xml'] = xml.encode('utf-8')

    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for n in names:
            z_out.writestr(n, files[n])
    os.replace(tmp, path)
    print(f"  [{lang.upper()}] Saved.")

print("Fixing EN CV...")
fix('en')
print("Fixing PT CV...")
fix('pt')

# Verify
print("\nVerifying EN:")
with zipfile.ZipFile(FILES['en']) as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', ' ', xml)
text = re.sub(r'\s+', ' ', text).strip()
idx = text.find('Automated Exchange Online')
print(text[idx:idx+900])
