# 050 — 繁簡中文字型的 Unifont 字形來源

狀態：**READY**（2026-10-01；第一輪獨立審查的必修與建議已併入本版，審查後的畫面比較見 phase-313）。
日期：2026-10-01
Issue：#36
前置：規格 035（發行打包）、041（簡體）；`font/README.md`（發行字型為 GNU Unifont 17.0.05 子集）。

## 1. 問題與證據（已證實）

發行字型的來源是 `unifont_all-17.0.05.hex.gz`。Unifont 的 `font/Makefile` 組出這個檔時，平面 0 的來源檔依序是
`unifont-base.hex`、`hangul-syllables.hex`、`izmg16-plane00.hex`、`plane00-nonprinting.hex`、`plane00-unassigned.hex`、
`spaces.hex`、`wqy.hex`（`ALL_HEX_PLANE00`，約 199 至 206 行），之後 `sort -u -k 1,1 -t ':'`（約 524 行）對同一碼位取先出現者。
`izmg16-plane00.hex` 是日文（JIS X 0213:2004）字形，排在文泉驛點陣宋體 `wqy.hex` 之前，所以兩者重疊的碼位一律取日文字形。
Unifont 的預設 `unifont-17.0.05.hex`（`UNIFILES`，約 156 行）不含 `izmg16`，CJK 字形取 `wqy.hex`；17.0.04 起另有台灣來源
`plane00/t-source.hex`（28,142 字），官方預編 `unifont_t-17.0.05.hex` 是預設加上它的覆蓋。

本機於 Docker 內比對（`workplace/phase312/glyph_scope.py`、`scope2.py`；來源 `unifont-17.0.05.tar.gz`，SHA-256
`f287cffb26e22723aa36e6684869b0f3ff3bfb822c4b01008bd847911ec1b631`）：

| 項目 | 數量 |
|---|---|
| `wqy.hex`／`izmg16-plane00.hex` 碼位數；兩者重疊；重疊中位圖相同 | 27,798／9,968；9,666；0 |
| zh-TW 字元清單（2,520 字）的 CJK | 2,402 |
| 　其中 `unifont_all` 取自 `izmg16`（日文字形） | 2,309 |
| zh-CN 字元清單（2,456 字）的 CJK | 2,339 |
| 　其中取自 `izmg16` | 1,634 |
| 　`unifont_t` 對 zh-TW 清單：有字形；與預設（`wqy`）位圖不同 | 2,402；2,384 |
| 　`unifont_t` 對 zh-CN 清單：有字形；與預設位圖不同 | 2,339；2,334 |
| ja 字元清單的 CJK | 1,505（日文要的就是 JIS 字形，不動） |

字形差異不只在筆畫細節：例如 U+9AA8 骨、U+6F22 漢、U+76F4 直，`izmg16` 是日文字形，`wqy.hex` 與 `t-source.hex` 是中文字形；
骨與 `t-source` 的差距：對 `izmg16` 37 位元，對 `wqy` 82 位元，所以台灣標準字形與 `wqy` 也不相同。zh-TW 與 zh-CN 發行字型現在多數
CJK 字用的是日文來源。

墨跡框（已證實，審查實測）：`izmg16` 字形墨跡在第 1 至 15 欄、第 0 至 14 列（只有 84 字觸及第 15 列）；`wqy`／`unifont_t` 字形在第 0 至 14
欄、第 0 至 15 列，zh-TW 清單中 `unifont_t` 有 2,154 字、預設有 2,172 字在第 15 列有墨。換字形來源會讓字與字、行與行的視覺間距改變
（16 點行距時上下行會相接），這是**版面可見的改變**，不是只有筆畫不同。

## 2. 決定與契約

決定（記錄理由）：zh-TW 用台灣來源（`unifont_t`，缺字回落預設），zh-CN 用預設（`unifont`，簡體字形只有 `wqy` 有）。拒絕的方案：
1. 維持 `unifont_all`（現狀）：大多數 CJK 字是日文字形，與 Issue #36 衝突。
2. 自製合併工具（以 `wqy` 取代 `izmg16`）：審查實測官方預編檔 `unifont-17.0.05.hex` 對兩份清單的字形與合併結果全等，不需要自製工具。
3. zh-TW 也用預設：台灣標準字形（`t-source`）存在，產品是繁體中文（台灣）。

契約：
1. 字形來源改為官方預編檔，直接釘上游雜湊，不產生衍生檔：
   - zh-TW（`buckrogers-unifont.golemfnt`）：`font/precompiled/unifont_t-17.0.05.hex`（SHA-256
     `169634258e4037b507beaafad5d72edc2e44b3faeaa856d9669e4657d1eee454`）。
   - zh-CN（`buckrogers-zh-CN.golemfnt`）：`font/precompiled/unifont-17.0.05.hex`（SHA-256
     `fd79af3613ec1b984a98d33428fdd43fcf06018d18059960d78edeb63d958622`）。
   - ja、ko：維持 `unifont_all-17.0.05.hex.gz`，字型位元組不變。
   以上兩個檔從已釘雜湊的 `unifont-17.0.05.tar.gz`（SHA-256 見 §1）解出；雜湊以解壓後內容計算，不以 `gz` 位元組計。
