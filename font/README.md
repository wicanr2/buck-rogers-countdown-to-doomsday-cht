# 字型建置入口

本目錄只保存可重生的字元需求，不提交第三方字型或生成的 `GOLEMFNT` 二進位。
`characters.txt` 必須只由正式 TSV 的 `translation` 欄透過
`tools/catalog_font.py chars` 產生；不得手工加入未使用字元。

歷史 prototype 曾使用本機 GNU Unifont 作測試輸入，不代表正式產品字型決策。第八十八階段
已證實目前 `workplace/` 沒有可回查的原始輸入或實際授權文字；舊 GOLEMFNT 產物也不能反推
來源或授權，因此不得當作正式候選。未來候選的授權檔若明載 GNU GPL 2+（含字型嵌入例外）及
SIL Open Font License 1.1 條款，仍須連同實際採用版本重新核對完整文字與必要告知；這不是
採用或可散布的聲明。

建置及驗證命令見 [`text/README.md`](../text/README.md)。

## 3× host 設定面板原生字型

使用者已為 3× host 面板選擇倚天原生 24 點：漢字與「×」24×24、
ASCII 數字 16×24；2× 仍用既有 16×16 字型。可版控的
[`tools/eten_host_font3.py`](../tools/eten_host_font3.py) 只保存抽字規則、
來源 SHA-256 與安全輸出邏輯，不含私有字模。它從正式
[`text/host-ui.zh-TW.tsv`](../text/host-ui.zh-TW.tsv) 取得五個標籤，
核對本機三份 24 點來源及 ETUNPACK 解壓器的固定雜湊，並把兩份
GOLEMFNT 與 manifest 寫到已存在的 ignored `workplace/` 子目錄。

以下命令**只在受限 Docker 內執行**：專案掛於 `/project`，本機倚天
來源唯讀掛於 `/etan`，已核雜湊的解壓器所在目錄唯讀掛於
`/decoder`，只有 `/project/workplace/host-only-3x-panel-ab` 可寫；
執行容器須另設 `--rm`、`--network none`、資源上限及目前 UID/GID。
輸出目錄須先存在，來源路徑須在掛載前逐項驗證存在且為檔案。

```sh
python3 tools/eten_host_font3.py \
  --catalog /project/text/host-ui.zh-TW.tsv \
  --std /etan/ET353S/FILES/STD.24M \
  --spc /etan/ET353S/FILES/SPCFONT.24 \
  --ascii /etan/ET353S/FILES/ASCFONT.24 \
  --etunpack /decoder/etunpack.py \
  --out-dir /project/workplace/host-only-3x-panel-ab
```

工具在來源缺失、雜湊不符、解壓截斷、空白／損壞字模或輸出位置不合規
時失敗即關閉，不以 22 點衍生字型補位；驗證失敗保留舊產物，發布中
若後續檔案替換失敗會回復已替換檔案。合成負例在
[`tools/test_eten_host_font3.py`](../tools/test_eten_host_font3.py)。
兩份字型、manifest、原始字型及衍生圖像均不可加入 Git、GitHub
或公開發行包。實際 A 子集雜湊及 host-only 畫面收據見
[phase212](../docs/re/phase-212-host-only-3x-eten-font-ab-draft.md)；
這不表示原版玩家路徑或規格 004 整體符合。

使用者提供候選與完整授權文字後，必須先在 Docker 內執行候選審查：

```sh
python3 tools/catalog_font.py validate-candidate text/manual.zh-TW.tsv \
  --manifest workplace/phaseNN/input/candidate-manifest.json \
  --source workplace/phaseNN/input/candidate.hex.gz \
  --license workplace/phaseNN/input/COPYING
```

命令只輸出檔名、SHA-256、format／version 與 glyph count metadata，不寫入 GOLEMFNT。它要求 strict
manifest、來源與授權文字雜湊、691 glyph coverage、`local-validation-only` 與 `undecided` 發行狀態；
通過只代表候選可進入後續權利審查，不代表採用、嵌入或可散布。

第九十三階段已依使用者指定，唯讀盤點本機倚天 `ET353S/FILES/` 的 15 點字模；第九十四階段再依
使用者確認的已購買字型之**本機遊戲使用**範圍，建立未追蹤的 16×16／691 glyph 對齊 preview。其定位、
檔案雜湊、兩案收據與停止線見
[`docs/spec/007-eten-15-font-candidate-intake-draft.md`](../docs/spec/007-eten-15-font-candidate-intake-draft.md)。
倚天本機建置器已實作於 [`tools/eten_font.py`](../tools/eten_font.py)，使用者已選定 `top-pad`。
以下命令在 Docker 容器內執行，專案掛在 `/project`、倚天來源唯讀掛在 `/eten`，工作目錄為 `/project`：

