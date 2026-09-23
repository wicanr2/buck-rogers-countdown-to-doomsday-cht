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

## 2026-09-23 訂正：受限 store 診斷補足已量 lifecycle

前節停止線保留，因為單看逐 step framebuffer 會漏掉「寫回相同色值」；首次候選也確實
在拒絕分支漏掉四筆 body text 重畫。後續只在本機 dosgolem CLI 的明示 body trace
加入 content-safe pre-execution store metadata：`F3 AA`／`ES=A000` span，以及 IDA 9.4
已證實的 glyph primitive `0763:184D`、`0763:1854` 單 byte `STOSB`。IDA 輸入是 runtime
`0763:0000` 8 KiB 快照，SHA-256
`436711fefc7071fcaf0811ef0b4243a5f2fd42840ca0f3b11aaaf121454deac6`；IDA EA 等於
runtime offset。`0763:1821–182E` 計算 `DI=((row*320)+column)*8`，`0763:1830–1833`
設定 `ES=A000`。診斷不輸出 AL、原始 bytes 或 framebuffer 內容。

最終本機 dosgolem commit `2755f7c`，runner SHA-256
`52a071e1b42dd0ec2affc8f659e8d2bc1fd8062fb95bb5175126b35f24d34802`。拒絕分支
A／B 逐 byte 相同，receipt SHA-256
`7971fd3aae514698cb8ee8846affb852b1e09b33e86640560bb6f79d2a880348`。已量 active
stamp 的最早相交 pre-write 為：selection `106000487`（`0CF4:1B3A`、`A000:F000`、
320 bytes）；old label `106244991`（`0763:184D`、`A000:3C40`、1 byte）；old action
`106247520`（`A000:6418`）；new label `106258513`（`A000:7840`）；new action
`106261034`（`A000:A018`）；confirmation→selection `106679836`（`A000:F000`）。確認
分支另證實 confirmation→save prompt 的 fill 為 `106227779`、`0CF4:1B3A`、
`A000:F070`、208 bytes。終端的新 selection／save prompt 沒有在已量停止點後虛構離頁。

ignored `workplace/body-icon-ready-atomic-core/` 的可丟棄 typed-core 直接解析正式
events／rects、三路 return receipts 與 pre-write receipts。它逐筆驗七 identity、
`0763:03D6` opcode `0xCA` RETF 回 `0763:049B`、同 SS／SP+`0x12`，以及每次高階
字串首 glyph `high_word_mask=0x7c`、其餘 glyph 為零；另測 generation／原子群組、
unknown／duplicate／partial、restore／discontinuity 與 pre-write 漂移失敗即關閉。
正式 DRAFT catalog 必須被拒，正例只用即時暫存 READY fixture。Phase 101 正式倚天字型
對七筆譯文零缺字，2× 16px 與 3× 22px ink 均落在各自 16／24px 高的縮放矩形內。
5 項 Docker 測試通過；typed receipt SHA-256
`22017162ace0bbaebbf16fcbddcd0478a6c346f0c66b1c99d6f3b6e7503e64bd`。

因此原先 return／ABI 與已量 lifecycle pre-write 的實質缺口已補足，可交獨立 READY
審查；本筆不自行升級 `text/body-icon-events.tsv` 或 spec 009，不接 production，也不宣稱
未量的儲存詢問離頁、完整開機或存讀檔生命週期。

## 2026-09-23 獨立審查勘誤：完整 A000 observer 取代 selective trace

前節 `2755f7c` 的 selective `REP STOSB`／glyph-store trace 只能列出已知 writer，不能排除
其他 A000 writer；其「確認分支 confirmation→save prompt 的 first 是 F3AA
`106227779`」結論亦被完整觀察推翻。後續 dosgolem `9eb9457` 在 `Machine.Write8` 實際
寫入前提供通用、預設關閉的 A000 observer，同值寫入也會被觀察。aggregate runner 是在
基底 `a16b028` 加入之後提交為 `9eb9457` 的來源上建置，binary SHA-256 為
`baaecad626494102281b22e8102d8fef42bc961bcc55565e525047cbf036abd5`；建置收據另保存實際
來源檔雜湊，不能與非 aggregate runner `a5313c...` 混用。

