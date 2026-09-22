# 第一百五十五階段：第八頁逐字返回與離頁 pre-write 證據

日期：2026-09-23  
狀態：**原版 READY 前證據補強；第八頁仍為 DRAFT，不授權正式覆繪。**

## 輸入、工具與權利

entry 從合法第七頁私有終態 `workplace/page7-next-trace/page7.state`
（SHA-256 `e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`）
於 step `341000000` 送正常 BIOS Enter，至 `350000000`。exit 從合法
`workplace/page8-next-trace/page8-a.state`（SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`）
於 step `351000000` 送 Enter，
至 `360000000`。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
位址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址。

使用本機 dosgolem HEAD `d42567de27da30b003584a777c63a5f91e8e39d6`、
Go 1.26.7，在無網路、有界 Docker 內建置 `cmd/buckrogers-text-receipt`；
runner SHA-256
`8d2b62cebaa38857b0a263c65103467746f853a268ca651febfeccf7af86fa7e`。
前一次嘗試碰上另一代理尚未提交的第七頁 CLI 中間態，缺少
`StoryPage7Watcher.Generation()` 而無法編譯，沒有有效收據；待完整
CLI 原子提交後以本段精確 HEAD 乾淨重跑，未將暫時的編譯失敗當成
第八頁產品缺陷。原版 state、完整事件與畫面只在 ignored `workplace/`，
不得進 Git／GitHub／公開封包。

## 雙重原版收據

`workplace/page8-ready-atomic-core/entry-{a,b}.json` 逐 byte 相同，
SHA-256 `64a8b4ce555562e4a57e3f0429ffc64d9a39e558f5eef667db9267cd54846779`。
第八頁 row 17–20 四行長度 `38/37/33/22`、共 130 glyph；130/130 筆
均為 `0763:03D6`、RETF opcode `0xCA`、返回 `0763:04FF`、同 SS
`1841`、`SP:3D66→3D78`（相對 `+0x12`）、七 ABI word 高位遮罩 0，
mode/repeat `1/1`、背景／前景 `0/10`，column 連續。原文 length／SHA
與 `text/story-page8-events.tsv` 一致；這是原版控制流證據，不是中文畫面。

`workplace/page8-ready-atomic-core/exit-{a,b}.json` 逐 byte 相同，
SHA-256 `366ce7212188c93ea3bc1ecc84bd548cf3bc874e008ada0f0952dba99b3f1164`。
對 row 17–20 候選區，合法 page8→page9 Enter 的最早相交
pre-execution fill 位於 step `351154334`、`0CF4:1B3A`、
`ES:DI=A000:AA08`、`CX=304`，即 row 136、x=8 起；早於
[第一百三十一階段](phase-131-story-page8-enter-trace.md)所記首筆
執行後可見像素寫入 step `351154358`。後者不能冒充最早 pre-write。

## READY 前剩餘停止線

第八頁安全矩形尚未經獨立正式審查；需以正式譯文與本機倚天
GOLEMFNT 驗 2× 16×16、3× 24×24 cell／22×22 ink 的真實墨跡
containment、缺字與右側動態欄排除。另須可丟棄 typed-core 驗證
四行原子、七 ABI 高／低位映射、RETF／stack／step、partial／錯序／
duplicate、未知／不相交／相交 write、restore／discontinuity 等失敗
即關閉邊界；正式 catalog 目前仍為 DRAFT。完成獨立審查後才可
考慮限縮升 READY；正式 runtime、control／2×／3×同狀態 A/B、
離頁無殘字、正常玩家路徑及存讀檔尚未驗，不能稱已中文化。
