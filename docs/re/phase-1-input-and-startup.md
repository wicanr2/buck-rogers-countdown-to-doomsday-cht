# 第一階段：輸入、啟動與重播收據

日期：2026-09-20  
狀態：已完成第一階段的啟動與可見選單基線；範圍限於此文件列出的正常路徑。

## 輸入與權利邊界

兩個輸入皆是使用者自備的原作材料，只能作本機研究；未驗證其公開散布權。因此壓縮檔、
解壓檔、IDA 資料庫、畫面傾印及可還原衍生物均留在被 Git 忽略的 `workplace/`，不得上傳
GitHub 或放入發行包。

| 輸入 | SHA-256 | 格式／處理狀態 |
| --- | --- | --- |
| `Buck Rogers - Countdown to Doomsday (1990).zip` | `f4293e52850c7b2e008656ec91bf6aaa9407f74f0becef4755bce610d7a5932a` | ZIP；以 Docker 的 Python `zipfile` 解壓到 `workplace/original/BRcdoom/`。ZIP 清冊有 92 項（1 個目錄、91 個檔案）。 |
| `珍074-拯救地球.rar` | `4d018c13cf2d7aa632435f8c03042bf42a2c8f901fe563abe432eb9c3f0e74c8` | RAR5；已登記但未解壓。現有離線工具映像沒有可用的 RAR 解壓工具；內容清冊、頁碼與手冊段落對應皆為 **未知**，未據此推論任何手冊文字。 |

可重生的完整輸入清冊在被忽略的
`workplace/inventory/input-manifest.json`；它保存 ZIP 的成員清冊、魔數、雜湊、Docker
工具識別與上述權利分類。

## 工具鎖定

| 用途 | 容器映像／版本 | 映像 ID | 條件 |
| --- | --- | --- | --- |
| ZIP 清冊與解壓 | `psychicwar-go-ebiten:latest`，Python `zipfile` | `sha256:083e45e6bc0f01ca46ba0774581572c80a607120431b530de72cdd6ffb36f2f7` | `--network none`，原始檔唯讀掛載 |
| dosgolem 探針 | `golang:1.24-bookworm` | `sha256:1a6d4452c65dea36aac2e2d606b01b4a029ec90cc1ae53890540ce6173ea77ac` | `--network none`、`--memory 2g --cpus 2 --pids-limit 256` |
| IDA 最小資料庫探針 | `ida-pro-9.4-idapython:locked-v1`，IDA 9.4 | `sha256:6f6d59af49d0008c4109a5295b5f374bdc007e2d1ab28cb9de08779584de2780` | `--network none`，輸入唯讀、輸出在 `workplace/ida/` |

dosgolem 原始碼版本：`d9c0c27ca9af8239c7e96272a7165e03d7da04bf`。此文件不把它稱為
正式版號；收據以 Git commit 鎖定。

## 被測原版與靜態定位

| 檔案 | SHA-256 | 已證實事項 |
| --- | --- | --- |
| `START.EXE` | `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1` | 真實 MZ 啟動檔；IDA 9.4 最小探針建立 `workplace/ida/START-v2.i64`，資料庫有 180 個函式。IDA 位址空間為「IDA database linear addresses」。 |
| `GAME.OVR` | `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0` | 真實覆蓋檔；本路徑在 #71004516 與 #71004529 從原始素材讀入。 |
| `8X8D1.DAX` | `15d332387c941bde5dd414ab060f9fedc44e4d7e03108e724000c4fe31d3c997` | 啟動期已載入的候選字型／圖資；尚未把它與選單字元位元組逐一對應。 |

## dosgolem 能力收據（限已跑路徑）

從 `START.EXE` 冷啟動執行一億道指令，進入 Mode 13h 標題畫面；再從
`workplace/probe/start-70m.state` 延續。探針報告在此路徑上沒有「未實作服務」。這只表示
下表列出的實際呼叫已經過，**不宣稱**遊戲全域或 dosgolem 全域支援。

| 類別 | 已觀測且可用 | 未支援／缺口 |
| --- | --- | --- |
| CPU／載入 | 16 位元 MZ 啟動、覆蓋檔載入、`GAME.OVR` seek/read | 本路徑未觀測 CPU 未支援；其他程式區段為未知 |
| DOS | INT 21h AH=`1A,19,25,2C,35,3D,3E,3F,42,44,47` | 本路徑未觀測未實作 DOS 服務 |
| BIOS／輸入 | INT 16h AH=`00,01`；BIOS BDA 鍵盤緩衝 | IRQ1 `-press` 輸入未被該程式的 INT 09h 接收；這是輸入路由差異，不是以記憶體改寫跨越的缺口 |
| 視訊 | INT 10h AH=`02,06,08,0F,10,11`；Mode 13h；AH=10h/AL=12 調色盤更新 | 本路徑未觀測未實作 VGA／BIOS 視訊服務 |
| 檔案 | `BUCK.CFG` 與遊戲圖資，以及上述 `GAME.OVR` 讀取 | 本路徑未觀測未實作檔案服務 |
| 滑鼠 | INT 33h AX=`0000,0001,0002,0003,0004,0009` | 未以滑鼠完成後續流程；互動語意仍未知 |

## 最小正常玩家路徑與重播

這條收據沒有傳送座標、沒有 `-poke`、沒有強制獲勝、沒有改寫原版資料，也沒有使用
DOSBox：

1. 用 `START.EXE` 與原始 `BRcdoom/` 冷啟動到 #70,000,000，儲存完整機器狀態
   `workplace/probe/start-70m.state`。
2. 從該固定狀態，在 #71,000,000 把一個空白鍵加入 dosgolem 的 BIOS BDA 鍵盤緩衝。
3. 原版於 #71,000,214 以 INT 16h AH=00 取走 `0x20`；原始程式再讀取 `GAME.OVR`，並在
   #71,130,187 寫出下節追蹤的第一個選單文字像素。
4. 在 #100,000,000 得到玩家可見的功能選單。兩次獨立重播的 raw Mode 13h VRAM 均為
   `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`。

重播所用 dosgolem 命令（在上述 Go 容器、`/src` 為 dosgolem、`/out` 為
`workplace/probe`、`/orig` 為唯讀的 `BRcdoom`）：

```sh
go run ./cmd/probe \
  -load-state /out/start-70m.state -root /orig \
  -bios-keys ' ' -bios-key-from 71000000 -bios-key-every 1000000 \
  -steps 100000000 \
  -dump-vram /out/after-bios-space-100m-replay-b.vram \
  -dump-palette /out/after-bios-space-100m-replay-b.pal
```

這個收據的輸出檔與命令日誌保留在 `workplace/probe/`。重播的固定狀態是 dosgolem
機器狀態，不是測試專用的原版記憶體寫入。
