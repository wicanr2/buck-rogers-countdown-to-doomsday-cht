# 第三百零三階段：韓文詞級排版與同狀態收據

日期：2026-10-01
狀態：規格 043 的部分驗收（見 §9）；dosgolem 韓文詞級排版已推到公開分支，四個時點與另外 16 個時點通過，trace 重播、串接抽審、語義抽樣與水平選單放寬仍待做。
推論等級：**已證實**＝重跑腳本或測試並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
原版遊戲與英文原文只在 ignored 的 `workplace/`，本文只記雜湊、數字與判定。

## 1. 環境與版本

| 項目 | 值 |
|---|---|
| Buck 主 repo 的韓文資料 | `ed1b969`（譯文、檢查工具、字集、名字表） |
| dosgolem 分支 | `buck-rogers-cht-output-overlay` `5bc0f0b`（詞級排版、名字表空白、`-lang`、ko 測試） |
| runner／前端 | `workplace/phase303-ko/runner`（SHA-256 前綴 `caf19215`，`cmd/buckrogers-text-receipt`）、`buckrogers-play`（前綴 `a3427bc4`），由 `5bc0f0b` 在 Docker 內建置 |
| 字型 | `font/buckrogers-ko.golemfnt` 42,862 位元組（前綴 `e567c89b`），由 `font/characters.ko.txt` 1,158 字重建，連建兩次雜湊相同 |
| 執行方式 | Docker `python:3.13-slim`，`--network none`，`-u` 目前 UID/GID，`--memory`／`--cpus`／`--pids-limit`，原版與工作樹唯讀掛載 |

收據都用正式 `text/` 與 `-lang ko`，不是測試用小檔。腳本由 phase-301 的日文版改寫（語言碼替換），放在 ignored 的 `workplace/phase303-ko/`。

## 2. 四個時點（規格 040 §5.3，2× 與 3×）

每個時點跑四種：S-zh-TW、S-ko、S-en（一開始就用該語言），以及 W-ko（zh-TW 切英文、再切回、最後切韓文）。`switch/compare.py` 逐項比對。

| 時點 | 停止步數 | 記憶體雜湊前綴 | CPU 雜湊前綴 | 檢查結果 |
|---|---|---|---|---|
| ECL 敘事 | 409,000,000 | `877f715f` | `91835ee6` | 2×、3× 全過 |
| 水平選單 | 432,500,000 | `7290b7b3` | `995a44ac` | 2×、3× 全過 |
| 手札 | 5,285,000,000 | `ceb6b6fc` | `29f8055d` | 2×、3× 全過 |
| 手冊題 | 266,650,000 | `7900785e` | `425cf745` | 2×、3× 全過 |

已證實：每個時點的六項檢查全過（2× 與 3×）：W-ko 的畫面等於 S-ko；S-en 的畫面等於原版 baseline；記憶體雜湊在 zh-TW、ko、en、無覆繪四種相同；
CPU 雜湊在三種語言相同；indexed、palette、停止步數相同；停止時語言通道為 ko。雜湊前綴與 phase-301 的日文收據逐項相同，同一原版狀態在各語言下的機器狀態不變。

覆繪命中計數在 zh-TW 與 ko 相同：ECL 時點 ecl 命中 5、未命中 8、hmenu 命中 14、engine-dispatch 命中 22、未命中 1；水平選單時點 hmenu 命中 3；
手札時點 ecl 命中 2、hmenu 命中 1；所有時點 Overflow 為 0。前三個時點 ko 與 zh-TW、ko 與 baseline 的畫面都不同（有疊字）。
手冊題時點 ko 的畫面等於 baseline：`manual.ko.tsv` 只有標頭，規格 043 §3.9 預期手冊題的提示句與段落顯示原版英文，與此一致。

截圖檢視（2×，`workplace/phase303-ko/*-ko-2x.png`）：

| 檔 | 內容 | 結果 |
|---|---|---|
| `ecl-ko-2x.png` | ECL 敘事，含「」與 `...` | 無缺字、無溢出；三行都在詞界換行（`끊은 게／틀림없었다`），「 不在行尾 |
| `hmenu-ko-2x.png` | 第 24 列水平選單 | 無缺字。括號內的助記字母空白，與 zh-TW、英文原版同一時點一致（原版先畫其他字母，助記字母後補） |
| `logbook-ko-2x.png` | 手札 41 番（含 `(Carlton Turabian)` 半形加註） | 無缺字、無溢出；名字後的助詞 `의` 緊跟括號，全文在詞界換行 |

