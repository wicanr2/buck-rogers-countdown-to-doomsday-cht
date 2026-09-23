# 第一百八十一階段：加入角色後功能選單 READY 獨立審查候選

狀態：**DRAFT；等待獨立審查，不授權 production。**  
日期：2026-09-23

本文件只把既有原版證據、幾何與失敗矩陣整理為狹窄 READY 審查輸入；它不自行把
[spec 018](../spec/018-post-join-menu-overlay-draft.md)升為 READY，也不授權正式 watcher、
loader、presenter 或 runtime A/B。

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
  審查若被接受，只能作 immutable READY fixture；文案、key、source、字型或 variant 任一
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
- 固定字型輸入 SHA-256 `ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`
  對七筆 text 的 2×／3×靜態 containment 必須維持零缺字、零墨跡外溢、非零 ink。
  2×為 16×16 cell／ink；3×為 24×24 cell、22×22 ink、`(1,1)` offset。這是 READY
  的幾何準入，不是 runtime A/B。
- 獨立審查必須回讀 21-row TSV、7-key text、字型雜湊、phase 161 原始收據、phase 180
  fork A/B observer，以及 ignored verifier 的 fail-closed matrix；任何輸入雜湊不符或
  原文素材意外進入版控即拒絕。

## READY 之後才做的工作

READY 僅授權以審查 fixture 實作正式 loader、watcher、generation core 與 RGBA presenter。
其實作與驗收不得倒灌為本次 READY 前置：production 必須再驗證 2×／3×同狀態 control A/B、
machine／DOS／indexed framebuffer／palette 不變、安全矩形外零 RGBA 差、每個已量 pre-write
在同幀 active→empty、row20→row21／restore／stop／unknown-writer failure matrix，及已量
正常路徑無殘字。這些通過後才可將相同狹窄範圍宣稱 CONFORMED。
