$csvPath = "$env:USERPROFILE\.gemini\antigravity\docs_candidates.csv"
$backupDir = "$env:USERPROFILE\Documents\My_Valuable_Docs_Backup"

if (-not (Test-Path $csvPath)) {
    Write-Host "CSV file not found!"
    exit
}

$csv = Import-Csv $csvPath

# Filter out trash and framework defaults
$filtered = $csv | Where-Object { 
    $_.Path -notmatch '\\\$RECYCLE\.BIN\\' -and 
    $_.Path -notmatch '\\\.claude\\' -and 
    $_.Path -notmatch '\\\.opencode\\' -and
    $_.Path -notmatch '\\node_modules\\'
}

Write-Host "Filtered down to $($filtered.Count) valuable files from $($csv.Count) total."

if (Test-Path $backupDir) {
    Remove-Item -Recurse -Force $backupDir
}
New-Item -ItemType Directory -Path $backupDir | Out-Null

$count = 0
foreach ($item in $filtered) {
    $srcPath = $item.Path
    # Create a nice relative structure in the backup dir
    $relPath = $srcPath -replace ':', '' # e.g. D\path\...
    $destPath = Join-Path $backupDir $relPath
    
    $destDir = Split-Path $destPath -Parent
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir | Out-Null
    }
    
    Copy-Item -Path $srcPath -Destination $destPath -Force -ErrorAction SilentlyContinue
    $count++
}

Write-Host "Copied $count files to $backupDir."

Set-Location $backupDir
git init
git add .
git commit -m "Auto backup of valuable MD and DOCX files before system reset"

Write-Host "Creating private GitHub repository 'my-valuable-docs-backup'..."
# Create repo and push
gh repo create my-valuable-docs-backup --private --source=. --push

Write-Host "Backup complete!"
