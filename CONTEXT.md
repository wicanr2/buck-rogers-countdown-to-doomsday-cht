# 目前狀態

更新：2026-09-24

使用者已選定 3× 設定面板的 **A 倚天原生 24 點**，排除 B 衍生 22 點。
[第二百一十二階段 A／B 證據](docs/re/phase-212-host-only-3x-eten-font-ab-draft.md)
已接續成 host-only 實際畫面收據：[規格 004](docs/spec/004-dosgolem-host-frontend-draft.md)
的 3× 字型子契約限縮 READY；本機 dosgolem fork `cc0b17a` 已將
正式 `Game.New`／`Draw` 改接 24×24 Wide＋16×24 ASCII，
2×→3×→2× 的合成畫布 RGBA 像素與安全矩形驗證通過，2× 往返全畫面
不變。[版控抽字工具](tools/eten_host_font3.py)能由已購本機字型
重建相同子集，字模仍只留 ignored `workplace/`。這些沒有
原版 DOS／存檔同狀態或完整玩家入口；規格 004 整體 DRAFT，
3× 字型也不升 CONFORMED。
本輪在既有 Docker／Xvfb 重新執行本機原生字型畫格測試：3× 五標籤
逐像素通過、24 點字模有 102 個墨點落在 22×22 裁切範圍外，
2×→3×→2× 的 1,116,160 bytes 畫面完全相同。這仍是合成畫布
host-only 收據，不能外推為原版 DOS 玩家路徑。

