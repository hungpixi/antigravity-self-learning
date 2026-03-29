$pathsToSearch = @("D:\", "$env:USERPROFILE\Documents", "$env:USERPROFILE\Desktop", "$env:USERPROFILE\Downloads")
$excludeRegex = "\\(node_modules|\.git|\.vscode|venv|\.venv|\.gemini|AppData|build|dist|tmp|temp)\\"

$allFiles = @()
foreach ($p in $pathsToSearch) {
    if (Test-Path $p) {
        Write-Host "Searching $p..."
        $mdFiles = cmd /c "dir /S /B /A:-D ""$p*.md"" 2>nul"
        if ($mdFiles) { $allFiles += $mdFiles }
        $docxFiles = cmd /c "dir /S /B /A:-D ""$p*.docx"" 2>nul"
        if ($docxFiles) { $allFiles += $docxFiles }
    }
}

$validFiles = @()
foreach ($f in $allFiles) {
    if (-not [string]::IsNullOrWhiteSpace($f) -and $f -notmatch $excludeRegex) {
        $fileInfo = Get-Item $f -ErrorAction SilentlyContinue
        if ($fileInfo) {
            if ($fileInfo.Extension -eq '.md') {
                $lines = 0
                try {
                    $lines = (Get-Content -LiteralPath $f -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
                } catch {}
                if ($lines -ge 100) {
                    $validFiles += [PSCustomObject]@{ Path = $f; Size = $fileInfo.Length; Type = 'MD'; Lines = $lines }
                }
            } elseif ($fileInfo.Extension -eq '.docx') {
                if ($fileInfo.Length -gt 20480) {
                    $validFiles += [PSCustomObject]@{ Path = $f; Size = $fileInfo.Length; Type = 'DOCX'; Lines = 'N/A' }
                }
            }
        }
    }
}

$csvPath = "$env:USERPROFILE\.gemini\antigravity\docs_candidates.csv"
$validFiles | Select-Object Path, Size, Type, Lines | Export-Csv $csvPath -NoTypeInformation
Write-Host "Found $($validFiles.Count) files. Saved list to $csvPath"

$validFiles | Sort-Object Size -Descending | Select-Object -First 50 | Format-Table -AutoSize
