# 第二百八十階段：發行包驗收（規格 035）

日期：2026-09-28
工具：`tools/package.sh all`（Docker、`--network none`）；dosgolem 以已推送分支的 commit `git archive` 建置。
驗收產物與原版副本只在 ignored `workplace/pkg-verify/`。

## 產物

| 產物 | 大小 | 內容 |
|---|---|---|
| `BuckRogersCHT-<版本>-x86_64.AppImage` | 約 5.0 MB | 執行檔、`text/`、Unifont 子集、授權文件、讀我、圖示 |
| `BuckRogersCHT-<版本>-win64.zip` | 約 4.4 MB | `BuckRogersCHT.exe`（PE32+、x86-64、GUI 子系統）與同樣資料 |
| `BuckRogersCHT-<版本>-macos.zip` | 約 7.8 MB | `BuckRogersCHT.app`（fat Mach-O，lipo 確認 x86_64＋arm64）、讀我、LICENSE |

連結的 Go 模組 7 個（Apache-2.0 與 BSD 類），授權檔全數找到；另附 Go 執行期、Unifont、LGPL 元件的授權。

## 驗收（規格 035 §4）

| 項目 | 結果 | 等級 |
|---|---|---|
| 1. AppImage 在另一個 cwd 以 `--appimage-extract-and-run` 執行，原版放在 AppImage 旁的 `original/`，`START.EXE`／`GAME.OVR` 改成小寫 | 第一次啟動匯入到 `$XDG_DATA_HOME/buckrogers-cht/game`（91 檔）；自動模式到功能選單的截圖與 repo 建置之執行檔（同字型、同原版）的截圖逐位元組相同 | 已證實 |
| 1. 第二次啟動 | 放進 `game/` 的標記檔保留；移走 `original/` 仍可啟動；截圖與第一次相同 | 已證實 |
| 2. 中斷與竄改 | 殘留的 `game.importing-1`、`game.importing-2` 在啟動時清除；竄改 `game/game.ovr` 一個位元組，啟動失敗並指向 `game/` 與「刪除後重新匯入」 | 已證實 |
| 3. 反向對照 | 缺原版：結束碼 1，錯誤紀錄列出找過的位置；缺字型：結束碼 1，訊息指出缺 `font/buckrogers-unifont.golemfnt`；成功啟動後舊錯誤紀錄被刪除 | 已證實 |
| 4. Windows（Wine 9.0） | 原版放在 exe 旁，`%APPDATA%\BuckRogersCHT\game` 建立；截圖與參照逐位元組相同；缺原版結束碼 1 | 已證實（Wine，非實機 Windows） |
| 5. macOS | zip 結構、Info.plist、icns、執行位元齊全；沒有 Mac 可實跑 | 只驗結構 |
| 6. 外洩掃描 | 三個產物（AppImage 以 `unsquashfs -o 944632` 解開）對原版樹、倚天來源與本機產物、手冊摘錄零命中；反向對照：放入改名的原版檔，掃描以檔案雜湊命中並中止 | 已證實 |
| 7. `-version` | 印出版本、dosgolem commit 與 Nuked OPL3 的 LGPL 聲明 | 已證實 |

## 過程中修正

Wine 驗收發現：原版與使用者資料目錄在不同磁碟機時，`bootroot` 的巢狀檢查呼叫 `filepath.Rel` 會失敗。dosgolem
`233256a` 讓不同磁碟機直接視為分離。

## 未涵蓋

- 實機 Windows、macOS 的執行與音訊輸出；Windows 的錯誤對話框（`MessageBoxW`）未在 Wine 下截圖驗證。
