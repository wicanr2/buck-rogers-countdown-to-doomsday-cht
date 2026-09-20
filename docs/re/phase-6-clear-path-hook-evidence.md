# 第六階段：清除路徑與失效 hook 證據

日期：2026-09-20  
狀態：已證實底層 byte-fill 與上層矩形清除例程；正式覆繪仍維持 DRAFT。

## 問題與輸入

第四、第五階段的 dosgolem watchpoint 都把舊文字像素清除記在 `0CF4:1B3C`。本階段要回答：

1. 該位置是單一像素、矩形 primitive，還是可直接代表畫面 generation 的上層事件？
2. Enter 向前與 Escape 返回實際清除哪些像素矩形？
3. 哪一層才適合作為遊戲 adapter 的 overlay invalidation 候選？

原版輸入雜湊沿用[第一階段清冊](phase-1-input-and-startup.md)，dosgolem 使用
`workplace/dosgolem/` 的 `buck-rogers-cht-output-overlay` 分支，基準 commit：
`d9c0c27ca9af8239c7e96272a7165e03d7da04bf`。所有下列地址都是 dosgolem 執行期
實模式 `segment:offset`；IDA 對 raw segment dump 建立的 database EA 另列，不與它混用。

## 工具與可回查產物

- dosgolem 執行 image：`golang:1.24-bookworm`，image ID
  `sha256:1a6d4452c65dea36aac2e2d606b01b4a029ec90cc1ae53890540ce6173ea77ac`。
- 主要靜態工具：IDA Pro 9.4，`ida-pro-9.4-idapython:locked-v1`，image ID
  `sha256:6f6d59af49d0008c4109a5295b5f374bdc007e2d1ab28cb9de08779584de2780`。
- 交叉驗證：GNU objdump 2.40，`gcc:13-bookworm`，image ID
  `sha256:3617a214e52a25bde5375dc9503b5e67f01b6c7322a30137e2790aa8e6db5d1f`。
- `0CF4:1800` 的 1,024-byte runtime dump SHA-256：
  `28e85f17dec2ef204746660ee11858503c895b81279fcba9fee636c0c96d3fe6`。
- `026F:0000` 的 1,536-byte runtime dump SHA-256：
  `8f26fa2bfd6655776f330b10ba3a04556c35b0643500e0b78c3b33674fb461eb`。
- IDA byte-fill database／JSON SHA-256：
  `78d80aad5801b35ca9debb8e71aae127e55a151f0aa805c56eb5556a9057b3fb`／
  `fd4b17022e48021bea8aa9f5af9b3ac081ad3f7758261c39bcefe42edf435402`。
- IDA rectangle database／JSON SHA-256：
  `d91c2f9abdc29c0d8ba414101f3e11f676b9cdcaefdd6f8de91136a5a8f0ab64`／
  `f3d6962b80c633235484759ed3a1bcc44121fcd5864bdb99f3b22bd6815fc9aa`。

IDA 兩份一次性資料庫均為 16-bit `pc` processor、UID/GID `1000:1000`。byte-fill raw 檔的
IDA database EA／file offset `0x032B` 對應 runtime offset `0x1B2B`，再配 runtime segment
`0CF4`；rectangle raw 檔從 offset 0 傾印，所以 database EA `0x029C` 對應 runtime
`026F:029C`。資料庫只保留自動名稱與原始定位，沒有用推測性名稱取代地址。

## `0CF4:1B3C` watchpoint 勘誤

IDA 與 objdump 對固定 bytes 得到相同指令邊界：

```text
0CF4:1B2B  8B DC           mov bx,sp
0CF4:1B2D  36 C4 7F 08     les di,ss:[bx+08]
0CF4:1B31  36 8B 4F 06     mov cx,ss:[bx+06]
0CF4:1B35  36 8A 47 04     mov al,ss:[bx+04]
0CF4:1B39  FC              cld
0CF4:1B3A  F3 AA           rep stosb
0CF4:1B3C  CA 08 00        retf 8
```

因此先前 watchpoint 的 `ip=0CF4:1B3C` 是 dosgolem 在 `REP STOSB` 完成後記錄的下一個 IP；
實際寫入指令是 `0CF4:1B3A`。函式範圍為 `[0CF4:1B2B, 0CF4:1B3F)`，輸入是填充值低 byte、
長度 word、目的 far pointer。這是**已證實的通用 byte-fill primitive**，不是畫面 generation
或上層清除事件；不得直接拿它作 overlay invalidation hook。

