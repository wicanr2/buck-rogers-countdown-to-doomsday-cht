# 第七階段：文字 post-call 與 generation 事件

日期：2026-09-20  
狀態：已證實一條正常 Enter 路徑的 post-call 與 generation 順序；正式覆繪仍為 DRAFT。

## 問題、輸入與位址空間

第六階段已把 `026F:029C` 證實為 Mode 13h 矩形清除候選，但中文覆繪必須發生在
`0763:0424` **完成**原版英文繪製之後。本階段回答：

1. 哪個事件能證明整段英文，而非只有 dispatcher entry，已畫完？
2. 現有 dosgolem `OnCall` 是否足以表達該事件？
3. dispatcher、post-call、矩形清除與下一筆文字的實際順序為何？

固定起點仍為 `workplace/probe/after-bios-space-100m.state`（#99,999,999），在
#100,010,000 以 BIOS BDA 排入 Enter。原版 `START.EXE`／`GAME.OVR`、dosgolem commit、
正常輸入路徑與地址空間沿用前六階段；下列地址均為 dosgolem 執行期實模式 `segment:offset`。
所有 raw 狀態、VRAM、字串與 IDA database 都只留在被忽略的 `workplace/`。

## 工具與可回查收據

- dosgolem 副本：`workplace/dosgolem/` 分支 `buck-rogers-cht-output-overlay`，基準 commit
  `d9c0c27ca9af8239c7e96272a7165e03d7da04bf`。
- 執行 image：`golang:1.24-bookworm`；本輪容器實測 Go `1.24.13 linux/amd64`。
- IDA Pro 9.4 image ID：
  `sha256:6f6d59af49d0008c4109a5295b5f374bdc007e2d1ab28cb9de08779584de2780`；
  processor `pc`、database bitness 16、UID/GID `1000:1000`。
- 第一筆 dispatcher IP／trace／摘要 SHA-256：
  `b253b829b4a44093c6900b42b12d6c63fefd03ab718114671eaaa6b1f91cb6ec`／
  `12dbce0f66ff977c829fd01dc33c008bd77eea58a1f244bde4202dc67eb1e783`／
  `962fcd30ca95e09cf9f003276302f45b68bbc667b189e63f55acb9544f4afc7a`。
- `Create New Character` 來源 dump SHA-256：
  `c6d61ad2b10fd31e35229beb0f2649ddae564654dcbd51c0d8b6730805ec8c2b`。
- 末字 glyph 寫入 log SHA-256：
  `5dd7e0a7a7188ee9ed9cf0536078b15ed83547dd1733df1b28864b95230e7728`。
- 九筆 entry／return 暫存器 log SHA-256：
  `a49b94a281c973a0ee054017ef4ec6baacf03d8cc65c6705115e61286d7e65d5`。
- caller runtime dump SHA-256：
  `1262aafe7d11e0193f9684a1d07b6ff3f36382cddafcafd28b62bc0a4890465a`。
- IDA caller-tail JSON／database SHA-256：
  `898c6af91a96d17ff41b3e71e6788f2c1aa8df05b081ad659c70b2d19128b995`／
  `85ee9d465d79faca8c058761b8fa4a5f4937dd42790981966634d18df2917505`。
- IDA dispatcher-tail JSON／database SHA-256：
  `2d2147803ea271cd70255984f124606afe4070a95256c3bfcf2d09cd3adea806`／
  `02d80b8494b7f35f8c646107e4b41cff3607a01d6b9bfe42dc84d66e853f78b1`。

## 第一筆已知字串的 entry 與 post-call

第一筆 `0763:0424` 在 #100,010,490 進入。當時 `ES:DI=1841:3CE9` 不是本次來源；真正的
far pointer 由 stack 參數給出 `1841:3CD4`。同一步傾印的 21 bytes 為：

```text
14 43 72 65 61 74 65 20 4E 65 77 20 43 68 61 72 61 63 74 65 72
```

即長度 `0x14` 與 ASCII `Create New Character`。其背景／前景為 `0x00`／`0x0A`，
row 12、column 9；最後一個 `r` 位於 `(x=224..231, y=96..103)`。

對該 8×8 格的逐筆 VRAM watch 得到恰好 64 個不同位址、每址一次寫入：第一筆
#100,025,234，最後一筆 #100,025,833，最後位址 `A000:81A7`，寫入指令為
`0763:184E`。dispatcher 直到 #100,025,943 才返回 `37F1:1856`。因此 post-call
比末端 glyph 的最後像素晚 110 道指令，足以證實這個事件看見的是完整英文繪製結果，
而不是只進入 dispatcher 或只畫完前幾個字元。

