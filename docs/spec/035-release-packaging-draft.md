# 035 — 發行包：Linux AppImage、Windows zip、macOS zip

狀態：**DRAFT**（2026-09-27）
日期：2026-09-27
前置：dosgolem 規格 240（音訊）、241（輸入）；本 repo 規格 034（手冊英文列，本機限定）；
參考先例 `/home/anr2/cht/psychic-war/docs/spec/021-packaging.md`（只取架構與驗收方法）。

## 1. 範圍與邊界

把 `buckrogers-play` 連同繁中資料、字型與授權文件打包成玩家解開就能跑的東西。產物一律輸出到被忽略的
`dist-all/`，每個平台只留最新一份。

| 產物 | 內容 |
|---|---|
| `BuckRogersCHT-<版本>-x86_64.AppImage` | 執行檔、`text/`、`font/`、授權文件、讀我 |
| `BuckRogersCHT-<版本>-win64.zip` | `BuckRogersCHT.exe` 與同樣的資料 |
| `BuckRogersCHT-<版本>-macos.zip` | `BuckRogersCHT.app`（universal：x86_64＋arm64） |

- **可散布版不含任何原版檔案**（遊戲檔、手冊掃描、倚天字型、本機手冊英文摘錄）。玩家自備原版，由程式核對雜湊。
- 本機自用變體（使用者曾要求「含原版遊戲」）：`BUCKROGERS_WITH_DATA=1` 時另出 `-with-data` 一份，包內附
  `original/`。**只存在 `dist-all/`，絕不推 git、絕不上傳 Release**；打包腳本在這個模式下拒絕執行任何上傳。
- 字型：GNU Unifont 17.0.05 子集（使用者定案），由正式譯文重建。
- 規格 034 的英文關鍵字列在發行包預設關閉（不附摘錄檔）。

## 2. 證據

