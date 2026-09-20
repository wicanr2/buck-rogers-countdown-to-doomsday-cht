# 第二十二階段：dosgolem xlate 通用整數倍率

## 結論

workplace dosgolem 分支 `buck-rogers-cht-output-overlay` 已在本機 commit
`ef7f8db32b20a6b9eb6d810bd4e6b99187c55f44` 將 `xlate.Layer.Draw` 從「只接受 3 的倍數」
改為接受正整數倍率。`scale <= 0` 失敗即關閉；`GlyphScale == 0` 改為
`max(1, scale/3)`，因此 16×16 `GOLEMFNT` 在 2× 與 3× 都以 1:1 字模像素繪製，6× 等
既有較大倍率仍維持原來的比例。這只解決 renderer 能力，不代表《拯救地球》已選定倍率。

## 程式與測試證據

- `xlate/layer.go`：倍率契約改為正整數；負的明示 `GlyphScale` 不畫字模。
- `xlate/layer_test.go`：新增 2× 的左上／右下字模點、前景色、背景色精確檢查。
- scale 0、-1、-3 均回傳 false 且不改動輸出緩衝區。
- 只提供 1 像素 RGBA 緩衝區時，超出目的範圍的背景與字模安全裁切，不 panic。
- 既有 3×、偏移、格緣裁切、缺字 callback、透明格及 snapshot round-trip 測試保留並通過。
- 以 Go 1.26.7 一次性、無網路 Docker 容器執行所有正式套件（排除 `workplace/`），全數通過；
  `internal/cpu` 等完整測試亦完成，並非只跑 `xlate`。

## 真實 GOLEMFNT 冒煙收據

輸入為被 Git 忽略的 `workplace/font/menu-unifont16.golemfnt`，由 production
`xlate.LoadFont` 載入；候選字串中實際覆蓋的繁中字元為「地球」。測試輸出只保存在
`workplace/phase22-xlate-smoke/out/`：

| 倍率 | 尺寸 | PNG SHA-256 |
| --- | --- | --- |
| 2× | 32×16 | `db2264ba97f18b6a7e73ce996e06e967b99f09af065c5b10726fc15b9b63d1fe` |
| 3× | 48×24 | `126315197d4a6ca7d8c85419527a1305e18207d36e72b4aa62345e902ce6acd0` |

兩張圖均逐張目視確認可辨，字模為整數像素且沒有濾波。3× 的 16×16 字模仍位於 24×24
輸出格左上方，保留既有 renderer 行為；置中與版面配置仍由呼叫端的 `GlyphX`／`GlyphY`
決定。

## 限制與後續閘門

- dosgolem commit 只存在本機 workplace 副本，未推送其遠端。
- 本階段沒有接入遊戲專用事件 adapter、分頁按鍵或正常玩家路徑。
- 2× 與 3× 現在都具備 renderer 能力；正式倍率仍須由使用者決定。
- 選定後仍須以同狀態原版畫面完成覆繪 containment、生命週期與分頁互動收據。