繪製前 raw VRAM SHA-256 為功能選單基線
`b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`；post-call 為
`b9a775bfce0b3dda6507a9a0c1f0187523f481a5b1110ec06bb45ec914436f4c`。這兩份 64,000-byte
raw VRAM 僅作本機收據，不進 Git。

## caller 與 stack 護欄

IDA 9.4 對 runtime `37F1:1851` 的固定 bytes 得到：

```text
37F1:1851  9A 24 04 63 07  call far ptr 0763:0424
37F1:1856  89 EC           mov sp,bp
37F1:1858  5D              pop bp
37F1:1859  CA 04 00        retf 4
```

dispatcher 自身尾端為：

```text
0763:04AD  89 EC           mov sp,bp
0763:04AF  5D              pop bp
0763:04B0  CA 0C 00        retf 0Ch
```

第一筆 entry 的 `SS:SP=1841:3CC4`，post-call 為 `1841:3CD4`，正好增加
`4 + 0x0C = 0x10` bytes。完整 Enter 畫面的九筆 dispatcher 亦全部符合相同關係；四種
動態 return 位址為 `37F1:1856`、`158C`、`15BD`、`175D`。

只在 return 位址掛無條件 hook **不安全**：`37F1:15BD` 在 #100,040,267 因正常 fall-through
自然執行一次，但第一筆真正以它為 return address 的 dispatcher 到 #100,059,989 才進入，
#100,066,316 才返回。故 `CS:IP == return` 本身不證明剛完成文字繪製。

## generation 時間線

Enter 向前路徑的已證實順序如下：

| 指令序號 | 事件 | generation 含意 |
| ---: | --- | --- |
| #100,010,174 | 原版取走 Enter。 | 玩家輸入已接受。 |
| #100,010,490 | `Create New Character` dispatcher entry。 | 舊功能選單最後一次重畫開始。 |
| #100,025,833 | 最後一個 `r` glyph 的最後像素寫完。 | 原版英文內容已完整落入 VRAM。 |
| #100,025,943 | post-call `37F1:1856`。 | 可在此覆繪這筆舊 generation 文字。 |
| #100,028,739 | `026F:029C` 矩形清除 entry。 | 立即使相交 overlay 失效；矩形為 `x=8..311,y=16..183`。 |
| #100,032,996 | `026F:0506 RETF 8`。 | 原版矩形清除完成。 |
| #100,032,997 | caller `37F1:1501`。 | 清除 post-call。 |
| #100,033,190 | 下一筆 `0763:0424` entry。 | 新畫面的第一筆已觀測文字開始。 |
| #100,040,266 | 該筆 dispatcher post-call `37F1:158C`。 | 新 generation 第一筆文字可覆繪。 |

這條序列證實轉場不是原子 repaint：輸入後先重畫舊選項，之後才清除矩形，再建立新畫面。
正確策略不是「看到任何新 dispatcher 就換 generation」，而是矩形清除使相交 overlay 失效，
其後每筆 dispatcher 在自己的 post-call 重建中文。

## dosgolem API 判定與 DRAFT 契約

現有 `oracle.OnCall` 的實作契約是「`CS:IP` 走到地址時、該道指令執行前觸發」，並不限制
該地址必須是 call entry；公開 API 另有 `Caller()`、`Regs()`、`Steps()` 與記憶體讀取。
因此本階段**沒有證實需要新增通用 dosgolem post-call API**。DRAFT 的 adapter-side 方法是：

1. 在 `0763:0424` entry 立即複製原文 bytes、顏色、row／column，並以 `Caller()`、entry
   `SS:SP` 建立 pending frame。
2. 每個新見 return address 只註冊一次 `OnCall`；該地址命中時，只有 pending frame 的
   return address、`SS` 與 `SP == entry SP + 0x10` 全部相符才送出 post-call 文字事件。
3. 無 pending frame 的自然 fall-through（已證實的 `37F1:15BD` 案例）必須忽略。
4. `026F:029C` entry 依已證實矩形立即使相交 overlay 失效；原版清除仍完整執行。

這是**證據支持的 DRAFT 設計**，尚未經 adapter prototype 與 A/B 像素測試，不能升為
READY／CONFORMED。未來若遇到 reentrant dispatcher、不同 `RETF` immediate、stack unwind
或非 far-call 入口，必須回到證據層，不能把 `+0x10` 外推成通用 dosgolem 規則。

## 下一個最小缺口

事件生命週期已足以開始一個可丟棄的功能選單繁中覆繪 prototype。下一階段應先建立首批
可版本控制的繁中譯文、可追溯字型候選與 text-safe rectangle，然後在上述 guarded post-call
與矩形失效順序上做英文／繁中 A/B 像素收據。手冊題目、劇情、戰鬥、捲動、存讀檔及其他
dispatcher／文字路徑仍未涵蓋，不能因功能選單成功就宣稱整體中文化。
