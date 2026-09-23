# 第二百零八階段：從第零步啟動的選單繁中視窗原型

日期：2026-09-24
狀態：**DRAFT；單次、被 Git 忽略的冷開機原型，不是可玩前端或同狀態 A/B。**

## 問題與輸入邊界

[第一百八十五階段](phase-185-ebiten-real-active-layer-router-draft.md)的真實繁中
Ebitengine 視窗仍從私有 checkpoint 起跑。本次原型改從本機原版
`START.EXE` 第 0 步啟動，在第一步前建立選單 watcher 與覆繪器；原版
目錄唯讀掛載，存檔 scratch 另掛可寫目錄。原版 EXE SHA-256 為
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。
這個雜湊是輸入版本釘選，不公開 EXE bytes、文字或畫面。

被 Git 忽略的原型位於 `workplace/cold-boot-frontend-proto/`；`main.go`
SHA-256 `0d62aa80417fc7b695d78113846828b61700c85e51939f2d14f797c96116b730`，
`go.mod` SHA-256 `fe0b0027d579048e2d02413b0978b7bfa3043ed36cc8cd66b0ce55a66a62ba13`，
`go.sum` SHA-256 `9de58f3cc583c84942a951a180b804539fe77ae6e2b827e825e4e1dae44976c1`。
本機 dosgolem fork 為 `674e3e3fcbf8e36d5ac115da9e9b5bf685564339`；
Go 1.26.7、Ebitengine 2.9.9，沿用 `eob-remake-go:1.26.7-ebiten2.9.9`。
位址採原型內 dosgolem 的 `segment:offset`，只沿用既有已量的選單 watcher
入口與清除入口，不在此檔重新宣稱逆向結論。

Docker 工作使用 `timeout 300s docker run --rm --network none --memory 2g
--cpus 2 --pids-limit 256`、目前 UID/GID、專案唯讀掛載及獨立可寫
`out/`／`scratch/`，以有 trap 的 Xvfb :99 執行 `go run -mod=mod .`。
掛載前已驗各來源存在且形態正確。私有收據
`workplace/cold-boot-frontend-proto/out/receipt.json` SHA-256
`d5cc466a909515d006f11da2f8031ae0268680fba9742974107d4d035dd5942b`；
只保存步數、key、雜湊與其他統計，不含原版文字或像素。

## 觀測與限縮結論

- watcher 的安裝標記在 `Machine.Steps=0`；第 71,000,000 步排入既有
  空白鍵輸入，首筆可辨識選單 request 於第 71,122,931 步出現。
- 有界跑到 100,000,000 步：watcher request 7 筆，終態作用中 key 6 筆，
  watcher drops 0、misses 24。`misses` 不是「已翻譯」；其他印字路徑仍未由
  此收據覆蓋。
- 終態原版 indexed SHA-256
  `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`，
  與既有第一階段基線吻合；2×覆繪 RGBA SHA-256
  `1b4ba7ef88995f57ad9280d743d2733758111434bcf9ee4c5c5b4b2bd860a611`。
  覆繪相對同一終態原版畫面相差 20,541 個 RGBA byte，缺字 0。
- Ebitengine／Xvfb 顯示該**已算好的終態靜態影格**三次；它沒有在視窗回合
  持續推進 DOS，也未處理玩家鍵盤、滑鼠或設定面板。因此只證從原版
  第零步能到已量選單並將繁中終態交給視窗繪製，不能稱可玩版。

代理執行後，主代理以唯讀 Docker 獨立核對上述來源／收據 SHA-256、
數值欄位與輸出目錄 UID/GID；**沒有**第二次重跑 1 億步，也沒有檢視
原版 PNG。原版資料及字型產物均未加入 Git。

## 下一閘門

仍須規格 [019](../spec/019-linux-frontend-session-turn-boundary-draft.md) 的
正式 typed session、真實 machine step receipt、失敗後 Close，及
[規格 004](../spec/004-dosgolem-host-frontend-draft.md) 的 live host 回合、
2×／3×、所有預定作用層、正常玩家輸入、退出／存讀檔與同狀態 A/B。
本原型不使規格 004／019 READY 或 CONFORMED；Issue #16／#18 保持開啟。
