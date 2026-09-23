# 第二百一十二階段：3× 設定面板倚天字型 A/B 原型

日期：2026-09-24
狀態：**DRAFT 視覺決策前置；未選方案、未改正式前端、未執行 3× Apply。**

## 為何先停在 host 字型

[第二百零九階段](phase-209-cold-boot-live-ebiten-panel-pause-draft.md)
已在 2×真實視窗驗到暫停／恢復；3× 的正式
`frontend/ebiten.Game.New` 目前要求 `HostFont3` 為 22×22，
但本案現有的倚天 host/current GOLEMFNT 是 16×16。先前 ignored
原型曾用 16→22 衍生字型滿足建構器，不能當成使用者已核准的
3×字型品質。正式 3× Apply 在本階段**未執行**。

使用者指定的本機倚天來源有原生 24 點字型：

| 本機唯讀輸入 | SHA-256 | 已驗形態 |
| --- | --- | --- |
| `ET353S/FILES/STD.24M` | `347ae2655807fc250a18673e6634a363dfba7feee6c3355b886a0810d2d9c030` | ETUNPACK 壓縮明體；用既有解壓器還原 13,094 個 24×24、942,768 bytes，未截斷 |
| `ET353S/FILES/SPCFONT.24` | `da7574d2eee10b9d3b2a2d90bbc39e2ba482b9b2b73a9803f1e4dbefdd91a92a` | 408 個 24×24 符號 |
| `ET353S/FILES/ASCFONT.24` | `7e69f74bfedf57579fad41a1bc2f0c3a6da873cba1734fd30a1c4afc64893ada` | 256 個 16×24 ASCII |
| 既有 `psychic-war/tools/font/etunpack.py` | `738e491f65a52e6c716269b5e78b4937510547647615985c1d60b00ec2a4bac6` | ETUNPACK 解壓器，未修改 |

六個面板中文字元的原生字模全有墨跡。把 24×24 直接裁到 22×22
不是無損方案：九種整數偏移全部會削掉六字筆畫，最好偏移仍損失
合計 57 個墨點。本機 ignored
`workplace/cold-boot-3x-apply-gap/receipt.json` SHA-256
`c9524423326adcae8157ec4321da4520b92b936d793026e8f9ab7154cd31fea1`
保存這個數值前置檢查，不含字模或影像。

## 不載原版遊戲的並列原型

ignored `workplace/host-only-3x-panel-ab/render.py` SHA-256
`f9f4422f602e077f4915f0c02993977c57db9bb71cd1573b23fc22ee4dd232c3`；
`receipt.json` SHA-256
`2b3128a2487fb3d376fc3034b4a8ed03376cfb2dba1baf353bf03da28d94c48a`。
只用本機倚天字型與 host 控制列的既有座標、顏色，生成 960px 寬
的設定面板／關閉按鈕圖；**沒有**載入 DOS、原版遊戲畫面或執行
`Game.Update`。圖片只在 ignored 本機工作區：

- A：`workplace/host-only-3x-panel-ab/A-native24-open.png`、
  `A-native24-closed.png`。漢字／符號用原生 24×24，數字用原生
  16×24；開啟面板 PNG SHA-256
  `56736c7da70949cec8bd9ed14f7aa508b863f9ad2610cf4590412b17d153adfd`。
- B：`workplace/host-only-3x-panel-ab/B-current22-open.png`、
  `B-current22-closed.png`。沿用既有原型的 16→22 衍生方式作視覺
  對照，**不是**已核准的正式 3× 字型；開啟面板 PNG SHA-256
  `8ef9aecfbbea1cf64ae547e8d72d31a8d739e3edbca87da160f8c0f832bd7dd4`。

A／B 的九個相異 host 字元都不缺字，五項文字的 advance 與墨跡
都在控制項安全矩形內。A 的 `2×`／`3×` advance 各 40px，
中文字標籤各 48px；B 分別為 44px、44px。兩案左邊距沿用既有
控制項起點，沒有移動遊戲畫布或 host hit rectangle。