使用者再次確認 Linux 設定面板開啟時暫停 DOS，排除背景持續推進；
Cancel／Apply 收合的當回合仍零步，下一關閉回合才恢復。這項排程已有
[第一百九十四階段](docs/re/phase-194-formal-ebiten-panel-pause-conformance.md)
的正式 `Game.Update` 限縮 CONFORMED 收據，但尚非完整 machine／DOS
狀態或可玩前端驗收。[規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
現為 session-turn 限縮 READY **候選**；[Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)
已補成功批次 epoch、零預算、整批路由拒絕，並在同一 ignored typed owner
接上合成 COM 的真實 `Machine.Steps`／raw stop／error 收據；仍缺正式
橋接提交原子性、`Draw` 同步故障通知與真實資源關閉，不能升 READY。
真實橋接的 Down→非法 Apply 負例已證明逐事件提交會留下 DOS 左鍵；
整批純預檢與單次提交契約已寫為待審候選，尚未改正式橋接。
另以真正 `Game.Update` 重播同批畫布 Down→鍵盤 transport 錯誤，
也證實錯誤返回後 DOS 左鍵仍按下；詳見上述 Issue #18 審查紀錄。
此為 READY 阻塞證據，不是已修正的正式前端。
最新可丟棄負例進一步證明：只比較面板／滑鼠完整值會遇到
Open→Cancel、Down→Up 的 ABA；若來源版本僅由外層 wrapper 管理，
直接呼叫正式 bridge 仍可繞過。規格 019 因此新增共同來源版本與
單次提交候選，但尚未獨立核准或改 production。

[第二百二十階段](docs/re/phase-220-linux-active-composite-draft.md)另以無原版素材的
合成測試驗過多作用層單影格投影候選：2×／3×各讀一次合成輸入影格、固定
z-order、原 layer 不變，缺群組／過期 generation 在讀影格前拒絕，
缺字不交付半張 RGBA。正式 provider 目前仍只接受一層；手冊背景與正文
至少已有兩層，真實同一 session 的並存與失效尚未接通。本證據保持 DRAFT，
不使 Linux 可玩前端 READY。
正式手冊 presenter 的背景／正文雙層合成測試亦證實 3× 現行
`manualThreeXFont` 因未命名而被單層 provider 拒絕；僅在測試內
命名並登錄後，可重現現行 presenter 的 2×／3× RGBA。獨立審查指出
測試用合成器的 nil stamp 會 panic，manifest／generation 未綁正式
owner；此與 3× host 面板的原生 24 點字型是不同路徑，仍只屬 DRAFT。

[GitHub Issue #20](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/20)
追蹤第九頁固定單行。[規格 022](docs/spec/022-story-page9-overlay-draft.md)
經獨立審查限縮升 READY，單筆 identity TSV 亦標為 READY；正式
watcher／presenter 已接入 dosgolem fork 本地 `7930b7a`（未推遠端）。
[第二百一十九階段](docs/re/phase-219-story-page9-runtime-entry-ab.md)
的合法第八頁→第九頁 control／2×／3× 收據：完整 machine snapshot、
DOS state、indexed 與正規化 JSON 同值；RGBA 差異僅在核准單行矩形，
2× 1,253、3× 2,615 像素，零缺字。先前原版重播亦證實
20 個 glyph frame 內共有 1,280 筆故事矩形 A000 寫入，故原先「任何
相交寫入都清 pending」的想法已撤回；限縮契約改為建構中只接受當前字格的
已量寫入，active 後任何相交 pre-write 才清層。自然離頁、實際
清層後畫面、Restore 重入及正常玩家路徑仍未知；規格 022 保持
限縮 READY，Issue #20 仍 OPEN，不能宣稱第九頁完整中文化。

同一合法第九頁存態的前進 8／後退 2 單鍵各雙重重播至固定
`370000000` 步，均已被讀取但沒有故事矩形 pre-write 或 DOS 結束；
此負結果只限該狀態與時窗，已停止擴鍵與延長探針。

[第二百二十一階段](docs/re/phase-221-command-status-columns-draft.md)與
[規格 023](docs/spec/023-command-status-overlay-draft.md)把 row 15／row 24
命令狀態列分成三條原版路徑：row 15 六次 12 格重畫只在同一狀態證實
第 0 格變動、其餘相同；row 24 的 21 格 dispatcher 與 33 格直接
glyph 路徑不能合併。A000 首寫與部分清除邊界已量，但跨狀態固定詞、
原文詞界和完整失效未知；保持 DRAFT，沒有新增 TSV 或正式 watcher。
追加跨進度合法初態雙重播後，row 15 同 caller／位置確實得到
不同的 11／12 格身分，部分 byte 固定、部分變動；但字節類別只有
數字、空白與其他非英文字母，不能辨識可核准的固定英文詞界。
row 24 的既有收據仍沒有同路徑的第二個不同值。故規格 023
維持 DRAFT，沒有 READY 譯文或正式接線。

[第二百一十八階段](docs/re/phase-218-exit-prompt-runtime-ab.md)現已把真正
Exit 後兩句 row 24 問句本體接上正式 dosgolem watcher／presenter；
在一個合法加入角色存態的 N／Y→Y 路徑，control／2×／3× 各雙重重播，
原版記憶體、indexed／palette、鍵盤與啟用追蹤的 FileOps 收據相同。
兩句 active 的 RGBA 差異只在本體，原版六格多色尾碼與外側零差；
N 返回與 DOS Stop 無殘層。正式生命週期軌跡另外證實 q2 pending 與
q1 active 短暫共存、同值 A000 首寫清 q1、q2 guarded Return 後才顯示、
Stop 清層。主代理與獨立審查通過，[規格 021](docs/spec/021-post-join-exit-prompt-body-only-draft.md)
僅此固定無頭路徑**限縮 CONFORMED**；dosgolem workplace 分支本地
commit 為 `a01e342`，未推送 dosgolem 遠端。其他初態、正式 Restore 事件來源、
存讀檔及 Linux 可玩視窗仍未驗，不能說整款遊戲已完成中文化。

[第二百一十三階段](docs/re/phase-213-exit-prompt-font-draft.md)已固定真正
Exit 後兩句 row 24 問句的 DRAFT 繁中候選，現行本機倚天字型的 2×／3×
墨跡皆零缺字、零本體越界，六格多色原版尾碼保護區的靜態遮罩零差。
[第二百一十四階段](docs/re/phase-214-exit-prompt-body-lifecycle-fake-draft.md)
的 ignored typed fake 又驗第一問與 row 21 短暫共存、同值 A000 清層、
第二問 pending 與第一問 active 的真實先後、DOS Stop 清層及未知
writer／錯序失敗即關閉。兩者都不是
正式 runtime 或原版 A/B。[第二百一十五階段](docs/re/phase-215-exit-prompt-body-ready-review.md)
獨立審查限縮核准兩句問句本體與原版多色尾碼保護；
[規格 021](docs/spec/021-post-join-exit-prompt-body-only-draft.md)當時僅為
**限縮 READY**；其後正式接線與收據以上述第二百一十八階段為準。
GitHub [Issue #19](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/19)
已按此固定路徑的完成條件關閉；整體中文化與可玩前端另由其他 Issue 追蹤。

[第二百一十二階段](docs/re/phase-212-host-only-3x-eten-font-ab-draft.md)
證實原生倚天 24 點明體與符號可覆蓋 3× host 面板九個字元，
但直接裁成正式前端要求的 22×22 會損筆畫。已做不載原版遊戲的
A 原生 24 點／B 原型衍生 22 點並列圖片，五項文字安全矩形均通過；
當時使用者尚未選外觀；現已選 A 並完成上文所述限縮字型接線與
host-only 驗證，正式玩家路徑仍未完成。

[第二百一十一階段](docs/re/phase-211-synthetic-session-receipt-candidate-draft.md)
已在 ignored 合成 typed 原型驗過「DOS 退出前置檢查→Step 嘗試數
差分→error 優先」候選收據與五組負例；退出後零新步。該階段尚未
決定零預算、`Epoch`、正式 Draw fault owner；目前以本頁頂端的
Issue #18 審查紀錄為準，規格 019 仍未升 READY。

[第二百一十階段](docs/re/phase-210-session-stop-receipt-probe-draft.md)
以獨立合成 COM 探針補證：DOS 正常退出仍可得 raw `StopBudget`；
已退出後再次正預算 `RunUntil` 還會多嘗試一步。正式 session 必須
先查 terminal state，再判 error／停止碼；零預算、Epoch 與完整
停止原因映射仍未定，規格 019 保持 DRAFT。舊 phase206 釘選來源
已精確恢復。

[第二百零九階段](docs/re/phase-209-cold-boot-live-ebiten-panel-pause-draft.md)
已從原版第零步到已量選單，再於真實 2× Ebitengine／X11 視窗的
`Update` 推進同一 machine：前兩回合各 16 步；實體 Open、持續展開、
Cancel 收合當回合零步，下一關閉回合恢復 16 步。只限 ignored
單次原型與選單；3×、完整狀態 A/B、存讀檔及正式 session 未驗。

規格 [019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)的獨立
READY 前審查仍判 DRAFT：同批鍵盤事件順序、真實 step／epoch／stop
映射與正式 Draw 故障回報尚未閉合；完整冷開機不是這個限縮子契約的
READY 前置，但仍是 Linux 可玩版必需的後續驗收。

[第二百零八階段](docs/re/phase-208-cold-boot-menu-ebiten-prototype-draft.md)
以 ignored 原型從原版 `START.EXE` 第零步在唯讀來源／獨立 scratch 下
跑到首個已量選單；終態繁中覆繪缺字零，Ebitengine／Xvfb 顯示三幀。
這是開窗前算好的靜態影格，沒有 live 玩家輸入或面板／session，
不能稱 Linux 可玩版；規格 004、Issue #16／#18 仍開啟。

[第二百零七階段](docs/re/phase-207-linux-session-six-stage-fault-fake.md)
以 ignored `TurnFake` 補測前端回合六階段故障：面板開啟時假 DOS 零步而
host 畫面仍可更新，Snapshot 純讀；每個故障點後皆拒絕新輸入／步進且
Close 副作用一次。這不是正式 Ebitengine 或原版收據；正式 Draw 故障回報、
資源釋放與冷開機仍待解，規格 004／019 與 Issue #18 維持 DRAFT／開啟。

[第二百零六階段](docs/re/phase-206-linux-session-machine-step-delta-draft.md)
以無原版素材的合成 COM 探針、同來源雙重播確認 machine 的
`Steps` 前後差分：提前停止少於 budget，CPU 出錯時失敗嘗試也
計入，`RunUntil` 的原始 `StopBudget` 不能蓋過非空 error。
這是 Issue #18 的 DRAFT 步數證據，不是正式 session 或玩家路徑。

[第二百零五階段](docs/re/phase-205-linux-session-failed-close-once-fake.md)
在 ignored 前端 session fake 補驗：先前進七個 fake steps，再注入
Deliver／Advance 故障；後續輸入與步進均拒絕，重複 Close 的副作用
計數恰一次。這不含 Snapshot／Draw／observer 或真實資源，
規格 004／019 與 Issue #18 繼續 DRAFT／開啟。

[第二百零四階段](docs/re/phase-204-action-bar-runtime-conformance.md)已訂正
技能操作列短譯文後殘留原版英文的缺陷：本機 dosgolem fork
`674e3e3` 先清除完整已核准標籤矩形，再覆繪白色助記字母與原色
繁中。八條職業／技術技能固定路徑及一條技術 Escape→Y 離頁，
control／2×／3× 各雙重播；原版 JSON（扣除呈現欄）、indexed
同狀態相同，RGBA 差異僅在安全矩形，英文尾段已清淨，離頁無殘層。
故 [fork 規格 215](workplace/dosgolem/docs/spec/215-buck-rogers-skill-action-bar-runtime-overlay.md)
僅此九條無頭路徑**限縮 CONFORMED**；disabled、其他重入、冷開機、
存讀檔與 Linux 視窗仍未驗。第九十九階段只證字型密度，不能再當作
英文完整清除的證據。

[第二百零三階段](docs/re/phase-203-linux-session-mixed-batch-fake-review.md)
將前端 session fake 的 DOS 鍵改為同批候選，驗證 Open／Apply／Cancel
與 Enter 同批時 BIOS 零副作用、DOS 零步，收合後下一回合才恢復。
這僅是 ignored fake 的 DRAFT 勘誤，未接正式冷開機玩家前端；
規格 004／019 與 Issue #18 仍待 READY／實作／驗收。

[第二百零二階段](docs/re/phase-202-skill-exit-runtime-ab.md)已讓
職業／技術技能頁兩句離開問句的正式 watcher／presenter，在兩個各自
合法的原版 Escape 前 state 中完成 control／2×／3× 同狀態 A/B。
active 中文像素僅落問句本體，六格原版多色尾碼零差；職業／技術
各 N／Y 的四條終態 JSON、indexed 與 RGBA 分別相等、無殘層。
[規格 020](docs/spec/020-skill-exit-confirmation-overlay-draft.md)因此只在
此無頭固定路徑升為**限縮 CONFORMED**。遊戲內存讀檔、正式 Restore
bridge、冷開機及 Linux 玩家視窗均未驗，Issue #17 繼續開啟；
下述較早的 READY 敘述是當時狀態，不覆蓋本段結論。

[第一百九十七階段](docs/re/phase-197-skill-exit-confirmation-prewrite-draft.md)
已從合法技能頁路徑量到職業／技術兩句離開問句的首次變值 A000
相交寫入、原版六格多色選擇尾碼與各自本體安全矩形；兩種起始
state 的證據已明確分開，不能混稱同狀態。
[規格 020](docs/spec/020-skill-exit-confirmation-overlay-draft.md)保存此
覆繪邊界；[第一百九十九階段](docs/re/phase-199-skill-exit-font-containment-draft.md)
已驗兩句現行倚天字型在 2×／3× 的靜態墨跡 containment、零缺字。
[第一百九十八階段](docs/re/phase-198-skill-exit-ny-all-store-prewrite-draft.md)
已量 N／Y 各兩條合法重播的本體與尾碼首筆相交 A000 store，包含舊變值
watcher 漏掉的三個同值首寫。[第二百階段](docs/re/phase-200-skill-exit-body-only-lifecycle-fake-draft.md)
用 typed fake 鎖住 entry→return、清層、故障與雙倍率尾碼零覆繪；
[第二百零一階段](docs/re/phase-201-skill-exit-body-only-ready-review.md)獨立審查後，
規格 020 **僅兩句本體限縮 READY**，不再為不觸碰的尾碼追逐格生命週期。
正式 watcher／presenter、DOS 停止／還原接線與原版同狀態 A/B 仍缺，
Issue #17 未完成。

[第一百九十六階段](docs/re/phase-196-ebiten-panel-batch-keyboard-gate.md)
修正正式 Ebitengine `Game.Update` 的同批鍵盤分流：面板起點開啟，
即使 Apply／Cancel 同回合收合，Enter 等鍵也不再進 DOS BIOS queue；
closed canvas 鍵盤仍正常轉送。本機 dosgolem `71f19cb`／spec 232 只在
此 host 鍵盤邊界限縮 CONFORMED。[規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
新列完整 typed session 的剩餘契約，仍為 DRAFT；冷開機、原版同狀態
與 Linux 可玩入口未完成。

[第一百九十四階段](docs/re/phase-194-formal-ebiten-panel-pause-conformance.md)已將
正式 `frontend/ebiten.Game.Update` 的面板暫停接線，雙倍率實體 X11 的
Cancel／Apply 收合當回合零 `Advance`、下一關閉回合恢復；本機 dosgolem
`c273db6`／spec 231 只在此 callback 排程限縮 CONFORMED。並非實際 DOS
指令數、冷開機或可玩玩家前端的完成證據；[規格 004](docs/spec/004-dosgolem-host-frontend-draft.md)
與 Issue #16／#18 仍為 DRAFT／待完成。Apply 與 Enter 同回合的鍵盤漏入
已由第一百九十六階段限縮修正；完整 session 契約仍待處理。

[第一百九十五階段](docs/re/phase-195-post-join-prewrite-runtime-receipt.md)
以本機 dosgolem `540a522` 的正式不含內容 pre-write 收據補上加入角色後
七列選單逐寫入 active→empty：合法 `a-joined.state` 的固定
`Right → Enter → rows 13、14、15、16、18、19、20` 與 row20 普通回寫
前清層，雙倍率無殘字，獨立審查只核准此範圍 CONFORMED。真正 Exit、
提示、重入、完整開機及存讀檔仍 DRAFT／未驗；[規格 018](docs/spec/018-post-join-menu-overlay-draft.md)
不得解讀為整體選單完成。下文較早的 READY 描述為當時狀態，以上述
2026-09-24 限縮勘誤為目前真相。

本機 dosgolem 正式 `host.MouseBridge` 已由雙倍率真實 Ebitengine 同狀態 A/B 與
2×畫布外／面板／失焦清理收據限縮標為 CONFORMED；正式與可丟棄原型七組 API／
完整 phase 逐欄相等，見[第一百七十九階段](docs/re/phase-179-formal-mousebridge-conformance.md)。
這只驗收 320×200 的通用滑鼠橋接元件，**不**表示 Linux 玩家前端已接線；
[spec 004](docs/spec/004-dosgolem-host-frontend-draft.md) 與 Issue #16 仍未完成。
本機 dosgolem fork `3092dad` 的 opt-in Ebitengine 測試已以私有加入角色存態顯示
真實原版畫布，並於實體 X11 驗證面板攔鍵、2×→3×套用及收合後的 DOS 鍵盤轉送；
詳細限制見 fork `docs/re/phase-180-linux-ebiten-router-draft.md`。這是**DRAFT 原型**，
該路徑未接正式中文覆繪與完整冷開機，不能稱為可玩版。其後另一條
[第一百八十五階段](docs/re/phase-185-ebiten-real-active-layer-router-draft.md) ignored 原型
已把真實首屏五行繁中 watcher 作用層交給正式通用 `frontend/ebiten.Game` 輸入路由，
在實體視窗連續推進原版並用滑鼠 Apply 2×→3×；雙倍率 RGBA 與既有 CLI 私有收據
逐位元組相同。它仍從私有 checkpoint 起跑、未驗完整玩家路徑或 save/load，
所以規格 004 和 Issue #16 仍未完成。
[第一百八十六階段](docs/re/phase-186-linux-ebiten-cold-boot-lifecycle-ready-gap-audit.md)
把最短正式前端缺口定為 fail-closed 冷開機 session 整合入口：在第一步前安裝
observer、分離唯讀原版與可寫存檔根、同 goroutine 管輸入／Step／作用層聚合／畫面；
目前沒有正式玩家 command。使用者已確認面板開啟期間暫停 DOS CPU Step，
關閉或 Apply 收合後恢復；這訂正既有原型持續 `Advance` 的行為，
其正式接線與同狀態驗收仍待 spec004 READY。
[第一百八十九階段](docs/re/phase-189-ebiten-panel-pause-resume-draft.md)現已在 ignored
真實繁中 Ebitengine caller 以實體 X11 完成 Cancel 與 Apply：面板開啟的 89 回合
零 Step、收合當回合零 Step、下一關閉回合各恢復 16 步，雙倍率畫布仍逐位元組等於
既有 CLI 私有收據。這只證實原型排程；正式前端、冷開機與完整 DOS 同狀態
A/B 尚未完成。
[第一百九十階段](docs/re/phase-190-linux-frontend-session-ready-prerequisites.md)
又核對固定 fork API：正式 `Game.Advance` 尚無 budget／step receipt／session phase，
也缺冷開機 preflight、多作用層 owner 與失敗後 `Close`；故暫停原型不能
直接升為正式可玩入口。
[第一百九十三階段](docs/re/phase-193-frontend-session-fake-draft.md)另以 ignored
純 Go fake 重跑 Open／Select／Cancel／Apply 零 Step、下回合恢復與故障後
拒絕再推進；仍未驗真實事件分類、冷開機或 DOS 同狀態，規格 004 維持 DRAFT。

目前 24 份繁中 TSV（含一份技能 Exit DRAFT、已限縮 READY 與尚未接通的 host UI）的倚天字型聯集仍為 1028 字模：版控內
[`font/characters.txt`](font/characters.txt) 與本機
`workplace/current-font/buckrogers-eten-top-pad.golemfnt` 的字元涵蓋完全一致，缺字為零。
舊的 961／997／1024／1026 字模收據只代表當時譯文，不可作目前前端的字型輸入；來源與雜湊見
[`font/README.md`](font/README.md)。這是字型覆蓋，不代表所有畫面都已中文化。

從正常「加入角色 → 名冊 EXIT → 功能選單」雙重原版重播，新確認七項固定選單文字；
繁中候選與原文雜湊已另存 [`post-join-menu`](text/README.md) catalog，現為 spec018 的限縮 READY fixture，
且已有正式 runtime 的局部 A/B。「JOIN A GAME」與「SHOW CHARACTER'S GAME」仍只有字面譯法，操作語意未知；
上方動態角色資料不納入這七項；七列的反白與普通回寫另列精確變體。
私有原文／畫面證據只在
`workplace/phase158-post-join-exit-probe/`；不能把此資料完成度算作已中文化畫面。
後續雙重正常 Down／Enter 收據已證實七項普通／反白重畫、提示列清除不相交，
以及 `026F:029C` 在 `125119490` 的 Enter 後第一筆全選單 clear；但該 Enter 前
選取的是 row 12 `Create New Character`，不是 row 21 `Exit to DOS`。原始
`START.EXE` bytes／檔案 offset、事件 SHA 與勘誤見
[`第一百八十三階段`](docs/re/phase-183-post-join-exit-identity-corrigendum.md)；舊重播見
[`第一百六十一階段`](docs/re/phase-161-post-join-menu-selection-and-exit.md)。
其後[規格 018](docs/spec/018-post-join-menu-overlay-draft.md)與 ignored 幾何／typed 原型
已補七項 2×／3×靜態字模 containment 及 20 筆已量 request 世代測試；主代理獨立重跑
四項測試通過。[第一百八十階段](docs/re/phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)
再以本案 dosgolem fork 雙重重播完整 A000 pre-write（包含同值寫入），將七列初畫／普通回寫／
反白共 21 種精確變體寫入 TSV。各選取世代最早相交寫入其實是更早的 `0763:184D`
原版 glyph 寫入，不是後續 row 12 Enter clear；必須先失效、再依完整 exact 變體重建。row 20 普通回寫後
遇到未收錄 row 21 反白時失敗即關閉。主代理回讀固定雜湊並獨立重跑七項正反例後，
[第一百八十一階段](docs/re/phase-181-post-join-menu-ready-review-candidate.md)已將 spec018
限縮升 READY；正式 watcher 與同狀態 A/B 屬 READY 後實作／CONFORMED 驗收，不能倒置閘門。
主機介面譯文導致本機字型擴為 1028 glyph 後，原 1026-glyph READY 字型 pin 曾暫停；
主代理以新字型在 Docker 重跑七項 verifier、21 變體與雙倍率逐列 containment 全通，
已於同一[第一百八十一階段](docs/re/phase-181-post-join-menu-ready-review-candidate.md)
記錄新 SHA 與再審，恢復**相同限縮範圍**的 READY；當時正式 CLI A/B 尚未完成。
其後本機 dosgolem fork `cb3ca77` 已接通正式 CLI，並以相同 state／keys 做
control、2×、3×局部終態 A/B：收據中的事件、BIOS 按鍵、記憶體、indexed
framebuffer 與 palette 逐 byte 相同，七列安全矩形外 RGBA 差異皆為零；
未收錄 row 21 selected 明確 fail-closed。完整 DOS 內部狀態與檔案副作用不在該收據內。
詳見[第一百八十二階段](docs/re/phase-182-post-join-menu-runtime-ab-partial.md)。
[第一百九十二階段](docs/re/phase-192-post-join-menu-prewrite-runtime-ab.md)進一步
沿相同固定 state／十筆鍵量到 row20 普通回寫前、返回後的 2×／3×控制組
同狀態 A/B：後點兩倍率覆繪 RGBA 皆逐 byte 等於 baseline，另有正式
同值 A000 首寫清層元件測試；尚未取得逐指令 runtime active→empty 收據。
真正 row 21 `Exit to DOS` 路徑已有 DRAFT 雙重原版收據：Enter 出現第一個離開詢問，
首次 Y 再詢問未存檔是否仍離開，N 會清除並重畫選單，兩次 Y 則使 DOS 於上限前退出；
詳見[第一百八十三階段](docs/re/phase-183-post-join-exit-identity-corrigendum.md)。
另以 ignored 雙重觀測器已量到 Enter 後 row 21 普通回寫的首筆相交
A000 pre-write：step `124800903`、`0763:184D`、像素 `(72,168)`。
N 返回及兩次 Y 退出的覆繪生命週期、中文候選幾何、逐幀 active→empty
與正式同狀態 A/B 仍未驗，
故 spec018 **仍為 READY，不是 CONFORMED**。
後續[第一百八十四階段](docs/re/phase-184-exit-prompt-draft-prototype.md)補兩個提示
的 2×／3×靜態候選與 A000 相交寫入，但自訂探針的退出步數較舊 runner 早六步，
提示覆繪仍 DRAFT；沒有改動正式 watcher 或原版離開判定。
[第一百八十七階段](docs/re/phase-187-exit-stop-six-step-corrigendum.md)用同一 fork／state／
按鍵分別重跑最小 A000 探針和原 text runner，兩者都在 `125006324` 退出，
排除了「A000 observer 造成六步差異」；舊 `125006330` 的環境來源仍未證實。
[第一百八十八階段](docs/re/phase-188-exit-prompts-draft-evidence.md)再以 N／Y→Y
各雙重原版重播確認兩個 row 24 提示的 guarded identity、選擇尾碼的多色／反白
狀態與同值 pre-write。第二提示在 DOS 退出前沒有自然相交清除；尾碼不能
直接套用「白色 Y/N」假設。Exit 提示仍 DRAFT，尚未接正式 watcher。
[第一百九十一階段](docs/re/phase-191-skill-exit-confirmation-translation-draft.md)
另從原版 `GAME.OVR` bytes／既有事件 SHA 核實職業與技術技能頁兩句
離開確認原文，推翻舊「職業提示原句未知」。兩句繁中已存獨立 DRAFT
TSV，未接 watcher；它們與功能選單 Exit 的多色尾碼不是同一輸出路徑。

功能選單／種族建立的[spec 001](docs/spec/001-menu-text-output-overdraw-draft.md)已回填一條
限縮 CONFORMED 路徑：固定 #99,999,999 state 的 Create New Character → Pick Race → Down → Up →
Enter，以 dosgolem `2755f7c` immutable runner、正式 menu TSV 與倚天字型做 2×／3×各兩次
runtime A/B。確認前為 13 exact requests／actions、零 miss、矩形外零差；最後 Enter 的
`026F:029C` 清除使 active overlay 歸零且終態 RGBA 等於 baseline。完整重播進入性別頁後的
4 筆 menu-only miss 屬下一頁非 menu identity，種族 13 筆仍零 miss。這不閉合
generation／streaming 總契約、訊息／存讀檔／其他出口或其他文字畫面，故 spec001 整體仍
DRAFT；2×／3×均已是使用者決定的正式可切換模式。

第七頁固定故事文字已在三輪獨立審查後限縮升
[規格 016](docs/spec/016-story-page7-overlay-ready.md)：合法第六頁終態
Enter 進入 row 17–22 六行、合法第七頁 Enter 離頁。190 glyph 原版逐字
return／ABI、最早相交 pre-write、七 ABI 低位映射、逐列半開寫入判定及
2×／3×字型 containment 已核對；此 READY 審查階段正式 dosgolem runtime
與同狀態 A/B 尚未做。證據與審查勘誤見
[第一百五十三階段](docs/re/phase-153-story-page7-ready-prerequisite-diagnostics.md)。
其後本機 dosgolem `d42567d` 已正式接通 watcher／loader／presenter／CLI；
同狀態 control／2×／3×與同程序兩次 Enter 離頁 A/B 證實六 key、零缺字、
安全矩形外零差、machine／DOS 全等，step `341018656` active 6→0
且終態無殘字。其後本機 dosgolem `940e5f3` 補齊正式雙倍率失敗即
關閉矩陣，主代理獨立重跑定向 test／vet／race 通過；因此第七頁
**只在固定六行及已量 Enter 離頁限縮 CONFORMED**；見
[第一百五十六階段](docs/re/phase-156-story-page7-runtime-ab-pending-failure-audit.md)。
第八頁四行先由雙重原版收據補足 130 glyph 的 SS／SP+0x12／RETF 與
合法 page8→page9 最早相交 pre-write；當時 2×／3×正式字型 containment
與 typed-core 失敗即關閉仍缺，故維持 DRAFT，見
[第一百五十五階段](docs/re/phase-155-story-page8-ready-prerequisite-evidence.md)。
現有四行譯文已由低階翻譯代理對原版畫面校對，無需修改；本機倚天
2×／3×正式幾何靜態 containment 亦零缺字、零越界，但尚非 runtime 授權。
其後端到端 verifier 與完整英文清除矩形經三次獨立審查、兩度退回後，
[規格 017](docs/spec/017-story-page8-overlay-ready.md)先在固定四行與已量
Enter 進出限縮升 READY。舊 `[8,96)` 已勘誤為 `[8,312)×[136,168)`。
本機 dosgolem `c0f6d76` 再接通正式 lifecycle；control／2×／3×與同程序
Enter 離頁驗得四 key、零缺字、矩形外零差、machine／DOS 全等，step
`351154334` active 4→0 且終態無殘字。獨立程式審查與定向 test／vet／race
通過，因此第八頁**只在固定四行及已量 Enter 進出限縮 CONFORMED**；見
[第一百五十七階段](docs/re/phase-157-story-page8-runtime-conformance.md)。完整開機、
其他出口、存讀檔、第九頁及其餘文字仍未驗。

互動式玩家前端的第一個可玩版本已由使用者決定先支援 Linux，架構保留日後
Windows／macOS 擴充；第一版三平台同步交付已排除。視窗後端也已選定
Go／Ebitengine，排除 SDL3；面板開啟時鍵盤由 host 消費、不送進 DOS，關閉後恢復。
Apply 提交倍率後自動收合面板並恢復遊戲鍵盤；倍率只保留本次遊戲期間，
不寫跨重啟設定檔，每次啟動預設 2×，遊戲中可 Apply 切到 3×；
未 Apply 即關閉面板會取消暫選，再開時選取值回到目前已套用倍率；
[spec 004](docs/spec/004-dosgolem-host-frontend-draft.md) 維持 DRAFT，工作項為
[Issue #16](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/16)。
同一真實面板外 click 的可丟棄 A/B 已證實：不轉送時 DOS mouse 座標不變，實驗性
轉送時座標改變；兩組未 Step machine，不能推論玩家可見反應。使用者已決定：面板關閉時
畫布內的滑鼠事件轉送原版，面板開啟時新事件由 host 消費；已轉送 Down 後，即使於畫布外、
控制列、面板放開或視窗失焦，也要只送一次 Release 而不移動最後 DOS 座標。MouseBridge
仍待完整真實事件矩陣與 READY 審查，見[第一百二十七階段](docs/re/phase-127-pointer-miss-ab-prototype.md)。
其後可丟棄 Ebitengine／Xvfb bridge 已取得 2×／3×畫布內 Down→Up 及畫布內 Down→控制列 Up
的真實事件、有界 Step 與滑鼠按鍵清除收據；3×兩組的起始 machine／DOS 正規化狀態相等。
這些收據不證明遊戲可由滑鼠操作，MouseBridge 仍是 DRAFT，見
[第一百三十三階段](docs/re/phase-133-real-ebiten-mouse-bounded-step.md)。
修正畫布內 Up 為 `Move→Release` 後，另以真實 Ebitengine 重跑 2×／3×
同畫布 Down→Up；兩倍率均為 `Move→Press→Move→Release`，DOS button
清除，輸入 API 邊界 BIOS／IRQ／indexed／memory 不變，見
[第一百四十六階段](docs/re/phase-146-real-ebiten-inside-up-corrected.md)。
後續[第一百五十階段](docs/re/phase-150-ebiten-mouse-geometry-prototype.md)
以真實 X11／Ebitengine 補齊 2×／3×四角映射與 chrome／右／下排除邊界
14 份私有收據；右／下 exclusive 邊界只用 ignored 原型 1 logical-pixel guard
觀測，不是正式視窗設計。cleanup 其餘矩陣與玩家可見滑鼠因果未驗，
MouseBridge 仍 DRAFT。
其後[第一百五十一階段](docs/re/phase-151-ebiten-mouse-release-cleanup-prototype.md)
又以真實事件補雙倍率控制列／畫布外右側／面板預先開啟／失焦的
release-only cleanup：Down 後只 Release、不 Move，最後 DOS 座標不變；
3×孤兒及重複 Up 的第二次 X11 mouseup 未由 Ebitengine public API
暴露 release edge。面板開啟是 harness 前提而非玩家點擊完整路由，
下邊界 cleanup 與正式前端仍未驗。
另以真實 X11 失焦驗到已送 DOS 的 Down 會只 Release、不 Move；無前置 Down 的實體 Up
及重複 Up 在 Ebitengine public input API 未產生新的 release edge，3× panel-open 前提下的
新 Down／Up 也不觸 DOS。這些仍是可丟棄 harness 的限定收據，不代表完整前端路由或
滑鼠可操作，見[第一百三十五階段](docs/re/phase-135-real-ebiten-mouse-focus-loss-and-release-edges.md)。
真實 X11／Ebitengine 的 2×／3× host Open hit 與 open-panel 空白 miss，以及 3× 已接受 Down
後開面板再於 chrome Up 的 release-only cleanup 亦已量到；空白 miss 的面板核心本身仍回
`ConsumedByHost=false`，不能冒稱完整 host hit/miss 路由已驗收。MouseBridge spec228 仍 DRAFT，
見[第一百三十七階段](docs/re/phase-137-real-host-panel-route-and-3x-cleanup.md)。
後續[第一百五十四階段](docs/re/phase-154-ebiten-panel-pointer-miss-prototype.md)
補雙倍率真實 hit／miss、閉面板 canvas 轉送及畫布外／控制列／面板／失焦
release-only 矩陣。空白 miss 仍由原型局部政策才完成 host 消費，正式
`PanelController`／整體 route 尚未接線或升 READY；面板展開後同一實體
點擊的 Up 座標重映射，也須依按下時的 host target 消費。
本機 dosgolem 已有通用唯讀畫面、active layer 快照、純面板事件核心與明示 BIOS
鍵盤橋。Linux／Xvfb 的真實遊戲載入 Ebitengine 原型已在同一事件迴圈驗證
Machine step→snapshot→Draw、2× 預設、Cancel 暫選後重開仍為 2×、Apply 3×
自動收合，以及面板開啟不送 BIOS 鍵、關閉後合法一鍵推進原版。第 116 階段最初
仍用空覆繪層；其後第 120 階段已在真實遊戲執行緒接上第一頁五行的作用中繁中層，
初始 2×、取消暫選後 2×、套用後 3× 均與正式 CLI RGBA 逐像素相同，修正了曾把
2×字模稀疏放大至 3× 的原型缺陷。這仍是受控事件的私有原型；正式 pointer hit、
實體鍵盤映射、完整開機玩家路徑、其他覆繪層切換與存讀檔未驗，不能稱可玩中文版。
見[第一百一十六階段](docs/re/phase-116-game-loaded-ebiten-prototype.md)與
[第一百二十階段](docs/re/phase-120-game-active-story-layer-prototype.md)。

手冊成功返回後第一個固定劇情畫面五行，已由本機 dosgolem `9f4c5f0` 在固定合法 state／
私有 BIOS 排程重生 control／2×／3×穩定及同程序 Enter 離頁。兩倍率 active 時五 key、
零缺字、安全矩形外零差；Enter 於 `281020548` 的 row-136 相交 pre-write 使 active 5→0，
終態 RGBA==baseline，且第二頁沒有 overlay。`state-compare` 對 control↔兩倍率 normalized
machine／DOS 均全等；raw state bytes 不能比較。strict catalog／generation／receipt gate 與
2×／3× failure matrix 已拒絕 partial、mixed、duplicate、錯 generation/key、缺字、非 READY
及未知 epoch 舊 stamp。因此[spec010](docs/spec/010-story-opening-overlay-draft.md) **只在固定
首屏五行及已量正常 Enter 離頁限縮 CONFORMED**。第二頁、其他離頁、完整開機與實際
存讀檔均明確排除；ABI 高位不屬 identity。見[第一百一十七階段](docs/re/phase-117-story-opening-runtime-ab.md)
及[第一百一十九階段](docs/re/phase-119-story-opening-enter-lifecycle.md)。
第二頁四行、第三頁五行與第四頁六行均有可重播低階 glyph 身分；以下記錄第四頁早期 DRAFT 勘誤，現況以後段規格 013 為準。第四頁由
第三頁合法 state 的同一筆 Enter 重生為 `0763:04FF → 0763:026B` 六行；舊
`visual-transcription` 前五筆 length／hash 與原版 trace 不符，僅第六筆相符，故繁中候選仍須
編輯審查、catalog 維持 DRAFT 且不得接 runtime。
第二頁其後另以同狀態原版收據量到四行完成、首屏失效、第二頁→第三頁的最早相交
pre-write、實際 far-return 與相對 SS/SP；獨立修正錯誤負例後，
[spec 011](docs/spec/011-story-page2-overlay-draft.md) 當時限縮升 READY，四筆事件身分資料也升
`confirmed/READY`。本機 dosgolem 已接第二頁四行 runtime：2×／3×正例與 control
的原版 machine／DOS 正規化狀態相等，四鍵啟用、零缺字、安全矩形外零差異；兩倍率
的 page2→page3 pre-write 均記錄 active 4→0、終態無殘字。獨立稽核發現 TSV caller／guard
驗證及 presenter 原子 Apply 缺口，已於本機 `2fa5be4` 修正；`db1a281` 補部分負例。
後續補齊雙倍率失敗矩陣與同幀輸出驗證，並以最新本機程式重跑 control／2×／3×
及合法 Enter 離頁；[第一百四十一階段](docs/re/phase-141-story-page2-runtime-conformance.md)
使 spec 011 **限縮升 CONFORMED**，只涵蓋第二頁四行與已量離頁。
第三頁離頁的合法 Enter 已以兩次一致收據量到最早安全矩形交集 pre-write：step
`301108549`，早於第一個可見差異 `301108573` 與第四頁首 glyph；此證據取得時第三頁仍為 DRAFT，
見[第一百三十八階段](docs/re/phase-138-story-page3-exit-prewrite.md)。
另從第二頁合法終態雙重重播第三頁，五行 144 個 glyph 均有已確認的 `RETF imm16`
返回 caller；審查後再補雙重 content-safe 收據，逐筆直接證實 entry／return 同 SS、
SP 相差 `0x12`，不再以首筆樣本外推其餘 143 筆。
[第一百三十九階段](docs/re/phase-139-story-page3-return-edge.md)與
[第一百四十二階段](docs/re/phase-142-story-page3-ready-review.md)獨立審查通過後，
[spec 012](docs/spec/012-story-page3-overlay-draft.md)當時限縮升 READY，授權五行 typed adapter。
本機 dosgolem `aae577f` 接上第三頁正式 runtime，`9a9b769` 再拒絕七個 ABI word
的非零高位；[第一百四十四階段](docs/re/phase-144-story-page3-runtime-conformance.md)
以修正後程式完成 control／2×／3×與合法 Enter 離頁同狀態 A/B：五鍵啟用、零缺字、
安全矩形外零差異，原版 machine／DOS state 全等，離頁 active 5→0、終態無殘字。
因此 spec 012 **僅上述路徑升 CONFORMED**，完整開機與存讀檔仍未驗。
從第四頁終態合法 Enter 已另量到第五頁底部五行的低階 glyph 身分與繁中 DRAFT；
初稿曾誤配右側人物姓名，經原圖座標核對訂正。第五頁五筆 exact catalog
與[規格 014](docs/spec/014-story-page5-overlay-ready.md)當時限縮升 READY；
本機 dosgolem `0f3ea89` 已接正式 watcher／presenter／CLI，control／2×／3×及
同執行 active→clear 離頁的同狀態 A/B 通過，見[第一百四十八階段](docs/re/phase-148-story-page5-runtime-ab-pending-audit.md)。
其後本機 dosgolem `a2dba44`／`6181e31` 補 presenter 原子性與 watcher
失敗即關閉負例；`6dcc427` 再補第四頁 DRAFT catalog／缺字雙倍率拒絕。
Docker Go test／vet／race 通過，私有收據雜湊已回讀；
規格 014 **僅上述固定玩家路徑限縮升 CONFORMED**。完整開機、
其他離頁與存讀檔未驗，不宣稱整段故事已全部中文化。
第四頁另有[第一百四十三階段](docs/re/phase-143-story-page4-ready-evidence-draft.md)
逐筆 192 glyph 返回；但獨立審查發現原 `story-fill-trace` 只看前五行，
不能單獨證明六行完整矩形的最早相交 pre-write。後續本機 dosgolem
`ac1f7fb` 以受限六行診斷補齊 row 22，雙重重播的 48 筆相交 span
一致；最早仍為 step `310023777`。typed 核心與字型覆蓋已有私有正反例，
第四頁六筆 exact catalog 與[規格 013](docs/spec/013-story-page4-overlay-draft.md)
已經獨立審查而限縮升 READY；本機 dosgolem `1cf9ec4` 已接正式
watcher／presenter／CLI，control／2×／3×及同執行 active→clear 離頁的
同狀態 A/B 通過，見[第一百四十七階段](docs/re/phase-147-story-page4-runtime-ab-pending-audit.md)。
失敗即關閉矩陣當時仍待獨立審查；
審查曾發現 presenter `Apply` 對後段無效事件可能留下前段 stamp；
本機 `cad9c3f` 已以兩階段驗證／提交與雙倍率負例修正；其後 `5652f11`
補 ABI／return／video write 負例，Docker Go test／vet／race 通過且私有收據雜湊
已回讀。規格 013 **僅上述固定玩家路徑限縮升 CONFORMED**；其他離頁、
完整開機與存讀檔亦未驗。
動態狀態列及右側人物姓名一律排除。第五頁譯文加入後，本機倚天完整 catalog
候選聯集重建為 1006 字模，正式 loader 已回讀且零缺字；這仍只證明字型覆蓋。
第五頁後的合法 Enter 也已量到第六頁 row 17–22 六行低階身分；低階翻譯代理建立
繁中 DRAFT。後續[第一百四十九階段](docs/re/phase-149-story-page6-ready-prerequisite-diagnostics.md)
補 200 glyph 的雙重 return／ABI 收據及第六頁離頁最早相交 pre-write；
後續由本機 `6dcc427` 重建 runner 並逐 byte 重生兩組收據，私有 typed-core
與雙倍率字型 containment 通過獨立審查。[規格 015](docs/spec/015-story-page6-overlay-ready.md)
與六筆 event catalog 當時限縮升 READY；其後本機 dosgolem `e3e1db1`、
`a7304e3`、`0ce4948` 接正式 core、負例與 CLI。
[第一百五十二階段](docs/re/phase-152-story-page6-runtime-conformance.md)
以 control／2×／3×及同執行 Enter 離頁同狀態 A/B 驗證六行可讀、零缺字、
安全矩形外零差、原版 machine／DOS 全等與失效後無殘字。因此規格 015
**僅上述固定路徑升 CONFORMED**；完整開機、其他離頁及存讀檔仍未知。
全部 17 份 catalog 的倚天聯集曾重建為 1014 glyph，dosgolem 正式 loader
對當時譯文字元零缺字；第六頁現行字型另由本機 1024 字模 loader
回讀零缺字，但仍不代表第六頁已接通 runtime。
第六頁後的合法 Enter 又確認第七頁 row 17–22 六行；同狀態 indexed 畫面與色盤重生一致，
六行繁中候選與 identity 當時先建為 DRAFT；後續三輪審查限縮升
[規格 016 READY](docs/spec/016-story-page7-overlay-ready.md)。全部 18 份 catalog 的
本機倚天聯集曾重建為 1022 字模，正式 loader 對當時 6136 個譯文字元
零缺字。第七頁仍尚未接 runtime 或做中文 A/B。
第七頁後合法 Enter 又到第八頁，固定故事區四行已有低階身分與繁中 DRAFT；右側動態狀態列
排除。全部 19 份 catalog 的私有倚天子集為 1025 字模，正式 loader 對 6175 個譯文字元
零缺字；第八頁仍未接 runtime。
第八頁後的合法 Enter 又量到第九頁唯一固定故事行，繁中 DRAFT 已建立，右側姓名與動態列
排除；全部 20 份 catalog 的本機倚天子集 1026 字模，正式 loader 對 6182 個譯文字元
零缺字。後續以固定 dosgolem runner 雙重重生，補齊該行 20 筆 verified RETF、同 SS、
SP+`0x12` 與七 ABI word 高位為零；但從合法 page9 state 再送 Enter 雖在 BIOS
`INT 16h AH=00` 被消費並進入 row 15 command/status，兩次至 370M 均未改寫 page9
故事區，沒有可授權失效的最早相交 pre-write。真正清除故事區的後續玩家動作仍未知，
因此第九頁保持 DRAFT，尚未接 runtime 或做中文 A/B；見
[第一百三十四階段](docs/re/phase-134-story-page9-enter-trace.md)。
手冊明示的數字鍵盤 4／6 在同一合法 page9 state 各做雙重、361M–361.1M 的有界重播：
兩鍵皆於 `361000150` 被 BIOS 消費，只在 row 24 產生 command/status clear／33 glyph，
`story_fill_writes`／`story_pixel_write` 均為空，沒有碰到故事區。這兩鍵不能當作 page9
失效邊界；下一個候選必須先由手冊證實是適用於此 command state 的不同玩家動作，詳見
[第一百三十四階段](docs/re/phase-134-story-page9-enter-trace.md)。
同一 consumer 已證實的手冊 Num Lock 8 亦做雙重、下一輪詢即停止的重播：step
`361000150` 消費後於 `361000605` 停下，無 clear、glyph、故事區 fill 或 pixel 寫入。
這不證明 8 的遊戲語意無效，但依停止條件不延長；目前所有已明示的 4／6／8 都沒有 page9
失效邊界，頁 9 維持 DRAFT，不能升 READY 或接 production。
第九頁後再送合法 Enter，兩次重播只見 row 15 command/status 重畫，無新固定故事行；
因此沒有第十頁 catalog，不猜補譯文，見[第一百三十六階段](docs/re/phase-136-story-page10-enter-stop-line.md)。
第 5、7、8 頁三處 DRAFT 譯文依私有原版畫面校訂後，20 份 catalog 的本機倚天子集
重建為 1024 字模，正式 loader 對 6179 個現行譯文字元零缺字；此變更不升格上述頁面。
見[第二、三頁證據](docs/re/phase-107-story-page2-draft.md)、
[第四頁勘誤](docs/re/phase-113-story-page4-corrigendum.md)、
[state 停止線](docs/re/phase-115-page4-state-recovery-stop.md)、
[首次 glyph trace 勘誤](docs/re/phase-124-story-page4-first-glyph-trace.md)與
[第五頁收據](docs/re/phase-122-story-page5-enter-trace.md)及
[第六頁收據](docs/re/phase-128-story-page6-enter-trace.md)及
[第七頁收據](docs/re/phase-129-story-page7-enter-trace.md)及
[第八頁收據](docs/re/phase-131-story-page8-enter-trace.md)及
[第九頁收據](docs/re/phase-134-story-page9-enter-trace.md)。

目前正式手冊 catalog 已補齊 39／39 題，每題是一段不超過 504 字的遊戲內繁中
意譯，不是整章手冊逐字轉錄。37 題有中文掃描對照；第 3、39 題因缺少直接的中文
掃描段落，依原版英文手冊翻譯並分開保存 URL、定位和本機快照 SHA。手冊單獨字模
934 個；新納入的身體圖示七筆譯文使 11 份 catalog 聯集成為 961 個，倚天字庫僅在
本機建置。39 題已通過資料、來源、字模與版面檢查；執行期同狀態收據目前涵蓋
第 32、38、36 題，
其餘仍待後續抽樣試玩，不宣稱逐題玩家路徑均已驗收。第三題新增收據見
[第一百零三階段](docs/re/phase-103-manual-third-question-runtime.md)。
手冊題目正確作答後的正常返回亦已於 2×／3× 驗證覆繪完全失效、完整
machine／DOS 狀態與控制組相等。由成功返回終態重新載入 dosgolem savestate 的
無鍵 A/B 也證明衍生手冊層不會復活；這不是原版遊戲內存檔／讀檔。手冊顯示
保存需進隊員管理選單並選 A–J 槽位；成功返回分支至 330M 仍只有 command/status，
已知的 Num Lock 前進鍵沒有可見或檔案效果；後續追蹤已證實此鍵被 BIOS 取走並交回
原版 consumer，且進入非零輸入分支，但尚未追至轉場或合法保存入口。
見[第一百零四階段](docs/re/phase-104-manual-success-return.md)、
[第一百二十一階段](docs/re/phase-121-manual-savestate-restore-boundary.md)與
[第一百二十三階段](docs/re/phase-123-manual-return-save-load-entry-boundary.md)、
[第一百二十六階段](docs/re/phase-126-manual-return-keyboard-consumer-boundary.md)。

操作列已在正常角色建立→技術技能頁接線；
2× 維持逐位元不變、3× 中文字模改為 22×22 並縮緊字距，白色快捷字母不變。
該頁控制組／雙倍率完整存態與原版 indexed 畫面相等，安全矩形外零差異；
其他焦點與離頁生命週期仍待驗收。身體圖示目前只完成 exact 事件、繁中 TSV、
安全矩形、字模覆蓋與離線 request projection。ignored、由 `git archive` 建立的
可丟棄 probe 已在正常移動／拒絕／確認雙重重播確認七筆低階 glyph 均經
`0763:03D6` 的 `0xCA` RETF 回到 `0763:049B`、同 SS、SP+`0x12`；每次字串首 glyph
的 ABI 高位 mask 為 `0x7c`，其餘 glyph 為零。production 未改；各安全矩形最早相交
pre-write 後續已由通用 A000 pre-write observer 完整量測 move／refuse／confirm 固定排程，
可丟棄 typed-core 與雙倍率正式倚天 containment 亦通過。第一次獨立審查指出的兩項缺口
後續已補：真實三路 receipt 時序直接驗證 event→group／transition→generation，A000
dirty-state 原型也在 first intersecting write 前原子失效整代並通過負向矩陣。第二次獨立
審查據此通過限縮 READY；production 後續已在 dosgolem `ae36f54` 接入正式 watcher、
A000 dirty-state 與雙倍率 presenter。固定 move／refuse／confirm 的 18 份 control／2×／3×
A／B 收據證實核心語意與 indexed 畫面相等、矩形外及動態圖示區零污染、零缺字與
first-write 清除生命週期；獨立 production 審查通過，現於此限縮範圍標為 CONFORMED。
儲存詢問離頁、restore、完整開機及其他輸入仍排除；詳見
[第一百四十階段](docs/re/phase-140-body-icon-ready-evidence-stop.md)與
[第九十九階段收據](docs/re/phase-99-action-bar-3x-density.md)。
身體圖示資料切片見[第一百零一階段](docs/re/phase-101-body-icon-text-catalog.md)，
手冊與快捷列的最新抽樣邊界見[第一百零二階段](docs/re/phase-102-overlay-audit.md)。

第九十七階段：依使用者檢視畫面後的要求，2× 手冊輸出維持逐位元不變，
3× 的手冊中文字放大到 22×22、置於原 24×24 字格內。新增並經原圖校正的
`Technical Skills` 題已在錯答換題正常重播中顯示，兩題均有同狀態收據；
首題存態重啟至下個穩定文字呼叫點亦不殘留中文。詳見
[第九十七階段收據](docs/re/phase-97-manual-cjk-density.md)。#14 的遊戲內返回／存讀檔
仍待正常玩家路徑驗收，host 互動視窗尚未接通。

第九十六階段已完成本階段實作切片：兩位 Terra 分別交付正式倚天建置器及手冊執行期接線。
首題 2×／3× 真實重播可見中文；錯答重抽清除舊中文。兩情境均與控制組完整持久化狀態相等，
正文矩形外像素差為零。來源色由原版 dispatcher 參數取得，不再使用預覽取樣替代。
收據與重跑入口見 [第九十六階段](docs/re/phase-96-eten-manual-runtime.md)。
尚缺：#14 返回／存讀檔驗收、互動式前端，以及目前未命中的題目翻譯；不以本輪外推完成。
以下階段段落為歷史能力紀錄；其中「尚未接線／尚未實作」以本段最新結果為準。

第九十五階段已完成：使用者已選定倚天字型 `top-pad`（output row 0 為零、source rows 0..14
落在 rows 1..15；排除 `bottom-pad`）。唯讀 Docker 探針已驗證正式手冊 691 glyph 的完整 Big5
分區、來源雜湊、保留區拒絕與 `GOLEMFNT` 16×16 載入契約；spec 008 已 READY。這只授權
GitHub Issue #15 實作本機 builder。第三方字型與衍生產物仍只准在 `workplace/`，不得進 Git、GitHub
或公開封包；#13 的前景色來源與 #14 的正常玩家 presenter 接線尚未開始。

第六十五階段已完成：角色資料／重擲頁 35 個靜態 request 已接入 dosgolem 明示 2×／3×
runtime overlay。base／`Y` 各雙倍率雙重重播決定，安全矩形外差異為 0、raw framebuffer
不變；spec 038 已 CONFORMED。產品預設倍率仍未選。此終態 dosgolem palette 將動態值色號
15 映成黑色，未覆繪 baseline 亦如此；這不是中文層清除，動態值可讀性／palette parity 尚未完成。

第六十四階段已完成：角色資料／重擲頁的 35 個靜態 exact identity 已建立繁中 catalog，
dosgolem spec 037 已 CONFORMED。四次 Enter 與其後 `Y` 分支各雙重重播，分別產生 43／52
筆 request；JSON 與 framebuffer 各自逐 byte 相同，原版畫面雜湊未變。動態姓名、身分、
摘要、能力值、技能值與骰值皆未進 catalog；本階段尚未接 renderer，也未選 2×／3×。

第五十七階段已完成：dosgolem 已將 14 筆靜態請求接到輸出端繁中 RGBA 覆繪；
`026F:029C` 清除矩形與同原點取代契約使終態只保留當下 `roster.add_prompt`。
2×／3× 各兩次可決定重生，原版 framebuffer、輸入、FileOps、writes 與存檔不變；
動態姓名列零覆繪差異。spec 035 已 CONFORMED，但 2×／3× 產品預設仍留給使用者決定。

第五十六階段已完成：保存→功能選單→名冊→加入隊伍 catalog 已接入 dosgolem 唯一 guarded
`MenuRequestWatcher`。兩次完整正常路徑皆為 18 events／14 requests／4 dynamic-name misses，
3 writes 與 2,611 FileOps 逐項等於無 catalog baseline；framebuffer 與保存檔亦逐 byte 不變。
spec 034 已 CONFORMED，專案 100 項測試及 dosgolem 全套 test／vet／race 通過。仍未接
renderer，2×／3× 尚待使用者決定。

第五十五階段已完成：第五十四階段保存→名冊→加入正常路徑的 18 筆事件已鎖成 exact identity
清冊。四筆姓名事件分別是固定欄寬 `A`、反白／正常 `A` 與已加入標記 `* A`，均明確禁止進入
翻譯 catalog；兩筆新增靜態文案與五筆尚缺功能選單文案已有正式繁中譯文。97 項專案測試
通過，字元清單含 37 個唯一字元。尚未接 renderer，2×／3× 仍待使用者決定。

## 已確認的產品方向

使用者於 2026-09-20 確認維持原訂的 **dosgolem 執行期輸出端繁體中文化**。已排除
clean-room remake／重寫引擎分支；後續只可在不改動原版 EXE、資料、規則、手冊驗證或
存檔語意的前提下，建立原版輸出事件、中文覆繪與同狀態收據。

- 第一階段「可觀測的原版啟動與文字輸出基線」已以 dosgolem 完成：真實 `START.EXE`／
  `GAME.OVR` 可由固定狀態經 BIOS 空白鍵走到玩家可見功能選單，兩次 raw VRAM 雜湊相同。
- 權威收據與未解項目見 [原版觀測證據索引](docs/re/README.md)；原始輸入與收據只在被
  Git 忽略的 `workplace/`。
- 已完成第二階段：`0763:0424` 已證實讀取 `[length:u8][ASCII bytes]`，再經 `0763:026B`、
  `0763:1809` 到 `0763:183A..1863` 畫出 8×8 英文 glyph；選單樣本含原文字串 pointer、
  色彩與文字格座標。完整證據見 `docs/re/phase-2-text-dispatch-and-lifecycle.md`。
- 清除／捲動、游標反白、畫面轉換、返回與存讀檔後的覆繪失效時機仍未知，因此
  `docs/spec/001-menu-text-output-overdraw-draft.md` 仍是 DRAFT，未授權 production hook。
- 功能選單的 BIOS Enter 轉場現已量到：新字串輸出可早於舊選單像素清除，因此覆繪不能以
  「下一筆字串已輸出」當成畫面失效判定。詳見 `docs/re/phase-4-menu-interaction-lifecycle.md`。
- `PICK RACE` 的 BIOS Escape 返回亦已量到：原版取走 `0x1B` 後，第一筆新文字 dispatch
  仍早於舊標題像素清除；終點逐位元等於既有功能選單基線，獨立重播結果相同。詳見
  `docs/re/phase-5-pick-race-return-lifecycle.md`。
- dosgolem 已依使用者指示複製至被忽略的 `workplace/dosgolem/`，工作分支為
  `buck-rogers-cht-output-overlay`，基準 commit 為 `d9c0c27ca9af8239c7e96272a7165e03d7da04bf`；
  後續 probe 與 adapter 變更只在該副本進行。
- 第六階段已訂正清除定位：watchpoint 的 `0CF4:1B3C` 是 `REP STOSB` 後的下一個 IP；實際
  寫入在 `0CF4:1B3A`，其函式 `0CF4:1B2B` 是通用 byte-fill，已排除為 invalidation hook。
  兩條轉場共用的上層候選是 `026F:029C` Mode 13h 矩形清除例程；Enter 清除
  `x=8..311,y=16..183`，Escape 返回清除 `x=0..311,y=0..183`。完整證據見
  `docs/re/phase-6-clear-path-hook-evidence.md`。
- 第七階段已證實 `0763:0424` post-call：`Create New Character` 最後 glyph 於
  #100,025,833 寫完，#100,025,943 才返回 `37F1:1856`。現有 `OnCall` 足以在 adapter
  觀測 return，但必須由 entry 建立 pending frame，並以 return address、`SS` 及
  `SP == entry SP + 0x10` 排除自然 fall-through；`37F1:15BD` 已有實際反例。Enter 的事件
  順序是舊選單 post-call → 矩形失效 → 新畫面 dispatcher／post-call。完整證據見
  `docs/re/phase-7-text-post-call-generation-event.md`。
- 中文手冊 RAR 已在 Docker 以 `lsar`／`unar` 盤點、完整性測試與解壓；80 個 archive
  項目通過、79 個實體檔案已有 SHA-256 清冊，並有 77 張 JPG 的 archive-order 定位。
  詳見 `docs/re/phase-3-manual-input-inventory.md`。手冊語意、頁碼與原版題目對應仍未知。
- 第八階段已建立首批 UTF-8 繁中 TSV，並由正常 Enter 路徑傾印九筆可見來源；六個種族
  譯名已用中文說明書核對。GNU Unifont 2× 填滿格與 3× 置中兩份本機 prototype 均完整
  清除第一筆 20 格原文且未越界。正式倍率仍待使用者選擇，尚未建立 production adapter。
- 第九階段已把 psychic-war 驗證過的遊戲無關 `xlate` package 移植到 workplace dosgolem
  專用分支，本機 commit `b33cfbf`；`xlate` 與全部正式 packages 均通過。現行 `Draw` 只接受
  3 的倍數倍率，所以仍不能把它解讀為使用者已選 3×。dosgolem 遠端推送待明確外傳授權。
- 第十階段已把 TSV 驗證、決定性字元清單與 Unifont→GOLEMFNT 16×16 子集建置工具納入
  專案。現有 8 筆譯文導出 24 個唯一字模；904-byte prototype 已由 dosgolem production
  `xlate.LoadFont` 回讀並覆蓋全部 29 個譯文字元；fontcheck 位於本機分支 commit `8a22460`。
  字型二進位只留 `workplace/`，正式字型與 2×／3× 決策仍 pending。
- 第十一階段已由載入 A 存檔後的正常功能選單路徑，證實進入冒險會顯示
  手冊查詢。第一題為英文 Log Book 第 34 頁 `Deimos Prison` 第十字；明確錯答
  後原版會重新抽題。對應繁中來源是 `SCAN0352_039.jpg` 印刷頁 73 的「49. 在監獄中」。
  `docs/spec/002-manual-paragraph-overlay-draft.md` 只允許輸出端顯示中文段落，禁止自動作答或改原版判定。
- 第十二階段已證實手冊題庫位於執行期 `0EC0:00C2..0553`，共有 39 筆 30-byte 紀錄；
  頁碼、英文標題與序數已形成可重生清冊。工具不解碼、不輸出答案；第 32 與第 38 筆已
  分別對回動態 `Deimos Prison` 與 `Technical Skills` 抽題。中文來源仍只有前者唯一確認。
- 第十三階段已逐筆建立繁中掃描來源對照：35 筆已證實、3 筆強推論、`Roll.` 1 筆因素材
  只到印刷頁 87 而未知。來源 SHA-256 全部通過既有 manifest 驗證；OCR 只作搜尋線索，
  尚未逐字校訂的段落沒有加入顯示 catalog。
- 第十四階段已由原圖校訂八筆單一短段落，連同既有 Deimos 共建立 9 筆
  `manual-events.tsv → manual.zh-TW.tsv` 精確映射。事件／題庫／來源／catalog 驗證要求
  來源必須為 `confirmed` 且沒有孤兒鍵；段落長度 35–236 字元，尚未據此決定分頁或倍率。
- 第十五階段再由原圖校訂八筆規則／生物／旅程短段落，事件與 catalog 增至 17 筆；新增內容
  長度 31–216 字元，全部通過既有 confirmed 來源與精確題目身分驗證。
- 第十六階段盤點剩餘 18 筆 confirmed 候選，只納入 5 筆非表格、非跨頁且內容完整的項目；
  事件與 catalog 增至 22 筆。其餘 13 筆已依跨頁、長章節、清單或表格分類，不以截斷內容
  湊數；完整排除收據見 `docs/re/phase-16-manual-compact-paragraphs-3.md`。
- 第十七階段以真實手冊查詢 VRAM 建立 2×／3× 分頁 prototype：安全矩形為
  `[7,312)×[7,184)`，正文 36×17 格、每頁 612 字；當時的 236 字段落為 1 頁，708 字壓力
  樣本為 2 頁，兩案安全矩形外皆為 0 px 變更。這是已由保留原題 504 字版面取代的整框
  prototype；2×／3× 的歷史 renderer 限制不再決定現行 production 容量。
- 第十八階段已由固定狀態兩次重播答錯換題：新題首於 #301,127,835 出現，局部矩形清除
  到 #301,166,163 才發生，證實原版不會先整面清空。DRAFT 契約改以精確題首 entry 立即
  使舊 generation 失效，累積頁碼／標題／序數後，只在 `word?` guarded post-call 顯示新
  中文段落；兩次終態 raw VRAM 雜湊一致。完整收據見
  `docs/re/phase-18-manual-generation-invalidation.md`。
- 第十九階段建立未接入 production 的題目事件收集器 prototype：題首建立 generation，六筆
  guarded post-call 依序累積 page／heading／ordinal，`word?` 才提交唯一鍵。真實事件重建
  `41 / Technical Skills / second`；9 項測試涵蓋缺欄、亂序、重複、未知 caller、錯誤頁碼及
  舊 generation 延遲返回，均失敗即關閉。完整設計見
  `docs/re/phase-19-manual-event-collector-prototype.md`。
- 第二十階段把完整題目鍵接到正式事件與繁中 TSV：`Deimos Prison / tenth` 唯一命中 73 字
  顯示請求，未有完整校訂段落的 `Technical Skills / second` 明確不顯示。12 項測試涵蓋
  generation、精確身分、各層唯一性、孤兒鍵、無效 UTF-8 及顯示請求不含答案。runtime
  ordinal 目前只動態證實 `second → 2`、`tenth → 10`，完整橋接仍是 READY 前置。詳見
  `docs/re/phase-20-manual-catalog-display-request-prototype.md`。
- 第二十一階段以 IDA Pro 9.4 與 runtime dumps 證實原版序數表：consumer 將題庫
  `record[+14]` 乘 19 後加 `0EC0:339B`，索引 `first` 至 `tenth` 十個長度前綴 slots。
  `text/manual-ordinals.tsv` 可由原版 dump 決定性重生，現有 22 筆 catalog ordinal 全數涵蓋；
  7 項正反向測試通過。完整證據見 `docs/re/phase-21-manual-ordinal-bridge-evidence.md`。
- 第二十二階段已在 workplace dosgolem 分支擴充 `xlate.Draw`：正整數倍率皆可用，2×／3×
  的 16×16 字模精確像素、非法倍率與短緩衝區裁切測試均通過；真實 GOLEMFNT 已畫出繁中
  「地球」。本機 commit 為 `ef7f8db32b20a6b9eb6d810bd4e6b99187c55f44`，未推送 dosgolem
  遠端。這不代表已選定產品倍率，詳見 `docs/re/phase-22-dosgolem-xlate-integer-scale.md`。
- 第二十三階段已將第 19–21 階段的事件／序數／catalog 契約審查為 dosgolem READY 子規格，
  並實作 `apps/buckrogers` 未接線純核心。正式 TSV、generation、poisoned 復原與 malformed
  反例測試、`go vet`、race detector 及所有正式 packages 均通過。本機 commit 為
  `8ce092f29d000ea7e6765c4f3389fe484aefa555`，未推送 dosgolem 遠端；玩家可見整合仍為 DRAFT。
- 第二十四階段已完成 dosgolem runtime watcher：`0763:0424` entry 保存 caller／SS／SP，
  只有 return address、相同 SS 與 `SP+0x10` 三重 guard 通過才提交片段；`026F:029C` clear
  亦已接線。由 #266,399,999 固定狀態重播的第一題在 #266,557,246 精確產生
  `manual.page34.deimos_prison.word10` 顯示請求，收據只含 metadata。watcher 不送鍵、不含
  答案、不寫原版狀態且尚未繪圖；dosgolem 本機 commit 為
  `38585dcd9e3861b6fa64a1b89dbec19e5a038dd7`，未推送其遠端。
  詳見 `docs/re/phase-24-manual-runtime-watcher.md`。
- 第二十六階段已完成 README 穩定入口：以 SSI 產品目錄、原版 Rule Book 保存掃描及
  MobyGames 版本／製作資料介紹作品歷史、Gold Box 系譜與核心循環；同時明確標示本專案
  非 remake、原版素材須合法自備、尚無玩家版或 Release，且繁中尚未接入正式畫面。
- 第二十七階段已由相同正常 Enter 固定輸入重生功能選單到 `PICK RACE` 的九筆 dispatcher
  entry／guarded post-call。`text/menu-events.tsv` 以長度／SHA-256、caller、色號與座標連到
  八個正式繁中 key，不保存原文全文；真實 receipt verifier 與正反向 schema 測試均通過。
  dosgolem 本機 commit 為 `98f3bec55d633cc2a69099f187848af4d765b7d1`，未推送其遠端。
- 第二十八階段已把九筆事件接成 dosgolem READY 純核心：`MenuCatalog` 嚴格載入正式事件／
  繁中 TSV，以完整 length／SHA-256、caller、色號與座標精確解析 `DisplayRequest`；真實
  第 27 階段 receipt 九筆全數命中，所有正式 packages test／vet 與 Buck Rogers race
  detector 通過。本機 commit 為 `0be85255d9cd5428c6b55a813410dcacbfd73a4f`，未推送
  dosgolem 遠端；尚未載入字型、繪圖或接入玩家可見路徑，選單整合仍是 DRAFT。
- 第二十九階段已把 `TextRecorder` 與 `MenuCatalog` 接成 CONFORMED runtime request watcher：
  同一正常 Enter 固定狀態在九筆 guarded post-call 各直接提交一筆繁中 `DisplayRequest`，
  零 drop／pending／catalog miss。收據只含事件 metadata、key 與譯文字數；dosgolem 本機
  commit 為 `c6a963dafaf3f060a43816f8a6acbda90aa8b7a0`，未推送其遠端。尚未載入字型或繪圖。
- 第三十階段由正常 Down／Up 證實種族選單 selection lifecycle：舊列先 normal redraw，新列
  再 selected redraw；同終點 Down 差異只在 `(24,24)–(79,39)`、832 pixels，Up 後逐位元
  回到 steady。正式 text-safe rectangle 已分離 col 1 原文清除範圍與 col 3 中文 anchor。
  三筆新增 variant 尚未接入 catalog；dosgolem 本機 commit 為
  `d55a4c84c3474034257cddf58d6fa32cff3d60d4`，未推送其遠端。
- 第三十一階段已把三筆 selection variant 納入正式 12-identity exact catalog；固定
  Enter→Down→Up 路徑兩次都產生逐位元相同的 13-event／13-request 收據，零 drop、pending、
  catalog miss。舊九事件收據仍嚴格驗證前九筆；dosgolem 本機 commit 為
  `79ecc2b9585f02339eef181ecb88b752bee4c2aa`，未推其遠端。字型、renderer 與倍率仍未接入。
- 第三十二階段以 steady／Down 真實 framebuffer、正式 TSV 與 dosgolem `xlate.Draw` 重生
  2×／3× 選單 A/B；兩批逐檔相同，四份收據皆零缺字、零重疊、零安全矩形外差異。
  2× 為 640×400／16×16 滿格，3× 為 960×600／16×16 ink 置中 24×24 格；本機 dosgolem
  commit 為 `09f580877b0d1e34ef00fa44eddefa12898b7e53`，未推其遠端。
- 第三十三階段以 steady／Down 各 978 點長窗口證實：完整 palette 不變，色號 0／15 同為
  黑色，selected row 完成後 pixels 與事件數都維持固定；取樣窗口內沒有 palette blink 或
  週期性 redraw。未來忠實 renderer 必須保留黑底黑字 selection style；dosgolem 本機
  commit 為 `41917c85007efe17154cb92422cba3fe6539ad88`，未推其遠端。
- 第三十四階段已把離線診斷命令的 stamp／ink／containment 規則移入 dosgolem
  `apps/buckrogers` 倍率中立純核心；呼叫端必須明示倍率，沒有產品預設值。steady／Down ×
  2×／3× 的繁中 PNG、base PNG 與 JSON 全部逐 byte 等於第 32 階段基線；spec 015 已
  CONFORMED，本機 dosgolem commit 為 `64b15779edc9d5be35e1acba0f854ba022008511`，未推其遠端。
- 第三十五階段由正常雙 Enter 選定預設種族，兩次重生相同的 14-event 收據與終點
  framebuffer；下一個性別選擇畫面新增提示、兩筆 normal 選項與 selected 第一選項共四筆
  content-safe identity。dosgolem spec 016 已 CONFORMED，本機 commit 為
  `7009315c5a04981eb1b048e7bba34a0b932fbf6d`，未推其遠端；尚未建立譯文或量方向鍵 lifecycle。
- 第三十六階段以正常 Down→Up 與 Escape 完成性別選擇生命週期：前者依序 normal／selected
  重畫兩列並逐位元回到第一列終點；後者先取消男性反白，再重建上一層功能選單，而非返回
  種族選單。兩路徑各自雙重重播一致，專案 50 項測試通過；dosgolem spec 017 已 CONFORMED，
  本機 commit 為 `57daa16fd3ab38ff19b8b1702fecf5b0ca14992d`，未推其遠端。仍未建立性別譯文或 renderer。
- 第三十七階段已把七個性別 identity 與三筆繁中 catalog 接到既有 guarded post-call watcher：
  Enter→Enter→Down→Up 兩次皆為 18 events／18 requests／零 miss；Escape 兩次皆為 22 events／
  15 requests／7 misses，且返回功能選單後不沿用性別請求。dosgolem 共用 exact catalog 核心，
  沒有第二套 watcher；spec 018 已 CONFORMED，本機 commit 為
  `24f0dd55cdce8a929ab513e2a2a1f78afb6fb56b`，未推其遠端。仍未載入字型、繪圖或選倍率。
- 第三十八階段由第三個正常 Enter 接受預設性別，證實下一畫面為五選項職業選擇；兩次
  22-event JSON 與終點 framebuffer 各自逐 byte 相同，新七筆 content-safe identity 已由
  嚴格 verifier 覆蓋。dosgolem spec 019 已 CONFORMED，本機 commit 為
  `371683b7f5793c7104e839202497c742ba3e13c0`，未推其遠端；尚未量職業方向鍵／返回，也未建立
  職業譯文或 renderer。
- 第三十九階段以正常 Down→Up 證實職業第一、二列依序 normal／selected 重畫，並逐位元
  回到第一列初始狀態；Escape 先取消第一列反白，再重建功能選單，而非返回性別選擇。
  兩條路徑各自雙重重播一致，專案 61 項測試通過；dosgolem spec 020 已 CONFORMED，本機
  commit 為 `d8f34f101c719e6939565fe8b6f0d8b531e07ccc`，未推其遠端。尚未建立職業譯文、renderer
  或倍率預設。
- 第四十階段由中文說明書原圖核對五個職業譯名，將十個職業 identity 接到 dosgolem 共用
  exact catalog 與 guarded post-call watcher。steady／Down→Up／Escape 各雙重重播一致，分別
  為 22／26／23 requests；Escape 返回選單的不同 identity 正確形成七次 miss，未放寬比對。
  專案 65 項測試與 dosgolem 正式測試、vet、race 全數通過；spec 021 已 CONFORMED，本機
  commit 為 `0025008fbb7d49c42e352f961585a10e82c118e5`，未推其遠端。仍未載入字型、繪製繁中像素
  或選定倍率。
- 第四十一階段以四個正常玩家路徑 framebuffer 完成性別／職業 2×／3× 覆繪 A/B；八組
  輸出各重生兩批，皆零缺字、零重疊、安全矩形外零差異且 ink contained。2× 是 640×400、
  16×16 滿格；3× 是 960×600、16×16 ink 置中 24×24 格。兩者幾何皆可行，2× 仍較接近
  PC-98 Golden Box CJK 密度，但尚未被使用者選定；spec 022 已 CONFORMED，本機 dosgolem
  commit 為 `73e610943cb26ed3f0990ecd13bd196d12fe162a`，未推其遠端。
- 第四十二階段由第四個正常 Enter 接受預設職業，證實下一畫面為角色資料／重擲能力值頁；
  兩次 118-event JSON 與 framebuffer 各自逐 byte 相同，新增 96 筆事件已區分靜態標籤、
  動態值、能力值、技能與重畫角色。固定 snapshot 可重生相同結果，但 seed 與亂數實作仍
  未辨識，不外推自然開局；dosgolem spec 023 已 CONFORMED，本機 commit 為
  `1e8060b5a83665da1e1b74a4f02cb391f938e25d`，未推其遠端。
- 第四十三階段以正常 BIOS `Y`／`N` 證實重擲與接受分支：`Y` 新增 31 筆事件後回到同一
  提示，`N` 新增 65 筆事件後進入姓名提示。兩分支各自雙重重播一致；固定 snapshot 可
  重生同一組結果，但 seed／亂數公式仍未知。spec 024 已 CONFORMED，dosgolem 本機 commit
  為 `4f899924b35e14fdb7ef23bbb2fcd2620284ae43`，未推其遠端。
- 第四十四階段證實姓名字元逐字回顯，Backspace 直接清除最後字元但沒有 dispatcher 事件；
  非空姓名 Enter 轉入職業技能點配置畫面。Escape 只重印提示，空字串 Backspace 無變化。
  編輯與確認分支各自雙重重播一致；spec 025 已 CONFORMED，dosgolem 本機 commit 為
  `260b3a7f504f7ade6b5487aa591e99911a82bd13`，未推其遠端。
- 第四十五階段以正常 BIOS 輸入證實職業技能配置畫面的 Down 會由第一列移到第二列，預設
  動作下 Enter 可替第一項技能合法加一點；仍有 6 點未用時 Escape 顯示確認提示，`N` 會
  回到逐 byte 相同的配置畫面。三條分支各自雙重重播一致，專案 82 項測試與 dosgolem
  正式測試、vet、race 全數通過；spec 026 已 CONFORMED，本機 dosgolem commit 為
  `a0bb175d4712b92ce183ac1bd8715aaa6b4bcbec`，未推其遠端。減點、`Y` 離開與配置完成後轉場
  仍未證實；本輪未翻譯、接 renderer 或選定倍率。
- 第四十六階段證實職業技能配置的預設 Enter 加點後，Right→Enter 會把同一技能與剩餘點數
  完整還原；終點逐 byte 等於零點／Right 選取畫面。Left 由預設位置環回離開位置；Escape→
  `Y` 在未用 6 點時仍可進入技術技能配置畫面。兩條正式分支各雙重重播一致，專案 85 項
  測試與 dosgolem 正式測試、vet、race 全數通過；spec 027 已 CONFORMED，本機 dosgolem
  commit 為 `dbd262607c90be3a0e92b7173b61bbf140823580`，未推其遠端。技術技能互動與角色建立完成
  仍未證實；本輪未翻譯、接 renderer 或選定倍率。
- 第四十七階段由正常路徑進入技術技能配置，證實 Down 選取移動、Enter 加點、Right→Enter
  完整減回、Escape→`N` 回到逐 byte 相同基線，以及 Escape→`Y` 進入角色身體圖示選擇。
  四條正式分支各雙重重播一致，專案 88 項測試與 dosgolem 正式測試、vet、race 全數通過；
  spec 028 已 CONFORMED，本機 dosgolem commit 為
  `0b66a03808f9d67e2c57ca23e82ad56eb08ac254`，未推其遠端。身體圖示互動與角色建立完成仍未
  證實；本輪未翻譯、接 renderer 或選定倍率。
- 第四十八階段證實四方向鍵皆改變角色身體圖示選取；正式 Right 分支固定為 297 events。
  Enter 與 Escape 顯示逐 byte 相同的確認提示，Enter→`N` 重建並回到圖示基線，Enter→`Y`
  進入儲存詢問畫面。三條正式分支各雙重重播一致，專案 90 項測試與 dosgolem 正式
  test／vet／race 通過；spec 029 已 CONFORMED，本機 dosgolem commit 為
  `b385b85103ada0e381063f4869e42b3f006c2f6b`，未推其遠端。尚未回答儲存詢問，也未翻譯、
  接 renderer 或選定 2×／3×。
- 第四十九階段證實儲存詢問採選項操作：直接字母 `Y` 無作用，直接字母 `N` 接受預設
  `NO`；Left→Enter 接受 `YES`。兩條接受分支都回到逐 byte 相同的功能選單，四份 writable
  overlay manifest 當時也相同。但該命令未設定 `DOS.Scratch`，所以零副作用結論已撤回，
  spec 030 改標 SUPERSEDED；畫面、輸入與事件結論仍有效。
- 第五十階段新增 `-scratch` 與 content-safe `-file-ops`，以正式 scratch-backed 收據重驗：
  `NO`／`YES` 都 shadow `CHARS.DAX` 但沒有 DOS write，四份 scratch 內容皆等於 pristine；
  兩分支進入加入角色功能都沒有角色列並返回相同功能選單。各雙重重播為 316 events，專案
  94 項測試與 dosgolem 正式 test／vet／race 通過，spec 031 已 CONFORMED，本機 dosgolem
  commit 為 `5b5f9b59318033acdd4d444754bb43abc68863d5`，未推其遠端。此路徑使用未用技能點
  離開，不能外推完整配置後的合法角色保存結果。
- 第五十一階段進行中：正常 BIOS 路徑已實際配置完 80 點職業技能與 40 點技術技能，兩者
  歸零後無警告進入身體圖示畫面。第一個完整配置後的保存／名冊 probe 仍沒有 DOS write，
  scratch `CHARS.DAX` 與 pristine 同雜湊並回到空名冊；尚須對齊第 48–50 階段後段事件與
  按鍵時點，未判定為 dosgolem 檔案服務缺口，也尚未形成正式雙重重播或 CONFORMED 規格。
- 第五十二階段已排除後段按鍵時點、身體圖示未移動與已記錄的未實作 DOS／BIOS 服務；
  `-unimplemented`／`-state-out` 的 spec 032／033 已 CONFORMED。完整配置正式雙重重播的
  JSON、framebuffer、scratch 及回讀後 1 MiB memory 一致，但 `SAVE A? YES` 仍無 DOS write，
  Add 仍無角色列。找到的 DGROUP／heap 差異均未被 Add consumer 讀取，原版保存條件仍未知；
  dosgolem 診斷功能在本機 commit `4bb3cc9d83868ea2d827cff33b43e2585c7f16ac`，未推其遠端。
- 第五十三階段已訂正保存選項：由同一 `save-before.state` 直接預設 Enter 才是真正保存，
  會決定性建立 259-byte `A.who` 與 124-byte `A.stf`；Left→Enter 不保存。先前第 49–52 階段
  的 `NO`／`YES` 標籤及零寫檔推論均已追加勘誤。兩路 IP trace 各自雙重一致，保存檔雜湊
  亦一致；完整 memory 因 DOS 取時而尚未證實逐 byte 決定性。下一步以真正保存分支接續
  Add 正常玩家路徑，確認名冊是否顯示角色。
- 第五十四階段已完成保存→Add→加入的正常玩家垂直鏈：Add 先讀 `A.WHO` 的 16-byte 起始區
  與 offset 194 資格 byte，列出角色 `A`；Enter 後顯示 `Loading...Please Wait`，完整讀取
  259-byte `A.WHO` 與兩筆 62-byte `A.stf`，回到 Add 時角色已從可加入名冊移除。兩次完整
  重播的 18-event／2,611-FileOps JSON 在正規化 scratch 路徑後逐 byte 相同，framebuffer
  與保存檔亦相同；未實作服務為空。原空名冊根因已關閉為不保存分支誤標。

下一個前沿決策仍是 2×／3× 輸出倍率；兩者 renderer 能力、倍率中立選單純核心及功能選單／
手冊離線 A/B 都已具備。確認後才能把選定倍率寫入 READY 規格並接入正常玩家路徑 renderer，再做連續幀反白、
轉場清除與同狀態 A/B。3 筆強推論與 `Roll.` 缺頁仍失敗即關閉；runtime 畫面與分頁互動
驗證前，手冊與選單覆繪 DRAFT 不升為 READY。不依賴倍率的目前安全切片是把完整技能配置後
的圖示確認、保存與名冊事件逐項對齊，再重驗合法角色是否可見。

第六十階段已完成手冊覆繪 READY 前置稽核：39 題來源為 35 confirmed、3 strong-inference、
1 unknown；正式事件與譯文各 22 筆，其餘 17 題維持原版英文。正式譯文最長 236 字；當時
依整框 prototype 的 612 字結論已由第八十三階段 504 字資料契約取代。spec 002 已把正常路徑
覆繪、錯答重抽、像素 containment 與同狀態 A/B 正確歸入實作後 CONFORMED；本輪未修改
dosgolem。

第六十一階段曾將整框 prototype 的 36 欄×17 列、612 字上限落成資料閘門；該閘門已由
第八十三階段依保留原題決定取代為 36×14、504 字。612／613 的測試收據只供追溯舊方案，
不再是現行 production 容量。當輪沒有新增分頁、截斷或 runtime 行為，dosgolem 未修改；
spec 002 仍為 DRAFT。

第六十二階段檢視真實手冊畫面後，發現第 17 階段整框 prototype 會遮住原版頁碼、英文標題
與序數，玩家將失去完成原版驗證所需的題目資訊；因此訂正 Phase 60「唯一 blocker 是倍率」
的結論。新的保留題目 prototype 把上方 `[7,312)×[7,72)` 留給原版，只在下方顯示中文；
正文容量為 36×14＝504 字，現有最長 236 字仍單頁。2×／3× 圖均已重生並目視通過。
目前最前沿決策是「保留原版題目」或「整框替換並另設計中文題目提示」；建議前者。使用者
當時尚未確認前不實作 production presenter，也不將 612 上限改成 504；此暫停已由使用者
後續決定及第八十三階段的 504 字資料契約取代。dosgolem 當輪未修改。

第六十三階段已把性別／職業 exact request 與安全矩形接進 dosgolem 長存 runtime overlay。
正常三 Enter＋Down 路徑在 2×／3× 各兩次均為 24 requests／24 actions、零 miss，終態只保留
職業畫面八個 keys；性別與舊 selected variant 已失效。兩倍率安全矩形外 0 px，原版 raw
framebuffer 全等於既有 class Down 基準。專案 105 項測試與 dosgolem 正式 test／vet／race
通過；dosgolem 本機 commit `e1d2070` 未推遠端。手冊版面與產品預設倍率仍待使用者決定。

第六十六階段已證實角色動態值呈黑是 dosgolem 的 mode 13h BIOS 預設色盤缺口：遊戲只寫
DAC 0–14，讓 index 15 沿用 BIOS 白色。通用修正載入標準 VGA 前 16 色，raw framebuffer、
事件與輸入完全不變；base／`Y`、2×／3× 各雙重重播決定性一致，HP 數值已在 RGBA baseline
成為可見白字。spec 205 已 CONFORMED；完整 DAC 16–255 預設表仍不猜補。產品倍率與手冊
版面仍待使用者決定。

第六十七階段已把角色姓名畫面的固定提示接成 exact runtime request。五鍵正常路徑固定為
183 events／1 request／182 misses；加送玩家 `A` 後為 184／1／183，單 byte 姓名回顯仍
失敗即關閉。兩路各雙重重播的 JSON 與 framebuffer 逐位元一致；本階段未新增安全矩形或
renderer，因此不影響仍待決的產品倍率與手冊版面。
dosgolem 實作已提交於本機 branch，commit `22f46b4`，未推送其遠端。

第六十八階段已將姓名提示接入明示倍率 runtime overlay：提示安全矩形止於 x=128，玩家輸入
始於 x=136。base／輸入 `A` 的 2×／3× 各雙重重播一致；差異只在核准矩形內，輸入欄零差異。
runtime 現在雙向拒絕缺少或孤兒 rectangle。本階段仍未選定預設倍率，也未處理手冊版面。
dosgolem 實作已提交於本機 branch，commit `6e16fe5`，未推送其遠端。

第六十九階段已關閉姓名提示轉場生命週期：`A`→Enter 後通用清除 hook 讓 active keys 歸零，
2×／3× RGBA 等於 baseline；Escape 已訂正為原地重印而非取消，兩次 request 以同 key replace，
終態只留一份 stamp。收據工具現可明示合法空終態 `drew=false`，但仍拒絕缺字或 active-key
不一致；沒有新增姓名專屬清除。本階段仍未選定產品倍率或手冊版面。
dosgolem 實作已提交於本機 branch，commit `8e60489`，未推送其遠端。

第七十階段已把職業技能配置的四個標題、八個一般技能列及兩個已證實 selected identities 接成
exact request。base 為 226／14／212，Down 為 234／16／218；動態點數與未實測 selected
variants 維持 miss。control／catalog 雙重重播的原版語意與 framebuffer 相同。本階段只建立
request，尚未建立安全矩形或繪製技能頁繁中像素。
dosgolem 實作已提交於本機 branch，commit `c4fb58c`，未推送其遠端。

第七十一階段已將上述 14 identities 建立 exact-width 矩形並接入執行期覆繪。
base／Down 的 2×／3× 各雙重重播一致；矩形外與 x≥184 動態數值欄均為 0 px，
原版 framebuffer 及 presentation 欄位外語意與 Phase 70 control 一致。選取列取代與
姓名提示轉場失效均無殘字。產品預設倍率及手冊版面仍待使用者決定。
dosgolem 實作已提交於本機 branch，commit `91407a4`，未推送其遠端。

第七十二階段已將技術技能配置頁接成 exact runtime requests。13 個技能譯名都回到
中文手冊 `SCAN0352_012.jpg` 第 19–20 頁原圖。technical catalog 新增 17 個不重複 identities；
「單項技能上限」與「點數／加值／總計」在兩技能頁是相同 identity，因此共享 career catalog，
不重複定義。base 為 289／32／257，Down 為 297／34／263；control／catalog 的原版語意與
framebuffer 相同。本階段只完成 request，尚未建立技術技能安全矩形或繁中像素覆繪。
<!-- phase-72-dosgolem-commit -->
- dosgolem 本機分支 `buck-rogers-cht-output-overlay` 的第 72 階段提交為 `790a41cbf03d056caedf87f06698f50cae90a8c1`；依專案規範僅保留於 `workplace/dosgolem`，未推送遠端。

第七十三階段已將技術技能配置的 17 個專屬 identities 與兩個 career 共享標題矩形接入 2×／3×
runtime overlay。首次沿用 request 停止點時人工圖像發現 selected stamp 尚為 `Pending`；延後至
下一穩定 frame 後繁中正常顯示，規格已把穩定 frame 與目視驗收列為必要條件。base／Down 的
兩倍率各雙重重播一致，矩形外與動態欄 0 px，原版 framebuffer 與語意不變。產品預設倍率及
手冊版面仍未替使用者決定。
dosgolem 本機分支提交為 `2d8561c8a87e6868c8e0d647fbcf69e6c18169c0`，未推送其遠端。

第七十四階段已證實技能頁底部五個操作標籤不經現有高階 dispatcher，而是
由上層 `37F1` caller 逐字進入 `0763:026B`，再由 `0763:1809` 畫 8×8 glyph。
職業三標籤與技術五標籤的初始／Right 焦點路徑、幾何、caller 與色彩已收進
content-safe 清冊；未觀測到獨立 disabled variant，維持 unknown。dosgolem spec 213 是
DRAFT，下一階段應實作 Buck Rogers 專屬 guarded glyph-event watcher，不能直接當成
原有字串事件。dosgolem 本機提交為 `7d8ca0b`，未推送其遠端。產品倍率與
手冊版面仍未決定。

第七十五階段已將技能頁底部逐字路徑接成 dosgolem `ActionBarWatcher`。
screen anchor 來自 exact 技能畫面標題，technical 只 allowlist 兩個 Phase 72 已證實的
career 共享標題；每字通過 `0763:026B` caller、mode=1、repeat=1、色彩、座標、
SS/SP far-return guard 與完整雜湊後才產生 content-safe event。八條正常路徑雙重播
均為 0 miss、0 drop，watcher/control framebuffer 與其餘語意收據一致；spec 213 已
CONFORMED。底部操作列仍未接繁中 request／overlay，disabled 仍是 unknown；下一個
不依賴產品倍率的安全切片是建立繁中 catalog 與 typed display requests。dosgolem
本機提交為 `356848c`，未推送其遠端。

第七十六階段已將技能操作列事件接成繁中 exact requests。「加點／減點／上頁／下頁／完成」
分級為 `runtime-interface`，不冒稱中文手冊逐字譯名。八條正常路徑的 event／request 數為
3／6／9／8／13／18／23／28；雙重播、純事件 control 與 framebuffer 非干擾均通過，
spec 214 已 CONFORMED。操作列仍未建立安全矩形或繪製中文；產品預設倍率與手冊版面仍未決定。
dosgolem 本機分支提交為 `6d17fd3`，未推送其遠端。

第七十七階段已證實技能操作列只應覆蓋原事件 `y=192..200` 的 8 logical-pixel band；既有
16×16 字模在 2×／3× 輸出均完整容納。向上擴張 16 logical pixels 會侵入金色底框，已排除。
dosgolem spec 215 為 DRAFT，本機提交 `952c596`，未推遠端。normal 原版採首字白、其餘綠；
繁中要保留首字白／次字綠或改為全綠仍待使用者依真實畫面 prototype 決定，故 production
overlay 尚未開工。產品預設倍率與手冊版面仍未決定。

第七十八階段已完成不依賴配色決策的 16 筆正式安全矩形與 style-neutral dosgolem 核心。
normal 必須逐 rune 明示 palette 10／15，沒有預設；兩個候選在 2×／3× 均通過 containment。
focus 固定沿用原版黑字白底。spec 215 仍是 DRAFT，CLI／runtime 尚未接線，繼續等待使用者
選擇 normal 配色。dosgolem 本機提交 `236cb3b`，未推遠端；產品倍率與手冊版面仍未決定。

第七十九階段已完成配色中立 `RuntimeActionBarOverlay`：同 action normal／focus 原子取代、
partial clear 整組失效、career／technical anchor 切換與 frame 後明示 palette 重套用均有測試。
兩候選及 2×／3× 共用相同 lifecycle，constructor 仍沒有預設值。spec 215 維持 DRAFT，正式
CLI 與正常玩家路徑覆繪只剩 normal 配色決策；dosgolem 本機提交 `6d230a1`，未推遠端。

第八十階段依使用者決定推翻前述兩個配色候選：技能操作列正式保留括號內拉丁助記字母，
只有字母為白色，括號與中文沿用 palette 10。五筆顯示改為 `(A)加點`、`(S)減點`、
`(P)上頁`、`(N)下頁`、`(D)完成`。ASCII 採 4、中文採 8 logical-pixel 前進；最窄 Add
安全使用下一標籤前的 8-pixel 空白，2×／3× 真實畫面均無裁切、重疊或框線侵入。
字母直接鍵盤控制作用仍為 unknown；spec 215 已 READY，但完整 runtime 玩家路徑尚未 CONFORMED。
dosgolem 本機分支提交為 `8bfd5b4`，未推送其遠端。

2026-09-21 使用者確認手冊採 Phase 62 方案 A：保留上方原版頁碼／標題／序數，只在下方
`[7,312)×[72,184)` 顯示 36×14、504 字繁中正文；排除整框替換與另造中文題目提示。
輸出不鎖定單一倍率，2×（640×400）與 3×（960×600）均須在遊戲執行中可切換。
現有 dosgolem 只有命令列明示倍率，尚無玩家 host-only 控制面；下一決策是切換入口，且任何
控制鍵不得進入 DOS BIOS／IRQ 鍵盤路徑。

使用者已選擇以 dosgolem 外層設定面板調整倍率，排除直接快捷鍵與循環切換。現有 dosgolem
未發現既有玩家視窗／設定面板可重用；需先決定面板開啟方式，再建立通用 host-only UI 能力。

使用者再決定以視窗頂端滑鼠按鈕開啟面板。Phase 82 以真實手冊 framebuffer 證實面板應在
host 控制列下方展開、將遊戲畫布完整下推：2× 640×480 畫布自 y=80、3× 960×720 畫布自
y=120；四個 active-selection prototype 的原畫布與複製畫布 SHA-256 全相同。下一個產品決策
是點擊倍率後立即套用並關閉，或先選取再確認；現有 dosgolem 尚無 production 視窗前端。

第八十三階段已把 Phase 62 的保留原題決定落成正式資料契約：
`text/manual-overlay-layout.tsv` 唯一固定下方 `[7,312)×[72,184)`、36×14、504 字正文；
`manual_catalog.py` 與 `manual_overlay_layout.py` 都接受 504、拒絕 505。22 筆校訂段落最長
236 字，均通過。第十七／六十一階段的 612 字敘述僅保留為已取代的歷史 prototype／收據，
不得再引用為 production 容量。此階段沒有接 presenter、改輸入或改原版驗證。

第八十四階段固定 dosgolem 本機 `buck-rogers-cht-output-overlay` 的
`8bfd5b4e5802f65d428d3fb439196b3c571c002b`：它已有 xlate／RGBA compositing 與明示 2×／3×
runtime overlay，卻沒有可重用的視窗或 host pointer event loop；`cmd/probe` 的滑鼠只屬
決定性 DOS 注入，不能充當 host UI。spec 004 因實際 backend 與 option click 套用語意未定而
維持 DRAFT。下一個阻塞決策仍是點擊倍率後立即套用／保持面板／Apply；本輪未修改 dosgolem。

使用者現已選擇 C：在 host 面板先選取 2×或3×，再按 Apply 提交；排除兩種 option 點擊即套用。
Apply 後是否自動收合、實際 frontend backend、focus 與持久化仍未決定，不能從 C 推定。

第八十五階段重跑 `phase12-before-question.state`，由 #266,399,999 至 #266,557,247 仍只在
已證實的終端 `word?` guarded post-call 產生 generation 1 的
`manual.page34.deimos_prison.word10` request。xlate／36×14 layout 足以支持獨立的 2×／3×
手冊 RGBA presenter，但現有 `RuntimeMenuOverlay` 只是單列選單 adapter，`Watcher` 也沒有
帶 generation 的 presentation lifecycle callback／queue。規格 005 因此維持 DRAFT；正式 691 glyph
字型、lifecycle 接線與同狀態 A/B 都是下一個 READY gate。沒有修改 dosgolem production code。

第八十六階段已在 dosgolem 本機 branch `buck-rogers-cht-output-overlay` 的
`47397ebd18e63a0daa4cb54bd593c5fbfd549ada` 實作並 CONFORM spec 216。Watcher 現在只有在 exact
begin、active-context clear、exact catalog-hit request 時輸出帶 generation 的 answer-free
presentation queue，accessor 為 value-copy；正常玩家 state 新增 begin→clear→request 三筆 metadata，
既有 request 保持不變。這個 branch 依規範沒有推送。手冊 renderer、正式字型與 RGBA A/B 仍為
規格 005 DRAFT，不可聲稱手冊中文已上畫面。

第八十七階段已在同一未推送 dosgolem branch 的
`21c9295c90fac44b5852fd5934a6d027342cde24` 實作 spec 217 的 CONFORMED 純核心。它嚴格載入
唯一 36×14／504 手冊 layout，預先驗證完整 catalog 字模，將確認的 presentation value queue 建成
14 個背景與 14 個文字 layer stamps，支援明示 2×／3×，並拒絕 stale／miss／缺字／錯誤 generation。
Docker 的 Go vet 與 race 測試通過；它尚未載入正式字型、接 command／normal runtime 或取得原版／繁中
A/B，因此規格 005 仍為 DRAFT，不可聲稱手冊已中文化。

第八十八階段完成字型來源 DRAFT 稽核。正式手冊的 691 glyph 清單可重生且雜湊固定，但目前
`workplace/` 沒有原始字型候選與完整授權告知；十份歷史 GOLEMFNT 子集最大只有 81 glyph，且
format 不保留可用的來源／授權資訊。dosgolem spec 218 固定此停止線並在同一未推送 branch 的
`3fc37fe2908c7247447e34dfe18ae3b44855b534` 留存。必須先由使用者提供候選及授權文字，或明確
授權取得指定候選，才可進入字型 READY；正式字型、runtime 接線與原版／繁中 A/B 仍未完成。

第八十九階段依使用者已選的 C，在 dosgolem 本機 `9240c3b19ad5eaba7a44a2b9b4f4420fe1653a0a`
完成 spec 219 的 CONFORMED 通用 `host.ScaleController`。Select 只更新 selected，Apply 才更新
active，2×／3×、invalid／nil、value isolation、vet 與 race 都通過，且 package 沒有 DOS／遊戲依賴。
它沒有 backend、視窗、hit event、重繪、持久化或玩家可切換功能；那些和正式字型、手冊 runtime
接線及 A/B 一樣仍未完成，dosgolem branch 依規範未推送。

第九十階段已在同一未推送 dosgolem branch 的 `b0721c605619a9e689c934994408e009e9231ff9` 完成
spec 220 CONFORMED 的 `ManualPresentationConsumer`。它只消費 `PresentationEvents()` 的 value snapshot：
先完整比對已消費 prefix，逐筆 `Apply` 成功才提交 cursor；snapshot 縮短、歷史漂移與非法 event
皆失敗即關閉，中段錯誤只保留成功 prefix。Docker 的 Go test、vet、race 均通過。沒有接 watcher
callback、command／遊戲 loop、正式字型、frame／draw 或正常玩家 A/B；spec 005 仍為 DRAFT，不能宣稱
手冊中文已顯示。

第九十一階段已在同一未推送 dosgolem branch 的 `bac3f3fafc3cc40b78eee66fdb1f756f21509e53` 完成
spec 221 CONFORMED 的 `ManualPresentationBridge`。它只取得 watcher 的 defensive
`PresentationEvents()` snapshot，原樣交給 consumer；不保存第二份 cursor、不讀 `Observations()`、不吞掉
consumer error。Docker 的 Go test、vet、race 均通過，並更正 spec 220 頂端狀態為 CONFORMED。沒有接
command、遊戲 loop、正式字型、frame／draw 或正常玩家 A/B；spec 005 仍是 DRAFT，手冊中文尚未顯示。

第九十二階段已完成 project spec 006 CONFORMED 的候選審查工具。`tools/catalog_font.py
validate-candidate` 只讀 manifest、候選 source、完整授權文字與 catalog，驗證 strict schema、basename、
SHA-256、非空 UTF-8 license、既有 Unifont parser coverage 與 character-list SHA，且 stdout 不回顯
notice／license／glyph bytes、不寫 GOLEMFNT。158 項 Python 測試含正式 691 glyph synthetic coverage
通過；synthetic data 不是候選字型。dosgolem 本機 `a4a87aad48607ea6ff6e4646de1292f5caaeade9` 僅回填
spec 218 的工具邊界，該 spec 仍 DRAFT：本機仍沒有 candidate source／完整授權文字，不能進入字型 build、
手冊 runtime 或正常玩家 A/B。

第九十三階段依使用者指定採用本機倚天候選 `/home/anr2/cht/etan_font` 作為研究輸入，排除下載
GNU Unifont 或改用其他候選。`ET353S/FILES/` 的 `STDFONT.15`、`SPCFONT.15`、`ASCFONT.15`
可定位正式手冊 691 glyph（44 ASCII、12 symbol、634 common CJK、1 secondary CJK，零缺字；空白
字元是唯一預期全空字模）。不過候選缺少完整授權告知，且 16×15／8×15 到 runtime 16×16 的對齊尚未
經 prototype／使用者決定；spec 007 與 dosgolem spec 218 均維持 DRAFT，不得建置、嵌入、散布或接入
runtime。既有 Unifont validator 正確拒絕此格式，未被修改。

第九十四階段依使用者後續明確確認的「以前購買的字型可直接使用」授權，解除**本機遊戲**的
轉換／嵌入停止線（不含 GitHub 或公開散布）。真實倚天來源已重生 bottom-pad 與 top-pad 兩份 16×16、
691 glyph、25,583-byte 本機候選，並以固定 Deimos Prison 手冊 state 透過 `RuntimeManualOverlay` 驗證
2×／3×均零缺字且正文 clear rectangle 外零像素變更。正文原版區全黑，preview 以原題目區 palette index
10 的受控 private sampling 使兩案可見；這不等於正式色彩策略。使用者已選定 B：`top-pad`，排除
`bottom-pad`；第 16 個空白列置頂，source row 0..14 轉為 output row 1..15。下一個可執行分支已拆為
#12（ETen top-pad parser 與本機建置）、#13（原版前景色來源）與 #14（正常玩家 runtime 接線），三者均須
走 DRAFT→READY 審查。dosgolem branch 仍為本機未推送的
`a4a87aad48607ea6ff6e4646de1292f5caaeade9`，沒有 production code 變更。

## 2026-09-22 — pointer route 決定與 MouseBridge DRAFT 邊界

- 使用者定案：面板關閉時，host chrome 外的 canvas pointer click 轉送原版 DOS mouse；面板開啟時所有 pointer 由 host 消費。永不轉送方案已排除。
- phase127 只量到同一 click 對 DOS mouse state 的差異，machine 未 Step，故尚未驗證玩家可見效果。下一切片先以 DRAFT/READY MouseBridge 純核心契約固定座標、down/up、canvas 邊界與焦點，再獨立取得 Step 收據。
## 2026-09-22 — 第一百二十五階段：實體 host input prototype

- Docker/Xvfb 對真實 Ebitengine 視窗送出的 pointer／Enter 驗證：Cancel 丟棄 3× 暫選並重開回 2×，Apply 3×後自動收合；host hit 與開啟面板 Enter 不寫 DOS，關閉後 Enter 才排入 BIOS。Xvfb letterbox 座標換算僅屬 private runner。
- prototype 仍非可玩版；pointer miss 不轉 DOS mouse 是安全 fallback，等待使用者 UX 決定。詳見[第一百二十五階段](docs/re/phase-125-ebiten-physical-host-input-prototype.md)。
