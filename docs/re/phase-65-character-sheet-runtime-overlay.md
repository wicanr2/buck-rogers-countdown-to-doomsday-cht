# 第六十五階段：角色資料頁安全矩形與執行期繁中覆繪

日期：2026-09-21  
狀態：完成

## 結論

第六十四階段 35 個靜態 request 已接入 dosgolem 既有 `RuntimeMenuOverlay`。正式
`text/character-sheet-text-safe-rects.tsv` 對每個 event key 提供單列安全矩形；33 筆完全等於
原文字串範圍，只有 `AC` 與 `THAC0` 依同列 col 35 動態值左界作具名擴張。中文 `THAC 指數`
在真實 PNG 會逐字佔滿 CJK 格，故依中文手冊語意訂正為完整中文「命中指數」，不是縮寫或規則
改寫。

## 規格與實作

- dosgolem spec 038 先達 READY；實作 `LoadCharacterSheetOverlayRects`、
  `-character-sheet-rects` 與同 frame/palette `-baseline-rgba-out` 後，經驗收升為 CONFORMED。
- 一般 catalog 仍要求安全寬度等於 `OriginalLength*8`；只有兩個具名角色紙 key 可延伸，且右界
  必須恰為 logical x=280。缺任一 key、錯誤右界、catalog／rect 部分旗標均失敗即關閉。
- 74-glyph GNU Unifont 子集 SHA-256 為 `5949e5b2…b2dc`；正式 Git 不納入字型二進位。

## 正常路徑與決定性

權威 state、四次 Enter、`Y` 時點與停止點沿用第六十四階段。每種分支、倍率都從 fresh state
獨立執行兩次。

| 分支 | events／requests／misses | 2× JSON | 3× JSON |
| --- | --- | --- | --- |
| base | 118／43／75 | `bd22f043…7e8f5` | `01775430…a7c67` |
| `Y` | 149／52／97 | `9e91f700…0422e` | `ed735717…46717` |

四組同倍率 JSON、RGBA、baseline RGBA 與 raw framebuffer 都各自逐 byte 相同；43／52 actions
逐筆等於 requests，技能重畫使用 replace，終態只有 35 個唯一 active keys。base／`Y` raw
framebuffer 分別保持 `1f3b8194…d4dd`／`03d9bf1f…0f97`。

## 像素與人工檢視

- 2×：安全矩形內 18,379 個差異像素，外部 0。
- 3×：安全矩形內 37,048 個差異像素，外部 0。
- 原始解析度 PNG 已確認「命中指數」、屬性／技能列、金框與底部 `ES` 回答均未裁切或重疊。

終態 palette 將原版動態值使用的色號 15 映成黑色；同 frame/palette 的未覆繪 baseline 也完全
相同，且 base／`Y` baseline RGBA 相同，雖然兩者 raw indexed framebuffer 不同。這是目前
dosgolem 原版 palette／終態可視性限制，不是中文安全矩形清除造成；矩形外零差異與 raw
framebuffer 不變已證明顯示語意隔離。本階段不把動態值可讀性或 palette parity 宣稱完成。

## 邊界

本階段仍未替使用者選定 2×／3×，也未處理手冊版面。只有角色資料／重擲頁的 35 個靜態欄位
可稱為已接通玩家可見繁中覆繪；後續技能配置、冒險、戰鬥與其他文字路徑仍需各自證據。
