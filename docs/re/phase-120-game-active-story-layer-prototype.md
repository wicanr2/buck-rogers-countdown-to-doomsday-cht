# 第一百二十階段：真實遊戲作用中劇情圖層（active story layer）Ebitengine 原型

日期：2026-09-22
狀態：原型（prototype）；補足 host DRAFT 的窄範圍實機證據，不構成可玩版或完整中文化。

## 範圍與輸入邊界

本階段只把已 READY 的首屏劇情五行，從真實 Buck Rogers 執行期 watcher 的
作用中 `xlate.Layer` 投影到 Linux Ebitengine 視窗。測試由本機合法手冊成功後的
私有 checkpoint `workplace/probe/phase12-before-question.state` 及其既有有界 BIOS
排程開始；排程、答案、原版檔、state、字型 bytes、RGBA、PNG 與完整 receipt 都只留在
被 Git 忽略的 `workplace/`，不進本文件或版本庫。

使用的資料與程式邊界如下：

- READY identity／譯文：`text/story-opening-events.tsv`、
  `text/story-opening.zh-TW.tsv`；僅五個 event key，不擴張至後續頁面。
- 本機 dosgolem 分支的 `42193b0` story watcher 執行期接線，及
  `e2761d9` 作用中圖層 presenter 邊界；watcher 只接受已證實的 `RETF`
  return edge，原版 glyph、答案與判定不會進 host layer。
- `9f6cac6` 修正 host Apply 3×後的輸出層重建：2× 使用 16×16 來源 glyph，3×
  僅在輸出 presenter 使用既有 22×22 CJK 衍生 glyph 與 24-pixel cell 內縮定位。
  此重建只讀取同一作用中 event／palette；不 Step machine、不寫 VRAM、不改 DOS memory、
  BIOS queue、原版輸入、檔案或存檔。

本機倚天字型是使用者已授權的本機輸入；衍生 `GOLEMFNT` 仍不得加入 Git、GitHub 或
公開包。前端字型 registry 以獨立 3× 衍生 font name 綁定實際 stamp pointer，避免將
3× 22×22 glyph 錯配為 2× 16×16 glyph。

## 同一 runtime thread 的投影

在同一 Ebitengine 執行緒內，原型依序執行 machine instruction、runtime watcher／
`onFrame`、`MachineFrameSource`、`LayerSnapshotProvider` 與 Ebitengine Draw。
`LayerSnapshotProvider` 只複製 indexed frame 與作用中 stamp，再在私有 RGBA 輸出上繪製；
它不保留 machine 或 DOS 可寫入口。

當 host 的已確認 Apply 事件將 active scale 從 2× 改成 3×時，原型只重建 story
輸出 presenter 與不可變 projection。Cancel 不重建：selected 回到 active 2×，現有 2×
作用中 layer 保持。這正是使用者確認的「未套用即取消」語意，不是原版遊戲輸入。

## 真實畫面與逐像素對照

Docker／Xvfb 以既有 `eob-remake-go:1.26.7-ebiten2.9.9`、無網路執行 ignored
`workplace/phase118-game-ebiten-active-story/`。前端畫面的圖層來自上述真實 state 的
watcher，非合成 fixture。下列是內容安全（content-safe）receipt 結果：

| 項目 | 結果 |
| --- | --- |
| `game_loaded`／`real_story_watcher`／`active_layer_connected` | `true`／`true`／`true` |
| active keys／缺字 | 5／0 |
| 初始 2×、暫選 3×後 Cancel | 仍為 active 2×，且與 phase115 CLI 2× RGBA 逐像素相同 |
| Apply 3×後自動收合 | 3×作用中 layer 與 phase115 CLI 3× RGBA 逐像素相同 |
| 面板開啟時 BIOS key | queue 不變 |
| 面板關閉後明示 BIOS key | 允許送入 queue |
| host 操作前／後 raw indexed SHA-256 | 同為 `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba` |

逐像素比較使用 phase115 同 state CLI 的 private RGBA receipt，而非僅比 PNG：

| 輸出倍率 | Ebitengine RGBA 與 CLI | RGBA SHA-256 | 私有 Ebitengine PNG SHA-256 |
| --- | --- | --- | --- |
| 2×（host 操作前） | 相同 | `35fcdbb0eb45cde3ec67db839ff165fc48cfdcfff2998e22104ec1f940666e91` | `c43ca22e988fc0fb27332cdb428765a5a386ad89f3ac2c8263716f778d03b65a` |
| 2×（Cancel 後） | 相同 | `35fcdbb0eb45cde3ec67db839ff165fc48cfdcfff2998e22104ec1f940666e91` | 同上 |
| 3×（Apply 後） | 相同 | `bebcfb0e7508280966915deec66d8a58c1cd6332f764638d6afe399f64689960` | `559a2bab9a24fb2b176567022709e37a90b27a3437b94d45bf19b560e306c7fe` |

人工檢視私有 2×與 3× PNG：2×維持既有密度；3× CJK 為較大的 22×22 glyph，字距與
phase115 CLI 圖一致，未再出現把稀疏 16×16 glyph 直接三倍放大的情形。

Docker 驗證通過 `go test -race ./apps/buckrogers ./presentation`、`go vet
./apps/buckrogers ./presentation` 與 prototype `go test ./...`。本輪的 Docker container 已
以 `--rm` 移除；檢查未發現本專案 root-owned 檔案或誤建 `.md` 目錄。

## 仍未完成，不能外推

這個收據只證明指定私有 state 的五行 story 作用中 layer 與 host scale state 可在真實
Ebitengine loop 正確投影。它沒有完成或驗收：

- 正式 Ebitengine host chrome、pointer hit test、實體鍵盤到 DOS scan／BIOS key 映射，及
  未命中 pointer 的 DOS mouse forwarding 決定；本階段使用的是受控的 `PanelController`
  直接事件呼叫，不能冒稱玩家已能操作視窗。
- 從遊戲開機一路正常進入此 state、host 操作之後繼續遊玩、存檔／讀檔，以及其他 overlay
  的同一套倍率切換（scale-switch）presenter lifecycle。
- 首屏以外的劇情、第二／第三／第四頁、手冊所有題目與其他玩家可見文字路徑。

因此 `docs/spec/004-dosgolem-host-frontend-draft.md` 保持 DRAFT，這不是 Linux 可玩版，
也不能以本階段聲稱整款遊戲或首屏劇情已完整中文化。