上述幾何只證 host-only 字形擺放。A 的原生 24 點目前仍不符合
正式 `Game.New` 固定的 22×22 `HostFont3` 契約；若使用者選 A，
須另走 READY 審查、正式 validator／字型資產接線與 3×實體 Apply
驗收。若選 B，也須先明確認可衍生字型的外觀，再做正式接線與
同狀態驗證。**目前兩者都不是已完成的 3× Linux 前端。**

主代理以唯讀 Docker 核對工具／輸入／收據／開啟面板 PNG 的雜湊
和數值欄位，沒有將字型、PNG 或原版畫面送入工具通道。原始
倚天檔與生成圖片只留本機，不進 GitHub 或公開包；本階段不記錄
尚未由使用者作出的視覺選擇。

## 2026-09-24 使用者視覺決定

使用者在並列圖上選擇 **A 原生倚天 24 點**，排除 B 的 16→22 衍生原型；
前文「未選方案」僅保留當時的原型形成歷程。正式 3× host 字型必須保留
原生 24 點筆畫，調整目前只接受 22×22 的前端驗證與繪製契約，並重驗
控制項安全矩形、2× 不變及實體 3× Apply。這項決定不是正式接線或
玩家路徑驗收；原版與已購字型仍只留本機 ignored `workplace/`。

## A 方案獨立審查補記（2026-09-24）

依已確認的視覺選擇 A，已於[規格 004](../spec/004-dosgolem-host-frontend-draft.md)
追加**3× host 字型限縮 READY 候選**。排除 B 的 16→22 衍生原型及
24→22 裁切；不變更 2× 16×16 字型。此補記是現行決策與最小接線
審查，前文「未選方案」保留 phase212 原型製作當時的歷史狀態。

本次只在受限 Docker 唯讀核對現有 `receipt.json` 與 `render.py`，
其 SHA-256 分別仍為
`2b3128a2487fb3d376fc3034b4a8ed03376cfb2dba1baf353bf03da28d94c48a`、
`f9f4422f602e077f4915f0c02993977c57db9bb71cd1573b23fc22ee4dd232c3`；
dosgolem fork HEAD `a01e34253fa59cc92c3fde1bf4b33577e318e9e7`。
沒有開啟倚天原始字型、GOLEMFNT 或 PNG bytes，沒有將其加入 Git。
原型收據的 A 覆蓋九個相異字元，`2×`／`3×` advance 各 40px、
「設定／套用／取消」各 48px；
五個控制項的 advance 與 ink box 全部 contained。此處釐清
「五項文字」是設定、兩個倍率選項、套用、取消，不是五個中文標籤。

正式路徑核對：`frontend/ebiten/game.go` 的 `Config.HostFont3`
仍是單一 `*xlate.Font`；`validateHostFont` 對 3× 固定要求
`W=H=22`，對每字以同一 `font.W` 計算安全矩形；`drawChrome`
依倍率選 `fontForScale`，`drawText` 對每字以該固定 W 前進。
`xlate.LoadFont` 的 GOLEMFNT 一份檔只有一組 W／H，不能在同一份
載入結果內表達 A 的 24×24 漢字／符號與 16×24 ASCII。
ignored `cold-boot-live-turn-proto/main.go` 載入本機 16×16
GOLEMFNT 後以 `font22(hostFont)` 填 `HostFont3`；那是已排除的 B
方向，不是原生 24 點接線。正式 `Game.New` 仍不能接 A，3×
Apply 與返回 2× 的實體路徑未驗。

最小正式變更候選：保留 `HostFont2` 與 2× 驗證、字距、畫筆；只把
3× config 改成分別持有 24×24 Wide 與 16×24 ASCII 的 typed view，
以逐字來源選擇、同一 advance 量測／繪製函式完成五個控制項。
本機抽字流程用 `STD.24M`、`SPCFONT.24`、`ASCFONT.24` 建立兩份
ignored 子集，不能把私有字型、衍生 GOLEMFNT 或字形圖加入正式
程式或發行包。phase212 host-only 圖不能證明 `Game.New` 的 fail-closed
驗證、3×實體 Apply、2×往返不變或真實 DOS 零副作用，故規格 004
維持 DRAFT；本限縮子契約的後續獨立 READY 審查如下，正反例列於規格 004。

