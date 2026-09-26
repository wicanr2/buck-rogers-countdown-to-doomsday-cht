# 文字目錄

本目錄保存 UTF-8 繁體中文顯示文字；鍵值只供 dosgolem 輸出端覆繪查詢，不得回寫原版
記憶體、規則、驗證答案或存檔。原版完整字串清冊與受著作權保護素材不納入 Git。

`host-ui.zh-TW.tsv` 保存玩家視窗的「設定／套用／取消／2×／3×」正式文案；這是
host 輸出端介面文字，不是原版 DOS 字串。字型子集必須一併納入；正式前端須從該檔
載入或以其雜湊固定同一組字串，不能另維護可漂移的文案副本。

目前 `menu.zh-TW.tsv` 僅是第八階段已由正常玩家路徑及中文說明書共同證實的 DRAFT。
`menu-events.tsv` 以事件鍵、正式文字鍵、原文長度／SHA-256、caller、色號與文字格座標保存
目前已收錄的 21 筆 typed identity（主選單 10 筆、種族相關 11 筆）；13 筆是譯文鍵數，
不是事件數。不保存原文全文。`tools/menu_events.py` 驗證 schema、順序、
唯一性、bounds 與 `menu.zh-TW.tsv` 雙向覆蓋。
`post-join-menu-events.tsv` 與 `post-join-menu.zh-TW.tsv` 另存加入一名角色後，正常從名冊的
EXIT 返回功能選單所見七項固定文字。事件身分由雙重原版重播與私有畫面逐列核對，原文
只以長度／SHA-256 保存；七筆編輯性譯文已於 spec 018 限縮 READY 審查固定。
本機 dosgolem fork 已以正式 catalog loader／watcher／presenter 做選單七列的
2×／3× 局部同狀態 A/B；後續[第一百九十五階段](../docs/re/phase-195-post-join-menu-prewrite-runtime-receipt.md)
另以正式逐寫入收據驗證七列 active→empty 與 row 20 普通回寫前清層，
因此**僅固定七列路徑限縮 CONFORMED**。真正 Exit、選單重入及存讀檔
仍未驗，不能將此結論擴張成整體選單完成。較早局部收據見
[第一百八十二階段](../docs/re/phase-182-post-join-menu-runtime-ab-partial.md)。
其中「加入遊戲」與「顯示角色所屬遊戲」只依原文字面翻譯，選項真正的遊戲語意仍未知；
不得擅自改譯為加入隊伍或存檔。上方角色姓名／數值及已收錄的鄰項不在這七筆內；
七項的選取反白變體另列 `post-join-menu-variants.tsv`。可用 `tools/menu_events.py`
對基本事件與譯文驗證 schema 與 key 雙向覆蓋；
後續[第一百六十一階段](../docs/re/phase-161-post-join-menu-selection-and-exit.md)已量到七項
普通／反白重畫與一條當時誤判為 `EXIT TO DOS` 的全選單清除；
[第一百八十三階段](../docs/re/phase-183-post-join-exit-identity-corrigendum.md)以原版
bytes 訂正：該 Enter 前選中的是 row 12 `Create New Character`，真正 row 21
`Exit to DOS` 是兩次確認後才退出。完整 A000 observer 的失效勘誤及
限縮 READY 見[第一百八十階段](../docs/re/phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)與
[spec 018](../docs/spec/018-post-join-menu-overlay-draft.md)。不能用舊 row 12
清除收據替真正 Exit 或其他選項背書。
`post-join-menu-variants.tsv` 以同一七筆的長度／SHA-256、caller、配色與格座標展開
21 筆初畫普通／普通回寫／反白 exact identity；不保存原文。它包含 row 20 在移向
未收錄 row 21 時的普通回寫，因此 production candidate 必須在這一筆後原子失效，
不得假定 `EXIT TO DOS` 的稍後清除仍能清除作用中 generation。此表已固定為限縮
READY fixture，且已作為本機 fork 正式 runtime loader 輸入；固定七列的
逐寫入清層驗收見第一百九十五階段，不代表未收錄 row 21 的真正 Exit 已中文化。
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
`name-prompt-events.tsv` 只收錄接受重擲後唯一的 16-byte 靜態姓名提示 exact identity，
`name-prompt.zh-TW.tsv` 將它顯示為「角色姓名：」。玩家輸入回顯不在 catalog；
`tools/name_prompt_catalog.py` 反查 `reroll-no-events.tsv` 並拒絕 identity、來源或文字治理漂移。
`name-prompt-text-safe-rects.tsv` 將原版 16-byte 提示範圍固定為 `[0,128)×[192,200)`；
`tools/name_prompt_text_safe_rects.py` 另以 `name-edit-events.tsv` 證實玩家輸入從 x=136 開始，
禁止安全矩形侵入動態姓名欄。
`career-skill-selection-events.tsv`、`career-skill-add-events.tsv` 與
`career-skill-refusal-events.tsv` 保存技能列下移、一次合法加點，以及仍有點數時 Escape→`N`
拒絕離開的 content-safe identity；動態數值與原版提示全文不列為譯文。
`career-skill-screen-events.tsv` 從姓名確認與 Down 清冊收錄四個固定標題、八個一般技能列及
兩個已證實的 selected variants；`career-skill-screen.zh-TW.tsv` 的技能譯名必須逐筆等於
角色資料正式 catalog。未收錄的選取 variant 與所有點數仍維持 miss。
`career-skill-screen-text-safe-rects.tsv` 以每個 exact event 的原文長度限定單列矩形；
技能列右界最遠 x=136，points／bonus／total 從 x=184／232／280 開始。
`tools/career_skill_screen_text_safe_rects.py` 驗證矩形、容量與動態欄零侵入。
`technical-skill-screen-events.tsv` 從職業技能離開清冊與技術技能 Down 清冊收錄
17 個不重複 exact identities：兩個專屬標題、13 個一般技能列與前兩列 selected variants。
「單項技能上限」與「點數／加值／總計」和職業技能頁是同一 identity，由 career catalog 共享，
不重複定義。`technical-skill-screen.zh-TW.tsv` 的 13 個技能譯名逐筆來自中文手冊
`SCAN0352_012.jpg` 第 19–20 頁原圖；動態點數與未實測 selected variants 仍維持 miss。
`technical-skill-screen-text-safe-rects.tsv` 以 17 個 technical exact events 的原文範圍建立單列
矩形；兩個共享標題直接沿用 career rectangles。`tools/technical_skill_screen_text_safe_rects.py`
驗證雙向 coverage、容量與 x=184 points 欄零侵入。
`career-skill-subtract-events.tsv` 與 `career-skill-exit-events.tsv` 保存先加後減的可逆重畫，
以及 Escape→`Y` 的確認提示與技術技能配置終點；Right 本身沒有文字事件，其動作語意由後續
重畫和逐 byte 畫面還原共同證實。
`technical-skill-selection-events.tsv`、`technical-skill-subtract-events.tsv`、
`technical-skill-refusal-events.tsv` 與 `technical-skill-exit-events.tsv` 保存技術技能列下移、
加後減、Escape→`N` 回復及 Escape→`Y` 進入身體圖示選擇的 exact identity；不含動態點數
或原版提示全文。
`skill-exit-confirmation.zh-TW.tsv` 另收錄職業／技術技能頁 Escape 離開確認的兩句
繁中譯文：原句 bytes 與既有事件 SHA 已逐筆核實，沿用正式技能頁術語。
後續已接正式 watcher／presenter，職業、技術各一個合法固定起點的
Escape→N／Y 在 2×／3× 通過本體像素及無殘層 A/B，僅此無頭路徑
限縮 CONFORMED；六格多色原版尾碼不覆繪。存讀檔、Restore bridge、
冷開機及視窗未驗，見[第二百零二階段](../docs/re/phase-202-skill-exit-runtime-ab.md)。
原句勘誤見[第一百九十一階段](../docs/re/phase-191-skill-exit-confirmation-translation-draft.md)。
`post-join-exit-prompt.zh-TW.tsv` 保存加入角色後真正 Exit 確認畫面的兩句繁中譯文；
`post-join-exit-prompt-events.tsv` 保存其原版 step、caller、色彩、座標與長度／SHA-256 身分，不含原文全文。
正式 watcher／presenter 已在固定合法加入角色存態的 N／Y→Y 路徑完成本體
2×／3× 同狀態 A/B，僅此範圍依[規格 021](../docs/spec/021-post-join-exit-prompt-body-only-draft.md)
限縮 CONFORMED；原版六格多色尾碼不覆繪，其他玩家路徑與 Linux 視窗未驗。
`body-icon-events.tsv` 與 `body-icon.zh-TW.tsv` 沿用第四十八階段移動／拒絕／確認的正常
玩家 trace，整理身體圖示畫面的七筆固定介面文字；`tools/body_icon_catalog.py` 會回查三份
既有事件清冊、驗證容量與雙向 coverage。`body-icon-text-safe-rects.tsv` 依同一 exact
identity 建立七筆 logical 安全矩形，並以 `tools/body_icon_text_safe_rects.py` 驗證同一畫面
群組內不重疊。後續 dosgolem 已將七筆固定文字接入正式 runtime；固定 move／refuse／confirm
的雙倍率同狀態與清除生命週期已限縮驗收，見
[`spec 009`](../docs/spec/009-body-icon-overlay-draft.md)。其他路徑仍待證據。
`skill-action-bar-events.tsv` 保存職業／技術技能頁底部五個操作標籤的長度、
SHA-256、逐字 caller、幾何與一般／焦點色彩。這些標籤經 `0763:026B`
的低階字元路徑，不是現有高階 dispatcher 事件；disabled 狀態尚未觀測，固定為
`unknown`。`tools/skill_action_bar_events.py` 會拒絕身分、幾何、色彩或證據分級漂移。
Phase 75 已由 dosgolem guarded glyph watcher 將此清冊接成 typed events；
`tools/skill_action_bar_runtime_receipt.py` 驗證八條正常路徑的雙重播、exact identity、
0 miss／drop、watcher／control 語意一致與 framebuffer 零差異。此階段仍只有事件，
尚未覆繪。`skill-action-bar.zh-TW.tsv` 以 editorial 的 `runtime-interface` 來源保存
「加點／減點／上頁／下頁／完成」五個繁中介面詞；`tools/skill_action_bar_catalog.py`
固定 UTF-8／NFC、來源與事件雙向覆蓋，不冒稱中文手冊逐字譯名。
`skill-action-bar-text-safe-rects.tsv` 將 8 個畫面配置展開為 16 個 normal／focus exact keys；
矩形只使用已證實的 `y=192..200`，同一 action 的 variant 共用幾何。
`tools/skill_action_bar_text_safe_rects.py` 拒絕缺漏、孤兒、幾何／容量漂移與同畫面跨 action
重疊；配色不屬於矩形資料。
本機 dosgolem fork 已將五筆譯文接到正式 `RuntimeActionBarOverlay`；
短譯文後的原版英文殘字現以完整核准矩形清底修正。八條固定操作路徑、
一條技術頁 Escape→Y 離頁在 2×／3× 的控制組同狀態 A/B 僅限縮
CONFORMED，見[第二百零四階段](../docs/re/phase-204-action-bar-runtime-conformance.md)。
disabled、未量重入、存讀檔、冷開機及 Linux 玩家視窗不在此結論內。
`manual-questions.tsv` 是原版 39 筆可抽題的頁碼、標題與序數清冊，不含答案；可由
`tools/manual_questions.py` 對執行期 `0EC0:0000` 資料段重生。`manual.zh-TW.tsv` 現有
39 筆題目專用繁中說明段落，全部保持 504 字內；這是遊戲內的段落意譯，不是整章手冊
逐字轉錄。37 題對照本機中文掃描，`More on Abilities` 與 `Roll.` 因中文對應頁缺失，
直接依原版英文手冊翻譯並在 `manual-english-sources.tsv` 留下 URL、原書定位及本機快照
SHA-256；不把這兩題冒充中文掃描來源。原版答案、判定和手冊全文均不在 TSV 中。