## 上層矩形清除例程

IDA 的 raw database `[0x029C,0x0509)` 對應 runtime `[026F:029C,026F:0509)`。函式在
`026F:029C` 建立 stack frame，依 `DS:3C78` 分派顯示模式；本作目前 Mode 13h 路徑取值 3，
進入 `026F:047D`。四個參數只讀各 word 的低 byte：

```text
[BP+06] bottom_row
[BP+08] right_column
[BP+0A] top_row
[BP+0C] left_column
```

Mode 13h 的已證實公式為：

```text
x0     = left_column * 8
y0     = top_row * 8
width  = (right_column - left_column + 1) * 8
y_last = (bottom_row + 1) * 8 - 1
offset = y * 320 + x0
```

`026F:04EC` 以 bytes `9A 2B 1B F4 0C` far-call `0CF4:1B2B`，每列填值為 0；
`026F:04F1` 將 offset 加 `0x0140`，`026F:0506` 以 `RETF 8` 返回。靜態公式、IDA bytes、
dosgolem IP trace、caller 暫存器與實際 VRAM 寫入互相一致，故矩形語意為已證實。

## 兩條正常路徑的動態範圍

| 路徑 | `026F:029C` 低-byte 參數 | 動態 fill | 已證實像素矩形 |
| --- | --- | --- | --- |
| 功能選單 Enter → `PICK RACE` | bottom=22, right=38, top=2, left=1 | `026F:04F1` 168 次；每次 304 bytes；首 offset `0x1408`，末 offset `0xE4C8` | `x=8..311`、`y=16..183` |
| `PICK RACE` Escape → 功能選單 | bottom=22, right=38, top=0, left=0；由 `026F:00D8` 包裝呼叫 | 184 次；每次 312 bytes；首 offset `0x0000`，末 offset `0xE4C0` | `x=0..311`、`y=0..183` |

Enter 的觀測窗共有 169 次 `0CF4:1B2B`：其中 168 次來自 `026F:04F1`，另 1 次來自
`37F1:14DC`，已分開計數，沒有把無關填充混入矩形列數。Escape 的矩形窗恰為 184 次。

## hook 判定與 DRAFT 邊界

結論如下：

- `0CF4:1B2B`／實際寫入指令 `0CF4:1B3A`：**已排除**為正式 invalidation hook，因為它只是
  可寫任意 far memory 的底層 byte-fill，沒有玩家畫面 generation 語意。
- `026F:029C`：**已證實的矩形清除事件，為失效 hook 候選**。對固定原版雜湊、runtime
  bytes 簽章與 `DS:3C78 == 3`，adapter 可從四個低-byte 參數計算半開區間矩形，讓相交的
  overlay 失效；原版函式仍須完整執行。
- `026F:00D8`：只在 Escape 返回樣本中包裝固定大矩形，Enter 路徑不經過它，故不是兩條
  路徑共用 hook。

這仍不足以把整份覆繪規格升為 READY。下一個最小缺口是證實 `0763:0424` **完成原版繪製後**
可用的 return／post-call 事件，並定義「矩形清除使既有 overlay 失效、之後新 dispatcher
事件屬於新 generation」的順序。中文字型、正式 catalog、text-safe rectangle 與 A/B 像素
驗證亦尚未完成。

## 失敗與更正紀錄

- 第一次全 VRAM watch 主控台輸出很大；權威集合改以 `watch-file`、IP binary trace、caller
  計數與暫存器收據，不用截斷畫面輸出支持結論。
- IDA `fill` v1／v2 因舊 API 與 raw loader 非零基址未產出合格 JSON／`.i64`；v3 解碼成功但
  未保存 DB，v4 保存 DB 後仍用了錯誤退出 API。v5 才同時通過 schema、版本、雜湊、16-bit、
  無 traceback 與非 root 擁有權，前幾版不得作證據。
- rectangle v1 的 end-exclusive `0x0507` 落在三位元組 `RETF 8` 中間；v2 改為
  `[0x029C,0x0509)` 並重建驗證。正式結論只引用 v2。

所有 raw dump、trace、JSON、`.i64` 與失敗產物都留在被忽略的 `workplace/`；Git 只保存
不可還原原版內容的地址、少量定位 bytes、雜湊、公式與結論。
