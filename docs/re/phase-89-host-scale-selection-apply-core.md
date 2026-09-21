# 第八十九階段：host 倍率預選與 Apply 純核心

日期：2026-09-21  
dosgolem 本機分支：`buck-rogers-cht-output-overlay`  
dosgolem 本機提交：`9240c3b19ad5eaba7a44a2b9b4f4420fe1653a0a`（未推送）  
狀態：**CONFORMED（純核心；非 host frontend）**

## 已實作的 C 語意

dosgolem 新增通用 `host` package 的 `ScaleController`。它只有 `activeScale` 與
`selectedScale`：constructor 明示接受 2 或3並令兩值相同；`Select` 只更新 selected；
`Apply` 才原子提交 selected 至 active，並以 `changed` 指出值是否實際改變。回選原 active
或重複 Apply 都不會產生額外狀態。

controller 沒有 direct import DOS、machine、oracle、`apps` 或 `cmd`，唯一直接 import 是標準庫
`fmt`。它不能繪圖、重繪、開視窗、接收滑鼠／鍵盤、送 BIOS／IRQ、寫 VRAM、改存檔或引用任何
繁中／手冊資料。

## 隔離驗證

Docker 內通過：

```text
go test ./host
go vet ./host
go test -race ./host
go list -f '{{join .Imports " "}}' ./host  # 僅 fmt
```

單元測試涵蓋 initial 2×／3×、Select 不套用、Apply 原子提交、idempotent Apply、選回原值、
zero／one／four／255、nil receiver、失敗後 state 不變與 snapshot value isolation。

## 明確未完成項

這不是 host 視窗或玩家可切換倍率的驗收。頂端按鈕、設定面板、hit test、命中事件的 DOS 隔離、
Apply 後是否收合、持久化、實際 RGBA 重繪、手冊 presenter 接線與正常玩家 same-state A/B 都沒有
實作。專案 spec 004 保持 DRAFT，僅回填這個已 CONFORM 的通用 state core。