## 3. 另外 16 個時點（`families.sh`）

狀態與按鍵取自 phase254 各家族腳本，S-zh-TW 與 S-ko 各跑一次（2×，`-compose-every-retrace`）。`compare-families.py` 要求記憶體、CPU、indexed、palette、
停止步數相同，停止時語言為 ko，且點數等於 16。

已證實：16 點的機器狀態全部相同，13 點 ko 與 zh-TW 畫面不同，3 點（story-2811、2815、2825）兩者相同。與 phase-301 的日文結果同一分布。

| 時點 | 覆繪生效 | ko 截圖檢視 |
|---|---|---|
| opening-2809 | 是 | 開場五行（`벅 로저스(BUCK ROGERS)와`、`러시아-미국 무역 연합(RAM)과`）在詞界換行，半形加註正常 |
| opening-275、282 | 是（275 為讀取中提示與座標列，282 為座標列） | 282 的 ECL 停在逐字印出中（畫面仍是英文原文），與 zh-TW 同狀態；275 未逐張檢視 |
| post-row20、post-n | 是 | 加入後選單九列，無缺字（post-n 未逐張檢視） |
| post-q1 | 是 | 底部「DOS로 나가기」列與提示；`예( )` 為半畫狀態，zh-TW 相同 |
| career-drawn、career-add | 是 | 職業技能頁（career-add 檢視）與動作列 `추가(A) 감소(S) 완료(D)` |
| cprompt、tprompt | 是 | 離開確認列與 `예(Y) 노(N)`（cprompt 檢視）；上方技能頁維持英文，與 zh-TW 相同 |
| tech-drawn | 是 | 技術技能頁，動作列 `추가(A) 감소(S) 이전(P) 다음(N) 완료(D)` |
| body-move、body-confirm | 是 | 圖示畫面；`저장: BUCK?` 與 `예(Y) 노(N)`（body-confirm 檢視），玩家名維持英文（規格 045） |
| story-2811、2815、2825 | 否，畫面與 zh-TW 相同 | 劇情第 2 至 9 頁在這些 state 沒有可觸發的畫面，未量 |

未知：story 第 2 至 9 頁的 ko 畫面。這些頁面的 ko 只有靜態驗證（`ko_check.sh` 的 `story_page*_catalog.py` 逐頁驗證器）。

## 4. phase254 七條回歸

新 runner（`rerun38`）與 `rerun36` 的七份文字輸出（story、opening、manual、post、skill、action、body）逐位元組相同，行數 6、6、8、8、8、10、6；body 與 `rerun37` 也相同。
已證實：加入詞級排版、`splitRows` 與名字表載入改動後，zh-TW 輸出沒有變。

## 5. 前端冷開機

`buckrogers-play` 在 Xvfb 內冷開機，1,600 幀，畫格 1300、1400、1450、1500 各送一次語言切換（`workplace/phase303-ko/k1.png`、`h1.png`）：

- 日誌依序印出 `lang=zh-CN`、`en`、`ja`、`ko`；DebugSummary 有 `lane[ko]`，沒有「語言停用=」。
- `ecl` 命中 0、`hmenu` 命中 1，Overflow 為 0（這段冷開機沒走到敘事窗）。
- 首頁選單顯示韓文（`연주(P) 폭파(D)`）；`lang=ko` 合成畫面雜湊 `4e5b52b7…` 不等於原版 `0dc3ec5d…`。
- 說明頁（`h1.png`）「目前語言」列為「韓文（機器輔助）」。
- `玩家名=off(no-transliterator)`：韓文玩家名音譯器（規格 045）未做，玩家名顯示英文。

## 6. Go 測試與靜態預檢

全部在 Docker 內跑（`BUCKROGERS_CHT_ROOT` 唯讀掛主 repo）。`go test ./apps/buckrogers/` 僅剩工作樹中既有的三個未追蹤 probe 測試失敗（它們讀 `/project/...`，與本階段無關）；
`go build ./...` 只有 `workplace/fd2-input-parity-20260907` 的既有 `main redeclared`。

