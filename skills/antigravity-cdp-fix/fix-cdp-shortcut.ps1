# ============================================================
# Antigravity CDP Auto-Fix Script
# ============================================================
# Giải quyết lỗi: "Multi Purpose Agent could not connect to CDP port 9004"
# Script tự động thêm --remote-debugging-port=9004 vào shortcut Antigravity
# Chạy mỗi khi Windows khởi động để đảm bảo flag không bị mất sau update
#
# Author: hungpixi (https://github.com/hungpixi)
# Website: https://comarai.com
# ============================================================

param(
    [int]$Port = 9004,
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Verbose
)

$ErrorActionPreference = "SilentlyContinue"

# ---- Hàm tiện ích ----
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "[$timestamp] [$Level] $Message"
    if ($Verbose -or $Level -eq "ERROR") {
        Write-Host $logLine
    }
    # Ghi log vào file
    $logFile = Join-Path $PSScriptRoot "cdp-fix.log"
    Add-Content -Path $logFile -Value $logLine -ErrorAction SilentlyContinue
}

function Get-AntigravityPath {
    $paths = @(
        "$env:LOCALAPPDATA\Programs\Antigravity\Antigravity.exe",
        "$env:ProgramFiles\Antigravity\Antigravity.exe",
        "${env:ProgramFiles(x86)}\Antigravity\Antigravity.exe"
    )
    foreach ($p in $paths) {
        if (Test-Path $p) { return $p }
    }
    return $null
}

# ---- Fix Shortcut ----
function Fix-Shortcuts {
    param([int]$Port)
    
    $shell = New-Object -ComObject WScript.Shell
    $flag = "--remote-debugging-port=$Port"
    $fixed = 0
    $checked = 0

    # Tìm tất cả shortcut Antigravity
    $shortcutPaths = @(
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Antigravity\Antigravity.lnk",
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Antigravity Tools.lnk",
        "$env:USERPROFILE\Desktop\Antigravity.lnk",
        "$env:PUBLIC\Desktop\Antigravity.lnk"
    )

    # Tìm thêm shortcut trên taskbar
    $taskbarPath = "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar"
    if (Test-Path $taskbarPath) {
        Get-ChildItem $taskbarPath -Filter "*Antigravity*" | ForEach-Object {
            $shortcutPaths += $_.FullName
        }
    }

    foreach ($path in $shortcutPaths) {
        if (Test-Path $path) {
            $checked++
            $lnk = $shell.CreateShortcut($path)
            
            # Chỉ fix shortcut trỏ đến Antigravity.exe
            if ($lnk.TargetPath -like "*Antigravity*") {
                if ($lnk.Arguments -notlike "*$flag*") {
                    # Giữ lại các argument cũ, thêm flag mới
                    if ($lnk.Arguments) {
                        $lnk.Arguments = "$($lnk.Arguments) $flag"
                    } else {
                        $lnk.Arguments = $flag
                    }
                    $lnk.Save()
                    $fixed++
                    Write-Log "Fixed: $path" "INFO"
                } else {
                    Write-Log "OK: $path (already has CDP flag)" "INFO"
                }
            }
        }
    }

    Write-Log "Checked $checked shortcuts, fixed $fixed" "INFO"
    return $fixed
}

# ---- Install: Thêm vào Startup ----
function Install-StartupTask {
    $shell = New-Object -ComObject WScript.Shell
    $startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    $lnkPath = Join-Path $startupPath "FixAntigravityCDP.lnk"
    
    $lnk = $shell.CreateShortcut($lnkPath)
    $lnk.TargetPath = "powershell.exe"
    $lnk.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    $lnk.WorkingDirectory = $PSScriptRoot
    $lnk.WindowStyle = 7  # Minimized
    $lnk.Save()
    
    Write-Host "Installed to Startup: $lnkPath" -ForegroundColor Green
    Write-Host "Script will run automatically on every Windows login." -ForegroundColor Cyan
}

# ---- Uninstall: Xóa khỏi Startup ----
function Uninstall-StartupTask {
    $lnkPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\FixAntigravityCDP.lnk"
    if (Test-Path $lnkPath) {
        Remove-Item $lnkPath -Force
        Write-Host "Removed from Startup." -ForegroundColor Yellow
    } else {
        Write-Host "Not found in Startup." -ForegroundColor Gray
    }
}

# ---- Main ----
Write-Log "=== Antigravity CDP Fix Started ===" "INFO"

if ($Install) {
    Install-StartupTask
    Fix-Shortcuts -Port $Port
    Write-Host ""
    Write-Host "Setup complete! Antigravity will always launch with CDP port $Port." -ForegroundColor Green
}
elseif ($Uninstall) {
    Uninstall-StartupTask
}
else {
    # Mode mặc định: chỉ fix shortcut (chạy silent khi startup)
    $result = Fix-Shortcuts -Port $Port
    if ($result -gt 0 -and -not $Verbose) {
        # Hiện notification nếu có fix gì đó (optional)
        Write-Log "Fixed $result shortcut(s) after Antigravity update" "INFO"
    }
}

Write-Log "=== Antigravity CDP Fix Completed ===" "INFO"