固定 move、refuse、confirm 三條排程均做 A／B；各組完整收據逐 byte 相同：

- move：SHA-256 `4c800ee0a4e96ecf9e9a9c0e452b8a7295b66dbf70445127530f5e043f075f72`，
  全 A000 730,752 次、安全矩形相交 61,248 次；
- refuse：SHA-256 `e5c53001cf00aadaed54fe3cc337581597b029a0f571a4fc11f08188fa3ecb86`，
  全 A000 760,256 次、安全矩形相交 66,176 次；
- confirm：SHA-256 `04ff0f4db1e47f294d37a4bc7c3a57ebd11c49f79e0baf049cd4ada4c653b8da`，
  全 A000 735,040 次、安全矩形相交 64,000 次。

完整 observer 證實：refuse 初始 selection 的 first 仍是 `106000488`、
`0CF4:1B3A`、`A000:F000`；confirmation／save prompt 的 first 則是 glyph store
`0763:184D`、`A000:F000`，confirm 為 `106216585`，refuse 為 `106679837`。稍後的
F3AA fill 不得再稱為 first。observer step 位於實際 pre-write callback，較舊 pre-exec
記錄多一個 step，兩者不可混寫成同一量測時點。

可丟棄 typed-core 現有 11 項測試通過，包含逐 glyph 低階 ABI、非法混合／部分群組、
偽造較早寫入、錯誤 F3AA-first confirmation、真實 GOLEMFNT 2×／3× raster containment
與全零字模負例；receipt 仍正確輸出 `ready:false`。獨立審查拒絕升 READY，原因有二：

1. 正式 watcher／dirty-state 尚未證明能在任何 A000 writer 的 first intersecting write 前
   失敗即關閉地介入；完整 observer 目前只量測原版，不能代替 production interception。
2. 真實 move／refuse／confirm receipt 的時間序列尚未直接餵入 watcher，故
   event→group／transition→generation 的垂直綁定仍未證實；現有群組測試只是人工序列。

本階段因此維持 DRAFT。下一步先補上述兩個可否證的核心契約；不得先接 production 再反向
宣稱 READY。完整 observer 僅涵蓋三條固定合法排程，亦不得外推到未量的儲存詢問離頁、
完整開機或存讀檔生命週期。

## 2026-09-23 第二次獨立審查：限縮 READY 通過

上述第一次審查的兩項證據缺口已在 ignored typed-core 補足，仍未接 production：

- 真實 move／refuse／confirm return-event 收據按 step 直接餵入 watcher，驗得合法群組依序為
  body-selection→selection-redraw、body-selection→confirmation→body-selection、
  body-selection→confirmation→save-prompt，generation 分別到 2、3、3；不再只靠人工序列。
- A000 dirty-state adapter 將完整 observer spans 與 event commit 依 recorded step 合併；三路
  均無 span 跨越 commit。first intersecting write 發生時會先原子失效整個 active generation，
  不以同值寫入或已知 writer 作捷徑。未知 writer／key、提早或缺失 first、錯 generation、
  partial／mixed／duplicate、跨 group 事件與 span 跨 commit 都有失敗即關閉負例。

typed-core 14 項測試通過；receipt SHA-256 為
`982e29362e5b98d812f91ba481b21fb8388932acee28f108d70d47444b7b1985`。第二位獨立 Terra
審查另在 Docker 重跑 14/14 與 dosgolem machine／receipt CLI 測試，判定「尚未接
production」不是 READY 阻擋，因 implementation 本來就位於 READY 之後；現有證據已能形成
可實作且可否證的限縮契約。

因此 spec 009 只在七個 exact identity、固定 move／refuse／confirm 三條正常重播與已量
step 視窗升為 READY。儲存詢問離頁、實際存讀檔／restore、完整開機、其他輸入路徑及
未觀察 writer 仍排除；production 接線後仍須 control／2×／3× 同狀態與清除生命週期收據，
通過前不得標為 CONFORMED。