- 原版必要檔（已證實，`docs/re/phase-1-input-and-startup.md`）：`START.EXE`
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`、`GAME.OVR`
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。覆繪依賴這兩個檔的位址；其他資料檔以
  內容雜湊辨識字串，不同版本只會少翻譯、不會錯位。
- 存檔目錄（已證實，程式）：`bootroot.Prepare` 要求存檔根不存在或為空，並把原版樹複製進去；遊戲的存檔寫在
  這棵樹內。
- Windows 建置阻礙（已證實，程式）：dosgolem `bootroot/bootroot.go` 與 `session/boot_original.go` 以
  `golang.org/x/sys/unix` 的 `Access` 檢查可寫，Windows 無法編譯。
- 授權：dosgolem 為 RRSAL-1.0，含 LGPL 元件 `audio/nukedopl` 與例外（dosgolem `LICENSE` 第 2 條 (d)）；
  Unifont 字型為 GPL-2.0-or-later（含字型嵌入例外）與 SIL OFL-1.1 雙授權（`COPYING`，已證實）；
  ebiten、oto、purego 為 Apache-2.0，`golang.org/x/*` 為 BSD-3-Clause（各模組 LICENSE，打包時逐一核對）。
  本 repo 尚無 `LICENSE`：公開前必須加上 RRSAL-1.0（使用者既定授權政策）。

## 3. 契約

### 3.1 路徑解析（旗標沒給時）

| 項目 | 依序找，第一個存在的就用 |
|---|---|
| `-text-dir` | 執行檔目錄的 `text/`；macOS `.app` 的 `Contents/Resources/text`；cwd 的 `text/` |
| `-font` | 同上的 `font/buckrogers-unifont.golemfnt` |
| 原版目錄 | 發行包旁的 `original/`（AppImage 取 `$APPIMAGE` 所在目錄；macOS 取 `.app` 所在目錄；Windows 取執行檔目錄）；再找使用者資料目錄下的 `original/` |
| 使用者資料目錄 | Linux `$XDG_DATA_HOME/buckrogers-cht`（未設為 `~/.local/share/buckrogers-cht`）；macOS `~/Library/Application Support/BuckRogersCHT`；Windows `%APPDATA%\BuckRogersCHT` |

- 旗標有給就照給的用；找不到即報錯，不靜默回退。`-exe-sha256` 預設為上列 `START.EXE` 雜湊。

### 3.2 匯入與存檔

- 遊戲樹 = 使用者資料目錄下的 `game/`。
- 第一次啟動（`game/` 不存在）：在原版目錄找 `START.EXE`（大小寫不拘），核對 `START.EXE` 與 `GAME.OVR` 雜湊，
  以 `bootroot.Prepare` 複製到 `game/`。核對失敗即停止並說明是哪個檔、預期與實際雜湊。
- 之後啟動：`game/` 已存在就不再複製，只重核 `game/START.EXE` 與 `game/GAME.OVR` 雜湊後開機；存檔因此保留。
- 截圖目錄預設為使用者資料目錄下的 `screenshots/`。
- 原版目錄只讀；程式不寫入它。

### 3.3 致命錯誤

- 一律同時輸出 stderr、使用者資料目錄的 `buckrogers-error.log`（覆蓋寫，含時間、命令列、訊息），Windows 另跳
  `MessageBoxW`。啟動成功後刪除上一次的錯誤紀錄。`BUCKROGERS_NO_DIALOG=1` 關閉彈窗（供自動驗收）。
- 缺原版的訊息寫明：要自備原版、放到哪裡（照平台給路徑例子）、或以 `-original` 指定。

### 3.4 dosgolem 可攜化

- `unix.Access` 換成跨平台的可寫檢查（build tag：unix 維持 `Access`；Windows 以建立並刪除暫存檔判定）。行為在
  Linux 不變，既有測試照過。

### 3.5 建置

- 一律 Docker：Linux 以 `eob-remake-go:1.26.7-ebiten2.9.9` 原生建置並以 appimagetool 包 AppImage；Windows 以
  `GOOS=windows` 交叉編譯（ebiten 在 Windows 不需 cgo），`-H windowsgui`；macOS 以 osxcross 建 x86_64 與
  arm64 後 `lipo` 合併（skill `osxcross-macos-cross-build`）。
- 字型在打包時以 `tools/catalog_font.py build` 由 `unifont_all-17.0.05.hex.gz`（SHA-256 核對）重建。
- 版本字串 `git describe --tags --always --dirty`，以 `-ldflags -X` 打進執行檔，`-version` 印出，並列出 dosgolem
  commit。
- 包內文件：`LICENSE`（本 repo RRSAL-1.0）、`LICENSE-dosgolem`、`COPYING.LGPL` 與 `nukedopl-SOURCE.md`、
  `font/OFL-1.1.txt` 與 `font/COPYING-unifont`、`THIRD-PARTY.md`（各 Go 模組授權與版本）、`讀我.txt`
  （自備原版、放置位置、按鍵、存檔位置、macOS 未簽章的開啟方式、授權摘要、原作權利聲明）。

### 3.6 外洩掃描

- 可散布版打包後，以本機原版目錄的**實際檔名與 SHA-256** 掃描包內每個檔案（AppImage 先解開）；也掃倚天字型
  與手冊摘錄的雜湊。命中即中止並刪除產物。

## 4. 驗收

1. AppImage：解開到空目錄，在另一個 cwd 執行；原版放在 AppImage 旁的 `original/`，`XDG_DATA_HOME` 指到暫存目錄；
   自動模式跑到功能選單截圖，與 repo 建置的執行檔逐位元組相同；`game/` 建立在資料目錄、原版目錄未被寫入。
   第二次啟動不再複製、畫面相同。
2. 反向對照：不放原版 → 結束碼非 0、錯誤紀錄內容可讀；`font/` 改名 → 明確報缺字型。
3. Windows：以 Wine 容器執行 zip 內的 exe，同 1 的自動模式截圖與 Linux 相同；`BUCKROGERS_NO_DIALOG=1` 下缺原版
   立即結束。
4. macOS：`lipo -archs` 為 `x86_64 arm64`，`.app` 結構齊全。沒有 Mac 可實跑，只驗結構，紀錄照實寫。
5. 外洩掃描對三個可散布產物皆為零命中；反向對照：在暫存副本放入一個原版檔，掃描必須中止。
6. 每個包都含 §3.5 的授權文件；`-version` 列出 LGPL 聲明與 dosgolem commit，該 commit 已推到公開分支。

## 5. 不做

- 程式碼簽章與公證、安裝程式、自動更新。
- 在發行包內附手冊英文摘錄或倚天字型。
