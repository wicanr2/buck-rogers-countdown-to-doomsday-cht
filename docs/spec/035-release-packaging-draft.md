# 035 — 發行包：Linux AppImage、Windows zip、macOS zip

狀態：**READY**（2026-09-28，兩輪獨立審查後）
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

- **發行包不含任何原版檔案**（遊戲檔、手冊掃描、倚天字型、本機手冊英文摘錄）。玩家自備原版，由程式核對雜湊
  （2026-09-27 定案；本規格不做含原版的變體）。
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
  本 repo 的 `LICENSE`（RRSAL-1.0）已於 `c2c8d79` 進版控。

## 3. 契約

### 3.1 路徑解析（旗標沒給時）

| 項目 | 依序找，第一個存在的就用 |
|---|---|
| `-text-dir` | 執行檔目錄的 `text/`；macOS `.app` 的 `Contents/Resources/text`；cwd 的 `text/` |
| `-font` | 同上的 `font/buckrogers-unifont.golemfnt` |
| 原版目錄 | 發行包旁的 `original/`（AppImage 取 `$APPIMAGE` 所在目錄；macOS 取 `.app` 所在目錄；Windows 取執行檔目錄）；再找使用者資料目錄下的 `original/`；只在第一次匯入時需要 |
| 使用者資料目錄 | Linux `$XDG_DATA_HOME/buckrogers-cht`（未設為 `~/.local/share/buckrogers-cht`）；macOS `~/Library/Application Support/BuckRogersCHT`；Windows `%APPDATA%\BuckRogersCHT` |

- 旗標有給就照給的用；找不到即報錯，不靜默回退。`-exe-sha256` 預設為上列 `START.EXE` 雜湊。

### 3.2 匯入與存檔

- 遊戲樹 = 使用者資料目錄下的 `game/`。匯入與核對都在 `cmd/buckrogers-play`，不改 `bootroot.Prepare` 的契約
  （存檔根須不存在或為空）。
- 主機端查找（大小寫不拘）：列出原版目錄的直接項目，以 `strings.EqualFold` 找 `START.EXE` 與 `GAME.OVR`；各須恰好
  一個一般檔（同名不同大小寫出現兩個以上即報錯）。之後一律使用實際找到的檔名：`bootroot.RequiredFile.Name`、
  讀回執行檔與核對都用它。遊戲內的 DOS 檔案層本來就大小寫不拘，不受影響。
- 第一次啟動（`game/` 不存在）：
  1. 刪除上次殘留的 `game.importing-*` 目錄（中斷的匯入）。不支援同時開兩個程式做首次匯入。
  2. 以 `bootroot.Prepare` 把原版複製到新的 `game.importing-<pid>`，同時核對兩個必要檔雜湊。
  3. 成功後 `os.Rename` 成 `game/`。行程在 1–3 之間被中止，只會留下 `game.importing-*`，下次啟動清掉重來；
     `game/` 只會以完整狀態出現。
  4. 核對失敗即停止，訊息寫明哪個檔、預期與實際 SHA-256。
- 之後啟動（`game/` 存在）：不呼叫 `Prepare`；讀 `game/` 內兩個必要檔（同樣大小寫不拘）核對雜湊後，以 `game/`
  當 `BootInput.SaveRoot` 開機。存檔因此保留。核對失敗時訊息說明 `game/` 位置與「刪除後重新匯入」。
- 旗標 `-original` 與 `-save` 仍可用（開發與驗收）；給了 `-save` 就照現行行為（新的空目錄、每次 `Prepare`）。
- 截圖目錄預設為使用者資料目錄下的 `screenshots/`。原版目錄只讀；程式不寫入它。

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
- 字型在打包時以 `tools/catalog_font.py build` 由 `unifont_all-17.0.05.hex.gz`（SHA-256
  `7b182454966046d35482469b979edce7d262fab5c53c2180e9b1fbb5d0b5e574`；官方 tarball `f287cffb26e22723aa36e6684869b0f3ff3bfb822c4b01008bd847911ec1b631`）重建；
  `font/README.md` 記錄定案與授權。
