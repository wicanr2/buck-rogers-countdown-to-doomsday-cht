# 第二百九十七階段：多語前端（規格 040 第二段）

日期：2026-09-30
狀態：定稿（主代理審閱，2026-09-30）；實作 dosgolem `9c6abb1`
規格：`docs/spec/040-multilang-framework-draft.md`（READY）§3.4、§5 的前端部分。
程式：dosgolem fork `workplace/dosgolem`（分支 buck-rogers-cht-output-overlay，HEAD `d685efd`，未提交修改）；
同步副本 `workplace/dosgolem-clean`（`sync.sh`，原檔備份在 `clean-backup/`）。
工具：`buckrogers-play` 自動模式，`eob-remake-go:1.26.7-ebiten2.9.9` 內 Xvfb，2×，`-save /tmp/save`（容器內），冷開機。

## 改動

| 檔案 | 內容 |
|---|---|
| `cmd/buckrogers-play/input.go` | `F4` 加入前端保留鍵（`actLang`）；腳本新增 `lang` 動作；腳本鍵名 `F4` 仍送 BIOS |
| `cmd/buckrogers-play/lang.go`（新） | 設定檔 `settings.json` 讀寫（暫存檔再改名）、起始語言優先序、說明頁語言列（`{lang}`、`{off}` 樣板） |
| `cmd/buckrogers-play/main.go` | `-lang`；`LoadLiveRuntimeOptions`（試載 zh-CN、ja、ko）；F4／`lang` 呼叫 `NextLanguage`＋`SetLanguage`，互動模式寫設定檔；視窗標題「拯救地球」；說明頁代入語言列；自動模式結束輸出 `memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256`，以及目前語言合成與原版放大畫面的雜湊；自動模式也印 fps |
| `cmd/buckrogers-play/launcher.go` | zh-TW 字型依序找 `buckrogers-eten-top-pad` → `buckrogers-zh-TW` → `buckrogers-unifont`；其他語言用 `LangFontPath`；錯誤對話框標題改用視窗標題 |
| `cmd/buckrogers-play/input_test.go`、`lang_test.go`（新） | 見下節 |
| 主 repo `text/host-ui.zh-TW.tsv` | `help.04` 加「F4 切換語言」、`help.10` 改「F5 到 F10」；新增 `help.14`（目前語言樣板）、`help.15`（未啟用樣板）、`lang.<代碼>` 五個語言名、`lang.off.files／font／load` 三種原因摘要，source 皆 `frontend-help` |
| 主 repo `font/characters.txt` | `tools/catalog_font.py chars text/*.zh-TW.tsv` 重生，只多「韓」（U+97D3）；SHA-256 `6a19054e9027afc82120d10b80d9440801bb2bed1476b903c7877c9c0fcecdad` |
| 主 repo `docs/release/讀我.txt` | F4 語言切換、F5–F10 照原版、英文模式與手札翻頁、設定檔與 `-lang` |

`apps/buckrogers` 未改。

說明頁未啟用列把同一原因的語言併成一組，例如「未啟用：簡體中文、日文、韓文（缺語言檔）」；全部啟用時不顯示這列。
完整原因（缺哪個檔）只寫 stderr。語言名稱缺字模時改顯示代碼並在 stderr 記一筆，不讓啟動失敗。

## 測試

| 項目 | 結果 | 收據 |
|---|---|---|
| `go test ./...`（dosgolem-clean，ebiten image，cgo 可建，`BUCKROGERS_CHT_ROOT` 唯讀掛主 repo） | 31 套件 ok，含 `cmd/buckrogers-play`、`frontend/ebiten` | `test-all.txt` |
| `cmd/buckrogers-play` 單元測試 | 21 項通過：F4 只產生語言動作、按住不連發、說明頁開啟仍可切換、F5／F10 照送；`lang` 腳本動作與腳本 `F4` 送 BIOS；優先序（含 `-lang` 已知未啟用不退回設定檔、設定檔不認得與 zz 退 zh-TW）；設定檔讀寫、壞 JSON、目錄、寫入失敗不留暫存檔；自動與開發模式不讀不寫；說明頁樣板代入、分組、截斷 38 格；正式 host-ui 代入後每列 ≤38 格、≤15 列；不認得的 `-lang` 結束碼 2 | `test-play.txt`、`test-final.txt` |
| `GOOS=windows CGO_ENABLED=0 go build ./...` | 通過 | `build-windows.txt` |
| `gofmt -l`、`go vet ./cmd/buckrogers-play` | 無輸出 | — |
| `tools/catalog_font.py lint text/host-ui.zh-TW.tsv`；tools 全部 Python 單元測試 | 通過；297 項 OK | `py-after.txt` |

## 前端實跑（冷開機 1500 畫格，停在標題畫面「播放(P) 示範(D)」）

| 執行 | 腳本／參數 | 結束語言 | memory／cpu 雜湊 | 合成 SHA-256 | 合成＝原版 |
|---|---|---|---|---|---|
| a0 | 無 | zh-TW | 13fb0226…／c4d05f4a… | fac72614… | 否（有覆繪） |
| b1 | `1300:lang` | en | 相同 | 0dc3ec5d… | 是 |
| b2 | `400,800,1300:lang` | en | 相同 | 0dc3ec5d… | 是 |
| b3 | `400,800,1300,1400:lang` | zh-TW | 相同 | fac72614…（＝a0） | 否 |
| l1 | `-lang en` | en | 相同 | 0dc3ec5d…（＝b1） | 是 |
| l2 | `-lang ja` | zh-TW（stderr：未啟用，改用 zh-TW） | 相同 | fac72614… | 否 |
| l3 | `-lang xx` | 用法錯誤、印 usage 結束 | — | — | — |
| base | 改動前的前端（fork HEAD 原檔建置） | zh-TW | 步數相同 | fac72614…（＝a0） | — |
| h2 | `1450:help` | zh-TW | 319c73aa…／8d0a5394… | — | — |
| h1 | `1300:lang,1450:help` | en | 與 h2 相同 | — | — |

