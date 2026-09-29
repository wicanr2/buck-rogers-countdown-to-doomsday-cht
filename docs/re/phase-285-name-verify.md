# 第二百八十五階段：規格 036 §5.3／§5.4 同狀態 A/B 與開場頁原版字模

日期：2026-09-29
狀態：**DRAFT（待主代理審閱後搬入 docs/re/）**

## 1. 輸入與方法

| 項目 | 舊（A） | 新（B） |
|---|---|---|
| runner | `runner-old`＝phase283 `runner-rerun25`，SHA-256 `dd449b29…42e03436` | `runner-new`＝`workplace/dosgolem-clean` 現行原始碼（含 b98c75f 加註）以 Go 1.26.7、`CGO_ENABLED=0` 重建，SHA-256 `181924ba…4e423a388` |
| catalog | `text-old/`＝`git archive 6b35726^ text`（3066b8e6ffd0） | 主 repo `text/`（HEAD 4aa1d6d；6b35726 之後 `text/` 無變更） |
| 字型 | `workplace/current-font/buckrogers-eten-top-pad.golemfnt`，SHA-256 `8d2103fa…b42826f0`（兩邊相同） | 同左 |

- 等價性：`runner-new` 與 phase254 rerun26 用的 runner（`afc70cb8…`，二進位雜湊不同）在 lb41-ecl2 的 2×／3× live RGBA 逐位元組相同。
- 每案同一 state、同一按鍵排程、同一停止點，舊新各跑 2×、3×。`diff.py` 比對：舊新 baseline RGBA、
  收據的 `memory_sha256`／`indexed_sha256`／`palette_sha256`／`stopped_at`、舊新 live 差異所在 8×8 格（邏輯座標）。
- 文字層：`textdiff.py` 對同一 key 舊新譯文逐字比對（`text-diff.txt`）。
- 探針：`workplace/dosgolem-clean/apps/buckrogers/zz_phase285_name_verify_probe_test.go`（新增檔，SHA-256
  `e77fa43c…2dac3666`），環境變數驅動；記錄 `0763:056C` 進入時的 ECL key、glossary person、手札編號，
  以及每個 retrace 呼叫 `FindOriginalASCII`。只記 key、長度、雜湊、步數與位址，不記原文。
- 全部在 Docker（`--rm`、`--network none`、`--cpus 3`、`--memory 4g`、`--pids-limit`、目前 UID/GID），
  原版 `/orig` 與主 repo `/project` 唯讀掛載。

## 2. 結果