| 測試 | 內容與結果 |
|---|---|
| `TestFrozenCopiesMatchPre043` | 舊版 `layoutEclTextP`、`layoutLogbookUnitsP`、兩列拆分的凍結副本，摘要與在 `88f391f` 以真實函式求得的摘要相同（ECL 4,000 組、手札 313 則、拆分 3,000 組，各 3 個 profile） |
| `TestLayoutWithoutWordLevelUnchanged` | 新版函式在 nil、ja、ko 字級 profile 下的摘要等於同一組舊版摘要 |
| `TestLayoutUnchangedOnFormalTexts` | zh-TW、zh-CN、ja 各 ECL 2,542 列（43,552 次排版，含各加註段、4 個窗寬、2 個起點、2 種 bottom）與手札 71 則（109 次）與凍結副本逐行相同 |
| `TestKoWordTokens` 等 | 詞 token、名字單位加助詞（窗寬 24 併、22 不併、12 沿名字內空白斷行）、「 不落行尾、長詞逐字、整次退回字級、拆點找空白與落在空白、手札退回字級 |
| `TestKoNeverWorseThanCharacterLevel` | 合成語料 4,000 組：字級放得下的，ko 都放得下 |
| `TestKoLoadNameGlossaryAllowsInnerSpaces` | ko 名字表允許單一內部空白；首尾、連續空白、括號拒絕；zh-TW、zh-CN、ja 讀含空白名字仍失敗 |
| `TestKoLaneOnFormalText` | F4 循環含 ko；`lane[ko]`；無語言停用；`resets`、`skips` 皆空；ECL 與引擎片段 watcher 使用 ko profile；zh-TW 無 profile |
| `TestKoNameMatchesAgreeWithZhTW` | 5,414 列逐列比對 zh-TW 與 ko 的 Go `Matches` 人物集合：差異 0（扣 5 條列級豁免，全數被使用） |

實作過程中踩到的一個錯：詞級 tokenization 在「收尾標點串延伸進下一個名字單位」時沒有前進，造成無窮迴圈並耗盡記憶體（差分測試的隨機語料觸發，正式資料不會）。
已改成「至少前進一個字元」，與舊版 tokenization 的同一處行為對齊。

### 靜態預檢（ko，ECL 2,542 列，純文字加 176 列最完整加註段，共 2,718 次；6 列高的窗）

| 窗寬（半形單位） | 溢出 ko（未加註）／字級／zh-TW | 行數 ko／字級 | 詞中斷行 ko／字級 | 整次退回字級 |
|---|---|---|---|---|
| 76 | 0（0）／0／0 | 3,206／3,201（多 5） | 0／283 | 0 |
| 56 | 0（0）／0／0 | 3,651／3,634（多 17） | 0／552 | 0 |
| 40 | 2（1）／2／0 | 4,581／4,527（多 54） | 9／1,094 | 3 |
| 30 | 41（23）／41／0 | 5,440／5,332（多 108） | 27／1,571 | 10 |

已證實：ko 與字級的 fits 逐列相同（不變量成立）；寬於一列的詞 0 個；窗寬 76 與 56 沒有詞中斷行，窗寬 40 與 30 剩下的詞中斷行來自整次退回字級與名字加助詞寬於一列。
手札 71 則：最長 24 行，頁數最大 ko 2／字級 2，詞級不比字級多頁，0 則需退回字級。

**已知風險（未知其實際影響）**：窗寬 40 與 30 是假想的窄窗。韓文在這兩個窗寬有 2、41 次溢出（字級相同，zh-TW 為 0）。溢出時該段顯示原版英文，不會壞畫面，
但遊戲是否有這麼窄的 ECL 窗，要等 trace 重播閘門（規格 042 §5.4，未做）才知道。列入規格 043 §6。

## 7. 名字：Go 與 Python 掃描

`cmd/buckrogers-name-scan -lang ko`（新增 `-lang`）對韓文 ECL 與手札的輸出，與 `tools/name_glossary.py` 的 `scan` 逐列比對（`scan-compare.py`）：
ECL 2,542 列（Go 列出有名字者 176）、手札 71 則（本文與標題），差異 0。Go 預估的加註段：ECL 176 列全在標準窗取最完整段（all），手札本文 71 則與標題 71 則皆為 all。