```sh
python3 tools/eten_font.py build text/manual.zh-TW.tsv \
  --asc /eten/ET353S/FILES/ASCFONT.15 \
  --spc /eten/ET353S/FILES/SPCFONT.15 \
  --std /eten/ET353S/FILES/STDFONT.15 \
  --out workplace/phase96-font/buckrogers-eten-top-pad.golemfnt \
  --manifest-out workplace/phase96-font/buckrogers-eten-top-pad.json
```

第九十六階段最初的 22 段手冊集合為 691 個字模；目前 39 段手冊為 934 個字模。
建置器亦可合併 11 份正式介面與手冊 catalog，目前本機完整聯集為 961 個字模，
來源與輸出均驗證 SHA-256，建置失敗時保留既有產物。完整入口與雜湊見
[第一百零一階段收據](../docs/re/phase-101-body-icon-text-catalog.md)。
它不使用 Unifont validator；兩套來源解析保持各自格式。字型與生成產物只留在本機 `workplace/`，
不得加入 Git、GitHub、Release 或公開封包。契約見
[spec 008](../docs/spec/008-eten-top-pad-local-font-builder-draft.md)。

先前校訂後的全部正式與 DRAFT `text/*.zh-TW.tsv` 聯集為 997 glyph；本機重建收據與
page2／page3／page4 分頁回讀結果見
[第一百一十八階段收據](../docs/re/phase-118-story-draft-font-rebuild.md)。此 997 glyph
是新的 DRAFT 字型涵蓋基準，不抹除上述歷史 961 glyph 基準，也不代表任何故事頁面
已完成 runtime 覆繪或可散布。生成的 `GOLEMFNT` 與 manifest 僅留於被忽略的
`workplace/phase118-font/`。

第五頁 DRAFT 敘事加入後，現行完整聯集為 1006 glyph；本機倚天重建與 dosgolem
正式 loader 零缺字收據見[第一百二十二階段](../docs/re/phase-122-story-page5-enter-trace.md)。
先前 997 glyph 為當時 catalog 的歷史基準，不能用舊字型驗收新譯文；新版產物仍只在
被忽略的 `workplace/phase122-font/`，不得公開散布。

第六頁 DRAFT 敘事及第五頁校譯加入後，全部 17 份 `text/*.zh-TW.tsv` 的本機倚天
聯集重建為 1014 glyph。`workplace/phase128-font/` 的 GOLEMFNT SHA-256 為
`16e0e8cd687bbcd0f12b8330a47a7eed9519dd861063c41c01388f9ffc41d024`，
字元清單 SHA-256 為 `91ed941652102ce935a0ff9afd1dd1b85da5964d0f8d53d8a3334a87e4f6d24c`；
dosgolem 正式 loader 對全部譯文字元回讀為零缺字。這只是 DRAFT 字型覆蓋收據，
並非第六頁 runtime 已接通或字型可公開散布。

