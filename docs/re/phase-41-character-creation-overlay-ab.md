# 第四十一階段：性別與職業繁中覆繪倍率 A/B

## 結論

以 dosgolem 正常玩家路徑重生的性別／職業 steady 與 Down 四個原版 framebuffer、正式
繁中 catalog、正式 logical text-safe rectangles 及同一份 GOLEMFNT，已各產生 2×／3×
離線覆繪。兩批十六份 JSON／繁中 PNG／base PNG 逐檔相同；每份都為零缺字、零安全矩形
重疊、安全矩形外零像素差異，所有 glyph ink 均落在核准範圍。

這是倍率決策用的可丟棄 prototype，不是 runtime renderer 完成證據，也沒有選定產品倍率。

## 原版與輸入證據

| 狀態 | 正常 BIOS 路徑 | indexed framebuffer SHA-256 |
| --- | --- | --- |
| gender steady | Enter→Enter | `dcf947d18c85b051ec85e1bc968f30cec5c315a9158d598055d14ebfe82a715c` |
| gender Down | Enter→Enter→Down | `2628bf531ba41feb8053166e061eedbd94f9f28d2a670d984b35a930526b070f` |
| class steady | Enter→Enter→Enter | `3a61cb542625bdb0fd353f1d337e87c68091bd2dd2185e9b2ba34dad7558012c` |
| class Down | Enter→Enter→Enter→Down | `49d8b036f2c6f0d7fe2d897b8ffcac46db15a5e8386fa0eb4d9c30ae8cccc81c` |

每個原版 framebuffer 各重播兩次且逐 byte 相同。palette 沿用 dosgolem 8-bit RGB 輸出，
SHA-256 `045796505f7ec3115cec8632ca7a29e6391687a2a013198e38dd68dd5b3564eb`。
性別＋職業 GOLEMFNT SHA-256 為
`bb1a1dbee7087c6fa8b222e66c45a215c757b95ea35a0f3b04188c019ea4e03c`。

## 安全矩形

`gender-text-safe-rects.tsv` 與 `class-text-safe-rects.tsv` 對每個 exact identity 固定：

```text
x = column × 8
y = row × 8
width = original_length × 8
height = 8
draw anchor = (x,y)
capacity = original_length
```

性別七筆、職業十筆均與事件表一對一。validator 會交叉驗證既有 post-transition 與 lifecycle
清冊，拒絕非 canonical 數字、越界、未對齊、改寬、缺鍵、錯 anchor 或譯文超容量。

## 2×／3× 比較

| 維度 | 2× | 3× |
| --- | --- | --- |
| canvas | 640×400 | 960×600 |
| 原版 8×8 logical cell | 16×16 px | 24×24 px |
| 16×16 glyph ink | 填滿 cell | 置中，四邊各留 4 px |
| 字距觀感 | 緊密、接近 PC-98 Golden Box CJK 密度 | 較疏、畫布較大 |
| 最長譯詞「太空船駕駛員」 | 六字完整容納 | 六字完整容納 |
| 缺字／重疊／矩形外差異 | 0／0／0 | 0／0／0 |

兩倍率皆幾何可行。目視檢查未見半字、裁切或相鄰列碰撞。selected row 仍沿用原版 palette
中同為黑色的 index 15／0，因此 selected 中文不可見；這是已證實的原版樣式，不是漏畫，
本階段沒有自行改色。

依 `research-pc98-golden-box-ui` 的 CJK 格密度比較，2× 仍較接近 640×400、16×16 點陣字的
PC-98 Golden Box 介面；這只是建議證據，使用者尚未採用，3× 也通過全部硬性幾何閘門。

## 決定性收據

| 畫面 | 2× JSON／PNG SHA-256 | 3× JSON／PNG SHA-256 |
| --- | --- | --- |
| gender steady | `35ebd3a0…d8d4e`／`508bd19c…b133` | `631895b6…e6a3`／`02a6e947…3315` |
| gender Down | `61b50290…25fa`／`5a80dc01…e87a` | `2c5c4870…6edc`／`6eb7fb76…be4d` |
| class steady | `1603e839…28a2`／`c0eff428…1309` | `d3edb316…3815`／`c5461f92…b74e` |
| class Down | `b1bd589b…bce9`／`04220ed9…2569` | `33df44fe…0c73`／`632885aa…e1c` |

`tools/character_overlay_receipt.py` 同時固定兩批 JSON、繁中 PNG、base PNG、事件數、canvas、
containment 與內嵌雜湊。專案 70 項測試及真實 A/B verifier 通過；dosgolem 全部正式套件
測試、`go vet`、`apps/buckrogers` 與 prototype command race detector 通過。dosgolem 本機
分支 commit 為 `73e610943cb26ed3f0990ecd13bd196d12fe162a`，未推送其遠端。

## 停止線

本階段未接 runtime `Layer`、未處理轉場失效、連續幀或手冊分頁，也未改原版資料。產品倍率
仍須由使用者確認；確認後才能建立玩家可見 renderer 的 READY 規格。
