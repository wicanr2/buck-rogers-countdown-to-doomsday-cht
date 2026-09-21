# 第六十八階段：角色姓名提示執行期繁中覆繪

日期：2026-09-21  
狀態：完成

## 結論

姓名固定提示已在 dosgolem 輸出端以「角色姓名：」覆繪；玩家姓名仍由原版輸入與顯示路徑
處理。2×／3× 均需明示，本階段沒有選定產品預設倍率。

## 幾何證據

- 提示事件：row 24／column 0／長度 16，原版範圍 `[0,128)×[192,200)`，已證實。
- 玩家第一個字元：row 24／column 17，即 x=136；提示右界與輸入欄間隔 8 pixels，已證實。
- 正式 rect SHA-256：`f04f3eddd44d8402dcd80cfe2f0f5d87d1b8cff44dd84a9f91f4dae06ce0ec13`。
- GNU Unifont 子集 SHA-256：`aa53cc31dd2a17fc5554792d3767c1cef757ecda69326c4d17643d211f4d0ea1`。

## 同狀態收據

| 路徑 | events／requests／misses | 2× JSON | 3× JSON | 矩形內差異 2×／3× |
|---|---:|---|---|---:|
| base | 183／1／182 | `343de86f…fb920` | `f50c5c27…73a92` | 941／2,038 |
| 輸入 `A` | 184／1／183 | `bee63ca2…d601` | `6a05c934…24b16` | 941／2,038 |

四組各重跑兩次，JSON、RGBA、baseline 與 raw framebuffer 均逐位元一致；presentation 欄位
以外的 JSON 等於第六十七階段 control。矩形外差異為 0，玩家輸入欄 x≥136 差異亦為 0。
原始解析度 2×／3× 圖已人工確認提示完整、金框不受影響且 `A` 可見。

## 實作邊界

dosgolem 新增 name-prompt rect 旗標及 catalog／rectangle 雙向 event-key coverage 驗證。這只
影響輸出 RGBA；不寫 VRAM、palette、姓名 buffer、輸入或存檔。本收據不涵蓋 Enter／Escape
離開姓名畫面後的 overlay 失效，後續須沿正常路徑另行驗證。
