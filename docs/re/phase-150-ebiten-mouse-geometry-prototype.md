# 第一百五十階段：真實 Ebitengine 滑鼠四角與排除邊界

日期：2026-09-23
狀態：**可丟棄的幾何原型證據；MouseBridge 與 Linux 玩家前端仍為 DRAFT。**

## 範圍與工具

Terra 在 ignored `workplace/phase118-game-ebiten-active-story/` 將原型擴成
資料驅動的 2×／3×四角與控制列／右／下排除邊界真實 X11 事件。
每格使用私有 `phase12-before-question.state` SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`，
原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
使用 `eob-remake-go:1.26.7-ebiten2.9.9`、Go 1.26.7、Ebitengine 2.9.9、
Xvfb，於有界、無網路、一次性 Docker 內執行；原型 `go test -race -count=1 ./...`
通過。收據中 `dosgolem_commit=b4e1fb7…` 是舊 harness 寫死欄位，**不能**
當本次原型 source 身分證明。未更動正式 dosgolem 程式。

為了讓真實 Ebitengine 可送出畫布 exclusive right／bottom 邊界事件，
此 ignored 原型暫加 1 個 logical pixel 的觀測 guard；它不屬 DOS 畫布、
正式視窗版面或已批准的產品幾何。正式實作不可默默照搬。

## 雙倍率實體事件結果

下表每格收據位於 ignored
`workplace/phase118-game-ebiten-active-story/out/phase149-geometry-<倍率>-<格>/mouse-receipt.json`。
SHA-256 只識別本機私有收據，收據與原版畫面不得加入 Git 或公開包。

| 格 | 2× SHA-256 | 3× SHA-256 | DOS 結果 |
| --- | --- | --- | --- |
| 左上 `tl` | `0f332229ada426115e7609cdcd71dc39d53261b76e94914f2c678fc8527e9667` | `47250473740bf1edc0356f7a46c67ad46b21dee1f93bcfad239abdb9eb1446e3` | `(0,0)` |
| 右上 `tr` | `6d2ca32576874aafe13150e4ca158507496fc672e040eaa7358a3b1010193df4` | `ae0c94f9881245c6bd33a1bd9f14f261e925610da94bf49f05478d6df4c39935` | `(319,0)` |
| 左下 `bl` | `98e63e4dc7a87c54e0f85bb25c1515e650d887dc949e990f5dc10f535d38f9ac` | `c26f84fb7a5c4e1b9308296d82d4e5cbd4bf7f4db4051b92964753cf2b0f3ed1` | `(0,199)` |
| 右下 `br` | `49e414d45c952b48e6d4f1b64ad52debf069b68bf765edbf45f751060967813d` | `74b7e702877c67e4f3d17d8c03cfd4cc0c9432aed80c3047d9eeb461c72a4909` | `(319,199)` |
| 控制列 `chrome` | `da3194e00249addf5fbe63b8e3ec5b9fdf0555f6ae3a187d8fc3a4cae26a8014` | `e64e9038d49767ad6133d84244c917dfc300f0995b608fe88c58b66820fdc460` | 零 DOS API |
| 右邊界 `right` | `3822c55533188e06ba0cae23f4d288675f660bf26fff1f0922562dcb09592c18` | `72c37d381cdaf399ad5ba82c198a5efeb1bd51a79c0f2eee60d5ede27f0398b2` | 零 DOS API |
| 下邊界 `bottom` | `d76184b04730859c241603e02caf4eae5d8e6a71462c358be19fbddcff788040` | `177c2577033b7ce2e4ffe2d34674319b9595a3c07c36cfb281398da2e07d6b52` | 零 DOS API |

四角的實體 Ebitengine logical Down／Up 在 2×為 `(0,36)` 至
`(639,435)`，3×為 `(0,54)` 至 `(959,653)`；各自按倍率整數換算
到上表 DOS 座標，API 均為 `Move→Press→Move→Release`，button 0→1→0。
控制列與右／下 exclusive 邊界均不建立 DOS 按鍵，DOS mouse 保持
`(160,100)`／button 0。各格輸入 API 邊界的 BIOS pending、Key IRQ
均為零；indexed framebuffer 在 API 邊界不被橋接改寫。
四角 mouse state 改變造成 memory hash 變化是預期，後續有界 Step 的畫面
變化不得直接歸因於滑鼠事件。本次是幾何與輸入路由證據，不是玩家可用
滑鼠完成遊戲功能的驗收。

## 尚缺的 READY 前沿

已接受 Down 後在畫布外、控制列、開面板或失焦的 release-only cleanup
尚未形成完整雙倍率矩陣；3×孤兒／重複 Up、正式面板空白 miss 消費契約、
正常玩家操作後繼續遊玩與存讀檔也仍缺。專案 spec 004 與本機 dosgolem
spec 228 均維持 DRAFT，不得把此 ignored guard 或 harness 當正式前端。