## 8. host-ui 變更與字型 manifest

`host-ui.zh-TW.tsv` 的 `lang.ko` 改為「韓文（機器輔助）」。依 `tools/eten_font.py build text/*.zh-TW.tsv` 重建 2× 倚天字型：輸出 `ebe7f045…` 與 `workplace/current-font` 的現行字型**逐位元組相同**
（8 個字本來就在字元清單內），只有 manifest 的 host-ui SHA-256 不同；已替換 manifest（舊檔留為 `pre043.json.bak`），`verifyCurrentCatalogs` 的 35 份譯文雜湊全部對上。zh-TW 收據不受影響（字型沒變）。
3× 的 `eten_host_font3.py` 要求 host-ui 恰有五個 `host.*` 標籤，`help.*`、`lang.*` 加入後就已經建不出來（phase-297 待決第 4 項），`cmd/` 沒有任何程式呼叫 `LoadHostFontsFromReviewedManifests`；
打包流程也不建 3× 字型，本階段不處理。

## 9. 打包模擬（Linux）

`tools/package.sh linux`（版本 `v1.0.2-65-ged1b969`，dosgolem `5bc0f0b`）先跑 `zh_cn_check.sh`、`ja_check.sh`、`ko_check.sh`，全過；AppImage 建置成功；外洩掃描 246 個檔案、236 個雜湊、267 個檔名，0 命中。
AppDir 含 `buckrogers-ko.golemfnt`（42,862 位元組）與 34 個 `*.ko.tsv`，不含 `ko-name-exemptions.tsv`、`ko-coverage-exemptions.tsv`。Windows、macOS 未跑。

## 10. 規格 043 §5 驗收現況

| 項 | 內容 | 現況 |
|---|---|---|
| 1 | `ko_check.sh`、`ja_check.sh`、`test_ja_check.py` 全綠，合成負例，字集與字型 | **已證實**（打包前置檢查；`ko_check.sh` 29 步、`test_lang_check.py`、名字表測試） |
| 2 | 覆蓋斷言 5,414 列、5,406 key、manual 0 列、`source` 等於 zh-TW | **已證實**（`ko_check.sh`） |
| 3 | ko 在 F4 循環內、`lane[ko]`、無語言停用、A 類零失敗、四時點 `skips=0` | **已證實**（§2、§5；`TestKoLaneOnFormalText`） |
| 4 | 版面單元測試、差分測試、phase254 七條回歸不變、靜態預檢入收據 | **已證實**（§4、§6）。trace 重播閘門與 `joinWrapped` 成功率**未做** |
| 5 | 串接批量驗證與 100 條抽審 | **未做** |
| 6 | 四時點與 16 個家族時點收據，截圖檢視 | **已證實**（§2、§3）。動詞後置片段、名字夾在片段之間的專屬路徑**未量** |
| 7 | 語義分歧對照與雙語分層抽審 100 列 | 稽核 3,300 列已做（phase-302 §4）；分層抽審與錯誤率**未做** |
| 8 | 覆蓋表與宣稱範圍 | 本文 §2、§3 即為第一版；README 與讀我.txt 的宣稱已限於「機器輔助」並說明玩家名與手冊題段落的限制 |
| 9 | 前端冷開機截圖、說明頁、打包外洩掃描、manifest 重建 | **已證實**（§5、§8、§9；Linux）。Windows、macOS 未跑 |

因此規格 043 維持 READY，不升 CONFORMED。宣稱範圍：ECL、水平選單、手札、開場劇情、加入後選單、技能與圖示各頁、離開確認列；其餘家族為載入與靜態驗證。

## 11. 下一步

1. trace 重播閘門（規格 042 §5.4）與 `joinWrapped` 統計，量測真實 ECL 窗寬，回答 §6 的窄窗溢出風險。
2. 串接批量抽審（ko 與 ja 共用工具）與雙語分層抽審。
3. 水平選單寬度放寬量測（042、043 共用）。
4. 掃 checkpoint 的 ECL 事件序列，補動詞後置片段與名字夾在片段之間的真實路徑截圖。
5. Windows、macOS 打包模擬。
6. 日韓玩家名音譯器（規格 044、045）與手冊段落。
7. zh-TW 疑似錯誤：Issue #37。
