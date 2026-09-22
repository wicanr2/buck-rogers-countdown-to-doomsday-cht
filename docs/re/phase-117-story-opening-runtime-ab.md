# 第一百一十七階段：首屏劇情 runtime 2×／3× A/B

日期：2026-09-22
狀態：首屏五行 runtime A/B 已重生並與 phase119 一併限縮 **CONFORMED**；範圍不含第二頁與其他生命週期。

## 範圍

本階段只驗證 READY 規格指定的首個固定五行故事畫面。輸出端 adapter 來自
dosgolem 本機提交 `42193b0`：它只在 `0763:03D6` 的 `RETF imm16`（opcode
`0xCA`）真正返回 `0763:04FF`，且 caller、SS、SP 與 entry step 都相符時，才把
glyph 交給 `StoryOpeningWatcher`。原版 indexed VRAM、CPU／DOS state、輸入與答案
判定均未被覆寫。

測試從 phase114 記錄的私有、合法手冊成功後 state
`workplace/probe/phase12-before-question.state` 開始；其 SHA-256 是
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`。
兩個倍率均由同一份私有有界 BIOS 排程重播。排程和答案只在被忽略的
`workplace/` receipt 內讀取，不寫入本文件、Git 或公開輸出。

## 同狀態 A/B 結果

2×、3×均以同一 input state、停止點與完整 BIOS 排程執行。兩份私有 receipt
逐項相等的 original-side terminal metadata 為：

- indexed framebuffer SHA-256：
  `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba`
- palette SHA-256：
  `fa97ee0c556490cc1c64f09cc0d9ead7b9836ff58c7c9ac965cd5e316757242c`
- READY event key：僅 `story.opening.line.001` 至
  `story.opening.line.005`，共五筆；沒有第二、三頁 key。

| 倍率 | active keys | 缺字 | safe rect 外差異 | safe rect 內差異／新增像素 | baseline RGBA SHA-256 | overlay RGBA SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| 2× | 5 | 0 | 0 | 10,616／10,616 | `edbbe358864dfca403cb6c0978a44b8c54c86b773781754b4bf2edd7f5b5db9d` | `35fcdbb0eb45cde3ec67db839ff165fc48cfdcfff2998e22104ec1f940666e91` |
| 3× | 5 | 0 | 0 | 23,019／23,019 | `7a101b0f1aa301d5e684b9b9bd3cca2d2e4024294208c45ec68e0f6841bb6544` | `bebcfb0e7508280966915deec66d8a58c1cd6332f764638d6afe399f64689960` |

差分允許區域是 READY contract 的 logical
`[8,320)×[136,176)`，依倍率放大。兩份 receipt 都確認這個區域外為零差異，且
區域內確有新增覆繪像素。私有 `overlay.png` 已人工檢視：2×與3×皆可讀出五行
繁中，字墨沒有離開下方故事框；PNG、GOLEMFNT、state、原版檔與完整 receipt
均不進 Git。

可重生的私有產物位於
`workplace/phase115-story-opening-ab/{2x,3x}/`；其中 `verification.json` 只保留上表
同類的 content-safe metadata，完整 receipt 仍含私有輸入而不得散布。

## phase160 固定 runner 複驗與限縮結論

本階段舊收據建立後，`9f4c5f0` 補齊首屏 strict catalog、restore／discontinuity 清除與完整
2×／3×失敗即關閉矩陣。固定該 runner 的 `phase160-story-opening-replay` 重跑 control／2×／3×；
2×／3× receipt SHA-256 仍分別為 `07e909f42d4fa0ef85217349651a30147a49eee555fef3d8372f1912c4931b98`、
`8e1d897fd7a6734b8628368f705928a4ce16a594adea43a8d05f09f51d8d909a`，並以 `state-compare`
確認 control↔兩倍率的 normalized machine／DOS 全等。raw `.state` bytes 含序列化差異，不是
machine／DOS parity 的比較依據。

## 可宣稱範圍與未驗項

可以宣稱：在既有合法手冊成功返回 state 的同一有界重播下，READY 首屏五行的
dosgolem runtime adapter 在 2×／3×都只於批准 rectangle 產生可讀繁中 RGBA 覆繪，
且未改變終態 indexed framebuffer 或 palette。

可宣稱本階段的固定五行 active A/B 已成為 spec010 CONFORMED 的一半 gate；另一半正常
Enter 離頁見 phase119。不得外推為第二頁中文化、其他離頁、完整開機或實際存讀檔；
restore／discontinuity 只有 fail-closed runtime matrix，沒有實際存讀檔玩家收據。
