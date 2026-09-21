# 第八十階段：技能操作列快捷字母保留與混合寬度版面

日期：2026-09-21  
證據等級：版面與色彩已證實；字母的直接鍵盤控制作用未知

## 決策與勘誤

使用者指定中文化後仍顯示拉丁快捷字母，字母保持白色，中文沿用原版一般標籤色。
因此 Phase 77 的「首個中文字白色」與「全綠」兩個候選均作廢。正式顯示文字改為
`(A)加點`、`(S)減點`、`(P)上頁`、`(N)下頁`、`(D)完成`；normal 只有括號內字母使用
palette 15，括號及中文使用 palette 10，focus 全組維持 palette 0 字／palette 15 底。

原版逐字輸出已證實五個英文標籤首字分別為 A、S、P、N、D，且以白色呈現；既有正常
玩家路徑只證實 Left／Right 選取與 Enter 執行，尚未用 A／S／P／N／D 直接觸發控制流。
因此本文件將它們稱為「可見助記字母」；顯示保留不冒稱已證實直接快捷鍵。

## 混合寬度與安全矩形

- ASCII `(`、字母、`)` 各前進 4 logical pixels；繁中文字各前進 8，合計 28 pixels。
- `Subtract`、`Prev`、`Next`、`Done` 的既有矩形均足以容納。最窄的 `Add` 原文矩形為
  `[0,24)`，而下一標籤從 x=32 開始；prototype 將 presentation-only 清除／focus 背景擴為
  `[0,32)`，只使用已量到的 8-pixel 空白，不碰相鄰標籤或金框。
- y 軸仍固定 `[192,200)`；沒有採用 Phase 77 已排除的向上擴張。
- 2× prototype 最大墨跡止於 x=55（`Add` 核准輸出矩形止於 64）；3× 最大墨跡止於
  x=79（矩形止於 96）。其餘標籤也全在各自矩形內。

## 可重生收據

輸入是真實 Phase 71／73 framebuffer，字型由本機 GNU Unifont 與五筆 prototype catalog
在 Docker 內重建。可丟棄輸出保存於 `workplace/phase80/`：

- technical 2× PNG：`9dd60e985f1e4bdc42dc54b45f533f8c1cba130757b05398f1397fb5fe708baa`
- technical 3× PNG：`0e0cf5db9613050ec63c49e9cd3a8efe49ebc36b07d3dc80ff89e710b0e86e23`
- career 2× PNG：`0c9ebfa0e859ab87031dde4dfd02244ab252b97276e6dc92c6a29c4ed593de5b`
- career 3× PNG：`c5fc6ad78d74c62ad2bf1c025807a344b16ee5953fa0d9b376cdf3699152c3d6`

正式 TSV 驗證器改用上述半形／全形前進量計算容量，並只允許 `Add` 使用經核准的額外空白格。
dosgolem 核心以五個原子 stamp 保存同一 action group，拒絕全綠或任何偏離
`[10,15,10,10,10]` 的 normal 配色。

## 尚未宣稱

- 本階段沒有證實字母鍵能直接執行五個命令；需要另開正常玩家路徑探針才能升級該結論。
- 尚未接正式 CLI，也未產生完整正常玩家路徑的 runtime overlay A/B 收據；spec 215 只升 READY，
  不標 CONFORMED。
- 產品預設倍率與手冊版面仍未決定。