| 項目 | 狀態 | 舊新差異位置（8×8 格，邏輯） | 收據檔名 | 推論等級 |
|---|---|---|---|---|
| A1 ECL 敘事含人名：`ecl.1.17.00143`（特必安），`checkpoints/logbook41-pre.state`，5,276.5M Enter，停 5,278.65M | 通過 | 只有第 17 列第 5–38 欄：第 5 欄是人名起點，其後同列因「(CARLTON TURABIAN)」加註右移；其他列、窗外零差異。舊新原版記憶體／indexed／palette 雜湊相同，baseline 相同。文字層只有人名收斂（卡爾頓•圖拉比安→卡頓•特必安）。`NameFirstOnly=0`、`NameUnannotated=0`（採第 1 段） | `ab/lb41-ecl2-{old,new}-{2,3}.json`、`-live.rgba/png`；`crop-lb41-ecl2-{old,new}.png` | 已證實 |
| A1 補充：同案 5,278M（打字中） | 通過 | 同上，第 17 列第 5–38 欄 | `ab/lb41-ecl-*` | 已證實 |
| A1 接句：該句之後的執行期碎片 | 記錄 | 下一個 `056C` 是手札尾段（ECL catalog miss，由手札／引擎模板處理），再來是 `ecl.1.17.00195`（無人名，舊新譯文相同） | `probe-lb41.txt` | 已證實 |
| A2 手札第 41 則（標題含特必安），5,285M 面板開啟 | 通過 | 只有第 2 列（標題列）第 11–36 欄；正文零差異。新標題 36 格（上限 38）。文字層：標題只有人名收斂，正文相同 | `ab/lb41-panel-*`；`crop-lb41-title-{old,new}.png` | 已證實 |
| A2 手札第 38 則（威廉、何茲漢、斯科特），6,886.5M Enter，停 6,889M | 通過（差異隨重排延伸） | 第 2 列第 12–26 欄（標題加註）；正文第 3 列第 12 欄起到第 14 列：起點在人名，之後因加註與舊全形註記移除而重排。文字層差異全在人名：加間隔號、移除舊「（Dr. Alexander William）」「（Holzerhein）」註記、Scot.dos→斯科特。原版雜湊相同 | `ab/lb38-panel-*`；`crop-lb38-panel-{old,new}.png` | 已證實（像素差異的「只在人名」依文字層＋目視判定；重排後的下游列屬連帶位移） |
| A2 手札第 60 則（維尼可夫、威廉），30,586.5M 上鍵，停 30,595.867M | 通過（差異隨重排延伸） | 第 2 列第 14–25 欄（標題）；正文第 4 列第 7 欄起到第 20 列，重排連帶。舊新譯文逐字相同，差異全由執行期加註造成。原版雜湊相同 | `ab/lb60-panel-*`；`crop-lb60-panel-{old,new}.png` | 已證實 |
| A3 開場第 6 頁，`phase123-story-page6-enter/page5.state`，321M Enter，停 330M | 通過 | 只有第 19 列第 1–25 欄與第 20 列第 1–17 欄，即 `line.003`、`line.004`；第 5、6 行零差異（在規格允許的第 3–6 行內）。原版雜湊相同。`tools/story_page6_catalog.py` 與 `story_opening_catalog.py` 對現行 catalog 皆 OK；保守格數 line.003＝31、line.004＝34（上限 39） | `ab/page6-*`；`crop-page6-{old,new}.png` | 已證實 |
| A3 開場第 1 頁 | 引用 | phase283 已做：o280900000 2×／3× 只有第 17 列第 8–21 欄 | `phase283-name-runtime/live-diff-rerun25-vs-rerun26.tsv` | 已證實（前一輪） |
| A4 含 Zane 的水平選單／怪物名遭遇 | 未量到 | — | — | 未知 |
| A5 規格 005 的 39／39 手冊收據 | 未涉及 | 6b35726 未改 `text/manual.zh-TW.tsv`（`git show --stat`），之後至 HEAD `text/` 無變更 | — | 已證實 |
| B 前端端到端截圖（2×） | 取得 | 敘事：`b-narrative-ecl-1-17-00143-2x.png`；手札：`b-logbook38-panel-2x.png`、`b-logbook41-panel-2x.png` | 同 A1／A2 的 new 2× 收據 | 已證實（LiveRuntime 合成；見 §3 限度） |
| C 開場頁期間原版 8×8 字模表 | 已在記憶體 | 見 §4 | `probe-c96.txt`、`probe-c104.txt`、`probe-c-page6.txt`、`probe-e-*.txt` | 已證實 |

## 3. 限度與未量項

- A4：Zane 的字串在 ECL5（`ecl.5.80.03321`，hmenu／monster 共用 `a4da3f4fffd1`）。本機 checkpoint 最遠只到 ECL2
  （廢棄飛船）；phase-272 記錄自動探索隊伍在第 8 層全滅，ECL3–6 沒有存態。未量到，不推測。
- 同一人物「只加第一次」與「不加」兩段退路在本輪樣本中都沒有觸發（`NameFirstOnly`、`NameUnannotated` 皆 0；
  手札四則都採第 1 段）。
