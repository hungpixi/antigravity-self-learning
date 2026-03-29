---
name: Antigravity CDP Port Fix
description: Auto-fix lỗi "Multi Purpose Agent could not connect to CDP port 9004" trên Antigravity IDE. Triggers khi gặp lỗi CDP connection, port 9004, hoặc MPA không kết nối được browser. Script PowerShell tự sửa shortcut thêm flag --remote-debugging-port=9004.
---

# ⚡ Antigravity CDP Port Fix

> Giải quyết lỗi kinh điển: **"Multi Purpose Agent could not connect to CDP port 9004"**

## Nguyên nhân gốc

Antigravity IDE (Electron-based) cần flag `--remote-debugging-port=9004` để Multi Purpose Agent kết nối qua Chrome DevTools Protocol (CDP). Mỗi khi app update, nó **ghi đè shortcut** và xóa mất flag này.

## Triệu chứng

- Dialog box: "Multi Purpose Agent could not connect to CDP port 9004"
- MPA không thể tương tác với browser
- Lỗi xuất hiện lại sau mỗi lần Antigravity tự update

## Fix nhanh (1 lần)

Khi gặp lỗi, chạy ngay:

```powershell
# Bước 1: Kill zombie browser processes (nếu có)
Get-Process -Name "chrome","msedge","chromium" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*9004*" } | Stop-Process -Force

# Bước 2: Fix shortcut Antigravity
$shell = New-Object -ComObject WScript.Shell
$flag = "--remote-debugging-port=9004"
@(
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Antigravity\Antigravity.lnk",
    "$env:USERPROFILE\Desktop\Antigravity.lnk",
    "$env:PUBLIC\Desktop\Antigravity.lnk"
) | ForEach-Object {
    if (Test-Path $_) {
        $lnk = $shell.CreateShortcut($_)
        if ($lnk.TargetPath -like "*Antigravity*" -and $lnk.Arguments -notlike "*$flag*") {
            $lnk.Arguments = if ($lnk.Arguments) { "$($lnk.Arguments) $flag" } else { $flag }
            $lnk.Save()
            Write-Host "Fixed: $_"
        }
    }
}

# Bước 3: Restart Antigravity từ shortcut đã fix
```

## Fix vĩnh viễn (auto-fix mỗi lần khởi động)

Dùng repo tool: [hungpixi/antigravity-cdp-fix](https://github.com/hungpixi/antigravity-cdp-fix)

```powershell
git clone https://github.com/hungpixi/antigravity-cdp-fix.git
cd antigravity-cdp-fix
powershell -ExecutionPolicy Bypass -File fix-cdp-shortcut.ps1 -Install -Verbose
```

Script sẽ:
1. Fix tất cả shortcut Antigravity (Desktop, Start Menu, Taskbar)
2. Tự thêm vào Windows Startup → chạy silent mỗi lần login
3. Ghi log vào `cdp-fix.log` để debug

## Gỡ cài đặt

```powershell
powershell -ExecutionPolicy Bypass -File fix-cdp-shortcut.ps1 -Uninstall
```

## Liên quan

- Bug Pattern: P24 trong `bug-fix-patterns/SKILL.md` (Playwright CDP Browser Process Leak)
- Áp dụng cho: Mọi Electron-based IDE cần CDP flag (Cursor, Windsurf, v.v.)

## Khi AI phát hiện lỗi này

Khi user gặp lỗi CDP port, AI nên:

1. **Kiểm tra port**: `netstat -ano | findstr ":9004"` → nếu có process chiếm → kill
2. **Kiểm tra shortcut**: Chạy script fix-cdp-shortcut.ps1
3. **Gợi ý install vĩnh viễn** nếu user chưa cài
4. **Restart Antigravity** từ shortcut đã fix
