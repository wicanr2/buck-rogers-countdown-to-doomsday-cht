# 第一百八十一階段：加入角色後功能選單限縮 READY 獨立審查

狀態：**獨立審查通過；僅授權 spec 018 限縮 READY 實作，不代表 runtime 符合。**
日期：2026-09-23

本文件把既有原版證據、幾何與失敗矩陣整理為狹窄 READY 審查輸入；主代理已依本節
核對並將 [spec 018](../spec/018-post-join-menu-overlay-draft.md)限縮升 READY。正式 watcher、
loader、presenter 與 runtime A/B 仍待實作／驗收。

## 審查範圍與固定輸入

- 僅限合法 `a-joined.state` 的 Right → Enter → rows 13、14、15、16、18、19、20 的
  初畫與已量 Down 重畫；row 12／17／21、動態資料、prompt、其他 Enter、重入、存讀檔
  與完整開機都排除。
- 原版 `GAME.OVR`、state、權威 fork `4589bfe` 與雙重 A000 receipt 雜湊以
  [phase 180](phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)為唯一來源。
- [`post-join-menu-variants.tsv`](../../text/post-join-menu-variants.tsv)的 21 筆是唯一
  identity fixture：七 row 各有 `initial_normal` (`37F1:15BD`, `0/10`)、
  `normal_redraw` (`37F1:1856`, `0/10`) 與 `selected` (`37F1:175D`, `15/0`)。
  每筆必須 exact 比對 length、原文 SHA-256、caller、background、foreground、row、column。
  不得由相似 hash、座標或 caller 補配。
- [`post-join-menu.zh-TW.tsv`](../../text/post-join-menu.zh-TW.tsv)仍是編輯性 DRAFT：七 key
  必須一對一、UTF-8／NFC、非空、無控制／格式字元，且不能改變原版語意路徑。它在本次
  審查已將其固定為 immutable READY fixture；文案、key、source、字型或 variant 任一
  改動都使本候選回到 DRAFT。

## READY 候選的 typed 生命週期

1. 初畫只接受七個 ordered `initial_normal`，再接受 row 13 `selected`，才 atomically
   install generation 1；partial、重複、漏項或重排一律清空 pending／active。
2. 每次已量 Down 先收到前一 row 的 exact `normal_redraw`。在該原版輸出前的第一個
   相交 A000 pre-write，必須 atomically invalidate 整個 active generation；不得等到
   framebuffer 變色或 `026F:029C`。
3. 僅當後續 exact `selected` 是已審查的下一 row，才以完整 normal／selected pair rebuild
   下一代；任何 caller、style、hash、length、格座標或排序錯誤均 fail-closed。
4. row 20 `normal_redraw` 是第 21 個已證實 variant，但下一個 row 21 selected 不在 fixture；
   因此它只會失效第七代，絕不能 rebuild 或保留舊 stamp。unknown row、restore、machine
   stop、execution discontinuity、未知 A000 writer、generation mismatch 與不完整 pair 都
   必須清空 pending／active。

這是「pre-write → invalidate → 完整 pair → rebuild」的唯一可接受順序。正式實作不得把
原版寫入延後、抑制或改寫；overlay 仍僅可在 RGBA presentation output 出現。

## 幾何、字型與文本 READY 條件

- 每列 logical safe rect 與 anchor 沿用 spec 018：
  `[72,72+8×original_length) × [8×row,8×row+8)`、單列 `single-line-reject`；無截斷、
  換行、擴寬或自行改譯。
