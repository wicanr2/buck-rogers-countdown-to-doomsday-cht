# 第三十九階段：職業選擇生命週期收據

## 結論

從既有 #99,999,999 固定 state 以三次正常 BIOS Enter 進入職業選擇後，Down 會先將第一列
恢復 normal，再以 selected 樣式重畫第二列；Up 依相反順序逐位元回到第一列初始狀態。
Escape 先取消第一列反白，接著重建上一層功能選單，而不是返回性別選擇。

兩條路徑各完整重播兩次，JSON 與 64,000-byte indexed framebuffer 均逐 byte 相同。這只
證實預設種族／性別下前兩個職業的移動及 Escape 返回，不外推其餘職業或 Enter 後畫面。

## 固定輸入

- state SHA-256：`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。
- `START.EXE`／`GAME.OVR` SHA-256：`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`／
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- receipt command SHA-256：`ed6e7b6537a9be3fe332f49821adee0d91c51a1f4510ca32648ed1b0f8fad5c9`。
- Enter：#100,010,000、#100,240,000、#100,400,000；方向鍵或 Escape 從 #100,650,000 開始；
  停止於 #102,000,000。

## Down→Up 時間線

- #100,650,515 → #100,659,121：第一職業 normal，`37F1:1856`。
- #100,659,520 → #100,663,533：第二職業 selected，`37F1:175D`。
- #100,720,463 → #100,724,476：第二職業 normal，`37F1:1856`。
- #100,724,843 → #100,733,449：第一職業 selected，`37F1:175D`。

JSON SHA-256 為 `650ad5b143c6a1382396289fcf9fc94105acd45f6fbc891bee3c6549d2876696`；終點
framebuffer SHA-256 為 `3a61cb542625bdb0fd353f1d337e87c68091bd2dd2185e9b2ba34dad7558012c`，
等於第三十八階段未移動終點。

## Escape 時間線

- #100,650,465 → #100,659,071：第一職業 normal。
- #100,760,834 起：功能選單五列、第一列 selected 與底列提示依序重建；最後事件在
  #100,902,418 完成。

JSON SHA-256 為 `653fc53dca4a971ba639f24c9f61cad79614b6718330367b5fdd395cd3bd6c51`；終點
framebuffer SHA-256 為 `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`，
等於既有功能選單返回基準。

## 驗證與邊界

- `text/class-selection-events.tsv` 保存 12 筆 content-safe identity，不保存英文全文。
- `tools/class_selection_receipt.py` 固定輸入雜湊、BIOS 排程、step、identity、JSON 與畫面雜湊；
  正反例測試拒絕 schema、筆數、次序、排程、step 與 identity 漂移。
- 專案 61 項 Python 測試與正式雙重收據通過。
- dosgolem 正式套件測試、`go vet` 與相關 race detector 通過；本機分支 commit 為
  `d8f34f101c719e6939565fe8b6f0d8b531e07ccc`，未推送 dosgolem 遠端。
- 本階段沒有新增譯文、字型、renderer 或產品倍率；2×／3× 決策仍 pending。
