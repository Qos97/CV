#!/usr/bin/env python3
"""Adds UserPortal bullet to both CV DOCX files."""
import zipfile, os

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
    'en': BULLET_TEMPLATE.format(text=(
        "Built internal IT self-service portal (ASP.NET 8 MVC, Windows Authentication, IIS): AD user creation "
        "with configurable OUs, password reset/unlock, group management, password age tracking, and Exchange Online "
        "Distribution List management via Graph API — eliminating helpdesk dependency on PowerShell/MMC"
    )),
    'pt': BULLET_TEMPLATE.format(text=(
        "Construiu portal interno IT de self-service (ASP.NET 8 MVC, Windows Authentication, IIS): criação de "
        "utilizadores AD com OUs configuráveis, reset/desbloqueio de passwords, gestão de grupos, tracking de "
        "idade de password e gestão de Distribution Lists Exchange Online via Graph API"
    )),
}

ANCHORS = {
    'en': "Manage Hybrid Azure AD, Active Directory",
    'pt': "Gestão de Hybrid Azure AD, Active Directory",
}

FILES = {
    'en': '/mnt/c/Users/filip/OneDrive/Documentos/CV/cv-documents/CV_Filipe_Fernandes_EN.docx',
    'pt': '/mnt/c/Users/filip/OneDrive/Documentos/CV/cv-documents/CV_Filipe_Fernandes_PT.docx',
}

def update(lang):
    path = FILES[lang]
    anchor = ANCHORS[lang]
    bullet = BULLETS[lang]

    with zipfile.ZipFile(path, 'r') as z:
        names = z.namelist()
        files = {n: z.read(n) for n in names}

    xml = files['word/document.xml'].decode('utf-8')

    idx = xml.find(anchor)
    if idx == -1:
        print(f"ERROR: anchor not found in {lang.upper()} CV"); return

    para_start = xml.rfind('<w:p>', 0, idx)
    new_xml = xml[:para_start] + bullet + xml[para_start:]
    files['word/document.xml'] = new_xml.encode('utf-8')

    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for n in names:
            z_out.writestr(n, files[n])
    os.replace(tmp, path)
    print(f"Updated {lang.upper()} CV")

update('en')
update('pt')
print("Done.")