## 2026-09-24 獨立 READY 審查

主代理獨立在唯讀、無網路 Docker 重算 A／B `receipt.json` 與
`render.py` 的 SHA-256，均與本文件所列相同；直接核對 A 五項
advance／ink box 及安全矩形，未缺字、未越界。另核對正式
`frontend/ebiten/game.go`：現行 `HostFont3` 為單一 `*xlate.Font`、
`validateHostFont` 限 22×22、`drawText` 逐字以同一 `font.W` 前進；
`xlate.LoadFont` 的單一檔頭也只載一組 W/H。這證明 A 的兩種字寬
必須由 3× 專用 typed view／量測與繪製同一分支接線，不能只換
字型檔或裁切。使用者已明確選 A；規格 004 的限縮 3× 字型節
列出來源雜湊、輸入型別、逐字 advance、2× 保持不變、負例及
私有素材邊界，足以授權**僅此字型接線**升 READY。

此審查不核准修改 DOS、原版輸入、完整 cold boot 或玩家路徑；
也不宣稱正式 3× Apply 已完成。這些須待正式程式、合成負例與
私有 Xvfb 收據通過後，才可於相同限縮範圍討論 CONFORMED。

## 2026-09-24 A 原生字型正式畫筆的本機限縮收據

依上述限縮 READY，`workplace/dosgolem/frontend/ebiten` 已把
`Config.HostFont3` 接成 `HostFont3{Wide, ASCII}`，3× 共用逐字選字、
量測與繪製分類，`Game.New` 在 Draw 前拒絕尺寸、缺字、壞列長、
空白字模、不支援的 ASCII 及安全矩形溢出；2× 的 16×16 畫筆與
驗證分支未改。無私有素材的合成 Go 正反例均通過。此處的「正式」
只指 dosgolem fork 中的 `frontend/ebiten` 程式，**不**等於本專案
已具正式玩家入口或規格 004 整體 READY。

本機三份倚天來源與 ETUNPACK 解壓器先以本文件列出的 SHA-256
在唯讀掛載內核對，再產生 ignored 兩份 GOLEMFNT：`host-wide24.golemfnt`
SHA-256 `621ed2c62e387916473cfcaefdd93585f085bfd4c2fc973e80cf691acac0fe49`
（7 字、24×24）；`host-ascii16x24.golemfnt` SHA-256
`7c411be15bee6911e1fec199af5643099831bd4f27b8a5676e20f96becbf2193`
（2 字、16×24）。ignored manifest SHA-256
`fe2da642b45b24ee086a5af4004d2835d952ed6a564dd0afc71e234b642ff9ff`。
本次子集 builder SHA-256
`5e82ddd8534ba580838fc8c43c9d313785a31bdb249150ff8ed1ab5f4f72494a`；
它仍位於 ignored `workplace/host-only-3x-panel-ab/`，且匯入同樣 ignored
`render.py` 的 `native24()`。因此**目前只能以本機現存工作區重播**，
尚不能宣稱由版控工具鏈從合法本機輸入乾淨重建。後續須把不含字模
bytes 的獨立 24 點抽字器放入既有 `tools/`，將三份本機來源與解壓器
設為明示且鎖雜湊的輸入，只向 ignored `workplace/` 寫產物，並有
來源缺席／雜湊錯誤／壞字模負例；這是 Issue #16 的未完條件。