完整雜湊：memory `13fb02261d3c583e0a5ff030549a66661993e7f330e85e8f39730f38cc790ab4`、cpu
`c4d05f4a185bcb4283006bef07ebf391b163e8d81a16f5be7287f06360ef8919`；原版放大畫面
`0dc3ec5ded3d99d5e1feb80a3ec9d2db1d60c0b76a9d989f3268a2883f6e8844`。

結論（已證實，限此路徑）：
- 插入 1、3、4 次 `lang` 與不插入，結束時記憶體與 CPU 雜湊相同；說明頁暫停的兩組（h1／h2）也相同。
- 英文模式的合成逐位元組等於原版 `ScaleIndexedRGBA`（b1、b2、l1）。
- 切回 zh-TW 的畫面等於一開始就用 zh-TW（b3＝a0），也等於改動前的前端（base＝a0）。

截圖：`a0.png`（繁中）、`b1.png`（英文）、`h2.png`（說明頁，目前語言：繁體中文）、`h1.png`（說明頁，目前語言：英文（原版））、
`hu.png`（Unifont 子集）、`hc.png`（`workplace/current-font` 舊倚天字型，缺「韓」改顯示 `ko`）。
本輪截圖只有標題畫面與說明頁，未進入手冊題。

互動模式（Xvfb，無音效裝置，`XDG_DATA_HOME` 指到本目錄 `xdg*/`，12–15 秒後中斷）：
- 設定檔 `{"lang":"en"}` → 起始語言 en；壞 JSON → stderr「讀取設定檔失敗（改用預設）」並用 zh-TW；
  `-lang zh-TW` 蓋過設定檔 en，設定檔未被改寫。
- 容器內沒有 ALSA 裝置，音訊初始化失敗（既有行為，與本輪無關）。互動按 F4 的寫檔路徑只由單元測試涵蓋。

## 效能（`-frames 3000 -clock 50`，4 CPU，各兩次）

| 語言 | fps | user CPU（秒／3000 格） | 每格 user CPU |
|---|---|---|---|
| zh-TW | 59.7、59.7 | 78.0、78.6 | 約 26 ms |
| en（`-lang en`） | 59.6、59.7 | 88.6、86.8 | 約 29 ms |

兩者都貼著 `SetTPS(60)` 上限。前端只載入 zh-TW 一條通道（en 不是通道），所以「zh-TW＋en」量的是兩種合成模式，
不是兩條通道；兩條通道的成本已由 phase-296 用收據工具量（每多一條約 0.87 ms／格）。英文模式 CPU 較高的原因未查
（推測是每次 `Draw` 都新配置 `ScaleIndexedRGBA` 的輸出，未證實）。

## 未量到

- 互動模式實際按 F4 後寫入設定檔、F4 按住不連發的實機手感（單元測試已涵蓋對映）。
- 手札面板開啟時切換語言、英文模式下 PgUp／PgDn 送進原版（規格 040 指定以單元測試驗證，本輪未新增前端實跑）。
- 3× 倍率下的說明頁語言列。
- Windows、macOS 實跑。

## 待決

1. dosgolem `docs/spec/241-buckrogers-play-input-draft.md` §3.3 的保留鍵表要加 F4（規格 040 §3.4 要求同步；本任務未授權改 dosgolem 文件）。
2. 發行包的 zh-TW 字型檔名仍是 `buckrogers-unifont.golemfnt`（`tools/package.sh`）。規格 040 的名稱是
   `buckrogers-zh-TW.golemfnt`；前端兩者都接受。是否改 `package.sh` 待定。
3. `workplace/current-font` 的倚天字型缺「韓」，本機 `play.sh` 的說明頁會顯示 `ko`。打包流程會依現行譯文重建，
   本機要用 `tools/eten_font.py build` 重建（本輪只在本目錄 `font-eten/` 重建驗證，未動 current-font）。
4. `tools/eten_host_font3.py` 要求 host-ui 恰有五個 `host.*` 標籤；`help.*` 加入後就已不成立（既有），本輪的 `lang.*` 列也一樣。
   `frontend/ebiten` 的 host 字型 manifest 釘了 host-ui 的 SHA-256，改檔後要重生（若仍使用該路徑）。
5. 冷開機 DebugSummary 的 `resets=map[skill-exit:2]` 在改動前的前端也出現（base），屬既有狀態，本輪未查原因。

## 檔案

`sync.sh`、`go.sh`、`run.sh`、`png.py`、`changed-files.txt`、`new-files.txt`、`clean-backup/`、`base-src/`（fork HEAD 的前端原檔）、
`buckrogers-play`、`buckrogers-play-base`、`font-uni/`、`font-eten/`（本輪重建的測試字型，不得散布）、`chars/`、
`*.log`（各次執行 stderr）、`*.rgba`／`*.png`、`test-*.txt`、`build-windows.txt`、`py-after.txt`、`xdg*/`（互動模式測試資料目錄，已刪除匯入的原版）。
