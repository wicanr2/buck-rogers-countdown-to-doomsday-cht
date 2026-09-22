# 第一百一十三階段：Ebitengine host 控制可丟棄原型

日期：2026-09-22
狀態：完成（Linux／Xvfb host-only 原型；非玩家前端）

## 輸入與範圍

原型只在被忽略的 `workplace/phase109-ebiten-host-controls/`。它使用 phase104
正常玩家路徑收據中的 320×200 indexed 畫面，從同幀 2× RGBA 逐像素驗證並
重建 palette；不是手工繪製的假遊戲畫布。原始 indexed SHA-256 為
`964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba`，
導出 palette SHA-256 為
`748a510ce78477e56d99c00dda947a24a7965f1e183ed663f204f94b6b7bc150`。
host 控制中文字由使用者授權本機倚天來源建成僅供原型的 9 字模字型，SHA-256
`5c518a92f800841b00e8e6833c7ee652bf9f9ad2470e7883035b0237be797749`；
原版素材、PNG 與字型都不入 Git。

既有 `eob-remake-go:1.26.7-ebiten2.9.9` Docker image 與 Xvfb 在 Linux 開窗
10 幀，實作可丟棄的 Ebitengine hit routing 與 `host.PanelController` 狀態轉移。
這裡沒有 dosgolem machine；收據的事件序列直接呼叫同一純 host controller，
不是 OS pointer injection，也沒有送任何 DOS 鍵。

## 已重播的 host 行為

初始 active／selected 均為 2×。開面板後鍵盤由 host 消費；暫選 3× 不改 active，
按「套用」後 active 變 3× 且面板自動收合。再開面板暫選 2×、按「取消」後
active／selected 都回 3×，關閉後鍵盤重新成為可轉送給遊戲的候選。全部事件
保持相同的原始 indexed SHA；`dos_machine_attached=false`、`dos_input_events=0`、
`game_keyboard_eligible_count=2`。取消前後 3× PNG 逐 byte 相同。

| 本機輸出 | SHA-256 |
| --- | --- |
| `out/01-closed-2x.png` | `abbec65992cc0b4a8af3d5f610cbfc44b9bf1a6be2a2a666b11bd2e26e52a789` |
| `out/02-open-selected-3x-pending.png` | `65741a67e6453b9be95d43469efabaec703f03389873a690a73019c831847d46` |
| `out/03-after-apply-3x.png` | `8f9b4011db7b8210f90645780ac5ab697ec85def1fa8e6723e5647998b09e88d` |
| `out/04-after-cancel-3x.png` | `8f9b4011db7b8210f90645780ac5ab697ec85def1fa8e6723e5647998b09e88d` |
| `out/receipt.json` | `69fff4e615b8a6dda7b0d93168346e6e87764ce07c7c0e99cf30d5a5c4e25e32` |

## 正式接線缺口

此原型只證明 host UI 與真實畫面收據可以同窗顯示，不證明 dosgolem 正在遊玩。
進入 spec004 READY 前仍需：同一 machine-stepping thread 的 indexed／palette／
active xlate layer 原子快照；真實 Ebitengine 事件與已確認 host hit／keyboard
路由的接線，以及關閉面板時的正式 DOS input bridge；最後以正常玩家路徑
驗證 2×／3×、Apply／Cancel 對原始畫面、DOS 狀態、BIOS queue／IRQ、存檔
零副作用，且 active 繁中 layer 不遺失。