- 現行固定字型輸入 SHA-256 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`
  對七筆 text 的 2×／3×靜態 containment 必須維持零缺字、零墨跡外溢、非零 ink。
  2×為 16×16 cell／ink；3×為 24×24 cell、22×22 ink、`(1,1)` offset。這是 READY
  的幾何準入，不是 runtime A/B。
- 獨立審查必須回讀 21-row TSV、7-key text、字型雜湊、phase 161 原始收據、phase 180
  fork A/B observer，以及 ignored verifier 的 fail-closed matrix；任何輸入雜湊不符或
  原文素材意外進入版控即拒絕。

## 獨立審查收據與 READY 之後的工作

主代理以權威 fork `4589bfe986a7414c418f7ec02d6da0888d7cfd11` 回讀：
`post-join-menu-events.tsv` SHA-256 `92ebceaf691807118392d2e284660c14694e34281a64b8b14bc5e9dcfd160ec1`；
21 筆 variant SHA-256 `8e81644e94213bd99e9f91c75e21e10e277f498a16257556516302da4e448eb5`；
七筆譯文 SHA-256 `0c2ed04b6d5942b01b41670b38ce6d11fe8af798c04cf3fb54354474f6202eb3`；
phase 161 雙重收據 SHA-256 `5b4c8f66ffd72651344c0dbb45de5946d273276b933dc9d4b902d69297841c36`；
phase 180 權威 fork 雙重 A000 收據 SHA-256
`7421d673aa5455fe243e01b11a2c6f261f0a07767904cbe82e70c274ac4d448c`；
本機倚天 GOLEMFNT SHA-256 `ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`。
七項可丟棄 verifier 正反例由主代理在 Docker 內重跑全通，輸出收據 SHA-256
`6e50d26ffdbb22ec7d05fe9069b3fad4d36105883bf588fc57911fa82289b31e`。
版控 TSV 無原版全文；上述字型與私有原版收據都仍在 ignored `workplace/`。

## 2026-09-23 主機介面字型擴充後的再審

新增 [`host-ui.zh-TW.tsv`](../../text/host-ui.zh-TW.tsv) 後，正式 TSV 增為 22 份、
字元聯集由 1026 增至 1028；因此原 1026-glyph 字型 SHA-256
`ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`
**只是先前審查的歷史輸入**，不能再拿來代表現行 `workplace/current-font/`。
主代理先暫停依賴該 pin 的正式接線，再於 Docker 獨立重跑同一份七項可丟棄 verifier：
21 筆 exact variants、phase 161 與權威 fork phase 180 收據、七筆譯文及負例均通過；
2×／3×七列逐一為零缺字、非零墨跡、零 cell／像素外溢，3×仍採 24×24 cell、22×22 ink
及 `(1,1)` anchor。新收據 SHA-256 為
`24100af2e74f17e5c22ae07ce1c452ba390c634e7c52bcd36541feeadb003536`，
`inputs.font` 明列新 SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`；
`post-join-menu.zh-TW.tsv` 仍為 `0c2ed04b6d5942b01b41670b38ce6d11fe8af798c04cf3fb54354474f6202eb3`。
本機 manifest SHA-256 `39eb11a95d95eed749fefa4d358230e5e449339eb2e189f1a8296f0cde8cd00f`
列明 16×16／1028 glyph、`top-pad`、`local-only-not-for-distribution`，並逐一釘選
`ASCFONT.15`、`SPCFONT.15`、`STDFONT.15` 的 SHA-256；字型來源與建置命令見
[`font/README.md`](../../font/README.md)。因此僅字型輸入更新後的同一狹窄幾何範圍
重新准入 READY；verifier 內的 `ready=false` 是它不自行裁決規格狀態的既有設計，
並非 runtime 通過。正式同狀態 A/B 與正常玩家路徑仍未驗收。

READY 僅授權以審查 fixture 實作正式 loader、watcher、generation core 與 RGBA presenter。
其實作與驗收不得倒灌為本次 READY 前置：production 必須再驗證 2×／3×同狀態 control A/B、
machine／DOS／indexed framebuffer／palette 不變、安全矩形外零 RGBA 差、每個已量 pre-write
在同幀 active→empty、row20→row21／restore／stop／unknown-writer failure matrix，及已量
正常路徑無殘字。這些通過後才可將相同狹窄範圍宣稱 CONFORMED。