`TestNativeHostFont3LocalPixels` 在受限、無網路、唯讀來源的
Docker/Xvfb 中，透過隔離測試子進程的真實 `ebiten.RunGame`，依序
`Game.New`、2× Open／Select 3×／Apply、3× Open／Select 2×／Apply，
於 `Draw` 回呼直接讀回 `screen.ReadPixels` RGBA。每個 pointer edge
各佔一個 `Update`；宿主面板指標送至 DOS mouse 次數為 0，關閉
回合 `Advance` 為 5。3× 五標籤白色墨點數依序為設定 334、2× 135、
3× 132、套用 356、取消 366；讀回像素逐點符合兩份原生字模，
全 chrome 的白色墨點均落在各自安全矩形。原生 24 點字模在
22×22 裁切邊界以外尚有 102 個墨點且畫面逐點相符，所以這份
收據沒有 22 點裁切。2×→3×→2× 前後，整張 640×436 RGBA
共 1,116,160 bytes 完全相同。`go test -count=1 -v ./frontend/ebiten`
和 `go vet ./frontend/ebiten` 同一唯讀 Docker/Xvfb 批次通過。

這是**合成畫布、合成 2× 字型、本機私有 3× 字模的 host-only 收據**：
實際測到正式 `Game.New`／`Update`／`Draw` 畫筆與倍率往返，
未載原版遊戲、未驗真正玩家入口、DOS raw 同狀態、存讀檔或完整
字型可散布性。先前將 `RunGame` 和其他 Ebitengine 繪圖測試放同一
進程，會在 `RunGame` 結束後的 `NewImage` 觸發測試生命週期 panic；
現以測試子進程隔離並全套乾淨重跑通過，該 panic 不屬產品缺陷。

## 2026-09-24 字型重建入口與 Draw 錯誤負例補證

上節所記「builder 仍依賴 ignored `render.py`」是該時點的缺口，
現已由可版控的 [`tools/eten_host_font3.py`](../../tools/eten_host_font3.py)
補上，不回寫或抹除先前原型的形成歷程。新工具從正式
`text/host-ui.zh-TW.tsv` 取五項標籤，明示接收本機 `STD.24M`、
`SPCFONT.24`、`ASCFONT.24` 與 ETUNPACK 路徑，先核對四份固定
SHA-256，借用既有 `tools/eten_font.py` 的 Big5 原始索引與
`workplace/` 輸出限制，不匯入 ignored `render.py`，不在版控保存
任何私有字模。三份輸出先完整驗證與暫存，才替換既有檔；合成測試
驗過來源缺失、SHA 不符、空白字模、第二檔替換失敗時舊輸出保留。
穩定命令入口見 [`font/README.md`](../../font/README.md)。

在來源唯讀、僅 ignored 輸出目錄可寫的受限 Docker 重建後，Wide
與 ASCII GOLEMFNT 分別仍為上節的
`621ed2c62e387916473cfcaefdd93585f085bfd4c2fc973e80cf691acac0fe49`、
`7c411be15bee6911e1fec199af5643099831bd4f27b8a5676e20f96becbf2193`；
新版 manifest SHA-256 為
`fd7a1da202bfdbcb3cb97172d33834871894f7e01bbd36bbd9d5f8b45b146af4`
（先前 `fe2da...` 是 ignored builder 格式，非字模差異）。正式
host catalog SHA-256
`c430f4424da2f090c4031a4079c1043fbd47dd6fa779c6eb208abcc5abf36b76`。
本輪工具 SHA-256 `ffac06f7623a8024664e3acec30ecaa15bdf0910a954d831eae8bfb876a763e6`；
五個不含私有字模的合成工具測試均通過。此收據解決「版控工具可由
合法本機輸入重建 A 子集」的窄缺口，不使字型或原版素材可散布。

另加 `TestNativeHostFont3DrawFailureLatchesBeforeNextDOSInput`：
`Game.New` 先接受合成有效字型並切到 3×，再刪除必要字模讓
`Draw` 的 `drawChrome` 回缺字錯誤；其後連續兩次帶畫布 Down 與
Enter 的 `Update` 都回同一鎖存錯誤，`Advance`、`Machine.Steps`、
BIOS pending 與 DOS mouse 次數均未增加。唯讀 Docker/Xvfb 的
frontend 全套 `go test -count=1 -v ./frontend/ebiten` 與
`go vet ./frontend/ebiten` 已通過。這只驗繪製錯誤發生後的
失敗即關閉（fail-closed）邊界，不代替 Issue #18 的整批 route
原子提交或完整 session owner。