- 版本：`cmd/buckrogers-play` 新增 `var version, dosgolemCommit string`，打包時以
  `-ldflags "-X main.version=<本 repo git describe --tags --always --dirty> -X main.dosgolemCommit=<dosgolem HEAD>"`
  注入；`-version` 在既有授權聲明之前印出兩者（未注入時印 `dev`／`unknown`）。
- 映像：Linux 與 Windows 用 `eob-remake-go:1.26.7-ebiten2.9.9`；macOS 以本 repo `tools/docker/osxcross.Dockerfile`
  建 `buckrogers-osxcross`：`FROM eob-remake-go:1.26.7-ebiten2.9.9 AS gobase`、`FROM psychicwar-osxcross`，
  `COPY --from=gobase /usr/local/go /usr/local/go`，三個平台同一版 Go（1.26.7）。兩個來源映像都已在本機，
  建置不需網路；只讀取、不修改或清理它們。AppImage 以 `psychicwar-appimage` 的 `mksquashfs` 與 type2 runtime 串接。
- 包內文件：`LICENSE`（本 repo RRSAL-1.0）、`LICENSE-dosgolem`、`COPYING.LGPL` 與 `nukedopl-SOURCE.md`、
  `font/OFL-1.1.txt` 與 `font/COPYING-unifont`、`THIRD-PARTY.md`（各 Go 模組授權與版本）、`讀我.txt`
  （自備原版、放置位置、按鍵、存檔位置、macOS 未簽章的開啟方式、授權摘要、原作權利聲明）。
- `THIRD-PARTY.md` 由 `go version -m <執行檔>` 列出實際連結的模組，逐一附上模組快取內的 LICENSE 檔名與類型；
  連結的模組缺 LICENSE 即中止。

### 3.6 外洩掃描

- 打包後，以本機原版目錄的**實際檔名（大小寫不拘）與 SHA-256** 掃描包內每個檔案；也掃倚天字型、倚天來源檔與
  手冊摘錄的雜湊。命中即中止並刪除產物。
- 解開方式：AppImage 以 `unsquashfs -o <runtime 大小>` 從 runtime 之後解出（runtime 由本流程串接，大小已知，
  不需 FUSE）；zip 以 `unzip`。

## 4. 驗收

1. AppImage：以 `--appimage-extract-and-run`（不需 FUSE）在另一個 cwd 執行；原版放在 AppImage 旁的 `original/`
   （檔名改成小寫一次，驗大小寫不拘），`XDG_DATA_HOME` 指到暫存目錄；自動模式跑到功能選單的截圖，與 repo 建置之執行檔的
   截圖逐位元組相同；`game/` 建立在資料目錄、原版目錄未被寫入。第二次啟動不再複製（`game/` 內新增的標記檔
   仍在）、畫面相同。
2. 中斷匯入：預先放一個 `game.importing-1` 殘留目錄，啟動後它被清掉且 `game/` 正常建立。竄改 `game/GAME.OVR`
   一個位元組，啟動失敗且訊息指向 `game/`。
3. 反向對照：不放原版 → 結束碼非 0、錯誤紀錄內容可讀；`font/` 改名 → 明確報缺字型。
4. Windows：以 Wine 容器執行 zip 內的 exe，同 1 的自動模式截圖與 Linux 相同；`BUCKROGERS_NO_DIALOG=1` 下缺原版
   立即結束。
5. macOS：`lipo -archs` 為 `x86_64 arm64`，`.app` 結構齊全。沒有 Mac 可實跑，只驗結構，紀錄照實寫。
6. 外洩掃描對三個可散布產物皆為零命中；反向對照：在暫存副本放入一個原版檔，掃描必須中止。
7. 每個包都含 §3.5 的授權文件；`-version` 列出 LGPL 聲明與 dosgolem commit，該 commit 已推到公開分支。

## 5. 不做

- 程式碼簽章與公證、安裝程式、自動更新。
- 建立 GitHub Release、上傳與推廣影片：屬 Issue #32，另行處理。
- 含原版的發行變體。
- 在發行包內附手冊英文摘錄或倚天字型。
