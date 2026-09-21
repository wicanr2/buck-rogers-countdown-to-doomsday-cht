# 第五十七階段：明示倍率的執行期繁中覆繪

## 結論

dosgolem 已將保存→功能選單→名冊→加入隊伍的 14 筆 typed 顯示請求接到
`xlate` presentation layer。覆繪只產生獨立 RGBA，不寫回原版 indexed framebuffer、
CPU、DOS 或存檔。2× 與 3× 都必須由命令明示指定，本階段沒有選定預設倍率。

## 生命週期訂正

- `026F:029C` 依第六階段已證實的 Mode 13h 文字格參數，轉為像素半開清除矩形；
  `xlate.Layer.Clear` 移除完全覆蓋的 stamp，部分相交時只使相交格透明。
- 首輪四次重播暴露功能選單與底列 loading 舊 stamp，因此 spec 由 READY 退回 DRAFT；
  失敗收據保留在忽略的 `workplace/phase57/`。
- 清除矩形解決功能選單殘留。底列 `roster.loading` 與後來的 `roster.add_prompt`
  同原點但分別長 21／17 格，改用通用 `Layer.Replace` 同原點輸出取代契約。
  這些判定均來自原版位址或輸出幾何，沒有依 event key 硬編終態清單。

## 決定性與同狀態收據

`f2/g2/f3/g3` 四份 fresh scratch 正常玩家路徑均為 18 events、14 requests、4 筆
dynamic-name misses、14 overlay actions、3 writes 與 2,611 FileOps；終態只保留
`roster.add_prompt`。四份 events、BIOS keys、writes 與 FileOps 逐項等於無覆繪 control。

- 2× RGBA 兩份 SHA-256：`a99fea2327fe20fb48263dadcbfe8fdec369c162c617e8721edd70605b70d7cd`。
- 3× RGBA 兩份 SHA-256：`8c7368243ab1e66b21d84e79ad7b8fe2dc4326fc24bb7c679e77ed2965200dce`。
- 四份原版 framebuffer SHA-256 都是
  `0c43f315a772f9f10281eb1fe38ebcb43a9d0cdc0b106f3cb06f49f707e7d003`。
- `A.who` 與 `A.stf` 分別維持第五十四階段收據的 `43b7dc3b…aa53` 與 `90bd8380…b1ab`。
- 由終態 indexed framebuffer 與安全矩形外色盤重建無覆繪 RGBA：2×／3× 差異分別只有
  90／65 個原版像素位置，全在 `x=0..135,y=192..199` 終態提示安全矩形；
  動態姓名列 `y=16..23` 零差異。

原版、savestate、scratch、字型、RGBA 與收據都只留在被忽略的 `workplace/`。
