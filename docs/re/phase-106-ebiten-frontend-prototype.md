# 第一百零六階段：Ebitengine host 前端 prototype

日期：2026-09-22
狀態：完成（可丟棄 Linux 視覺／輸入隔離證據；非 production）

## 結論與邊界

在既有 Docker image `eob-remake-go:1.26.7-ebiten2.9.9` 中，Go
`go1.26.7 linux/amd64` 與 Ebitengine `v2.9.9` 已於 Xvfb 成功開啟有限更新幀的
Linux 視窗。prototype 從一份固定的 320×200 indexed framebuffer、256 色 palette
與既有 `buckrogers.BuildMenuOverlay`／`xlate.Layer.Draw` 繪製鏈建立 host output；它不
持有 dosgolem machine，也沒有 DOS 輸入轉送實作。

此項只證實已選定的 Ebitengine 可作為 Linux-first host presenter 的原型，及已確認的 host
input isolation 可以在 presentation-only 原型內被表達。它不是正式玩家視窗、不是
正常玩家路徑、不是 dosgolem 同狀態收據，也不授權 production 接線、跨平台打包或任何
原版規則／輸入語意改變。

所有程式、GOLEMFNT 本機輸入、PNG 與收據均留在被忽略的
`workplace/phase85-ebiten-frontend/`；本文件不附上 PNG 或字型。

## 已驗證呈現鏈

| 項目 | 結果 |
| --- | --- |
| 論理畫布 | 固定 320×200 indexed framebuffer 與同幀 `[256][3]uint8` palette |
| 覆繪 | 現有 `BuildMenuOverlay` 建立「地球」的 active stamp；`xlate.Layer.Frame` 後以 `xlate.Layer.Draw` 畫入新的 RGBA，不回寫 indexed source |
| 字型輸入 | 既有、被忽略的本機 `workplace/font/menu-unifont16.golemfnt`；僅於容器內讀取，未上傳或加入 Git |
| 2× output | 640×400，PNG SHA-256 `8be393fdfb37d763320751bd31854e692b8f3f167ad9e5cd7ecae4898d6f2a59` |
| 3× output | 960×600，PNG SHA-256 `a0eb8e0e983da304efae326e773882e1496dd81ed0fa89694a4195ca5c958aff` |
| 原始 source | `raw_indexed_sha256=274c7e74863be37a53125d64bc382209d98545784351fc19c1e7e1155d0b0801`，Apply 前後相同 |

prototype 以 `host.ScaleController` 明示 `Select` 後再 `Apply`，各以同一份 raw
indexed framebuffer、palette 與覆繪狀態重建 2×／3× output。沒有重啟 DOS、沒有
清除 VRAM，也不建立或改寫 DOS machine。

本原型使用的 Unifont 僅是既有測試字型，不能外推為正式 host 面板字型；
正式繁中面板應使用使用者指定的本機倚天字型，並另行驗證字級與版面。

## Host 輸入隔離收據

host chrome hit 先由 output-space rectangle 消費，原型沒有可到達的 DOS coordinate
conversion 或 input API。收據記錄：

```text
host_hits_consumed=1
host_keyboard_events=1
closed_panel_game_keyboard_eligible=1
dos_input_events=0
```

面板開啟時，鍵盤由 host 消費；關閉時 `routeKeyboard` 回傳未消費，表示未來 adapter
可以恢復遊戲鍵盤路由。這個 prototype 本身仍不送任何鍵到 DOS，故 `dos_input_events`
保持零。這只驗證邊界，不能取代玩家實際鍵盤、BIOS queue、IRQ 或 DOS mouse 的同狀態驗收。

## Apply 後面板狀態：兩個決策樣張

以下樣張使用同一 960×600 3× canvas、同一 source SHA 與零 DOS side effect；只有
host chrome 高度不同。使用者檢視後已選擇 A「Apply 後自動收合」，排除 B「保持展開」。
這是前端操作契約的選擇，不代表原型已接通玩家視窗，亦不建立持久化語意。

| 候選 | host output | PNG SHA-256 | 被忽略輸出 |
| --- | --- | --- | --- |
| A：Apply 後自動收合 | 960×636 | `e13a99b879f496bc84ce3a7e848a6079d468d68036843cb1739a6e013db333f8` | `workplace/phase85-ebiten-frontend/out/apply-auto-collapse-3x.png` |
| B：Apply 後保持展開 | 960×720 | `6f80d5532bd679a8a37f0c462335afb2fb20f10d9326ef9bae28ce9b175e50f5` | `workplace/phase85-ebiten-frontend/out/apply-keep-panel-open-3x.png` |

## 可重播命令

在專案根目錄執行；所有分析、建置與 Xvfb 都在一次性、無網路 Docker 容器內進行：

```sh
docker run --rm --network none --memory 2g --cpus 2 --pids-limit 256 \
  -u "$(id -u):$(id -g)" \
  -v "$PWD/workplace:/work:rw" \
  -w /work/phase85-ebiten-frontend \
  eob-remake-go:1.26.7-ebiten2.9.9 sh ./run-xvfb.sh
```

`run-xvfb.sh` 有 Xvfb trap，結束後輸出 `out/frontend-2x.png`、
`out/frontend-3x.png`、兩張 Apply 候選與 `out/receipt.txt`。本輪未留下相關容器。

## 最小 production 接線缺口

目前缺少一個只讀的 presentation snapshot provider，供未來 host 每幀取得：

1. 固定時點的 indexed framebuffer；
2. 同時點 palette；以及
3. 已 active 的 runtime overlay presentation state。

它必須不暴露 DOS input、VRAM 寫入、BIOS／IRQ 或存檔能力。補上這個 provider 前，原型的
fixture 不能被誤接為玩家畫面，host frontend DRAFT 也不能升為 READY。
