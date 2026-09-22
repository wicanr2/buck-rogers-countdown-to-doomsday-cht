# 第一百零八階段：第三頁固定劇情 DRAFT catalog

日期：2026-09-22
狀態：**DRAFT；已取得五筆固定劇情 glyph-run identity 與 DRAFT 繁中候選，尚未接 runtime。**

## 範圍與證據

本階段從 phase104 成功返回後的 280M state，以正常 BIOS Enter 於 `281000000`、`291000000`
各送入一次，重生第三頁畫面。第二次 Enter 後底部固定敘事為 row `17–21` 五行；row `24`
狀態列與其他動態欄位排除。兩次相同重播的 content-safe 收據只保留長度／SHA-256、caller、
guard、色號、座標與步數；glyph bytes、原文全文、state、PNG 與輸入排程均留在被 Git 忽略的
`workplace/phase108-page3/`。

既有 page3 基準 PNG `phase104-post-return-enter-3/baseline.png` 的 SHA-256 為
`9f87cb573aaf19ba3f403acf46071ae4c3059b22a26e8c058c0c4a8bebc78150`；兩次新生的
content-safe receipt SHA-256 均為
`d2a34cf8f1ca399b885cd2ea2b131a698345610508db7de7580d31e7ee58dd3e`，且逐 byte 相同。

五行 exact identity 已寫入 `text/story-page3-events.tsv`，全部是
`0763:04FF` caller、`0763:026B` guarded glyph、背景 0／前景 10、欄 1。row 24 的
`14321:0823`、背景 15／前景 0 status glyph 不得混入 catalog。

## DRAFT 繁中候選與證據分級

`text/story-page3.zh-TW.tsv` 的五行候選為：

1. 「你們坐進不舒服的椅子，」
2. 「焦急地想儘快完成此事並」
3. 「離開。先前的喧鬧聲逐漸」
4. 「平息，房間的燈光也逐漸」
5. 「熄滅。」

這五行是依第三頁原版畫面語意所作的 editorial DRAFT，並非中文手冊逐字摘錄；目前沒有
找到該段劇情在中文手冊的固定翻譯。因此 TSV 逐行使用 `runtime-editorial`，明確表示
它是正常 runtime 路徑的編輯性暫譯，不是手冊來源。尚未確認的英文標點／分句不進 catalog
identity，只以已確認畫面行序與 DRAFT 語意保留。

## 驗證與限制

`tools/story_page3_catalog.py` 以 exact identity、順序、caller／guard、顏色、row、步數、
NFC、控制／格式字元與雙向 key 驗證。文字寬度使用 DRAFT 的保守 ETen 近似：全形／寬字元
2 個原版 8px 格、其他字元 1 格，故事區上限 39 格；不是 runtime 實測 advance。
目前五行分別為 22、22、22、22、6 格，均在 39 格內。

以全部 14 份 `text/*.zh-TW.tsv`（包含 page3 DRAFT）在 Docker 內重建 ETen 候選字型，
builder 回報 `GOLEMFNT` 16×16、990 個 glyph，沒有缺字；候選檔只留在被忽略的
`workplace/phase108-font/`。輸出 SHA-256 為
`21613e029ad4754d87fc5fbfdc5fb1100417009063e3422197ec804e17193f9e`，character-list
SHA-256 為 `c1949bbe74ee39f0f5928acdc3941917fb4ad5c8897386c9311840f81a8c0920`；這只是
DRAFT 字型涵蓋證據，不代表 runtime 已接通或可公開散布。

本階段不建立 production dispatcher hook、不宣稱第三頁已中文化；需待 READY 審查、實際
文字安全矩形、字型回讀、轉場失效與 2×／3× 同狀態 A/B 後才能接 runtime。
