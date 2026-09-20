# 第四十階段：職業選擇繁中執行期顯示請求

## 結論

第三十八、三十九階段的十個職業 exact identity 已接到 dosgolem 共用 catalog 與既有
guarded post-call watcher。正常三 Enter、Down→Up 與 Escape 三條路徑均能產生決定性的繁中
顯示請求；本階段仍未載入字型或改寫 framebuffer。

## 譯詞證據

中文說明書原圖 `SCAN0352_007.jpg` 至 `SCAN0352_009.jpg` 的「C.職業」章節明確並列中英文：

| runtime 語意 | 繁中譯詞 | 原圖位置 |
| --- | --- | --- |
| 職業選擇提示 | 選擇職業 | `SCAN0352_007.jpg`「C.職業」與介面動詞 |
| Rocket Jock | 太空船駕駛員 | `SCAN0352_008.jpg` 印刷頁 11 |
| Warrior | 戰士 | `SCAN0352_008.jpg` 印刷頁 12 |
| Medic | 醫生 | `SCAN0352_009.jpg` 印刷頁 14 |
| Engineer | 工程師 | `SCAN0352_009.jpg` 印刷頁 13 |
| Rogue | 流浪漢 | `SCAN0352_009.jpg` 印刷頁 14 |

`text/class-events.tsv` 保存十個完整 identity；`text/class.zh-TW.tsv` 保存六鍵譯文，來源全標為
`manual-and-runtime`。原文全文不進 Git。

## 實作與收據

- dosgolem `LoadClassCatalog` 只包裝既有 `loadExactCatalog`；menu、gender、class 三表合併後
  仍由同一 `MenuRequestWatcher` 解析，沒有第二套 watcher 或模糊比對。
- receipt command 新增成對的 `-class-events`／`-class-translations`；任一缺件即拒絕。
- steady：22 events／22 requests／0 misses，雙重 JSON SHA-256
  `e2ea55e875a3a74a4ff0be92da3ddc4cab3f992f6fbed7c76dece88e8b2c37e0`。
- Down→Up：26 events／26 requests／0 misses，雙重 JSON SHA-256
  `3f542218d0098103fd6249c8cccabab7d1869cd4860c81e0648995433d341399`。
- Escape：30 events／23 requests／7 misses，雙重 JSON SHA-256
  `16033cc1e4f901d9857f8bc4f1ccb68e8455630d29a80333140acd28f3761f66`。

Escape 首次以錯誤的 30-request 預期失敗，證實返回功能選單七筆 identity 與初始 menu inventory
不同；契約依 exact identity 證據訂正為七次 miss，沒有為達到零 miss 而放寬比對。

## 驗證與邊界

- `tools/class_events.py` 交叉驗證 post-gender 與 lifecycle 清冊；
  `tools/class_request_receipt.py` 固定輸入、命令、事件、請求、排程及三組 JSON 雜湊。
- 65 項 Python 測試與六份正式收據通過。
- dosgolem 全部正式套件測試、`go vet` 與相關 race detector 通過；本機分支 commit 為
  `0025008fbb7d49c42e352f961585a10e82c118e5`，未推送 dosgolem 遠端。
- 本階段沒有 GOLEMFNT、英文像素清除、繁中繪圖、倍率預設或原版規則修改；玩家可見繁中
  仍須等待倍率決策及獨立 READY renderer 規格。
