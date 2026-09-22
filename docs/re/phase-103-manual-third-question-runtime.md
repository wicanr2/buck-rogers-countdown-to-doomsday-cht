# 第一百零三階段：第三題手冊覆繪執行期抽樣

日期：2026-09-22  
狀態：**已確認一條新增題目的固定狀態抽樣；未完成 39 題的玩家路徑驗收。**

## 範圍與固定條件

本階段從既有正常玩家路徑產生的本機狀態
`workplace/probe/phase12-before-question.state` 重播。它不寫入原版 EXE、資料檔、
答案、輸入判定、VRAM 或存檔；錯答 `x` 與 Enter 仍由原版接收並自行重抽題目。

- 初始 state SHA-256：
  `8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`
- 指令步數：`266399999` → `304000000`。
- BIOS 鍵排程：`300100000:2d:78`、`301100000:1c:0d`、
  `302000000:2d:78`、`303000000:1c:0d`。
- 本輪未另行設定或辨識 RNG seed；可重播條件是上述完整原版 state 與固定鍵排程，
  不以同名 seed 宣稱跨實作亂數一致。這是輸出覆繪的同狀態抽樣，不是
  `RND()` 規則或跨實作亂數對拍的正式種子收據。
- 字庫是本機倚天 top-pad 產物，961 glyph，SHA-256
  `7e8f5d0e70cc75505279de0575b3bcc489c0b0901ddc3c39c179124c9e544b18`。
  原始字型、字庫 bytes、原版檔、完整 state 與 PNG 都只留在被忽略的 `workplace/`。

## 已確認結果

原版在第二次錯答後，於 dosgolem 實模式位址 `2A33:0309` 的 guarded post-call
（指令步 `303101761`）完成第三個題目。其 exact identity 是
`manual.page36.acidic_victory.word7`，顯示鍵
`manual.log.57.acidic_victory`。這是第一個既有 #32 `Deimos Prison` 與 #38
`Technical Skills` 以外，實際由本固定原版狀態重抽並顯示繁中的題目。

| 倍率 | 核准正文內變更 | 正文外變更 | 完整原版狀態 | 可見／缺字 |
| --- | ---: | ---: | --- | --- |
| 2× | 6,249 像素 | 0 | 等於無覆繪控制組 | 可見／0 |
| 3× | 12,115 像素 | 0 | 等於無覆繪控制組 | 可見／0 |

2×／3× 的原始 indexed framebuffer 與控制組相等；完整持久化狀態由
`state-compare` 解碼正規化後比較。收據目錄為
`workplace/phase100-third-question-961/`，其中的 `verification.json` 保存輸入、
字庫、像素與狀態比較摘要。

## 可重播入口

以下命令必須在一次性、無網路 Docker 容器內執行；`/orig` 是只讀的使用者原版目錄，
輸出目錄必須尚不存在。

```sh
python3 tools/manual_runtime_smoke.py \
  --command workplace/dosgolem/workplace/out/buckrogers-text-receipt \
  --state-compare workplace/dosgolem/workplace/out/state-compare \
  --state workplace/probe/phase12-before-question.state \
  --font workplace/phase101-font/buckrogers-eten-top-pad.golemfnt \
  --out-dir workplace/phase103-third-question-rerun \
  --until 304000000 \
  --bios-key-at 300100000:2d:78 \
  --bios-key-at 301100000:1c:0d \
  --bios-key-at 302000000:2d:78 \
  --bios-key-at 303000000:1c:0d \
  --expect visible
```

本輪亦修正本機 dosgolem 分支的收據命令：未明示操作列 catalog 的純手冊收據，
不再因無關、未設定 watcher 的 pending 狀態遭拒；若操作列 catalog 被啟用，原有的
失敗即關閉終態檢查仍完整適用。修正提交為本機
`640f91847ea945df5cd0a19b3b9f1452c68d2016`，未推送。兩種操作列
catalog 同時設定時，請求型 watcher 仍優先；正反測試與 Docker race／vet／建置通過。

## 抽樣邊界

本固定 state 已實際覆蓋 #32、#38、#36 三題；其中 #36 是本階段新增的動態題目。
載入第三題終態後，DOS 狀態已結束，無法在同一份固定 state 再送入下一輪答案，
因此不能把它當作無限題庫搜尋器。#3 `More on Abilities` 與 #39 `Roll.` 尚未在
執行期命中，不得稱為 runtime 已驗收。

這份收據也不驗收遊戲內返回、存檔／讀檔後清除、所有其他題目，或互動式 host 前端；
它只證明已量測的 #36 輸出端覆繪不影響原版行為，且變更侷限於核准正文矩形。
