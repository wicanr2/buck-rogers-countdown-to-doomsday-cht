# 文字目錄

本目錄保存 UTF-8 繁體中文顯示文字；鍵值只供 dosgolem 輸出端覆繪查詢，不得回寫原版
記憶體、規則、驗證答案或存檔。原版完整字串清冊與受著作權保護素材不納入 Git。

目前 `menu.zh-TW.tsv` 僅是第八階段已由正常玩家路徑及中文說明書共同證實的 DRAFT。
`menu-events.tsv` 以事件鍵、正式文字鍵、原文長度／SHA-256、caller、色號與文字格座標保存
同一路徑的九筆 typed identity；不保存原文全文。`tools/menu_events.py` 驗證 schema、順序、
唯一性、bounds 與 `menu.zh-TW.tsv` 雙向覆蓋。
`post-race-events.tsv` 保存選定預設種族後性別畫面的四筆 content-safe identity；這些事件
已由 `gender-events.tsv` 接入繁中 request，但尚未加入正式 renderer。`tools/post_race_receipt.py` 會把它
與既有選單 inventory、固定雙 Enter 收據及終點 framebuffer 一起驗證。
`gender-selection-events.tsv` 保存性別畫面 Down→Up 四筆與 Escape 八筆生命週期 identity；
`tools/gender_selection_receipt.py` 以兩條各自重播兩次的收據驗證精確排程、事件與終點畫面。
返回功能選單的不同 identity 只保存語意位置，不以相似語意模糊擴張 catalog。
`gender-events.tsv` 將其中七個唯一性別 identity 接到 `gender.zh-TW.tsv` 的「選擇性別／男性／
女性」；`tools/gender_events.py` 反查前兩份證據表並要求事件與譯文鍵雙向完整。提示中的
「性別」由中文說明書 `SCAN0352_005.jpg` 原圖核對，男性／女性則明示為標準介面譯詞，
不冒稱手冊逐字摘錄。
`post-gender-events.tsv` 保存接受預設性別後職業選擇畫面的七筆 content-safe identity；
`class-events.tsv` 再與 `class-selection-events.tsv` 交叉核對，形成十個唯一職業 identity，
並接到 `class.zh-TW.tsv` 的「選擇職業／太空船駕駛員／戰士／醫生／工程師／流浪漢」。譯名
由中文說明書 `SCAN0352_007.jpg` 至 `SCAN0352_009.jpg` 原圖核對；目前只產生 runtime request，
尚未接入正式 renderer。
`gender-text-safe-rects.tsv` 與 `class-text-safe-rects.tsv` 逐筆由 exact identity 的 row、column
及 original length 導出 logical 320×200 清除矩形、anchor 與單列容量；Phase 41 已用四個真實
framebuffer 驗證 2×／3× 都零缺字、零重疊且安全矩形外零差異，但仍只是離線 prototype。
`post-class-events.tsv` 是確認預設職業後角色資料／重擲畫面的 96 筆 content-safe 清冊；它區分
靜態標籤、動態值與重畫事件，不是可直接逐列翻譯的 catalog。
`reroll-yes-events.tsv` 與 `reroll-no-events.tsv` 分別保存正常 `Y` 重擲及 `N` 接受分支的新事件；
能力值與轉場重畫只供生命週期比對，不得當成固定譯文。
`name-edit-events.tsv` 與 `name-confirm-events.tsv` 保存短測試姓名的回顯及確認後技能配置畫面
identity；玩家輸入不是譯文，Backspace 的直接像素清除則由 framebuffer 收據驗證。
`manual-questions.tsv` 是原版 39 筆可抽題的頁碼、標題與序數清冊，不含答案；可由
`tools/manual_questions.py` 對執行期 `0EC0:0000` 資料段重生。`manual.zh-TW.tsv` 只收錄
已唯一核對中文掃描來源並回到原圖校字的段落，目前共有 22 筆。

`manual-ordinals.tsv` 保存原版 1–10 序數詞、runtime 位址與完整 19-byte slot；可由同一份
執行期資料段透過 `tools/manual_ordinals.py` 重生。它只橋接題目顯示身分，不含答案。

`manual-source-crosswalk.tsv` 逐筆記錄題目對應掃描、archive-order、SHA-256、印刷頁、
中文錨點與證據等級。它是來源索引，不是可直接顯示的譯文 catalog；OCR 未經逐字校訂的
內容不得搬入 `manual.zh-TW.tsv`。可用下列命令搭配本機解壓清冊驗證：

```sh
python3 tools/manual_crosswalk.py text/manual-questions.tsv text/manual-source-crosswalk.tsv \
  --manifest workplace/inventory/manual-extracted-manifest.json
python3 tools/manual_catalog.py text/manual-questions.tsv text/manual-source-crosswalk.tsv \
  text/manual-events.tsv text/manual.zh-TW.tsv
python3 tools/manual_ordinals.py workplace/probe/phase12-manual-runtime-0EC0_0000.bin \
  text/manual-ordinals.tsv --events text/manual-events.tsv
python3 tools/menu_events.py text/menu-events.tsv text/menu.zh-TW.tsv
python3 tools/menu_receipt.py workplace/phase27/menu-receipt.json \
  text/menu-events.tsv text/menu.zh-TW.tsv
```

`manual-events.tsv` 是 DRAFT 事件映射：只允許來源為 `confirmed` 的題目，以頁碼、英文標題及
序數精確指向一筆文字鍵。它不含英文答案，也不會送鍵或改寫原版記憶體。

## 驗證與 prototype 字型

以下命令必須在專案規範要求的隔離 Docker 容器內執行：

```sh
python3 tools/catalog_font.py lint text/menu.zh-TW.tsv
python3 tools/catalog_font.py chars text/menu.zh-TW.tsv --out font/characters.txt
python3 tools/catalog_font.py build text/menu.zh-TW.tsv \
  --font /inputs/unifont.hex.gz \
  --out workplace/font/menu-unifont16.golemfnt
```

`lint` 失敗即關閉地驗證 UTF-8、精確標頭及欄數、唯一 key、非空譯文、來源枚舉、控制／
格式字元與 NFC。`chars` 依 Unicode 碼點排序，每行固定為 `U+XXXX<TAB>字元`；字型建置若
缺任一字模、遇到非 8×16／16×16 字模或格式錯誤便中止。
