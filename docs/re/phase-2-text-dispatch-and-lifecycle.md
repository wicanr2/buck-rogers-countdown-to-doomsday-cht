# 第二階段：文字分派與生命週期追蹤

日期：2026-09-20  
狀態：已完成 DRAFT 前置證據；未授權任何 production 覆繪。

## 輸入、工具與位址空間

原版輸入雜湊、Docker 映像與 dosgolem commit 繼承
[第一階段輸入與啟動收據](phase-1-input-and-startup.md)：`START.EXE` 為
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`、`GAME.OVR`
為 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，dosgolem 為
`d9c0c27ca9af8239c7e96272a7165e03d7da04bf`。

本文件所有 `0763:xxxx`、`5747:0002` 與 `3D21:xxxx` 都是 **dosgolem 執行期實模式
段:位移**。它們不是 IDA database linear address，也尚未被靜態映射為某個原始檔的
偏移。下列原始 bytes 由被忽略的 `workplace/probe/phase2-menu-segment-0763_0000.bin`
（SHA-256 `234053de48bcd2747aabdcb05b2550c791e7016e6990f61d9f562d0dfc33b4b9`）重生。

## 固定狀態與收據

全部實驗由 `workplace/probe/start-70m.state` 開始，在 #71,000,000 把空白鍵放入 BIOS
BDA，原版於 #71,000,214 經 INT 16h AH=00 取走。沒有 `-poke`、座標注入、forced-win 或
DOSBox。

| 收據 | 觀測 |
| --- | --- |
| `phase2-text-wrapper.log` | `0763:03C5` 以 `push cs; call 0763:1809` 呼叫 glyph wrapper；#71,130,060 的參數為 glyph `1`、背景 `0`、前景 `0x0A`、格列 `13`、格欄 `9`。 |
| `phase2-char-renderer.log` | `0763:026B` 在 #71,100,000–#71,150,000 被呼叫 43 次；原始 byte 參數形成可見選單英文字元序列，並攜帶前景／背景色與格座標。 |
| `phase2-string-dispatch.log` | `0763:0424` 由 `37F1:15BD` 呼叫；#71,107,478 的來源為 `5747:0002`、前景 `0x0A`、背景 `0`、格列 `12`、格欄 `9`。 |
| `phase2-string-source-seg-5747_0002.bin` | 在 #71,107,500 以 `-dump-seg 5747:0002:32` 直接擷取：`14 43 72 65 61 74 65 20 4E 65 77 20 43 68 61 72 61 63 74 65 72`。首 byte `0x14` 是長度，後續 20 bytes 是 ASCII `Create New Character`。 |

`-dump-mem-at` 會以 IDA 位址語意解析地址，曾對 `57472` 傾印出零值；這是位址空間誤用的
環境／觀測失敗，不是原版資料為零。後續以 `-dump-seg` 重跑成功，且本文件只引用後者。

## 原始輸出鏈

| 層級 | 原始定位與 bytes／資料流 | 等級 | 可採用結論 |
| --- | --- | --- | --- |
| 字串分派 | `0763:0424`：`LES DI,[BP+6]` 取 far pointer；以長度 `0xFF` 複製到 `SS:BP-0x100`；讀第一 byte 當長度，索引 `1..length` 讀入每個 byte，再呼叫 `0763:026B`。 | 已證實 | 這是長度前綴 byte-string renderer；本選單樣本的 byte 編碼為 ASCII。來源資料的更上游表格／資產檔仍未知。 |
| 字元 renderer | `0763:026B` 接收原始 byte、樣式、前景／背景、格列／欄；樣本 byte `0x41` 透過以 `0x40` 為基的頁面／glyph 運算，輸出 glyph index `1`。其直接 caller `0763:049B` 從 stack 字串緩衝讀 byte。 | 已證實 | 可量到每個原文 byte、色彩及 40×25 文字格座標；頁面／樣式的完整語意僅為強推論。 |
| glyph wrapper | `0763:1809` 載入 `[DS:5F32]` 的 far glyph base，計算 `glyph_index × 8`；計算 `DI=((row×320)+column)×8`，接著呼叫 pixel primitive。 | 已證實 | 單一英文 glyph 佔 8×8 像素；格欄 `9`、格列 `13` 的 origin 為 `(72,104)`。 |
| pixel primitive | `0763:183A..1863`；`MOV AL,[SI]`、遮罩 `0x80..0x01`、依 `[BP+8]`／`[BP+0A]` `STOSB` 到 Mode 13h VRAM。 | 已證實 | 原版以背景與前景色逐像素重繪 8×8 glyph；第一階段的 `(74,105)`、色盤索引 `0x0A` 是此格內像素。 |
| 選單資料來源 | #71,107,478 的 `5747:0002` 指向上表擷取的長度前綴資料；caller 是 `37F1:15BD`。 | 已證實／未知 | 字串 buffer 與其內容已證實；`37F1:15BD` 如何選擇或產生該 buffer、以及它是否由 `GAME.OVR` 的固定表產生，為未知。 |
| 清除、捲動與失效 | 只量到標題轉選單的完整重繪；沒有孤立清除、捲動、游標反白、翻頁或後續輸出覆蓋。 | 未知 | 不得建立永久覆繪或宣稱可安全清除原文；這些是 READY 前的阻擋項。 |

## 對覆繪的已知幾何

對已量到的選單字串，英文原文矩形可由 `(column×8, row×8, length×8, 8)` 取得。例如
`Create New Character` 的 `(9,12,20)` 導出 `(72,96,160,8)`；其實際重繪色彩為背景
`0x00`、前景 `0x0A`。這只證明此 static text row 的原版 geometry；**不**是中文文字安全
矩形、中文換行規則或完整選單生命週期的證明。

## 未解與停止線

- 現行能力已可在 `0763:0424` 量到 pointer、長度、bytes、色彩與格座標，沒有 dosgolem
  通用觀測缺口；不需要為本階段修改 dosgolem。
- 上游字串表／資產來源、非 ASCII／控制碼、樣式頁面完整語意、清除、捲動、游標與返回畫面
  皆未證實。不得用這一條選單收據外推至劇情、戰鬥、角色名稱或手冊提示。
- 下一階段的 production 前工作應先做另一個可重播畫面轉換或選單互動，量到失效時機；再由
  DRAFT 經證據審查決定是否有足夠資料升為 READY。
