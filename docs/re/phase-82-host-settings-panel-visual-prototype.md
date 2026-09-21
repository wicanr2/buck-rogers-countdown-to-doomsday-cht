# 第八十二階段：host 設定面板控制列視覺 prototype

日期：2026-09-21  
狀態：完成（可丟棄視覺／幾何證據；尚非 production 前端）

## 結論

使用者決定由視窗頂端 host-only 滑鼠按鈕開啟 dosgolem 設定面板。現有 dosgolem 是無頭、
決定性執行器，沒有可重用的互動視窗或 host UI；因此本階段只建立 presentation contract
prototype，不聲稱已具有可派送的視窗事件。

prototype 採「控制列＋面板在遊戲畫布上方保留 host 空間，展開時將畫布下推」：面板不覆蓋、
不裁掉、不平移畫布內任一像素。這個配置符合原版輸出端覆繪邊界；反之，任何浮在畫布上的
選單都會遮住原版題目或中文段落，已排除。

## 幾何與輸入契約

| 輸出倍率 | host 視窗 | 遊戲畫布 output rectangle | 面板鈕 output rectangle | 2×／3× option rectangles |
| --- | --- | --- | --- | --- |
| 2× | 640×480 | `[0,80)–[640,480)` | `[568,4)–[624,20)` | `[16,28)–[184,50)`／`[16,54)–[184,76)` |
| 3× | 960×720 | `[0,120)–[960,720)` | `[852,6)–[936,30)` | `[24,42)–[276,75)`／`[24,81)–[276,114)` |

- 控制列為 12 logical pixels，展開面板為 28 logical pixels；全部按 output scale 放大。
- 遊戲畫布仍是完整的 320×200 logical pixels，只改 host window 中的 output origin。
- 任何命中表中 host rectangle 的滑鼠移動、按下、放開與座標都在轉換 DOS 座標、DOS mouse API、
  BIOS 或 IRQ 前被 host 消費；未命中才可以走既有遊戲輸入路徑。
- 切換時須以同一份 raw indexed framebuffer、palette 與 active overlay state 重繪新的 output
  canvas；不得重新啟動 DOS、送鍵、改 VRAM 或遺失 overlay stamps。

## 可重生收據

來源是 Phase 62 的真實保留原題手冊畫面；prototype 以 Docker 內
`workplace/phase82/make_host_panel_prototypes.py` 產生，四張圖皆驗證 copied game canvas SHA-256
等於來源：

| 畫面 | PNG SHA-256 |
| --- | --- |
| 2×、選取 2× | `8ab83da8461b2848e965450e3a0c6f1be260d2814e2a591bd70fb9946b3da44d` |
| 2×、選取 3× | `c30bdd287ceca4df33ac8cf3569ec541a4d30945ce1d4b2bebd5c2edf2c5e4b2` |
| 3×、選取 2× | `6182ac3d58112fab08c277585fc424529a1f53f553acc3a572fa22a4e443388b` |
| 3×、選取 3× | `43179549163620afce5a889d0428df99748e9cc006d1d561421e3af506db7634` |

所有圖片、程式和 JSON 收據都留在被忽略的 `workplace/phase82/`；不含原版可散布素材。

## 分層

- 通用 dosgolem 層：host canvas layout、hit test、輸入消費、scale state、output re-render。
- `apps/buckrogers/`：只提供 indexed framebuffer、palette、已存在的繁中 overlays；不得知道
  host menu rectangle、按鈕、視窗尺寸或滑鼠分流。
- 未知：實際視窗 backend、host 事件迴圈、面板字型與焦點行為；尚未由 prototype 證實。

## 下一個決策前沿

倍率選項點擊後應立即套用並關閉面板，或先選取、再以專用按鈕確認。這改變玩家操作節奏，
需要使用者確認後才能寫 READY spec。
