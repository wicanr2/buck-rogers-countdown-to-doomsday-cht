# 第三十六階段：性別選擇生命週期收據

## 結論

從既有 #99,999,999 固定 state 以兩次正常 BIOS Enter 進入性別選擇後，Down 會先把男性列
以 normal style 重畫，再以 selected style 重畫女性列；Up 以相反順序回到男性列。按 Escape
時，原版先把男性列恢復 normal，接著重建上一層功能選單，並非返回種族選單。

兩條路徑各自完整重播兩次；JSON 與 64,000-byte indexed framebuffer 均逐 byte 相同。
這證實性別選擇的移動與返回生命週期，不外推 Enter 確認性別後的下一畫面。

## 固定輸入與工具

- state：`workplace/probe/after-bios-space-100m.state`，SHA-256
  `cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。
- `START.EXE`／`GAME.OVR` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`／
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- `cmd/buckrogers-text-receipt/main.go` SHA-256：
  `8ce3a79a791659f72f4fa4190274155462ce701431bf11c8d7da7ee8ae291506`。
- dosgolem spec 017 已達 CONFORMED；本機分支 commit：
  `57daa16fd3ab38ff19b8b1702fecf5b0ca14992d`，未推送 dosgolem 遠端。

所有 caller 都採 dosgolem runtime `segment:offset`。原版完整文字不進 Git；正式清冊只保存
長度、SHA-256、caller、色號、座標與語意角色。

## Down→Up 時間線

- #100,400,000：排入 Down。
- #100,400,478 → #100,403,733：男性列 normal 重畫，`37F1:1856`。
- #100,404,132 → #100,408,910：女性列 selected 重畫，`37F1:175D`。
- #100,460,000：排入 Up。
- #100,460,432 → #100,465,210：女性列 normal 重畫，`37F1:1856`。
- #100,465,577 → #100,468,832：男性列 selected 重畫，`37F1:175D`。

女性 selected／normal identity 的長度均為 6，原文 SHA-256 均為
`e8cca808ae5aaa03a7fc3060856e6d4ad776fb1cb8cfe441a9bd240988cde151`；只有 caller 與
bg/fg 分別為 `15/0`、`0/10`。這將第 35 階段的「可能沿用種族選單兩格縮排」由強推論
升為已證實。

Down→Up JSON SHA-256 為
`e5d58d61cc74cb464343692355f68d5f4d54f3ecdd0f57f6e832f6d2de8cbd52`；終點 framebuffer
SHA-256 為 `dcf947d18c85b051ec85e1bc968f30cec5c315a9158d598055d14ebfe82a715c`，等於第 35
階段未移動終點，證實 Up 後逐位元回到第一列狀態。

## Escape 返回時間線

- #100,400,000：排入 Escape。
- #100,400,428 → #100,403,683：男性列先以 normal style 重畫。
- #100,505,151 起：功能選單五列依序以 normal style 重建。
- #100,616,533 → #100,631,986：第一列以 selected style 重畫。
- #100,632,796 → #100,646,735：底列操作提示完成。

Escape JSON SHA-256 為
`333960a20c5699ece5430e93a1fd3f7b04f0b5bd02a45c39a5e1050a0e96198a`；終點 framebuffer
SHA-256 為 `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`。
`text/gender-selection-events.tsv` 保存 Down→Up 四筆及 Escape 八筆完整 identity；返回選單
中尚未納入繁中 catalog 的列只用語意位置鍵標識，不猜譯文。

## 驗證與邊界

- `tools/gender_selection_receipt.py` 固定輸入雜湊、兩條 BIOS 排程、14 筆共同前綴、12 筆
  生命週期 identity、精確 step、JSON 雜湊及 framebuffer 雜湊。
- 負向測試拒絕排程、identity、step、筆數、頂層 schema、BOM、重複鍵與缺列。
- 專案 50 項 Python 測試通過；真實雙重收據驗證通過。
- 本階段沒有新增翻譯、字型、renderer 或產品倍率；2×／3× 決策仍維持 pending。

下一個不依賴倍率的最小切片可量測 Enter 確認性別後的下一畫面；若要把性別選單接入正式
繁中覆繪，仍須先建立繁中 catalog、文字安全矩形及 READY 規格，不得由本收據直接猜補。

