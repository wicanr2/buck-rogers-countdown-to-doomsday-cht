# 第二百二十三階段：手冊首題實體視窗與中英混排 DRAFT

狀態：**DRAFT 視覺及接線原型**。本階段沒有修改正式譯文、字型、
手冊 presenter 或 Linux session；不代表冷開機直播、39 題逐題、
換題、存讀檔或玩家可用前端已驗收。

## 輸入與實驗邊界

- 首題原版終態 `control.state` SHA-256
  `2cdb2065a22591fb2909272611b66ee5f84fb211e30c9fe5c2769421f3b5ee22`；
  原版 `START.EXE` SHA-256
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。
  原版與已購倚天字型只在本機 ignored `workplace/`，唯讀掛載。
- 正式 `text/manual.zh-TW.tsv` 的首題 `manual.log.49.deimos_prison`
  目前為 73 字元，保留 `RAM`、`Deimos`、`Stockade` 的拉丁字母；
  對應原版手冊位置與 identity 仍依[規格 005](../spec/005-manual-runtime-presenter-draft.md)。
- 測試程式為 ignored
  `workplace/cold-boot-live-turn-proto/manual_owner_window_draft_test.go`
  SHA-256 `8e06dab9985b9a83d91273a38dc5f91835ba0a0c5898a16fc56091725145412a`，
  以及 ignored `workplace/dosgolem/apps/buckrogers/manual_ascii3_typography_draft_test.go`
  SHA-256 `6b92cbfad35f1e0b0dcc204a8a6b8e7b29f3b1c2c0a1c7ecb6cf1970468e7042`。
  工具是 dosgolem fork `cbd5683`、Go 1.26.7、Ebitengine 2.9.9，
  有界無網路 Docker／Xvfb。PNG 僅存 ignored `workplace/`，不入 Git。

## 真實視窗的限縮正收據

從已核實的 step 266557247 原版終態及 formal begin→clear→request
presentation queue，建立兩份正式 `ManualSnapshotOwner`，分別以 2×、3×
對同一個 indexed／palette 影格投影。正式 `frontend/ebiten.Game` 接收實體
X11 設定→暫選 3×→Apply；2×／3× 分別產生 39／15 次 snapshot，
每一張均逐 byte 等於既有正式原版收據的同倍率 RGBA。測試期間
`Machine.Steps` 保持 266557247、原版 indexed 全畫面不變。
私有視窗圖 `manual-first-question-3x-host.png` SHA-256
`5130bbfd4104583ecc52ef3ebf1c748db0084565ba54e4ae64315501a08047fa`。

這份測試的 `Advance` 故意是 no-op，只驗「已量原版終態→正式手冊
owner→實體 host 畫面」；不是從 cold boot 走到首題的直播 session。
字型與譯文只用於顯示，沒有進答案或 DOS 記憶體。

## 視覺觀測與 A／B／C／D 原型

實體圖初看像有英文殘字；核對 formal TSV 與原版清除 layer 後，
那些字母其實就是譯文內的 `RAM`、`Deimos`、`Stockade`。因此
**「原版英文未清掉」已被推翻**，不可把它當成清層故障。
真正問題是每個半形拉丁字母在 3× 仍佔 24px cell，詞被拉長，
`Deimos` 的括號還碰到固定 36-rune 行界。這是玩家可見的混排品質問題。

用同一首題、同一原版終態建立下列本機圖；正式程式與 TSV 均未變：

| 版 | 私有 PNG | 僅供判讀的改動 |
| --- | --- | --- |
| A | `manual-3x-A-current-ascii16.png` | 正式 3×：拉丁字模 16 點、字格 24px。 |
| B | `manual-3x-B-derived-ascii22.png` | 拉丁字模也最近鄰放大到 22 點，字格不變；A/B 差 865 像素，核准手冊正文矩形外零差。 |
| C | `manual-3x-C-chinese-names-mockup.png` | 只在測試記憶體把首題英文專名改為繁中排版示意，62 字元；**不是核定譯名**，未寫正式 catalog。 |
| D | `manual-3x-D-compact-latin-mockup.png` | 保留原譯文，單詞內試 18px 拉丁 advance；固定 row-major 分行及單詞後空白仍未解。 |

A／B 的 RGBA SHA-256 分別為
`c6e87ba6267ae12f99f7110c02328e0844c32946e7ad8a77cae70a6bb712206e`／
`96be22db1c850f6850e976c1104153a039f7cdfb5a37e95e98e08d3a28cc7e69`；
C／D 分別為
`97f4f2cd397d5c4d7e763bef120e1a651f7135dbb5191c624c98ac1d12ef17e3`／
`5aa777e6f99aa423651bb04ad741a1a71fab7cac8238f28a1e6d62bc79bfe338`。
這些都是同一原版影格上的測試繪製，不能將 C 的縮寫文字或 D 的
像素後處理直接搬入 production。後續是產品取捨：保留中文手冊的
英文專名並設計混排／詞界，或逐項核定繁中專名；已請使用者選擇，
決定前不改正式手冊段落。

PC-98／金盒繁中版面參考只支持將字模尺寸、字格 advance、行高分開
測量；原版行為及畫面仍以《拯救地球》DOS/dosgolem 為準。
