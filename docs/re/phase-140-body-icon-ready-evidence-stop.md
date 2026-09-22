# 第一百四十階段：身體圖示 READY 前置證據停止線

狀態：DRAFT；未接 runtime，未升 READY。

本筆是對既有[第四十八階段](phase-48-body-icon-selection-lifecycle.md)與
`text/body-icon-events.tsv` 的證據稽核，**沒有產生新的原版重播收據**。引用的原版
`GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
下列 `segment:offset` 是 dosgolem 實模式位址，不是 IDA 線性位址。Phase 48 文件
沒有列出起始 state 檔名／雜湊與工具 commit；因此本筆不能取代正式重跑的完整 provenance，
這也是 READY 前需要補的條件。

## 已回查事實

Phase 48 的正常 BIOS 重播已可決定重生身體圖示畫面及其 Enter→N、Enter→Y 分支。正式 identity 對應的四個固定圖示文字 caller 為 `1C41:2708`、`1C41:2729`、`1C41:274A`、`1C41:276B`；其原始長度、SHA-256、色彩與格座標已由 `text/body-icon-events.tsv` 鎖定。確認與儲存詢問則是 `37F1:101E`。

這些僅證實高階 dispatcher 的 completed event，**不**證實低階 `0763:026B` glyph 的 return edge；不得把既有 event 的 `post_call_step` 當成 glyph return 收據。

## READY 前的最小剩餘量測

同一個 phase-48 正常玩家輸入排程至少要各雙重重播移動、Enter→N、Enter→Y 三條分支，並記錄：

- 每一筆四 caller 的 glyph entry、實際 `RETF imm16` 前一指令、返回 CS:IP、entry／return SS 與 SP 差；
- 每條 active body-icon、confirmation、save-prompt stamp 的轉場中，最早與該 stamp 安全矩形相交的原版 pre-write；
- 兩次收據的 content-safe metadata 與終態 indexed framebuffer 相同。

未同時取得上述兩類原版收據前，唯一安全策略是整組失效；這不是可升 READY 的專用清除契約，也不得接 production watcher。

## 本輪探針停止線與可用工具鏈訂正

本輪只嘗試在 Docker 的暫存 dosgolem 副本擴大既有 glyph-return trace 篩選；候選既有映像 `golang:1.24-alpine` 與 `fd2-go-test-local:20260909` 均不含 `go`。依 Docker-only 規則，未以主機替代執行，也未完成這份暫存探針。
訂正：同專案第三頁量測已實際以 `golang:1.26.7-bookworm` 在 Docker 內執行
`go run ./cmd/buckrogers-text-receipt` 並通過測試；因此**不存在全專案 Go 工具鏈阻塞**。
本階段未取得身體圖示低階收據，是這個暫存探針未完成，不是必須退回主機或
另建重複 image。下一輪應沿用該可用 image 與已驗證的唯讀原版掛載繼續量測。

## 2026-09-23 補量：return／ABI 已確認，pre-write 仍缺

本輪在 ignored `workplace/body-icon-ready-atomic-core/` 以 `git archive` 從 dosgolem
commit `c0f6d76b0eb60caa72e74a619c1b981c91b340a5` 建立可丟棄 probe source，只在副本將
既有 glyph-return trace 的篩選擴至已證實的 `0763:049B` caller；production dosgolem
工作樹與本專案 runtime 均未修改。建出的 probe runner SHA-256 為
`d8e29a6d7597c8f0757aeee5d7fe24f2f6e30894f0080189a4917ec192a7a740`。原版輸入
`GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；合法起始
state `after-bios-space-100m.state` SHA-256 為
`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。以下
`segment:offset`、SS 與 SP 均是 dosgolem 8086 實模式位址／暫存器值，不是 IDA
線性位址。

依第四十八階段已證實的正常移動、Enter→N 拒絕、Enter→Y 確認 BIOS 排程，各做
兩次 Docker 重播。三組 A／B JSON 逐 byte 相同，SHA-256 分別為：

- 移動：`464b2c648553729bdd6ffc28158fdceb653421a2f14c878f96c357d658379033`；
- 拒絕：`382ca0d5d8ca070ec42a9faa2efba9666b872ce98fc817193852783ba95b6eec`；
- 確認：`14aecfcd5c7f77e5e9855690dc8a592e70b2aa9250972533a5bd47865bb90a00`。

對應終態 indexed framebuffer 的 A／B SHA-256 也分別相同：移動為
`bf38b570cf63a978fe88d5cb3b30fb233675d6acec7d5847220a8db57e309d90`、拒絕為
`d8c15be5805741ed45cfd42fc2211ec16664499c1895e3f840072cb13eb5296f`、確認為
`927ec313f9e5a10937c23735c843ef20f6d2fc9cf2b0ef2aec5fff9d8f303078`。

七筆正式 identity 的 glyph 都由 `0763:049B` 呼叫低階 primitive；每筆 return 前一
指令均為 `0763:03D6`、opcode `0xCA`，回到 `0763:049B`。逐 glyph 的 entry／return
SS 相同（本次錨點 `1841h`），return SP 相對 entry SP 增加 `0x12`。mode、repeat、
背景色、前景色、row、column 的低位逐筆符合 catalog，column 連續。七個 ABI word
的高位不能套用故事頁「全零」假設：每次高階字串呼叫的**首 glyph**
`high_word_mask=0x7c`，該字串其餘 glyph 均為 `0`；這是本路徑實測契約，不得正規化
成零或外推到其他 caller。

這些收據仍不足以把七筆 catalog 升 READY。現有 runner 只能記 glyph entry、高階
cell clear 與故事頁專用 fill／pixel trace；glyph entry 只是候選失效點，不能排除圖示
或背景在首 glyph 前已寫入安全矩形。下一步必須在 dosgolem 新增**受限於七個已設定
安全矩形的通用 pre-execution video-write 診斷，或逐 step framebuffer 比對診斷**，
再以相同三條合法路徑雙重重播，找出每個 active stamp 最早相交寫入。未取得這份
pre-write 證據前，不建立 READY typed-core、不接 production，七筆仍維持 DRAFT。
