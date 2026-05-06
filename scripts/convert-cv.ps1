# convert-cv.ps1
# Converts CV DOCX to PDF via Word COM.
# Copies files to C:\Temp first to avoid OneDrive Protected View issues.

$cvDir  = "C:\Users\filip\OneDrive\Documentos\CV\cv-documents"
$pubDir = "C:\Users\filip\OneDrive\Documentos\CV\website\public"
$tmpDir = "C:\Temp\cv-convert"

$files = @(
    "CV_Filipe_Fernandes_EN.docx",
    "CV_Filipe_Fernandes_PT.docx"
)

# Ensure temp dir exists
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null

$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $true   # must be visible or export hangs on dialogs

    foreach ($file in $files) {
        $src     = Join-Path $cvDir $file
        $tmp     = Join-Path $tmpDir $file
        $pdfName = [System.IO.Path]::ChangeExtension($file, ".pdf")
        $pdfTmp  = Join-Path $tmpDir $pdfName
        $pdfDoc  = Join-Path $cvDir $pdfName
        $pdfPub  = Join-Path $pubDir $pdfName

        if (-not (Test-Path $src)) {
            Write-Host "  SKIP: $file not found"
            continue
        }

        # Copy to local temp (avoids OneDrive Protected View)
        Copy-Item $src $tmp -Force
        Write-Host "  Converting $file ..."

        $doc = $word.Documents.Open($tmp, $false, $true)   # ReadOnly=true, no dialogs
        $doc.ExportAsFixedFormat($pdfTmp, 17)
        $doc.Close($false)

        # Copy PDF back to cv-documents and website/public
        Copy-Item $pdfTmp $pdfDoc -Force
        Copy-Item $pdfTmp $pdfPub -Force

        Write-Host "  OK: $pdfName"
    }

    Write-Host "Done."
    exit 0
}
catch {
    Write-Host "ERROR: $_"
    exit 1
}
finally {
    if ($word) { $word.Quit() }
    Remove-Item $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
}
