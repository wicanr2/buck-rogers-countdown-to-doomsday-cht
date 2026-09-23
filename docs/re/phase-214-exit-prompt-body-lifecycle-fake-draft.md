# 第二百一十四階段：Exit 問句本體生命週期合成原型

日期：2026-09-24
狀態：**DRAFT；僅可丟棄型別化模型，不授權正式 watcher、TSV 或 READY。**

## 證據與輸入邊界

依[第一百八十三階段](phase-183-post-join-exit-identity-corrigendum.md)及
[第一百八十八階段](phase-188-exit-prompts-draft-evidence.md)已量的真正 row 21
選取、兩筆 row 24 問句、N 返回與 Y→Y 退出時序，建立無原版素材的
`workplace/post-join-exit-body-lifecycle-fake/` 原型。原版
`START.EXE` SHA-256 為
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`，
`GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
原型本身**不載入**兩者、存態、手冊、字型或畫面。

原型 `fake_test.go` SHA-256：
`50ccb08e7b189a282a12142e90ad85c0b08041b68f019367804274e3fa7ed773`；
重跑說明 `README.md` SHA-256：
`ca763e505d10cdc50353006f3d9ba44f2f93e69dadd8db95d42d3a58b12d8f51`。
其中 `37F1:…`、`0763:…` 是 dosgolem 8086 實模式位址；
`0xA0000` 加上 `VideoWrite.Offset` 後才是線性視訊位址，兩者不能混用。

## 限縮測試結果

主代理在無網路、唯讀掛載、`golang:1.25.0-bookworm`／Go 1.25.0 的
Docker 內，以 `--rm --memory 1g --cpus 2 --pids-limit 128`、目前 UID/GID、
`GOCACHE=/tmp/go-cache` 執行 `go test fake_test.go -count=1 -v`，七組頂層
測試及其負例全通。模型固定：

- 完整 identity 的 Entry→guarded Return 才可建立問句本體層；錯序、部分
  identity、未知 identity 與重複 Entry 會失敗即關閉。
- row 21 與第一問使用獨立層：N 返回時 row 21 已重新選取、第一問尚未遇到
  本體首筆 A000 寫入，兩者可短暫共存；第一問遇含同值寫入即只清問句。
- Y→Y 的第二問 Entry `124906582` 早於第一問同值本體寫入 `124906844`；
  第二問 pending 與第一問 active 可暫時共存。該筆寫入只清第一問並保留
  pending，第二問的 `124929724` guarded Return 後才啟用；若在清除前
  就 Return，原型失敗即關閉。初版原型把 Entry／清層排反，已由這組
  負例訂正；初版綠燈不得當成時序證據。
- 第二問沒有已量的自然本體清除；DOS Stop 須轉 Closed 並清空所有層，
  同一擁有者不能重新啟用。
- 待處理或作用中本體若遇到未量寫入者，清空並轉 Failed；段內 A000
  offset 越界、Restore、Discontinuity、Fault 與 2×／3× 本體／尾碼遮罩
  邊界亦有合成負例。寫入者 `0763:184D` 的白名單僅是已量路徑的候選，
  遇到其他正常寫入者須重新審查，不能據此改原版行為。

## 限制與下一門檻

[第二百一十三階段](phase-213-exit-prompt-font-draft.md)另驗兩句繁中候選
的倚天字型靜態 containment；本模型不驗真實字模、原版六格多色尾碼、
同狀態 A/B、正式 `Restore` 來源或 Linux 玩家視窗。要升限縮 READY，
須把本體安全矩形、獨立層 owner、尾碼零覆繪與失敗邊界寫成 DRAFT 規格，
再獨立審查；正式接線及原版 control／2×／3× 驗收是 READY 之後的工作。
GitHub 工作項為 [#19](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/19)。
