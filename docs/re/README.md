# 原版觀測證據索引

- [第二百五十一階段：sealed 冷開機的即時選單覆繪](phase-251-sealed-cold-boot-live-menu.md)：原版冷開機至種族選擇屏，有無觀測器三組狀態雜湊相同，2×／3× 合成畫面為繁中；sealed session 存檔不落地待處理。
- [第二百五十階段：選單家族即時元件與 runner 對照](phase-250-live-menu-runner-parity.md)：兩條路徑五個時間點，即時元件與 runner 的 2×／3× RGBA 逐位元相同。
- [第二百四十九階段：加入隊伍路徑的決定性 A/B](phase-249-roster-join-deterministic-ab.md)：dosgolem 規格 237 修正後，間隔 3 秒的 control 與 2×／3× 記憶體雜湊相同，無大小寫重複檔；覆繪只在第 24 列。
- [第二百四十八階段：加入隊伍路徑的暫存層非決定性](phase-248-roster-join-scratch-nondeterminism.md)：暫存層新建檔的主機 mtime 經 DTA 進入記憶體；寫時複製產生大小寫重複檔。
- [第二百四十七階段：儲存詢問離頁正式 A/B](phase-247-save-prompt-leave-runtime-ab.md)：`BUCK` 回答 Y／N 後回主選單；中間態 stamp 保留、第 24 列首寫時成對失效，終態全畫面零差，scratch 存檔三組相同。
- [第二百四十六階段：儲存詢問離頁時序](phase-246-save-prompt-leave-timing.md)：Y／N 都先畫主選單，第 24 列約 510.64M 才改寫；覆繪應保留到該寫入時失效。
- [第二百四十五階段：儲存詢問前後綴覆繪正式 A/B](phase-245-save-prompt-affix-runtime-ab.md)：四個名字雙倍率同狀態，差異只在前綴與後綴、名字格零差；move／refuse 回歸不變；離頁需擴充路徑，未驗。
- [第二百四十四階段：儲存詢問名字模板證據](phase-244-save-prompt-name-template.md)：名字 1–15 字、前綴 5 bytes／後綴 2 bytes、四個名字的前後綴像素一致。
- [第二百四十三階段：正常命名直播鏈與 A/B 重跑](phase-243-named-live-chain-ab.md)：`skill504` 訂正為命名提示，以 `BUCK` 重建至存檔問句；兩頁離開問句與身體圖示 move／refuse 雙倍率同狀態通過，存檔問句帶名字需模板比對。
- [第二百四十一階段：技術技能離開問句直播鏈正式 A/B](phase-241-technical-skill-exit-live-chain-ab.md)：由 `point1.state` 以 Escape→y→Enter 到達技術表並加一點，Escape→N／Y 的 control／2×／3× 同狀態；active 僅本體差異，N／Y 終態零殘層，Y 的 FileOps 三方相同。
- [第二百四十階段：職業技能離開問句直播鏈正式 A/B](phase-240-skill-exit-live-chain-ab.md)：冷開機按鍵鏈到達的 `point1.state` 上 Escape→N／Y，control／2×／3× 同狀態；active 僅本體差異，N／Y 終態零殘層；技術頁直播鏈、存讀檔與 Linux 視窗未驗。
- [第二百二十四階段：未譯安全區候選負面盤點](phase-224-translation-batch-negative-inventory-20260924.md)：24 份正式 catalog／196 筆譯文及十個文字安全矩形家族逐鍵盤點，沒有符合條件的未譯固定字串；row 15 與未觀測第十頁因缺固定詞／安全區證據排除。
- [第二百二十一階段：row 15／row 24 命令狀態欄位 DRAFT](phase-221-command-status-columns-draft.md)：既有合法存態的整串 identity、跨進度欄位相等／變動遮罩、原版 clear 與 A000 首寫；row 15 未證固定詞，row 24 未取得不同值，無 READY 譯文。
- [規格 024：手冊背景／正文群組與字型身分限縮 READY](../spec/024-manual-layer-group-font-identity-ready-candidate.md)：獨立複審後，正式雙層封存元件與 session 字型身分已在本機 dosgolem fork 實作並通過合成雙倍率負例；原版同狀態、Linux 接線及玩家路徑仍未驗收。
- [第二百二十階段：Linux 多作用層單影格合成候選](phase-220-linux-active-composite-draft.md)：ignored 合成 evaluator 驗一次 frame、固定 z-order、完整群組與零部分 RGBA；真實 presenter generation／失效、同狀態及玩家路徑未驗，規格 004 仍 DRAFT。
- [第二百一十九階段：第九頁固定單行正式入頁 A/B](phase-219-story-page9-runtime-entry-ab.md)：合法第八頁存態的雙倍率同狀態入頁，及後續 Ctrl+C 退出 DOS 時同次 active 1→0、終態零殘層；規格 022 僅此範圍限縮 CONFORMED，遊戲內自然離頁仍未知。
- [Issue #18：Linux session-turn 限縮 READY 候選審查紀錄](issue-18-session-turn-ready-candidate-review.md)：ignored typed owner 已接合成真實 machine 收據；正式橋接後段失敗可留下 DOS 左鍵，整批純預檢契約仍待正式驗證，不升 READY。

- [第二百一十八階段：真正 Exit 問句本體正式無頭 A/B](phase-218-exit-prompt-runtime-ab.md)：固定合法加入角色存態的 N／Y→Y、control／2×／3× 雙重正式重播，含 FileOps 零筆自證與正式生命週期軌跡；獨立審查後僅此本體範圍限縮 CONFORMED。
- [第二百一十七階段：真正 Exit 問句八列初畫寫入審查](phase-217-exit-prompt-full-body-writer-review.md)：可重生探針與固定 Y→Y 雙重收據盤點 q1／q2 pending 八列，限縮核准 `0763:184D`、`0763:1854`；舊首列型 q1／N 綠燈撤回，當時正式 A/B 尚未完成。
- [第二百一十六階段：真正 Exit 第二問繪字寫入勘誤](phase-216-exit-q2-glyph-writer-draft-corrigendum.md)：固定合法 Y→Y 雙重原版重播證實 `0763:1854` 的 q2 pending 首列寫入屬正常 glyph run，並聚合該首列兩個寫入點；仍為 DRAFT，不擴張正式 writer 白名單。
- [第二百一十五階段：真正 Exit 問句本體限縮 READY 審查](phase-215-exit-prompt-body-ready-review.md)：核對 exact 身分、q2 pending／q1 active 真實時序、雙倍率字型與訂正後 fake；僅兩句本體升 READY，正式接線與同狀態 A/B 未完成。
- [第二百一十四階段：Exit 問句本體生命週期合成原型](phase-214-exit-prompt-body-lifecycle-fake-draft.md)：ignored typed fake 驗 row21／第一問與第一問／第二問 pending 的兩種短暫共存、含同值 A000 清層、DOS Stop、未知 writer 與錯序失敗即關閉；仍 DRAFT，未接正式程式。
- [第二百一十三階段：Exit 提示繁中候選與倚天字型 DRAFT 靜態收據](phase-213-exit-prompt-font-draft.md)：固定兩個 post-join Exit 提示的 DRAFT 用字，倚天 2×／3×本體 containment 零缺字零越界，尾碼六格採 body-only 遮罩零差；未接正式 TSV 或 watcher。
- [第二百一十二階段：3× 設定面板倚天字型 A/B 原型與後續畫筆收據](phase-212-host-only-3x-eten-font-ab-draft.md)：使用者已選 A 原生 24 點；版控抽字器與正式畫筆的 host-only 像素／2× 往返已驗，原版 DOS／存檔及完整玩家路徑未驗，字型子契約仍限縮 READY。
- [第二百一十一階段：合成 typed session 收據候選與負例](phase-211-synthetic-session-receipt-candidate-draft.md)：ignored 原型以 DOS 退出前置檢查、step 差分與 error 優先保存候選收據；五組合成測試通過，零預算與 Epoch 未定。
- [第二百一十階段：session 停止收據與 DOS 退出的合成探針](phase-210-session-stop-receipt-probe-draft.md)：正常 DOS 退出仍可回 `StopBudget`、已退出後再呼叫仍會多嘗試一步；舊 phase206 釘選探針已精確恢復，規格 019 仍 DRAFT。
- [第二百零九階段：冷開機選單的實體視窗回合與面板暫停](phase-209-cold-boot-live-ebiten-panel-pause-draft.md)：ignored 原型從 `START.EXE` 第零步到選單後，正式 Ebitengine `Update` 實際推進同一 machine；2×實體 Open／Cancel 暫停零步、下一回合恢復，仍非正式可玩版。
- [第二百零八階段：從第零步啟動的選單繁中視窗原型](phase-208-cold-boot-menu-ebiten-prototype-draft.md)：原版 `START.EXE` 唯讀冷開機至首個已量選單，繁中終態於 Ebitengine／Xvfb 繪製；靜態影格、單次重播，不是可玩前端。
- [第二百零七階段：Linux session 六階段故障矩陣 fake](phase-207-linux-session-six-stage-fault-fake.md)：ignored 可丟棄模型驗證面板暫停仍繪圖、Snapshot 純讀，以及六階段故障後拒絕復活與 Close 一次；正式 Ebitengine Draw 錯誤邊界仍未知。
- [第二百零六階段：Linux session machine 步數差分 DRAFT](phase-206-linux-session-machine-step-delta-draft.md)：合成 COM 雙重播證明早停時 `Steps<budget`，CPU 故障時原始 `StopBudget` 須由非空 error 覆蓋；計數包含失敗嘗試，非可玩前端收據。
- [第二百零五階段：Linux session 故障後拒絕推進與單次關閉 fake](phase-205-linux-session-failed-close-once-fake.md)：可丟棄 typed fake 在 Deliver／Advance 故障後拒絕新輸入與重試步進、Close 計數恰一次；規格 004／019 仍 DRAFT。
- [第二百零四階段：技能操作列完整清底正式 A/B](phase-204-action-bar-runtime-conformance.md)：修正短譯文後殘留原版英文，八條操作列路徑與技術頁 Escape→Y 雙倍率雙重播、負控制及獨立審查，僅固定範圍限縮 CONFORMED。
- [第二百零三階段：Linux session 同批輸入 fake 勘誤](phase-203-linux-session-mixed-batch-fake-review.md)：可丟棄 fake 現將 DOS 鍵視為同批候選；Open／Apply／Cancel＋Enter 零 DOS 副作用、零步及下一關閉回合恢復通過，規格 004／019 仍 DRAFT。
- [第二百零二階段：技能頁離開問句本體正式 A/B](phase-202-skill-exit-runtime-ab.md)：兩個合法固定 state 的 Escape→N／Y 無頭 2×／3× 正式覆繪；active 僅本體有像素差、尾碼零差，四條終態同狀態且無殘層，限縮 CONFORMED。
- [第二百零一階段：技能頁離開問句本體覆繪 READY 審查](phase-201-skill-exit-body-only-ready-review.md)：兩筆 exact 問句本體限縮 READY，尾碼零覆繪；正式接線與原版 A/B 尚未完成。
- [第二百階段：技能離開問句 body-only lifecycle fake](phase-200-skill-exit-body-only-lifecycle-fake-draft.md)：以已證實 entry→return 時序提出 guarded-return 啟用候選、N／Y 任意 writer 本體 pre-write 清層、Stop／Restore／Discontinuity／錯誤同步清除及尾碼 sentinel 零覆繪的 DRAFT fake；此 fake 未接 production，後續 READY 結論見第二百零一階段。

- [第一百九十九階段：技能頁離開問句雙倍率字型靜態檢查](phase-199-skill-exit-font-containment-draft.md)：兩句 DRAFT 譯文在本機倚天 2×／3×安全矩形內零缺字、零越界；未驗 N／Y 清除及執行期。
- [第一百九十六階段：設定面板同批鍵盤不漏入 DOS](phase-196-ebiten-panel-batch-keyboard-gate.md)：正式 `Game.Update` 修正 Apply／Cancel 同批鍵盤隔離，僅此 host 分流邊界限縮 CONFORMED。
- [第一百九十五階段：加入角色後七列選單逐寫入清層](phase-195-post-join-prewrite-runtime-receipt.md)：正式收據記錄七次 watcher／presenter 清層，雙倍率 row20 回寫後無殘字；只限合法固定路徑 CONFORMED。
- [第一百九十四階段：正式 Ebitengine 面板暫停閘門](phase-194-formal-ebiten-panel-pause-conformance.md)：正式 `Game.Update` 與實體 X11 雙倍率 Cancel／Apply 的零 `Advance`／下一回合恢復；只限回合排程 CONFORMED。
- [第一百九十三階段：面板暫停與前端 session 的可丟棄 fake 測試](phase-193-frontend-session-fake-draft.md)：Open／Select／Cancel／Apply 零 Step、下回合恢復及故障後拒絕再推進；僅 DRAFT fake，不是正式前端驗收。
- [第一百九十二階段：加入角色後選單第七列清層執行期 A/B](phase-192-post-join-menu-prewrite-runtime-ab.md)：相同原版 state／十筆鍵的控制組與 2×／3×收據逐 byte 相同；row20 普通回寫後兩倍率繁中層均清空，另以正式元件測試固定同值 pre-write，spec 018 保持限縮 READY。
- [第一百九十一階段：技能頁離開確認提示原文勘誤與繁中草稿](phase-191-skill-exit-confirmation-translation-draft.md)：原版 bytes 推翻職業技能提示「原句未知」舊結論，兩筆 exact identity 與 DRAFT 繁中 TSV 已固定；幾何／清除／runtime 尚未驗。
- [第一百九十階段：Linux 前端正式 session 的 READY 前置 API 稽核](phase-190-linux-frontend-session-ready-prerequisites.md)：固定 dosgolem API 的唯讀稽核；確認現有 Ebitengine backend 缺少 typed session 回合、cold-boot composition root、active composite 與 failure teardown，規格 004 仍 DRAFT。
- [第一百八十九階段：真實繁中視窗的面板暫停／恢復 DRAFT 原型](phase-189-ebiten-panel-pause-resume-draft.md)：實體 Cancel／Apply 共 89 個開面板回合零 DOS Step、收合同回合略過、下一回合各恢復 16 步；雙倍率 RGBA 對既有 CLI 逐位元組相等，正式前端仍 DRAFT。
- [第一百八十八階段：真正 Exit 提示身分、色彩與失效邊界](phase-188-exit-prompts-draft-evidence.md)：以雙重正常 N／Y→Y 原版重播確認 row 21、兩個 row 24 prompt 的 guarded identity、可見六格多色選擇尾碼、A000 pre-write 與 DOS terminal 邊界；仍是 DRAFT，未接 watcher。
- [第一百八十七階段：Exit 六步停止點差異的重播勘誤](phase-187-exit-stop-six-step-corrigendum.md)：固定 fork／存態／按鍵下，A000 探針與原 text runner 都在同一步退出；否定探針致差，舊收據產生環境仍未知，Exit 保持 DRAFT。
- [第一百八十六階段：Linux Ebitengine 冷開機玩家前端 READY 缺口稽核](phase-186-linux-ebiten-cold-boot-lifecycle-ready-gap-audit.md)：從私有 checkpoint 視窗到正常 cold boot 的 composition root、typed lifecycle、失敗界線與測試矩陣；規格 004 仍 DRAFT。
- [第一百八十五階段：真實繁中作用層接入 Ebitengine 輸入路由原型](phase-185-ebiten-real-active-layer-router-draft.md)：實體 2×／3× 視窗、連續原版 Step、設定 Apply 與 CLI RGBA 逐位元組相等；仍是 ignored DRAFT caller。
- [第一百八十四階段：Exit 與確認提示 DRAFT 原型](phase-184-exit-prompt-draft-prototype.md)：row21／兩個 row24 prompt 的雙重 N、Y→Y 收據、矩形、2×／3×靜態 containment 與 fail-closed typed 原型；未接正式 watcher。

- [第一百七十九階段：正式 MouseBridge 限縮符合性](phase-179-formal-mousebridge-conformance.md)：雙倍率同狀態點擊 A/B、2×三種 release-only 清理與正式 bridge／原型收據逐欄全等；完整前端仍 DRAFT。
- [第一百八十階段：加入角色後功能選單完整 A000 pre-write 勘誤](phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)：21 個 exact variant、含同值 observer 與較早 glyph pre-write；維持 DRAFT。
- [第一百八十一階段：加入角色後功能選單限縮 READY 獨立審查](phase-181-post-join-menu-ready-review-candidate.md)：固定 21 變體、pre-write 失效／pair 重建、未知 row 21 與 2×／3×字型條件；僅授權正式實作，未驗 runtime。
- [第一百八十二階段：加入角色後選單正式輸出覆繪局部 A/B](phase-182-post-join-menu-runtime-ab-partial.md)：已收錄觀測量同狀態相同、七列安全矩形外零像素差，row 21 未收錄 identity 拒絕；逐幀失效與真正 Exit Enter 尚待驗，spec 018 不升 CONFORMED。
- [第一百八十三階段：功能選單 Exit 身分與舊清除收據勘誤](phase-183-post-join-exit-identity-corrigendum.md)：原版 bytes 證實 row 21 為 `Exit to DOS`、舊 Enter 前的 row 12 為 `Create New Character`；新雙收據量到 Enter→Y→Y 才退出、N 返回選單及 row 21 Enter 後首筆相交 A000 寫入，覆繪仍 DRAFT。
- [第一百六十一階段：加入角色後功能選單反白與選取清除](phase-161-post-join-menu-selection-and-exit.md)：七項固定文字的 normal／selected 身分、底部提示列不相交清除及一條後來證實為 row 12 Enter 的全選單清除；舊 Exit 解讀見第一百八十三階段勘誤。
- [第一百五十七階段：第八頁四行 runtime 限縮 CONFORMED](phase-157-story-page8-runtime-conformance.md)：control／2×／3×、同程序 active 4→0、正規化 machine／DOS 全等及獨立失敗即關閉審查。
- [第一百五十六階段：第七頁正式 runtime 雙倍率同狀態 A/B](phase-156-story-page7-runtime-ab-pending-failure-audit.md)：六行繁中、machine／DOS 全等、同程序 active 6→0 與雙倍率完整失敗矩陣；固定路徑限縮 CONFORMED。
- [第一百五十五階段：第八頁逐字返回與離頁 pre-write 證據](phase-155-story-page8-ready-prerequisite-evidence.md)：130 glyph 雙重 SS/SP／RETF 與 page8→page9 最早相交寫入；字型幾何及 typed-core 未完成，仍 DRAFT。
- [第一百五十四階段：雙倍率面板空白點擊與滑鼠釋放原型](phase-154-ebiten-panel-pointer-miss-prototype.md)：真實 2×／3× host hit/miss 與 release-only 清理；空白 miss 核心未消費的正式契約缺口。
- [第一百五十三階段：第七頁 READY 前逐字返回與離頁診斷](phase-153-story-page7-ready-prerequisite-diagnostics.md)：190 glyph 雙重返回、最早相交 pre-write、可丟棄核心與雙倍率字型 containment；尚待獨立審查。
- [第一百五十二階段：第六頁六行雙倍率執行期同狀態驗收](phase-152-story-page6-runtime-conformance.md)：control／2×／3×及同執行 Enter 離頁 A/B、原版 machine／DOS 全等、安全矩形與失敗即關閉驗收；只限固定路徑 CONFORMED。
- [第一百五十一階段：真實 Ebitengine 畫布外放開與失焦清理](phase-151-ebiten-mouse-release-cleanup-prototype.md)：雙倍率畫布外／控制列／面板開啟／失焦 release-only，及 3×孤兒／重複 Up public API 停止線；只屬 ignored 原型。
- [第一百五十階段：真實 Ebitengine 滑鼠四角與排除邊界](phase-150-ebiten-mouse-geometry-prototype.md)：2×／3×四角 DOS 座標與控制列／右／下 exclusive 邊界的 14 份實體事件收據；只屬 ignored 原型，MouseBridge 維持 DRAFT。
- [第一百四十九階段：第六頁逐字返回、離頁寫入與 READY 審查](phase-149-story-page6-ready-prerequisite-diagnostics.md)：200 glyph 逐筆 ABI／RETF、48 筆相交寫入、精確 runner 重生與可丟棄核心後限縮升 READY；正式 runtime／A/B 未完成。
- [第一百四十八階段：第五頁五行 runtime A/B 與追加負例稽核](phase-148-story-page5-runtime-ab-pending-audit.md)：control／2×／3×與同執行 active→clear 離頁同狀態通過；追加失敗矩陣後規格 014 僅固定路徑升 CONFORMED。
- [第一百四十七階段：第四頁六行 runtime A/B 與追加負例稽核](phase-147-story-page4-runtime-ab-pending-audit.md)：control／2×／3×與同執行 active→clear 離頁同狀態通過；追加失敗矩陣後規格 013 僅固定路徑升 CONFORMED。
- [第一百四十六階段：修正後畫布內滑鼠放開的實體收據](phase-146-real-ebiten-inside-up-corrected.md)：真實 Ebitengine 2×／3× Down→Up 均驗得 Move→Press→Move→Release；滑鼠前端仍為 DRAFT。
- [第一百四十五階段：第五頁 READY 審查](phase-145-story-page5-ready-evidence-draft.md)：雙重收據確認五行 168 glyph 的逐字 stack／RETF／高位遮罩與 page5→page6 最早安全矩形 pre-write；可丟棄 typed-core、正式 loader 與 2×／3×靜態墨跡檢查支持限縮 READY，runtime 尚未接通。
- [第一百四十四階段：第三頁五行 runtime 限縮 CONFORMED](phase-144-story-page3-runtime-conformance.md)：最新程式的 control／2×／3×與合法 Enter 離頁同狀態重跑；只證實第三頁已量路徑。
- [第一百四十三階段：第四頁 READY 前最小證據與幾何勘誤](phase-143-story-page4-ready-evidence-draft.md)：192 glyph 逐筆 return；保留舊五行 fill 勘誤，後續六行補證與獨立審查已支持規格 013 限縮 READY，runtime 尚未接通。
- [第一百四十二階段：第三頁五行 typed adapter READY 審查](phase-142-story-page3-ready-review.md)：144 筆逐筆 stack、五行身分、清除契約、字型覆蓋與可丟棄核心負例通過；僅 adapter 契約升 READY，尚未接正式 runtime。
- [第一百四十一階段：第二頁四行 runtime 限縮 CONFORMED](phase-141-story-page2-runtime-conformance.md)：最新程式的 2×／3×、控制組及合法 Enter 離頁同狀態重跑；結論僅及第二頁已量路徑。
- [第一百四十階段：身體圖示 READY 前置證據停止線](phase-140-body-icon-ready-evidence-stop.md)：低階 glyph／ABI、完整 A000 first pre-write、真實時序、production presenter 與 18 份雙倍率收據已驗；固定 move／refuse／confirm 限縮 CONFORMED。

- [第一百三十九階段：第三頁五行 glyph 的真實 far-return](phase-139-story-page3-return-edge.md)：兩次一致收據證實五行 144 個 glyph 的 RETF caller；補充雙重收據逐筆證實相對 SS／SP+0x12；當時仍是 DRAFT。
- [第一百三十八階段：第三頁合法離頁的最早故事區 pre-write](phase-138-story-page3-exit-prewrite.md)：兩次一致原版重播證實第四頁出現前的最早安全矩形交集寫入早於首個可見像素差異；第三頁仍為 DRAFT，未接 runtime。
- [第一百三十七階段：真實 host panel route 與 3× cleanup](phase-137-real-host-panel-route-and-3x-cleanup.md)：2×／3×真實 Open host hit 與 open-panel miss route、3× accepted Down 後 panel-open chrome release-only，以及正規化同狀態收據；spec 228 仍維持 DRAFT。
- [第一百三十六階段：第九頁後合法 Enter 的第十頁停止線](phase-136-story-page10-enter-stop-line.md)：兩次一致重播只得到 row 15 command/status 重畫，沒有新的固定故事行，未建立第十頁 catalog。
- [第一百三十四階段：第八頁後合法 Enter 的第九頁 trace](phase-134-story-page9-enter-trace.md)：一筆 `0763:04FF → 0763:026B` identity、20 筆返回、兩次一致收據與獨立審查；入頁本體已限縮 READY，正式接線與 A/B 見第二百一十九階段，自然離頁仍未知。

- [第一百三十二階段：第二頁劇情 READY 審查與首屏轉場收據](phase-132-story-page2-ready-review.md)：第 2 頁四行穩定 frame、catalog／字型／矩形、glyph far-return／relative stack guard 與第 2 頁→第 3 頁最早視訊寫入收據；錯序假負例已勘誤，獨立無快取測試全綠，spec 011 已升 READY typed adapter contract，尚未接 production 或完成 A/B。
- [第一百三十一階段：第七頁後合法 Enter 的第八頁 trace](phase-131-story-page8-enter-trace.md)：四行 `0763:04FF → 0763:026B` DRAFT identity、同狀態畫面與繁中候選；右側動態列排除，未接 runtime。
- [第一百三十階段：手冊返回 Num Lock 8 分支至下一次鍵盤輪詢](phase-130-manual-return-numlock8-next-poll-boundary.md)：同一合法 8 在非零分支後回到已證實的無鍵 BIOS poll；同狀態 A/B 無畫面、色盤、檔案或服務差異，未得到遊戲內保存／讀檔入口。
- [第一百二十九階段：第六頁後合法 Enter 的第七頁 trace](phase-129-story-page7-enter-trace.md)：六行 `0763:04FF → 0763:026B` DRAFT identity、同狀態畫面與繁中候選；未接 runtime。
- [第一百二十八階段：第五頁後合法 Enter 的第六頁 trace](phase-128-story-page6-enter-trace.md)：六行 `0763:04FF → 0763:026B` DRAFT identity、繁中候選與 page5 首筆 story-region 改寫；未接 runtime。
- [第一百二十七階段：pointer miss A/B prototype](phase-127-pointer-miss-ab-prototype.md)：同一實體 click 的 no-forward／實驗性 DOS mouse state 對照；非正式 UX。

- [第一百二十六階段：手冊成功返回後的鍵盤 consumer 邊界](phase-126-manual-return-keyboard-consumer-boundary.md)：同一合法 Num Lock 8 被原版 BIOS 取走並回交 consumer，已確認其非零分支；未證實玩家語意、轉場或遊戲內保存／讀檔入口。
- [第一百二十五階段：Ebitengine 實體 host 輸入 prototype](phase-125-ebiten-physical-host-input-prototype.md)：Docker/Xvfb 真實 pointer／Enter 事件驗證 Cancel 回 2×、Apply 3×收合、鍵盤隔離與 DOS 邊界；仍非可玩版。
- [第一百三十三階段：真實 Ebitengine MouseBridge 有界 Step 收據](phase-133-real-ebiten-mouse-bounded-step.md)：2× canvas Down/Up 與外部 Up 的真實事件收據；raw 存態檔雜湊不可跨 run 比，spec 228 維持 DRAFT。
- [第一百三十五階段：真實 Ebitengine 焦點遺失與放開邊緣](phase-135-real-ebiten-mouse-focus-loss-and-release-edges.md)：2× accepted Down→真實 X11 focus-loss cleanup、orphan／repeated release 的 Ebitengine edge 停止線，以及 3× panel-open 新事件隔離；以正規化 state digest 比對起點，spec 228 仍維持 DRAFT。
- [第一百二十四階段：第四頁首次 glyph trace 勘誤](phase-124-story-page4-first-glyph-trace.md)：從第三頁合法 state 以同一筆 Enter 可重生第四頁六行 `0763:04FF → 0763:026B` identity；前五筆 visual-transcription 候選與原版 metadata 不符，第六筆相符。catalog 保持 DRAFT、未接 runtime。

- [第一百二十三階段：手冊成功返回分支的保存／讀檔入口邊界](phase-123-manual-return-save-load-entry-boundary.md)：手冊確認 save/load 的選單與槽位條件；從成功返回的最早可重播 command/status state 以 Num Lock 前進鍵驗證仍無轉場，故不拼接建角收據、不猜鍵、未做 save/load A/B。
- [第一百二十二階段：第四頁後合法 Enter 的下一頁 trace](phase-122-story-page5-enter-trace.md)：確認第五頁底部五行敘事的 `0763:04FF → 0763:026B` content-safe identity，校正誤配人物名的初稿並重建 1006 字模；轉場失效與 runtime A/B 未驗，catalog 維持 DRAFT。
- [第一百二十一階段：手冊成功返回 savestate restore 邊界](phase-121-manual-savestate-restore-boundary.md)：成功返回 state 的無鍵 2×／3× A/B 證實 restore 後不復活衍生手冊層；明示這不是遊戲內保存／讀檔，並記錄合法保存入口的停止線與 spec 002 現況勘誤。
- [第一百零六階段：Ebitengine host 前端 prototype](phase-106-ebiten-frontend-prototype.md)：Linux／Xvfb 的 Go 1.26.7＋Ebitengine 2.9.9 可丟棄視覺與輸入隔離證據；2×／3×、Apply 後兩個未定面板候選與 presentation snapshot provider 缺口，非 production／非正式玩家路徑。
- [第一百零四階段：手冊正確作答後的遊戲內返回](phase-104-manual-success-return.md)：以本機手冊的合法正常 BIOS 輸入通過原版判定，驗證 2×／3× 中文覆繪在後續遊戲畫面清除、像素隔離與完整存態 A/B；不記錄答案，存讀檔仍待驗收。
- [第一百零五階段：手冊成功返回後首個劇情畫面追蹤](phase-105-first-story-screen-trace.md)：確認首個玩家可見劇情畫面、五筆首屏 DRAFT identity 與第二頁失效候選；尚不接 runtime。
- [第一百零七階段：第二頁固定劇情 DRAFT catalog](phase-107-story-page2-draft.md)：以正常 Enter 重播建立四筆第二頁固定敘事 glyph identity 與 DRAFT 繁中候選；row 24 動態狀態列排除，尚不接 runtime。
- [第一百零八階段：第三頁固定劇情 DRAFT catalog](phase-108-story-page3-draft.md)：以兩次正常 Enter 重播建立五筆第三頁固定敘事 glyph identity 與 DRAFT 繁中候選；row 24 動態狀態列排除，尚不接 runtime。
- [第一百零九階段：第四次 Enter 後的 command loop 分類與勘誤](phase-109-post-return-enter-4-command-loop.md)：當時的 trace 只抓到 row 24；既有原版畫面反證「沒有第四頁劇情」，保留舊推論並待追不同印字路徑。
- [第一百一十階段：command/status 最小 inventory](phase-110-command-status-inventory.md)：以兩個不同 Enter 時間重播取得相同 row 24 identity 與終態畫面；固定詞／動態欄位仍待不同遊戲狀態比對，暫不建立翻譯 catalog。
- [第一百一十一階段：command input 證據停止線](phase-111-command-input-stop-line.md)：既有資料沒有手冊返回後可移用的合法移動／查詢按鍵，因此不猜 scan code、不送新輸入，保留 phase110 的可比收據與停止條件。
- [第一百一十二階段：手冊轉向按鍵與可逆 command/status 重播](phase-112-command-turn-manual-evidence.md)：以中文手冊第 10–12 頁明示的數字鍵盤 4／6 完成左右轉向 pair；row 24 重畫為 33-cell identity 且終態回復，固定詞仍未證實。
- [第一百一十三階段：第四頁劇情勘誤與 screenshot-derived DRAFT](phase-113-story-page4-corrigendum.md)：勘誤 phase109–112 對 page4 的錯誤分類，確認既有 PNG 的固定六行劇情並建立 visual-transcription DRAFT；真正 dosgolem glyph identity 尚待找回原始 state／停止點。
- [第一百一十五階段：page4 原始 state 找回停止線](phase-115-page4-state-recovery-stop.md)：窄查既有 300M 附近 state 與 final state，仍未找回能重生 `4f9d1bb…` 首次繪製的 checkpoint；page4 caller／entry／post 維持 unknown。
- [第一百一十三階段：Ebitengine host 控制可丟棄原型](phase-113-ebiten-host-controls-prototype.md)：真實正常玩家畫面收據與本機倚天 host 字型在 Linux／Xvfb 開窗，驗證 2×／3×、Apply／Cancel 與面板鍵盤隔離；尚非 DOS 玩家前端。
- [第一百一十六階段：真實遊戲載入 Ebitengine host 原型](phase-116-game-loaded-ebiten-prototype.md)：本機原版 state 的 Machine→snapshot→Draw、倍率／Cancel／Apply 與 BIOS key receipt；active layer 尚未接通。
- [第一百一十四階段：首屏字元返回邊與 READY 輸入](phase-114-story-return-edge-ready.md)：合法手冊返回路徑重生 160 個 `RETF` 完成字元，確認 `0763:03D6` 與低位顯示 ABI；答案與原文仍只在本機。
- [第一百一十七階段：首屏劇情 runtime 2×／3× A/B](phase-117-story-opening-runtime-ab.md)：同一私有成功返回 state／排程下的五行首屏覆繪，確認雙倍率 indexed／palette 不變、safe rect 外零差異與可讀繁中；未驗轉頁、存讀檔與完整玩家路徑，spec010 維持 READY。
- [第一百一十八階段：故事 DRAFT 字型重建與 loader 回讀](phase-118-story-draft-font-rebuild.md)：以本機倚天來源重建校訂後全部 catalog 的 997 glyph 子集，dosgolem 正式 loader 驗證 page2／page3／page4 與全集零缺字；僅為 DRAFT 字型涵蓋，不是 runtime 驗收。
- [第一百一十九階段：首屏劇情 Enter 轉場 runtime lifecycle A/B](phase-119-story-opening-enter-lifecycle.md)：以完整私有成功返回重播驗證 2×／3×在最早 row 136 video-span 寫入前移除五行 stamp、終態與 control 一致；訂正舊 row 137「首筆寫入」說法，存讀檔仍待驗。
- [第一百二十階段：真實遊戲作用中劇情圖層（active story layer）Ebitengine 原型](phase-120-game-active-story-layer-prototype.md)：真實執行期 watcher 的五行作用中 layer 接到 Linux Ebitengine；2×、Cancel 後 2×與 Apply 後 3×均逐像素等於 phase115 CLI，仍非可玩版。
- [第一百零三階段：第三題手冊覆繪執行期抽樣](phase-103-manual-third-question-runtime.md)：以最新 961 glyph 字庫在原版錯答重抽路徑實際命中 #36，記錄雙倍率、同狀態、像素隔離與 #3／#39 未命中邊界。
- [第一百零二階段：手冊與快捷列覆繪稽核](phase-102-overlay-audit.md)：第一百階段 959 字模的雙倍率首題收據、504 字單頁／3× 密度、白色快捷字母，以及尚缺的玩家路徑驗收。
- [第一百零一階段：身體圖示選擇文字目錄](phase-101-body-icon-text-catalog.md)：沿用正常移動／拒絕／確認 trace，建立七筆固定介面文字的 exact identity、繁中 catalog 與安全矩形；runtime overlay 尚待下一階段。
- [第一百階段：39 題手冊查閱段落翻譯補齊](phase-100-manual-39-translation.md)：37 題中文掃描、2 題英文原書直譯的來源分流、勘誤、504 字靜態驗證與後續抽樣界線。
- [第九十九階段：技能操作列 3× 中文密度](phase-99-action-bar-3x-density.md)：正常技術技能頁操作列接線、白色快捷字母、3× 22 像素中文與 2× 不變的同狀態收據。
- [第九十六階段：倚天手冊中文執行期整合](phase-96-eten-manual-runtime.md)：正式建置器、原版樣式參數、雙倍率中文與錯答清除，以及完整存態語意比較。
- [第九十七階段：手冊 3× 中文密度與第二題](phase-97-manual-cjk-density.md)：2× 不變、3× 22 像素中文字、校正後技術技能翻譯、雙題換題及 restore 收據。
- [第五十五階段：保存、名冊與加入隊伍繁中事件 catalog](phase-55-save-roster-join-translation-catalog.md)：鎖定 18 筆完整路徑 identity，隔離四筆動態姓名並建立七筆繁中 key。
- [第五十六階段：保存、名冊與加入隊伍執行期繁中顯示請求](phase-56-save-roster-join-runtime-display-requests.md)：由唯一 guarded watcher 產生 14 筆請求，四筆動態姓名維持 miss。
- [第九十三階段：倚天字型候選輸入盤點](phase-93-eten-font-candidate-intake.md)：使用者指定候選的字模清冊、691 glyph coverage、Big5 索引分級與權利／對齊停止線。
- [第九十四階段：倚天字型本機建置與對齊原型（prototype）](phase-94-eten-font-local-build-prototype.md)：本機授權下的兩個 16×16 候選、固定手冊狀態（state）、雙倍率範圍約束（containment）與待決的顏色／對齊界線。
- [第九十五階段：倚天 top-pad parser 的格式與索引證據](phase-95-eten-top-pad-parser-evidence.md)：完整 Big5 分區、691 glyph mapping、top-pad、保留區拒絕與 `GOLEMFNT` 載入邊界；不含字型 bytes 或 runtime 接線。

此目錄保存 dosgolem 的原版行為收據與推論分級，不保存原版遊戲、手冊、可還原素材或
其完整輸出。所有位址均須標明使用的位址空間；不可把 IDA 線性位址與 dosgolem 執行期
段位址混用。

| 文件 | 職責 |
| --- | --- |
| [第一階段輸入與啟動收據](phase-1-input-and-startup.md) | 輸入雜湊、權利邊界、dosgolem 能力與正常重播 |
| [第一階段選單文字輸出追蹤](phase-1-menu-text-trace.md) | 一條可觀測文字像素輸出鏈、位址與未知項目 |
| [第二階段文字分派與生命週期追蹤](phase-2-text-dispatch-and-lifecycle.md) | 長度前綴 ASCII 字串、字元 renderer、glyph primitive 與生命週期邊界 |
| [第三階段中文手冊輸入清冊](phase-3-manual-input-inventory.md) | RAR 完整性、解壓成員雜湊與僅 metadata 的頁面定位 |
| [第四階段選單互動與失效生命週期](phase-4-menu-interaction-lifecycle.md) | BIOS Enter 正常路徑、轉場字串輸出與舊文字清除時機 |
| [第五階段種族選擇返回生命週期](phase-5-pick-race-return-lifecycle.md) | BIOS Escape 正常返回、逐位元功能選單重建與反向清除時機 |
| [第六階段清除路徑與失效 hook 證據](phase-6-clear-path-hook-evidence.md) | byte-fill 勘誤、Mode 13h 矩形清除例程、Enter／Escape 動態範圍與 hook 邊界 |
| [第七階段文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md) | 末 glyph 完成證據、guarded return、自然落入反例與轉場事件順序 |
| [第八階段功能選單繁中字型與版面 prototype](phase-8-menu-font-layout-prototype.md) | 九筆來源、手冊譯名、字型授權邊界、2×／3× 整數覆繪與 containment |
| [第九階段 dosgolem 通用繁中覆繪基礎](phase-9-dosgolem-xlate-foundation.md) | `xlate` 來源、移植 commit、能力邊界、測試收據與倍率限制 |
| [第十階段繁中 catalog 與字型建置](phase-10-catalog-font-build-pipeline.md) | TSV 驗證、決定性字元清單、GOLEMFNT builder 與 dosgolem 回讀收據 |
| [第十一階段手冊查閱事件映射](phase-11-first-manual-check-event-map.md) | 正常進入路徑、動態題目、錯答重抽與中文掃描對應 |
| [第十二階段手冊題庫結構](phase-12-manual-question-table-inventory.md) | 39 筆定長 schema、解碼器、消費者、無答案 metadata 清冊與動態反向驗證 |
| [第十三階段繁中手冊來源對照](phase-13-manual-source-crosswalk.md) | 39 筆逐項來源、證據分級、OCR 搜尋收據與缺頁邊界 |
| [第十四階段首批短篇手冊段落](phase-14-manual-compact-paragraphs.md) | 八筆原圖校訂、事件鍵、繁中 catalog、長度與失敗即關閉驗證 |
| [第十五階段第二批短篇手冊段落](phase-15-manual-compact-paragraphs-2.md) | 第二批八筆原圖校訂、事件擴充、長度與回歸驗證 |
| [第十六階段第三批已證實手冊段落](phase-16-manual-compact-paragraphs-3.md) | 剩餘候選篩選、五筆原圖校訂、排除原因與回歸驗證 |
| [第十七階段手冊分頁與倍率 prototype](phase-17-manual-pagination-scale-prototype.md) | 真實安全矩形、2×／3× 容量、逐頁對照與 renderer 限制 |
| [第十八階段手冊題目世代與舊覆蓋失效](phase-18-manual-generation-invalidation.md) | 答錯換題時間線、局部清除反例與失敗即關閉世代契約 |
| [第十九階段手冊題目事件收集器 prototype](phase-19-manual-event-collector-prototype.md) | typed lifecycle、真實事件重建與跨世代／亂序負向測試 |
| [第二十階段手冊 catalog 顯示請求 prototype](phase-20-manual-catalog-display-request-prototype.md) | 正式 TSV 精確命中、ordinal bridge 缺口與顯示／語意隔離測試 |
| [第二十一階段手冊序數詞橋接證據](phase-21-manual-ordinal-bridge-evidence.md) | 原版 1–10 長度前綴表、索引 consumer、IDA 收據與可重生 TSV |
| [第二十二階段 dosgolem xlate 通用整數倍率](phase-22-dosgolem-xlate-integer-scale.md) | 2×／3× renderer、邊界安全、真實 GOLEMFNT 冒煙收據與本機 commit |
| [第二十三階段手冊事件 adapter](phase-23-manual-event-adapter.md) | READY 純核心、generation／catalog 正反向測試、正式 TSV 與本機 commit |
| [第二十四階段手冊 runtime watcher](phase-24-manual-runtime-watcher.md) | dispatcher entry／guarded post-call 正式接線、固定狀態 metadata 收據與失敗即關閉測試 |
| [第二十七階段功能選單文字事件清冊](phase-27-menu-event-inventory.md) | 九筆 content-free runtime identity、guarded post-call 收據與正式 TSV 雙向驗證 |
| [第二十八階段功能選單顯示請求純核心](phase-28-menu-display-request-core.md) | READY exact-match catalog、九事件顯示請求與失敗即關閉驗證 |
| [第二十九階段功能選單執行期顯示請求 watcher](phase-29-menu-runtime-request-watcher.md) | guarded post-call 直接產生九筆 request、content-free 收據與 CONFORMED 子規格 |
| [第三十階段種族選單反白與文字安全矩形](phase-30-race-selection-highlight-lifecycle.md) | Down／Up normal→selected 重畫、同終點 framebuffer 與 logical text-safe rectangle |
| [第三十一階段反白 variant 執行期繁中請求](phase-31-selection-variant-runtime-requests.md) | 12-identity exact catalog、13-request 固定重播與舊九事件相容性 |
| [第三十二階段功能選單覆繪倍率 A/B prototype](phase-32-menu-overlay-scale-ab-prototype.md) | 同一原版 framebuffer 的 2×／3× xlate 覆繪、幾何與決策收據 |
| [第三十三階段種族選取列閃爍與色盤生命週期](phase-33-selection-blink-lifecycle.md) | 978 點 palette／row 取樣、黑底黑字選取狀態與無週期重畫證據 |
| [第三十四階段倍率中立的功能選單覆繪核心](phase-34-scale-neutral-menu-overlay-core.md) | READY→CONFORMED 純核心、2×／3× 同 API 與四組逐位元回歸收據 |
| [第三十五階段選定種族後的文字路徑清冊](phase-35-post-race-text-path-inventory.md) | 正常雙 Enter 路徑、性別畫面四筆 content-safe identity 與決定性 framebuffer |
| [第三十六階段性別選擇生命週期](phase-36-gender-selection-lifecycle.md) | Down／Up normal→selected 重畫、Escape 返回功能選單與雙重決定性收據 |
| [第三十七階段性別選擇繁中執行期顯示請求](phase-37-gender-runtime-display-requests.md) | 七 identity 繁中 catalog、18-request 正常路徑與 Escape 失敗即關閉證據 |
| [第三十八階段確認性別後的職業選擇文字路徑](phase-38-post-gender-text-path-inventory.md) | 正常第三次 Enter、七筆職業畫面 identity 與決定性 framebuffer |
| [第三十九階段職業選擇生命週期](phase-39-class-selection-lifecycle.md) | Down／Up normal→selected 重畫、Escape 返回功能選單與雙重決定性收據 |
| [第四十階段職業選擇繁中執行期顯示請求](phase-40-class-runtime-display-requests.md) | 手冊職業譯名、十 identity exact catalog 與三路徑 request 收據 |
| [第四十一階段性別與職業繁中覆繪倍率 A/B](phase-41-character-creation-overlay-ab.md) | 四個真實 framebuffer 的 2×／3× 安全矩形覆繪與決策證據 |
| [第四十二階段確認職業後的角色資料文字路徑](phase-42-post-class-text-path-inventory.md) | 四次正常 Enter 後角色資料／重擲頁的 96 筆 content-safe 事件收據 |
| [第四十三階段重擲提示輸入與動態欄位生命週期](phase-43-reroll-input-lifecycle.md) | `Y` 重擲與 `N` 接受分支的正常 BIOS 輸入、事件及 framebuffer 收據 |
| [第四十四階段角色姓名輸入生命週期](phase-44-character-name-input-lifecycle.md) | 字元、Backspace、Enter 與 Escape 的輸入／回顯／轉場證據 |
| [第五十二階段合法保存後段事件對齊](phase-52-valid-save-event-alignment.md) | 完整技能配置後的圖示／保存／加入角色 checkpoint、未實作服務排除與記憶體候選分級 |
| [第五十三階段保存選項控制流與名冊接納狀態](phase-53-save-choice-control-flow-and-admission-state.md) | 保存分支勘誤、YES 寫檔控制流、決定性與後續 Add 驗證邊界 |
| [第五十四階段已保存角色的名冊與加入隊伍路徑](phase-54-saved-character-roster-and-add-path.md) | 保存檔掃描、角色列、完整載入、加入後移除與雙重正常路徑收據 |
| [第五十七階段明示倍率的執行期繁中覆繪](phase-57-scale-explicit-runtime-overlay.md) | 2×／3× 輸出端覆繪、清除／同原點取代生命週期與同狀態收據 |
| [第六十階段手冊覆繪 READY 前置稽核](phase-60-manual-overlay-ready-prerequisite-audit.md) | 39 題／22 譯文邊界、單頁容量、失敗即關閉與 READY／CONFORMED 分流 |
| [第六十一階段手冊單頁容量驗證](phase-61-manual-single-page-capacity-validator.md) | 36×17 單頁上限、612／613 字邊界與正式 catalog 失敗即關閉收據 |
| [第六十二階段手冊原版題目保留版面 prototype](phase-62-manual-prompt-preservation-prototype.md) | 整框覆蓋操作缺口、保留題目的 36×14 雙倍率對照與待決版面前沿 |
| [第六十三階段性別與職業執行期繁中覆繪](phase-63-gender-class-runtime-overlay.md) | 正常角色建立雙倍率 runtime overlay、轉場失效、同原點取代與像素 containment 收據 |
| [第六十四階段角色資料靜態繁中執行期請求](phase-64-character-sheet-static-runtime-requests.md) | 隔離 35 個靜態 identity，完成 exact catalog、base／Y runtime request 與 framebuffer 非干擾收據 |
| [第六十五階段角色資料頁執行期繁中覆繪](phase-65-character-sheet-runtime-overlay.md) | 35 筆安全矩形、base／Y × 2×／3× runtime overlay、同 palette baseline 與像素 containment |
| [第六十七階段角色姓名靜態提示執行期請求](phase-67-character-name-static-text-runtime-requests.md) | 姓名固定提示 exact request、玩家輸入 miss 與雙重正常路徑收據 |
| [第六十八階段角色姓名提示執行期繁中覆繪](phase-68-character-name-prompt-runtime-overlay.md) | 提示／輸入欄幾何、2×／3× containment 與動態姓名零干擾收據 |
| [第六十九階段角色姓名覆繪轉場失效生命週期](phase-69-character-name-overlay-transition-invalidation.md) | Enter 空終態清除、Escape 同 key 重印與雙倍率無殘字收據 |
| [第七十階段職業技能配置靜態繁中請求](phase-70-career-skill-static-runtime-requests.md) | 四標題／八技能 exact catalog、selected variants 與動態點數 miss 收據 |
| [第七十一階段職業技能配置執行期繁中覆繪](phase-71-career-skill-runtime-overlay.md) | 14 筆 exact 矩形、base／Down 雙倍率取代生命週期與動態數值零干擾收據 |
| [第七十二階段技術技能配置靜態繁中請求](phase-72-technical-skill-static-runtime-requests.md) | 13 個手冊譯名、17 個不重複 identities、共享標題勘誤與 base／Down 收據 |

`workplace/` 是被 Git 忽略的原始輸入與可重生收據存放處；其檔名與雜湊由上述文件引用。
| [第七十三階段：技術技能配置執行期繁中覆繪](phase-73-technical-skill-runtime-overlay.md) | 17 筆專屬矩形、共享標題、穩定 frame 訂正與雙倍率同狀態收據。 |
| [第七十四階段：技能配置底部操作列輸出路徑清冊](phase-74-skill-action-bar-output-path-inventory.md) | 逐字輸出路徑、五標籤幾何、焦點色彩與 disabled unknown 邊界。 |
| [第七十五階段：技能配置底部操作列執行期事件](phase-75-skill-action-bar-runtime-events.md) | Guarded glyph watcher、錨定訂正、八路雙重播與 framebuffer 非干擾收據。 |
| [第七十六階段：技能操作列繁中顯示請求](phase-76-skill-action-bar-display-requests.md) | 五個繁中介面詞、16 個 exact identities、八路 request 與語意隔離收據。 |
| [第七十七階段：技能操作列覆繪幾何與配色前沿](phase-77-skill-action-bar-overlay-geometry.md) | 8-pixel command band、雙倍率字模 containment、底框排除與 normal 配色 prototype。 |
| [第七十八階段：技能操作列配色中立覆繪核心](phase-78-skill-action-bar-style-neutral-overlay-core.md) | 16 個 exact rectangles、明示逐字配色 API、雙候選雙倍率核心驗證。 |
| [第七十九階段：技能操作列配色中立 runtime 生命週期](phase-79-skill-action-bar-style-neutral-runtime-lifecycle.md) | 原子 group 取代、clear／anchor 失效、frame 後明示 palette 重套用。 |
| [第八十階段：技能操作列快捷字母保留與混合寬度版面](phase-80-action-bar-hotkey-preserving-layout.md) | 白色助記字母、原色中文、28-pixel 混合寬度與 Add 空白格擴張證據。 |
| [第八十二階段：host 設定面板控制列視覺 prototype](phase-82-host-settings-panel-visual-prototype.md) | 上方 host 控制列、下推而不遮畫布的面板，以及 2×／3× hit rectangle 契約。 |
| [第八十三階段：手冊保留原題的 504 字容量契約](phase-83-manual-preserved-prompt-capacity-contract.md) | 保留題目時的正式 36×14／504 字幾何、catalog 邊界與已取代 612 字契約的分界。 |
| [第八十四階段：dosgolem host 前端能力盤點](phase-84-dosgolem-host-frontend-capability-audit.md) | 無頭現況、可重用 output compositing、DOS 滑鼠輸入邊界與必須新增的通用 host 能力。 |
| [第八十五階段：手冊繁中 presenter 整合就緒稽核](phase-85-manual-presenter-integration-readiness-audit.md) | 重跑正常手冊 request、xlate／14 行 layout 能力，以及 lifecycle 與字型 READY 缺口。 |
| [第八十六階段：手冊 presentation lifecycle 接線](phase-86-manual-presentation-lifecycle.md) | CONFORMED typed begin／clear／request queue、正常玩家 metadata 重播與無輸入邊界。 |
| [第八十七階段：手冊多行 presenter 純核心](phase-87-manual-multiline-presenter-core.md) | CONFORMED 的 36×14／504、背景＋文字 layer、2×／3×與 lifecycle synthetic 收據；未接玩家 runtime。 |
| [第八十八階段：手冊正式 GOLEMFNT 子集來源稽核](phase-88-manual-formal-font-subset.md) | DRAFT：691 glyph 清單已重生，但本機沒有可核對的候選字型與授權告知。 |
| [第八十九階段：host 倍率預選與 Apply 純核心](phase-89-host-scale-selection-apply-core.md) | CONFORMED 的 selected／active state；不含 backend、hit event 或玩家切換。 |
| [第九十階段：手冊 presentation queue consumer 純核心](phase-90-manual-presentation-queue-consumer.md) | CONFORMED 的 append-only value cursor；不含 watcher callback、command 或玩家畫面。 |
| [第九十一階段：手冊 watcher snapshot bridge 純核心](phase-91-manual-watcher-snapshot-bridge.md) | CONFORMED 的 watcher→consumer 單一轉送；不含 command、字型或玩家畫面。 |
| [第九十二階段：正式字型候選 manifest 驗證補強](phase-92-formal-font-candidate-manifest-validation.md) | CONFORMED 的候選審查工具；不採用、建置或散布字型。 |
| [第一百九十七階段：技能頁離開確認提示 pre-write DRAFT](phase-197-skill-exit-confirmation-prewrite-draft.md) | 兩頁 row24 prompt 的 A000 首次變值相交、六格尾碼與矩形；N／Y clear 仍未量到，未達 READY。 |
| [第一百九十八階段：技能頁離開確認 N／Y all-store pre-write DRAFT](phase-198-skill-exit-ny-all-store-prewrite-draft.md) | 同 phase-197 合法 pre-ESC state 的 Escape→N／Y，分別量到本體與六格尾碼首筆 A000 store；career／technical N 尾碼有較早同值 store，維持 DRAFT。 |
| [第二百二十二階段：原版主選單 3× 實體切換與中文字距](phase-222-original-menu-3x-typography-draft.md) | 真實冷開機選單的 2×→3× Apply、24 點 host 面板、16／22 點繁中畫布 A/B；限可丟棄 DRAFT，不代表完整 session。 |
| [第二百二十三階段：手冊首題實體視窗與中英混排](phase-223-manual-first-question-host-mixed-script-draft.md) | 正式手冊 owner 終態影格接實體 2×→3× host，釐清拉丁專名不是原版殘字，保留 A／B／C／D 私有視覺原型與待決取捨。 |
