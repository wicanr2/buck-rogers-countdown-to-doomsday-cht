# 第一百一十六階段：真實遊戲載入 Ebitengine host 原型

狀態：prototype；不構成可玩版或中文化完成。

## 範圍與權利

2026-09-22 在 Docker／Xvfb 內，以僅限本機的
`workplace/original/BRcdoom/` 原版資料與
`workplace/phase104-post-return-enter-4/control.state` checkpoint，執行 ignored
`workplace/phase114-game-ebiten/`。兩者均不得加入 Git、Release 或公開包。

原型只輸出 content-safe receipt 與本機 PNG；本文不保存原文、題目、答案、字型 bytes 或原版像素。

## 已驗證

同一 Ebitengine goroutine 依序執行 Machine step、`onFrame` lifecycle、
`MachineFrameSource`／`LayerSnapshotProvider` 與 Draw。12 個 window frames 後的 receipt：

- `game_loaded=true`、初始倍率 2×；
- Cancel 暫選 3×後回到 2×：`cancel_returns_2x=true`；
- Apply 3×後收合：`apply_3x_closes=true`；
- 面板開啟時 BIOS Enter 不變更 queue：`open_bios_unchanged=true`；
- 關閉後透過明示 BIOS `{scan, ASCII}` 鍵送入並推進：`closed_bios_delivered=true`；
- 畫面 indexed SHA-256：前 `4f9d1bb280724737ca72599c3e7d387c23c076f7e0a8637d8d3ebc9164514bf2`，後
  `5869dd6d91d7f0fc84d2204cce43f8e229ce140bd1b0e75aa712bf295e21ecab`；
- 本機 `game-3x.png` SHA-256：`fd22af7f5b54b214495b347dd6ebae47614119cce7859de0507fb5926806447a`。

## 明確限制

receipt 的 `active_layer_connected=false` 是刻意限制：原型只接了空 `xlate.Layer`，尚未接出
Buck Rogers adapter 的 private active layer。因此未驗證中文 stamp、手冊 presenter、實際 host
pointer hit、Ebitengine 實體按鍵映射或完整玩家路徑；spec 004 維持 DRAFT。