`manual-overlay-layout.tsv` 是保留原版頁碼、標題與序數時唯一的正式正文幾何：只清除
`[7,312)×[72,184)`，以 x=16、y=72 的 36 欄×14 行格顯示，單頁容量固定為 504 字。
`tools/manual_overlay_layout.py` 會把 schema、矩形、格線、容量與 `manual.zh-TW.tsv` 一起
失敗即關閉驗證；這不是 presenter，也不改寫原版題目或答案流程。

`manual-ordinals.tsv` 保存原版 1–10 序數詞、runtime 位址與完整 19-byte slot；可由同一份
執行期資料段透過 `tools/manual_ordinals.py` 重生。它只橋接題目顯示身分，不含答案。

`manual-source-crosswalk.tsv` 逐筆記錄題目對應掃描、archive-order、SHA-256、印刷頁、
中文錨點與證據等級；沒有中文掃描的兩題由 `manual-english-sources.tsv` 獨立記錄英文原書
證據。兩表都是來源索引，不是可直接顯示的譯文 catalog；OCR 未經校訂的內容不得搬入
`manual.zh-TW.tsv`。可用下列命令搭配本機清冊與被忽略的英文來源快照驗證：

```sh
python3 tools/manual_crosswalk.py text/manual-questions.tsv text/manual-source-crosswalk.tsv \
  --manifest workplace/inventory/manual-extracted-manifest.json \
  --english-sources text/manual-english-sources.tsv \
  --english-snapshot workplace/buckrogers-original-manual-english.html
python3 tools/manual_catalog.py text/manual-questions.tsv text/manual-source-crosswalk.tsv \
  text/manual-events.tsv text/manual.zh-TW.tsv
python3 tools/manual_overlay_layout.py text/manual-overlay-layout.tsv text/manual.zh-TW.tsv
python3 tools/manual_ordinals.py workplace/probe/phase12-manual-runtime-0EC0_0000.bin \
  text/manual-ordinals.tsv --events text/manual-events.tsv
python3 tools/menu_events.py text/menu-events.tsv text/menu.zh-TW.tsv
python3 tools/menu_receipt.py workplace/phase27/menu-receipt.json \
  text/menu-events.tsv text/menu.zh-TW.tsv
```

