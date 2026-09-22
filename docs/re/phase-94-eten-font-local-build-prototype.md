# 第九十四階段：倚天字型本機建置與對齊 prototype

日期：2026-09-22
輸入權利分類：使用者已購買、明確授權放入**本機遊戲**的第三方字型；僅限本機使用，不進 Git、GitHub、Release 或公開封包。

## 目的與方法

本收據只比較真實倚天 15 點字模填入現有 16×16 手冊格時的上下補列位置。它不是公開散布、
正式解析器（parser）、執行期掛鉤（runtime hook）或玩家路徑中文化收據。

在 `python:3.12-slim`／`golang:1.24-bookworm` 的一次性、無網路 Docker 容器內，以使用者 UID/GID：

1. 對 spec 007 固定雜湊的 `STDFONT.15`、`SPCFONT.15`、`ASCFONT.15` 做 Big5 分區查找，重生正式
   `manual.zh-TW.tsv` 的 691 個 Unicode 碼點；ASCII 的 8-bit 列依既有 16-bit 版面置於 x=4..11。
2. 將每個 16×15／8×15 source row 組成兩份 16×16 本機 `GOLEMFNT`：`bottom-pad`（第 16 列置底）與
   `top-pad`（第 16 列置頂）。每份立即以 header、總長、691 key、tag 與 32-byte glyph 全量回讀。
3. 由被忽略的 `phase12-before-question.state` 從 #266,399,999 重生到 #266,557,247；不注入鍵盤或
   答案，取得既有已證實的 `34 / Deimos Prison / tenth` request，再以 `RuntimeManualOverlay` 繪製 2×、3×。
4. 每張以未改的原版 indexed VRAM 建立 RGBA 基準（baseline），驗證差異（diff）僅在正式清除矩形
   （clear rectangle）內。

所有 binary、PNG、JSON、重生器與原版 framebuffer 只寫入被忽略的 `workplace/phase94/`；本文件不保存
字模 bytes、手冊全文、原版畫面或可散布 font。

## 結果

| 項目 | 分級 | 收據 |
| --- | --- | --- |
| 本機使用權利 | 已證實（使用者授權範圍） | 使用者於本對話確認先前購買的倚天字型可直接放入本機遊戲；未擴張為公開再散布許可。 |
| `bottom-pad` 字型 | 已證實 | 16×16、691 glyph、25,583 bytes、SHA-256 `4ea9692120712c5666de359e84ff855e668e82086aae2d9dc23fa1096b790a84`。 |
| `top-pad` 字型 | 已證實 | 16×16、691 glyph、25,583 bytes、SHA-256 `78c10dec8055110764013007899c4455b91256a78f94e212294ac9c51c01364e`。 |
| 原版基準 state | 已證實 | VRAM SHA-256 `d53948dc2a75e255691e5c44287fe2e76cf7a630196f6d1546ac18c4730bd495`；palette SHA-256 `045796505f7ec3115cec8632ca7a29e6391687a2a013198e38dd68dd5b3564eb`。 |
| 兩個變體（variant）的 2×／3×字模覆蓋 | 已證實 | 四張 `RuntimeManualOverlay` 預覽皆缺字 0，清除矩形外差異 0。 |
| 上下對齊的產品選擇 | 未知／待使用者決定 | 兩案僅差 source 第 16 列的垂直位置；不可由 bit coverage 或 agent 偏好代替使用者選定。 |
| 正式前景色來源 | 未知 | 正文安全區在這個原版狀態（state）是全黑；為使純對齊預覽可見，只在 `Frame` 的拷貝每行放入原版題目區的色盤索引 10，`Draw` 基準未改。這不是正式色彩策略或同狀態繪製器（same-state renderer）收據。 |

## 結論

本機候選的資料、格式、全量 coverage 與 2×／3× safe-rectangle 均已通過，足以供使用者依畫面選擇
`bottom-pad` 或 `top-pad`。但未選定前，轉換規格維持 DRAFT；正式解析器（parser）、前景色來源、命令
（command）／迴圈（loop）接線及正常玩家 A/B 仍不可宣稱完成。
