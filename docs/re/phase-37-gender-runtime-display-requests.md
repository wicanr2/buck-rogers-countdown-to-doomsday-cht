# 第三十七階段：性別選擇繁中執行期顯示請求

## 結論

第 35、36 階段已證實的性別選擇文字事件，現已經正式七 identity inventory 與三鍵繁中
catalog 接到 dosgolem 既有 guarded post-call watcher。Enter→Enter→Down→Up 正常玩家路徑的
18 個完成事件全部精確產生 18 個顯示請求，零 catalog miss；Escape 路徑在取消男性反白後
停止產生性別請求，返回功能選單的七個尚未登錄 identity 各自失敗即關閉。

這只證明執行期 request 層；尚未載入字型、清除原文、繪製繁中像素或選定 2×／3×，不能
宣稱玩家畫面已中文化。

## 用語來源與證據等級

- 中文說明書 `SCAN0352_005.jpg` 的角色資料圖直接使用「性別」，因此提示採「選擇性別」。
- 男性／女性是由原版選項語意採用的標準繁中介面譯詞；中文說明書未找到逐字列舉，故來源
  標為 `runtime-interface`，不冒稱手冊原文。
- 本輪 RapidOCR 僅掃描 `SCAN0352_003.jpg`–`010.jpg` 作搜尋線索，沒有找到男性／女性字樣；
  OCR 輸出位於被忽略的 `workplace/manual-ocr/phase37-character-creation.json`，未當成證據。

## 正式 catalog

`text/gender-events.tsv` 保存七個唯一完整 identity：提示、兩筆初始 normal 選項、selected
male、short normal male、selected female、short normal female。Up 的 selected male 重用同一
identity，不建立重複列。

- `gender-events.tsv` SHA-256：
  `a8c96c8edc393c26717a5d05bc46fc031d25a8d0c269f3fe1c6b617ee0dda297`。
- `gender.zh-TW.tsv` SHA-256：
  `8fd64b9a15fc94aff73a8f7d06ff100b406763b09ac562989a82344eeeac6857`。
- `tools/gender_events.py` 逐欄反查 `post-race-events.tsv` 與
  `gender-selection-events.tsv`，並驗證事件／譯文鍵雙向完整、來源枚舉、格式與唯一性。

## dosgolem 實作

dosgolem spec `018-buck-rogers-gender-runtime-display-requests` 依 READY→實作→真實重播達
CONFORMED；本機分支 commit 為 `24f0dd55cdce8a929ab513e2a2a1f78afb6fb56b`，未推送遠端。

- `LoadMenuCatalog` 與 `LoadGenderCatalog` 共用同一個 exact identity 載入／解析核心。
- `MergeMenuCatalogs` 拒絕任何跨 catalog identity 衝突。
- `buckrogers-text-receipt` 新增成對的 `-gender-events`／`-gender-translations`；menu 與 gender
  嚴格載入後只合併成一個 resolver，仍使用同一個 `TextRecorder`／`MenuRequestWatcher`。
- request 收據只保存 event key、text key 與譯文字數，不含英／中文全文。

## 真實正常玩家路徑

共同輸入是 SHA-256
`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164` 的固定 state，第一與
第二個 Enter 分別排在 #100,010,000、#100,240,000，停止於 #101,000,000。

### Down→Up

- Down #100,400,000，Up #100,460,000。
- 18 events／18 requests、零 miss、pending、drop。
- 性別請求次序為：提示、normal male、normal female、selected male、normal male、selected
  female、normal female、selected male。
- 兩份 JSON 逐 byte 相同，SHA-256 均為
  `d5bafaf03cd1fb3c5f54346239aab7754b7ceb828789436d73957cca9854faa4`。

### Escape

- Escape #100,400,000。
- 22 events／15 requests／7 misses、零 pending、drop。
- 最後一筆 request 是 `gender.selection.normal.male`；後續七個返回選單事件沒有產生空白、
  重複或沿用的性別 request。
- 兩份 JSON 逐 byte 相同，SHA-256 均為
  `0b7518bc5ea5583954f33b153c77d900b77ca09f7584de9e21325f618890628b`。

## 驗證與下一步

- `tools/gender_request_receipt.py` 固定輸入／命令雜湊、完整事件、BIOS 排程、request 次序、
  譯文字數、miss 與兩份收據雜湊；負向測試拒絕順序、鍵、字數、miss 及 schema 漂移。
- 專案 55 項 Python 測試通過；dosgolem 255 份 spec 索引計數、全部正式 packages test／vet、
  `apps/buckrogers` 與 receipt command race detector 通過。

下一個玩家可見接線仍受 2×／3× 決策阻擋；在決定前，可繼續量測 Enter 確認性別後的正常
角色建立文字路徑，或補齊 Escape 返回功能選單七個 identity 的 catalog，但不得藉此假裝
renderer 已完成。