`manual-events.tsv` 是精確事件映射：只允許來源為 `confirmed` 的題目，以頁碼、英文標題及
序數精確指向一筆文字鍵。它不含英文答案，也不會送鍵或改寫原版記憶體。

`story-opening-events.tsv` 與 `story-opening.zh-TW.tsv` 是首屏劇情五行的 READY catalog：
保存 `0763:04FF`／`0763:026B`、row 17–21、原文長度與 SHA-256，不保存原文全文；
繁中譯文依中文手冊 `SCAN0352_003.jpg`–`SCAN0352_004.jpg` 印刷頁 1–3 的「巴克羅吉斯」
、「新地球組織（NEO）」與「美蘇貿易聯邦（RAM）」用語建立。`tools/story_opening_catalog.py`
驗證五筆 identity、譯文雙向覆蓋、NFC、控制／格式字元與 39 格資料層上界；
首屏五行已接 dosgolem runtime 並通過 2×／3× 同狀態 A/B 及 Enter 轉頁失效驗證；
完整開機玩家路徑與存讀檔仍未驗；規格 010 僅在固定首屏五行與已量 Enter 離頁
限縮 CONFORMED，不外推整款遊戲已中文化。
`story-page2-events.tsv` 的四筆固定敘事 identity 已依 spec 011 審核為 `confirmed/READY`；
`story-page2.zh-TW.tsv` 的文字屬編輯性譯文，已於已量原版畫面完成 2×／3× A/B 驗收；
`tools/story_page2_catalog.py` 另外驗證 row 17–20、排除 row 24 動態狀態列與 39 格保守容量，
正式 dosgolem runtime 已接第二頁四行與合法 Enter 離頁失效，限縮驗收見
[`docs/re/phase-141-story-page2-runtime-conformance.md`](../docs/re/phase-141-story-page2-runtime-conformance.md)。
Chiagong 的「奇亞貢」仍只是未由中文手冊逐字確認的編輯性音譯。
`story-page3-events.tsv` 是第三頁五行固定敘事的 READY 身分目錄；`story-page3.zh-TW.tsv` 仍是編輯性譯文；
`tools/story_page3_catalog.py` 驗證 row 17–21、排除 row 24 動態狀態列與 39 格保守容量。
第三頁五行依原版畫面語意翻譯，已接正式 dosgolem runtime；
[`docs/re/phase-144-story-page3-runtime-conformance.md`](../docs/re/phase-144-story-page3-runtime-conformance.md)
僅對同一合法 state 的五行與已量 Enter 離頁給出雙倍率限縮驗收。
`tools/story_page3_ab_verify.py` 是唯讀收據驗證入口：逐欄比對 control 與 2×／3×
原版欄位，並檢查覆繪差異只在五行安全矩形內；它不能取代正常玩家完整開機與存讀檔。
`story-page4-events.tsv` 是第四頁六行 READY 身分目錄，`story-page4.zh-TW.tsv` 保持編輯性
繁中候選；原先 `visual-transcription` 的前五筆身分已被兩次合法 Enter 的低階 glyph trace
否定並訂正。`tools/story_page4_catalog.py` 驗證 exact hash、caller／guard、步數、幾何、READY
狀態與翻譯容量。後續正式 runtime 已完成雙倍率同狀態 A/B、轉頁失效與失敗即關閉
驗證；規格 013 僅在固定六行及已量 Enter 離頁限縮 CONFORMED。
`story-page5-events.tsv` 與 `story-page5.zh-TW.tsv` 是第四頁後合法 Enter 所見的
第五頁下方五行固定敘事 READY；`tools/story_page5_catalog.py` 驗證低階 glyph
length／hash、caller／guard、row 17–21、39 格容量與 READY 狀態。右側人物姓名未納入此
catalog；後續正式 runtime 已完成雙倍率同狀態 A/B 與 page5→page6 清除，規格 014
僅在固定五行及已量 Enter 離頁限縮 CONFORMED。
`story-page6-events.tsv` 與 `story-page6.zh-TW.tsv` 是第五頁後合法 Enter 的第六頁下方六行
固定敘事；`tools/story_page6_catalog.py` 驗證低階 glyph 身分、譯文 key／來源、NFC、
控制字元與保守 39 格寬度。右側人物名與 row 24 狀態列排除；後續正式 runtime 已完成
雙倍率同狀態 A/B 與 page6→page7 清除，規格 015 僅在此固定路徑限縮 CONFORMED。
`story-page7-events.tsv` 與 `story-page7.zh-TW.tsv` 是第六頁後合法 Enter 所見的第七頁下方六行
固定敘事；`tools/story_page7_catalog.py` 驗證同狀態 glyph 身分與繁中格式。
右側人物名及 row 24 排除；後續正式 runtime 已完成雙倍率同狀態 A/B、合法 Enter 離頁
及失敗即關閉矩陣，規格 016 僅在固定六行與已量進出限縮 CONFORMED。
`story-page8-events.tsv` 與 `story-page8.zh-TW.tsv` 是第七頁合法終態後 Enter 所見的第八頁
下方四行固定敘事；事件檔只保存低階 glyph identity，不保存原文全文。右側人物姓名與
row 24 動態狀態列排除；後續正式 runtime 已完成雙倍率同狀態 A/B 與 Enter 離頁清除，
規格 017 僅在固定四行與已量進出限縮 CONFORMED。原版定位證據見
[`docs/re/phase-131-story-page8-enter-trace.md`](../docs/re/phase-131-story-page8-enter-trace.md)。
全部 19 份 catalog 的本機倚天子集為 1025 字模，dosgolem loader 對 6175 個譯文字元
檢查零缺字；這組字型清冊是早期靜態證據，正式中文覆繪 A/B 另見規格 017。
`story-page9-events.tsv` 與 `story-page9.zh-TW.tsv` 是第八頁合法終態後 Enter 的第九頁唯一
固定敘事行；只保存限縮 READY 的 content-safe identity 與繁中譯文，排除右側姓名、row 24 動態列。
全部 20 份 catalog 的本機倚天子集為 1026 字模，正式 loader 對 6182 個譯文字元
零缺字；這是第 134 階段的歷史靜態收據，當時尚未接 runtime 或完成 A/B。證據見
[`docs/re/phase-134-story-page9-enter-trace.md`](../docs/re/phase-134-story-page9-enter-trace.md)。
後續依私有原版畫面校訂第 5、7、8 頁三處譯文，在當時未改 event identity 或 DRAFT 狀態；
當時 20 份 catalog 重建後的本機倚天子集為 1024 字模，正式 loader 對 6179 個
譯文字元零缺字。上述 1026／6182 是校訂前的第 134 階段收據，不是目前字型產物。
再加入 post-join 選單七項 DRAFT 譯文後，當時 21 份 catalog 的本機倚天子集
重建為 1026 字模；這是新的字型需求，不是前述第 134 階段的同一份 1026 字收據。
後續七列已完成正式 runtime 局部 A/B，但完整生命週期尚待驗；見
[第一百八十二階段](../docs/re/phase-182-post-join-menu-runtime-ab-partial.md)。
第九頁單行後續已接正式 watcher／presenter，合法第八頁→第九頁的
control／2×／3× 入頁同狀態 A/B 已驗；自然離頁及清層後畫面仍未驗，
故[規格 022](../docs/spec/022-story-page9-overlay-draft.md)維持限縮 READY，
不能把單行入頁稱為整頁 CONFORMED。