新增 post-join 選單前，20 份 `text/*.zh-TW.tsv` 的字元聯集為 1024 字。`font/characters.txt` 曾用
`python3 tools/catalog_font.py chars text/*.zh-TW.tsv --out font/characters.txt` 在 Docker 內重建，
SHA-256 為 `daa100bfbcc917a3f9dc811a2b34262a9e26dc5666c0b085c58c1d0815abbd93`。
已接通的畫面容許不同 catalog 共用同一文字鍵，所以 `chars` 逐檔驗證格式後取字元聯集；
`lint` 的跨檔唯一鍵檢查仍保留，不可用於這批共享鍵 catalog 的合併驗證。
當時本機倚天產物 `workplace/current-font/buckrogers-eten-top-pad.golemfnt` 的 SHA-256 為
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`，manifest 為
`06acf27f04027f473a29e14d221bbc64a1abfcc725ca8890d22940282777caa5`；兩者不加入版控。
Docker 回讀確認全部 20 份 TSV 的譯文字元均有字模，缺字及多餘字模均為零。這僅證明
字型覆蓋，不表示所有文字路徑均已接通或可公開散布。

加入獨立 DRAFT `post-join-menu.zh-TW.tsv` 後，當時 21 份 catalog 的字元聯集為
1026 字，`font/characters.txt` SHA-256 更新為
`04d33bb125b00dad647abadfb3c9da8f7a714d722581fc6676d393a32eb6a03f`。
同一路徑的本機 `top-pad` GOLEMFNT SHA-256 為
`ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`，manifest 為
`d4810497db8b47b1e67c329d3a2b373986b5b30656198ae9e67e1c7da126c66b`。
舊 1024 字模產物已由本機新建置結果取代；它的雜湊只保留作歷史定位。

正式 Linux host 面板需顯示「設定／套用／取消／2×／3×」；先前 21 份遊戲 catalog 的
1026 字模不含所有 host 標籤，真實 Ebitengine 測試因缺「套」而正確拒絕。
新增 [`text/host-ui.zh-TW.tsv`](../text/host-ui.zh-TW.tsv) 作唯一正式文案來源後，
22 份 TSV 的字元聯集為 1028 字，`font/characters.txt` SHA-256
`3931dd4d7825feefe3fadf7ea8f35925991d07a6947894a4651d2d909cb5f578`。
本機 `top-pad` GOLEMFNT SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
manifest SHA-256 為 `39eb11a95d95eed749fefa4d358230e5e449339eb2e189f1a8296f0cde8cd00f`；
兩者仍只在 ignored `workplace/current-font/`，不得公開散布。

第一百九十一階段新增兩句技能 Exit DRAFT TSV 後，現為 23 份繁中 TSV；
Docker 內以全部 `text/*.zh-TW.tsv` 重生的字元聯集仍與版控
`font/characters.txt` 逐 byte 相同（1028 字、SHA-256
`3931dd4d7825feefe3fadf7ea8f35925991d07a6947894a4651d2d909cb5f578`）。
兩句共用現有字模，無需替換上述已釘選的本機 GOLEMFNT；這只證明
靜態字元覆蓋，不代表新提示的版面或執行期已驗收。

2026-09-24 的 24 份正式 TSV 校訂後，重新執行上述 `chars` 與
`eten_font.py build`／`verify`；目前 `font/characters.txt` 與本機
`workplace/current-font/` 子集均為 1,025 字模，字元清單 SHA-256
`eee90d5182a49f21260911b2a56913a809ec4ed2157767188135ac5a3e1fa23e`，
本機 GOLEMFNT SHA-256
`78c43d0758db5aaa97b60574c06ba1fdccc27b187cd465c3deb8b37c4b0e226f`。
dosgolem 正式 loader 逐字回讀為 1,025／1,025。
所有本機字型與 manifest 仍不得加入版控或公開散布。這僅為字型覆蓋，
不表示 Linux 玩家視窗已接通原版輸出攔截。

2026-09-25 手冊前 18 筆校譯後，上述 1,025 字模為歷史收據，
其後的 1,030 字模收據亦見[規格 024](../docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)。
目前全部 24 份正式 TSV 重生的 `font/characters.txt` 為 1,046 字，
SHA-256 `7aa7ed9f4fbff670cdba023b8c5f3a20486423c42393b94495c3c7da6eace55b`；
本機 2× `GOLEMFNT` 已重建並通過 `eten_font.py verify`，與既有
3× 面板原生 24 點 A 版共同通過正式雙倍率 manifest 前檢。
兩份字型仍只可在本機使用，不進入 Git 或公開封包。

2026-09-25 第三頁確證詞義校譯後，上一段 1,046 字與雜湊只保留
為校譯前收據。現行 24 份 TSV 重新產生的 `font/characters.txt`
為 1,045 字，SHA-256
`17a8be6af375860b45f55d11642f0d223b42b02ba0dc6aecb1ae5eba024664ec`；
本機 2× `GOLEMFNT` SHA-256
`cd96fbd1c00e82e3deaa5e357c6140c0f88ad2cefc4cae72eae6bea2ff6949d3`，
manifest SHA-256
`6512eafb389b78e6cbfe09e693e39ce27ddab5fc6df1e61538440be73f12a822`。
`eten_font.py build`／`verify` 通過；本機字型與 manifest 仍僅在
ignored `workplace/current-font/`，不得散布。

2026-09-25 手冊 crosswalk 第 9–12 筆四處中文印刷本修訂，
使用者已選**中文印刷本優先**，上一段 1,045 字僅保留為校譯前收據。
現行 24 份 TSV 產生的 `font/characters.txt` 定版為 1,046 字，SHA-256
`e6973763953ba738854376bdcc049a87b76540616b6626405ed1fb5489073b0b`；
本機定版 top-pad GOLEMFNT SHA-256 為
`14fca041c98198f778b06552a2a2fc34773b1fbdcf9e6683e72ea244228d4dca`，
manifest SHA-256 為
`703cb633fad24001c6041cb3cf9eed9397c49bc1d9a519bdcfac35082297e4b3`。
同一個 `eten_font.py verify` 唯讀核驗通過；兩份私有產物不入版控。
來源衝突及原版局部驗收限度見[規格 024](../docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)。
