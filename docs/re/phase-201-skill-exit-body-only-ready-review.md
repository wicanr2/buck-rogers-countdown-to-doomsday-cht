# 第二百零一階段：技能頁離開問句本體覆繪 READY 審查

日期：2026-09-24
狀態：**限縮 READY 審查通過；正式覆繪與原版 A/B 尚未實作。**

## 審查輸入與結論

獨立審查核對[規格 020](../spec/020-skill-exit-confirmation-overlay-draft.md)、
[第一百九十一階段](phase-191-skill-exit-confirmation-translation-draft.md)的原文身分與
entry→return 時序、[第一百九十七階段](phase-197-skill-exit-confirmation-prewrite-draft.md)
的本體／尾碼分界、[第一百九十八階段](phase-198-skill-exit-ny-all-store-prewrite-draft.md)
的四條 N／Y 含同值首寫、[第一百九十九階段](phase-199-skill-exit-font-containment-draft.md)
的雙倍率靜態字型檢查，及[第二百階段](phase-200-skill-exit-body-only-lifecycle-fake-draft.md)
的可丟棄型別化狀態機。原版與本機字型、存態、畫面、探針收據仍只在 ignored
`workplace/`，未進 Git 或 GitHub。

審查核准的 **READY 範圍只有兩筆 exact 問句的本體**：職業
`[0,264)×[192,200)`、技術 `[0,272)×[192,200)`，座標為 320×200 logical
半開矩形。六格原版多色選項尾碼不是譯文、不是覆繪或清除目標；每次繪製都須
驗證其 2×／3× RGBA 保護矩形零差。這個停止線使尾碼逐格生命週期不再是
本體覆繪的 READY 前置，卻不冒稱其行為已完整解出。

## 型別化契約審查

- 原版 exact identity 的 SHA-256、原文長度、`37F1:101E` caller、row 24、
  column 0、`bg/fg=0/13` 與頁面 context 必須全欄相符。只有同世代
  `Entry → pending → verified Return` 才能建立中文本體 layer；初畫最早
  *same-value* store 未知，因此不能在 Entry 時搶先顯示。
- 已啟用 layer 的任何本體相交 `machine.VideoWrite` 都要在 VGA 實際寫入前
  同步清 watcher 與 presenter，不問 old/new 值或 CS:IP。技術頁 Y 路徑的
  `103906680 AF0A8 0CF4:1B3A` 是同值首寫，不能退回只看變值的 watcher。
  `machine.VideoWrite.Offset` 是段內 offset，必須先拒絕不在 `[0,0x10000)`
  的值，再轉成 `0xA0000 + Offset`；`0xF0A8 → 0xAF0A8`，越界即失敗即關閉。
- partial、重複、錯序、錯頁、錯 caller、錯雜湊／長度／顏色，以及不可信
  位址都清除並 poison。Stop 即同一 session 的 terminal Closed；
  Discontinuity／Fault 為 terminal Failed。Restore 清層後只能以更大世代的
  全新 exact Entry／Return 重建；pending 期間的四種 lifecycle 事件也同樣
  必須清除，不得留下半套 layer。

ignored `workplace/phase200-skill-exit-body-only-lifecycle-fake/fake_test.go`
最終 SHA-256 為
`3f01fe67a40d4778cd0d99ac90d9bd48e4be7b40fa6ecdab049a36ff2a05e1ff`。
主代理在無網路、唯讀專案掛載、目前 UID/GID、`--rm --memory 512m --cpus 1
--pids-limit 128` 的 `golang:1.24` 容器重跑
`GO111MODULE=off go test -count=1 -v .`，所有頂層及子案例通過。
獨立審查者再核對最後兩個 `badEntry=true` 的 caller CS／IP 負例後，確認
型別化失敗矩陣足以授權限縮實作。fake 只證明候選契約自洽，並未載入
原版或正式字型，不能當同狀態對拍。

## 實作與驗收停止線

依專案狀態機，此時才可在 dosgolem fork 實作本體 watcher／presenter，
把原版 dispatcher 事件、`ObserveVideoWrites`、session Stop／Restore／
Discontinuity／Fault 接到單一 owner，並以正式 2×／3× raster 驗證尾碼
零差。實作完成後仍須從各自相同合法原版 state 重生職業／技術
`Escape→N`、`Escape→Y` 的 control／2×／3×，核對原版 machine／DOS／
indexed／palette／檔案與存檔語意不變、批准本體外零差、離頁無殘字。
這些是後續 CONFORMED 條件；本次 READY 不表示技能頁提示已中文化，
也不表示 Linux 完整可玩、冷開機或存讀檔已完成。