## 驗證與 prototype 字型

以下命令必須在專案規範要求的隔離 Docker 容器內執行：

```sh
python3 tools/catalog_font.py lint text/menu.zh-TW.tsv
python3 tools/catalog_font.py chars text/menu.zh-TW.tsv --out font/characters.txt
python3 tools/catalog_font.py build text/menu.zh-TW.tsv \
  --font /inputs/unifont.hex.gz \
  --out workplace/font/menu-unifont16.golemfnt
python3 tools/catalog_font.py validate-candidate text/manual.zh-TW.tsv \
  --manifest workplace/phaseNN/input/candidate-manifest.json \
  --source workplace/phaseNN/input/candidate.hex.gz \
  --license workplace/phaseNN/input/COPYING
```

`lint` 失敗即關閉地驗證 UTF-8、精確標頭及欄數、唯一 key、非空譯文、來源枚舉、控制／
格式字元與 NFC。`chars` 依 Unicode 碼點排序，每行固定為 `U+XXXX<TAB>字元`；字型建置若
缺任一字模、遇到非 8×16／16×16 字模或格式錯誤便中止。
來源枚舉中的 `runtime-editorial` 表示依正常 runtime 畫面語意建立的編輯性 DRAFT，
`manual-term-editorial` 表示句子仍是編輯性 DRAFT、但其中專名／術語有中文手冊證據；
兩者都不代表手冊逐字摘錄。`manual-and-runtime` 僅用於確有手冊段落與 runtime 對應的資料。
`validate-candidate` 不建置字型；它只驗證被忽略工作區內的 strict manifest、實際來源／授權文字雜湊、
既有 Unifont parser coverage 與本機驗證／發行未定狀態，stdout 不回顯 license、notice 或 glyph bytes。

## ECL 敘事窗通用 catalog（規格 027）

- `ecl-text-events.tsv`：由 `tools/ecl_text_catalog.py` 從本機 `ECL1.DAX`–`ECL6.DAX`
  靜態抽取，只存 key、長度、SHA-256、來源位置。字串保留頭尾空白，雜湊與執行期
  `0763:056C` 收到的整串逐位元相同。
- `ecl-text.zh-TW.tsv`：批次譯文，`source` 為 `ecl-batch-editorial`，由
  `tools/ecl_translation_merge.py` 驗證（key 順序、NFC、Big5、非空）後合併。
  缺譯文的 key 在執行期顯示原版英文。
- `ecl-text-excluded.tsv`：規格 010–017、022 逐頁劇情家族已涵蓋的字串，
  逐頁家族拆除前不進正式譯文檔。
- 翻譯工作區（原文、術語表、批次）在 ignored `workplace/ecl-l10n/`，不入版控。