2. `tools/package.sh` 先核對 tarball 雜湊，解出兩個 `.hex` 並核對各自雜湊，zh-TW、zh-CN 用它們建字型；任何一項不符即失敗。
3. 字元清單 `font/characters*.txt` 不變，仍只由正式譯文產生。>U+FFFF 的字元一律失敗（平面 2 的來源 `izmg16-plane02` 優先於
   `zh-plane02`，本規格不處理；目前清單沒有此類字）。
4. 版面相關的檢查（§4）必須在 2×、3× 通過，因為字形墨跡框與間距會改變：dosgolem 的 `menuInkRect`（`menu_overlay.go`）在 action bar、
   body icon 等 overlay 以墨跡框判斷安全矩形，超出即載入失敗。
5. 下游同步：`THIRD-PARTY.md` 由 `tools/release/third_party.py` 產生，發行包 `讀我.txt` 與 `font/README.md`、`text/README.md` 的字型命令同步；
   授權敘述改為：GNU Unifont 17.0.05（OFL-1.1／GPL-2.0-or-later 含字型嵌入例外）；CJK 字形含 Unifont 收錄的文泉驛點陣宋體
   （Qianqian Fang，經授權），zh 字型在此之前已含 `wqy` 字形（zh-TW 93 字），這是補上既有的歸屬缺口；`izmg16` 為公有領域，
   ja 字型仍使用它。
6. `package.sh` 以 zh-TW 字型畫圖示（`appicon.py`，「拯救地球」四字原本取自 `izmg16`）：圖示會改變，是預期的。

## 3. 不在範圍

- 倚天字型（本機用，不發行）。
- ja、ko 的字形選擇。
- 平面 2 字形。
- 字形的美觀評比：選擇依據是「中文來源字形優先於日文來源」，zh-TW 另取台灣標準字形。

## 4. 驗收

1. 字型層（用實際輸入，實測值記入證據）：以新來源重建 zh-TW、zh-CN 字型，與現行字型比對。zh-CN 預期：只有 1,634 個取自 `izmg16` 的 CJK 字
   位圖不同，字格寬度與非 CJK 字元都不變。zh-TW 的來源 `unifont_t` 另覆蓋了台灣來源字形，所以不同的是 `unifont_t` 與 `unifont_all`
   位圖不同的全部 CJK 字（實測 2,401／2,402），另加全形標點（、。，！「」『』《》…，台灣習慣的位置與字形）；`…`（U+2026）
   原本是 8 點寬字形，新字形是 16 點寬，與版面的全形單位（`runeUnits`）一致。其餘字元（ASCII 等）位圖相同。ja、ko 字型位元組與前一版相同；
   重建兩次位元組相同。
2. 載入層：離線重播（`workplace/phase312/replay.sh`，字型換成新字型）的五份輸出與舊字型逐位元組相同；`apps/buckrogers` 套件測試除既有失敗外無新增；
   正式 runtime 在 2×、3× 各載入全部家族（選單、action bar、body icon、劇情頁、ECL、hmenu、引擎片段、手札面板、手冊）都成功，沒有因墨跡框落到英文原版。
3. 畫面層：同一固定腳本，舊字型與新字型各跑 zh-TW、zh-CN 的 2×、3×：`memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256` 相同；
   `-lang en` 的畫格逐位元組相同；中文模式的畫格有差異，以接觸表檢視選單、敘事（兩行相接處）、隊伍表、手冊頁、標題：字形正確、無缺字、無裁切、
   上下行可讀。
4. 打包：`package.sh linux` 通過（含發行包通道冒煙）；發行包內 zh-TW、zh-CN 字型雜湊與 §4.1 的重建一致；圖示重生。
5. README 的 zh-TW、zh-CN 展示截圖依新字型重生（只收覆繪後畫面）。已發行的 v1.1.0 影片不重製，隨發行說明註明畫面是舊字形。

## 5. 風險

- 行距：16 點行距下上下行相接。以 §4.3 的畫面檢視把關；若不可接受，退回方案由使用者決定，不在本規格自行加行距（行距屬版面規格）。
- `xlate/layer.go` 把字型 SHA 綁進快照：舊的覆繪快照無法在新字型下還原，本機用的舊 state 若含覆繪層要重建（不含覆繪層的原版 state 不受影響）。
- 發行字型改變後，使用者既有的字型雜湊（若有人釘它）會變：發行包只釘整包 SHA-256，沒有外部釘字型雜湊的流程。