- A 的「差異只在人名處」：像素層只能證明差異起點在人名，加註使同列或後續列重排，差異範圍會延伸到重排區。
  逐字核對在文字層（`text-diff.txt`），重排區內容已目視確認（crop PNG）。
- B：`cmd/buckrogers-play` 沒有載入 emulator state 的入口，自動化腳本只能從冷開機推，到不了 ECL1 基地與廢棄飛船。
  截圖改用 text-receipt runner 的 live 輸出；它與前端都呼叫 `LiveRuntime.Compose`，但字型用倚天 top-pad，
  不是發行版預設的 Unifont（`workplace/font-unifont/` 的 GOLEMFNT 早於 6b35726，是否缺新字未量）。
- Buck Rogers／巴克的 ECL 敘事未另找樣本；A1 以特必安滿足「至少一段」。
- 戰鬥或選單中同名人物只顯示中文（§5.4 後半）：未量到，理由同 A4。

## 4. C：開場逐頁期間的原版字模表

- 探針在每個 retrace 呼叫 `FindOriginalASCII`（掃 0–0xFFFFF，CRC-32 前綴＋SHA-256 `83a33300…631e`），
  另以同規則列出所有 CRC 候選位址。
- 結果：

| 路徑 | 步數範圍 | 涵蓋的開場頁 | 畫格 | 找到 | 位址 |
|---|---|---|---|---|---|
| `phase96-first-final/control.state`＋phase254 opening.sh 按鍵 | 266,557,247–292,000,000 | 第 1 頁（`056C` 於 268,684,426，逐字到 275,724,767，顯示到 281M）、第 2 頁 | 155 | 155／155，frame 1 起 | 0x3D211（唯一 CRC 候選） |
| `phase104-manual-correct-return/control.state`＋281M…351M 每 10M Enter | 280,000,000–360,000,000 | 第 1 頁尾段、第 2–9 頁 | 485 | 485／485，frame 1 起 | 0x3D211 |
| `phase123-story-page6-enter/page5.state`＋321M、331M Enter | 320,000,000–332,000,000 | 第 5 頁尾段、第 6 頁、第 7 頁開頭 | 73 | 73／73 | 0x3D211 |
| 更早的冷開機存態 `probe/start-30m`、`start-50m`、`after-space-100m`、`phase12-before-question` | 各自起點後 3M 步 | 開場前 | 各 19 | 全部找到 | 0x3D211 |

- 結論（已證實）：字模表最晚在 step 30,000,000 已在模擬記憶體 0x3D211，並在開場第 1–9 頁顯示期間的
  每一個 retrace 都找得到。首次出現的精確畫格在 30M 之前，本輪沒有量（沒有更早的存態）。
- 因此字模的取得不是限制。開場頁拉丁字每字佔一整格，是因為規格 031 §3.3 把原版字模限定在四個通用家族，
  劇情逐頁仍用倚天字型的 ASCII；而且 LiveRuntime 只在通用家族有內容時才搜尋（`genericActive`）。
  開場頁要改用原版字模需要修訂規格 031 的適用範圍，不需要新的取得時機；經查劇情 stamp 每字一格，行寬量測不受影響。

## 5. 檔案

`workplace/phase285-name-verify/`：`probe.sh`、`ab.sh`、`ab-inner.sh`、`diff.py`、`textdiff.py`、`crop.sh`／`crop.py`、
`ab/`（收據、RGBA、PNG）、`ab-diff.txt`、`text-diff.txt`、`probe-*.txt`、`crop-*.png`、`b-*.png`、`text-old/`、
`runner-old`、`runner-new`、`runner-p254`。

## 6. 補記：手札第 38 則殘留舊寫法

截圖發現第 38 則第二段仍有一處 `Scot.dos`。原因是 TSV 以 `\n` 表示換行，名字緊接在跳脫序列後，
`tools/name_glossary.py` 把 `n` 當成相連的英文字母而略過。已修正邊界判斷並補單元測試，重跑收斂只多這一筆。
