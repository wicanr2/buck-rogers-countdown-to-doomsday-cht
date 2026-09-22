# 第一百五十六階段：第七頁正式 runtime 雙倍率同狀態 A/B

日期：2026-09-23  
狀態：**正常六行與同程序 Enter 離頁驗收通過；雙倍率失敗矩陣未通過前，規格 016 仍為 READY。**

## 固定輸入、工具與權利

從合法第六頁私有終態
`workplace/phase123-story-page6-enter/page6.state`（SHA-256
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`）
開始。穩定第七頁組於 step `331000000` 排正常 BIOS Enter、停止於
`340000000`；同程序離頁組再於 step `341000000` 排第二筆 Enter、停止於
`350000000`。control／2×／3×使用完全相同 state 與排程。
原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
原版與字型唯讀掛載；狀態、PNG、RGBA 與完整收據只在 ignored
`workplace/page7-runtime-evidence/`，不得進 Git／GitHub／公開包。

使用本機 dosgolem branch `buck-rogers-cht-output-overlay` HEAD
`d42567de27da30b003584a777c63a5f91e8e39d6`，Go 1.26.7／
`golang:1.26.7-bookworm` 無網路、有界 Docker；正式
`cmd/buckrogers-text-receipt` binary SHA-256
`7427f60810481fbb291d093181c9983acd449d286c4fd580cc98b6a8a3c69501`。
本機倚天 GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。
正規化 `cmd/state-compare` binary SHA-256
`ef392757aa409317f08f8a8d206df38a45dbf8fdab35e3ce6ad53e55c287820a`。

## 穩定第七頁

`stable-{control,2x,3x}.json` SHA-256 依序為
`086167d804da41a33a1b5d37b30e2f95021c92372dab041ab6d2fb08ada0d9c0`、
`8a9bda7b0c5b06b6345a474e4cef2dc6a023240ffaac196e0d4ae28c6dc47ef8`、
`e83d8025e534387f40b8bd603ebfe77662ce9e99d1dcc5499c23f090b082109f`。
2×／3×均啟用六個 `story.page7.line.001`–`.006` key，缺字零、
`drew=true`；邏輯安全矩形外差異零，矩形內分別 11,987／26,319
像素差。兩張 PNG 已抽看：六行繁中可讀，未侵入右側人物資訊或
row 24。2×／3×的原版記憶體、indexed framebuffer、palette digest
均與 control 相同。`state-compare` 對兩倍率均 `equal=true`，
machine SHA-256
`ef146aed0a78772b7471f9c476aa22be0235225f6b285c3e253dfc79e51aae65`、
DOS SHA-256
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。

## 同程序 Enter 離頁

`twoenter-{control,2x,3x}.json` SHA-256 依序為
`7ce892fad1ae797afb41c0afce1562bb7c603e5bf076f94a53fb61302046e477`、
`fe79a6e34ad0724b4b591c35f5d0776777dd02f1492b9b1a6c5ebb4bfeedfbde`、
`fc70bc7c5f6ad98b69132ff717e35cf2f799dc7c0cc0058d688955ddd759d04f`。
兩倍率在 step `341018656`、原版 pre-execution
`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304` 各記一筆
`active_keys_before=6` 失效。終態 active=[]、`drew=false`、
缺字零、安全矩形內外差異均零；2×／3×各自 RGBA 與 baseline
逐 byte 相同。這是**同一程序先啟用再清除**的證據；另外從第七頁
savestate 新開的 `exit-*` 收據只會由 inactive 開始，不能替代本組。

兩倍率原版記憶體、indexed framebuffer、palette digest 與 control
相同；`state-compare` 均 `equal=true`，machine SHA-256
`07f1729a494618dc2e8856008f389666f9b44464a4d97f77292c0bf996fd2c63`，
DOS SHA-256 同上。以 `-file-ops` 重跑兩筆 Enter，control／2×／3×
收據逐 byte 等於未加旗標的上述各份收據；三者均無額外 file-op
欄位或操作。BIOS 排程均為同一兩筆 `331000000`／`341000000` Enter。

## 不外推的停止線

這些正例已證實原版狀態不受覆繪影響及已量離頁無殘字，但
[規格 016](../spec/016-story-page7-overlay-ready.md)要求正式 2×／3×
各自完整失敗即關閉矩陣。獨立程式稽核已確認 loader／step 來源、
discontinuity 舊事件及同程序 lifecycle 問題已修；完整雙倍率
catalog／字型、group、ABI、return／stack／step、write／restore 到
presenter 的零 stamp／零 draw 對照仍待驗。故本階段不能升
CONFORMED，也不能外推完整開機、其他離頁、遊戲內存讀檔或全遊戲中文化。
