# 第一百四十四階段：第三頁五行覆繪的雙倍率同狀態驗收

日期：2026-09-22
狀態：**CONFORMED 僅限第三頁五行與已量 page3→page4 Enter 離頁；不是完整開機、存讀檔或全遊戲中文化。**

## 輸入、工具與權利

起點是私有第二頁合法終態 `workplace/phase104-post-return-enter-2/control.state`，
SHA-256 `b15abdf487f59d982657d1d097c0b38fe3668ca3fd6d15e49c310a5486e238e2`。
原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`
只讀掛載於 `/orig`。control、2×、3×皆於 step `291000000` 排入同一筆正常 BIOS
Enter，穩定畫面停止於 `300000000`；離頁三組另於 `301000000` 排入同一筆 Enter，
停止於 `310000000`。未注入座標、跳頁或改寫原版狀態。

本機 dosgolem branch `buck-rogers-cht-output-overlay` commit `9a9b769`、
Go 1.26.7／`golang:1.26.7-bookworm` Docker；`cmd/buckrogers-text-receipt` 與
`cmd/state-compare` 均從該版重建。20 份現行繁中 TSV 的本機倚天 top-pad
GOLEMFNT SHA-256 `b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。
原版、字型、state、PNG、RGBA、完整收據都留在 ignored
`workplace/phase144-page3-final/` 或既有 ignored 輸入目錄，不進 Git／GitHub／公開包。
所有原版位址均為 dosgolem 實模式 `segment:offset`。

## 穩定第三頁 control／2×／3×

私有 `control/receipt.json`、`2x/receipt.json`、`3x/receipt.json` 的 SHA-256 依序為
`9b41d79d6c3681df3bb5d2688d654fc954954582bbd58da36b69c47a87c79111`、
`2c2b182c44b57c12ab392aaa061bb4318bc1f5cdb0804849e72166126bccf663`、
`4b2653a929f73776c4274d2630fc79f54264764da187aed92c0528adde5986ec`。
兩倍率皆完整啟用 `.001`–`.005` 五 key，`drew=true`、缺字 0；原版右側人名、
row 24 與安全矩形外沒有覆繪差異。2×／3×的 `[8,320)×[136,176)` 內
分別有 9647／20941 個像素差，外部均為 0；兩張真實 PNG 的繁中五行可讀。

唯讀 `tools/story_page3_ab_verify.py` 移除唯一 output-only 的
`story_page3_overlay`／`story_page3_invalidations` 後，逐欄比對 control 與雙倍率
原版 JSON 全等，包含 BIOS 排程、檔案操作、未實作服務及 memory／indexed／palette
摘要。三組 memory SHA-256 均為
`7891aa0b7a23b04ce93cb8e2dfdfe492973dfdd80e108d9b95fd87d3c98a20e8`，
indexed 均為
`9bb708331258b5239c1bfd7b299c0594c4be4475b0523b07c40387790db3958c`。
`cmd/state-compare` control→2×及 control→3×均 `equal=true`，完整 machine digest
`35a43a9b094283fb40267de4562762ae0732baf6f98b446c6a06291afcf79eaa`、
DOS digest `8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。

## 已量 Enter 離頁與失敗即關閉

`exitcontrol/receipt.json`、`exit2x/receipt.json`、`exit3x/receipt.json` 的 SHA-256
依序為
`592b873a711f6b89660e22059af8b5b37c52c2e8ef33f31748ab32524f1cf5a1`、
`234f2d4bd4178b5a2b6dfdb1aed9ab6793f452983886c822ec08aa0696c81eae`、
`af7da277fee42325cba4880a2078c6d8ef64e92cd993c78ce258d53aa818c4fb`。
2×／3×均在原版 step `301108549`、`0CF4:1B3A`、`ES:DI=A000:AA08`、
`CX=304` 的執行前安全矩形交集處記錄 `active_keys_before=5`，立即清空 watcher
及 presenter。終態 active 空、`drew=false`、覆繪 RGBA 與 baseline 逐 byte 相同，
內外差異皆 0；沒有第三頁殘字。移除 output-only 欄位後，兩倍率原版 JSON
與 control 全等。完整 machine／DOS state 各自 `equal=true`；離頁 machine digest
`961639c34e16aacc97eacdc6dd984609e784439a5b5be14f9167551a73f20e63`，
DOS digest 與穩定畫面相同。

正式 loader 只接受五個已審核 READY key／順序／長度／SHA-256／caller／guard／樣式。
原版 144 個 glyph 的七個 ABI word 高位遮罩全為 0；watcher 在截成 8 位前拒絕
任何高位，七欄均有負例。雙倍率測試另涵蓋完整一行才觸發的 SHA mismatch、
partial、錯序、caller／guard／style、真實 return caller／相對 SS/SP、font miss、
non-READY TSV、unknown write、restore／discontinuity 與已量 pre-write 清除，
均不得產生部分中文。Docker 中相關 Go 套件的 `go vet`、`go test -race -count=1`
及專案 234 項 Python 測試通過。

此結論只覆蓋上述合法 state、第三頁五行、雙倍率與已量 Enter 離頁；其他離頁、
完整開機玩家路徑、遊戲內存讀檔、第四頁以後及整款遊戲仍未驗。
