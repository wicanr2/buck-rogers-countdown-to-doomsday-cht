# 第一百零七階段：第二頁固定劇情 DRAFT catalog

日期：2026-09-22
狀態：**DRAFT；已取得四筆固定劇情 glyph-run identity 與 DRAFT 候選譯文，尚未接 runtime。**

## 範圍與證據

本階段承接 phase104 成功返回後的正常 BIOS Enter 路徑，僅收錄第二頁底部固定敘事區
row `17–20` 的四行；row `24` 是動態狀態列，明確排除。完整 glyph bytes、原文全文、
輸入排程、state 與 PNG 只留在被 Git 忽略的 `workplace/phase105-story-page-clear/`。

`story-page-2-full.json` 由兩次相同起點／同一 Enter 重播得到，四行均為
`0763:04FF` caller、`0763:026B` guarded glyph primitive、背景 0／前景 10、欄 1，
其 identity 已寫入 `text/story-page2-events.tsv`；row 24 的 `14321:0823`、背景 15／前景 0
status glyph 不得混入此 catalog。

## DRAFT 繁中候選與術語分級

`text/story-page2.zh-TW.tsv` 的四行候選為：

1. 「作為新進隊員，NEO 已帶你們前往」
2. 「奇亞貢太空港接受訓練。」
3. 「抵達後不久，你們」
4. 「便被召集到講堂。」

「NEO」沿用中文手冊 `SCAN0352_004.jpg`（SHA-256
`08b8504eb4b9adffb0f8b165b157d893040d86b06b121d09977eda531c7c5a6c`）的「新地球組織（NEW
EARTH ORGANIZATION, NEO）」。目前沒有找到中文手冊原圖直接使用「太空港」對應本頁
`spaceport` 的證據，因此「太空港」只是依遊戲語境作的 editorial DRAFT，不宣稱沿用手冊
固定譯名。`奇亞貢` 是從 page2 原版固定專名所作的 DRAFT 音譯，中文手冊目前沒有找到
逐字對應，故不升級為已證實術語。TSV 只有含 NEO 手冊術語的第一行使用
`manual-term-editorial`；其餘三行使用 `runtime-editorial`，明確表示都是 DRAFT 意譯，
不把 page2 敘述冒稱為手冊逐字來源；
「訓練／講堂」是依本頁英文語意的 editorial DRAFT，不是手冊逐字摘錄。

## 驗證與限制

`tools/story_page2_catalog.py` 以 exact identity、順序、caller／guard、顏色、row、步數、
NFC、控制／格式字元與雙向 key 驗證。文字寬度使用目前 DRAFT 的保守 ETen 近似：全形／寬
字元 2 個原版 8px 格、其他字元 1 格，故事區上限 39 格；不是 runtime 實測 advance。
目前四行分別為 28、22、16、16 格，均在 39 格內。

以全部 13 份 `text/*.zh-TW.tsv`（包含 page2 DRAFT）在 Docker 內重建 ETen 候選字型，
builder 回報 `GOLEMFNT` 16×16、981 個 glyph，沒有缺字；候選檔只留在被忽略的
`workplace/phase107-font/`。輸出 SHA-256 為
`49461a32b88408b02cc8f2d148fc805a2235e064937e21d67844c711d427d2d6`，character-list
SHA-256 為 `6ccb159bb1954c7dbfb5c74167307b18ccd724a4de78c9c310bcf10ad737fdca`；這只
是 DRAFT 字型涵蓋證據，不代表 runtime 已接通或可公開散布。

本階段不建立 production dispatcher hook、不宣稱第二頁已中文化；需待 READY 審查、實際
文字安全矩形、字型回讀、轉場失效與 2×／3× 同狀態 A/B 後才能接 runtime。
