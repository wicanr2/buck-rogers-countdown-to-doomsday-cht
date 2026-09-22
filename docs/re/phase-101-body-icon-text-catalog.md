# 第一百零一階段：身體圖示選擇文字目錄

## 結論

沿用第四十八階段的正常玩家重播，將身體圖示畫面七個固定文字 identity 整理成正式
UTF-8 TSV：確認詢問、儲存詢問、舊／新標籤、舊／新狀態標籤，以及選擇說明。事件只
影響輸出端翻譯查詢；玩家輸入、圖示選擇、儲存判定與原版資料仍維持原樣。

## 證據與資料

- `text/body-icon-events.tsv` 的七筆 identity 分別回查 `body-icon-move-events.tsv`、
  `body-icon-refusal-events.tsv`、`body-icon-exit-events.tsv`；確認詢問與選擇說明的
  重複出現都必須命中相同 identity。
- `body.icon.old.action` 與 `body.icon.new.action` 的 14-byte identity 雖然相同，
  不以 hash 單獨推定語意；Docker 內檢視第四十八階段原版 `workplace/phase48/probe/enter.png`
  （SHA-256 `624853c658b696a5ea19aecb51503972354116fe558d1463670edace3d282c0a`）可讀到
  舊／新圖示下方的 `READY ACTION`，因此以「準備動作」作為同一介面詞。14-byte 長度包含
  原版欄位間距，正式譯文只保留語意且仍受矩形容量限制。
- `text/body-icon.zh-TW.tsv` 提供七筆繁中介面譯文，來源標為 `runtime-interface`；
  不把畫面中的原版全文寫入 Git。
- `text/body-icon-text-safe-rects.tsv` 依已證實 row／column／原文字格建立七筆單列矩形；
  confirmation、save prompt、body icon 與 selection 是不同畫面群組，驗證器只在同一群組
  內拒絕重疊。
- `tools/body_icon_catalog.py` 驗證 UTF-8／NFC、exact identity、字格容量、來源清冊
  雙向覆蓋與重複事件的一致性；控制字元、BOM、錯誤 caller／hash 或超長譯文均失敗即關閉。
- `tools/body_icon_text_safe_rects.py` 另驗證 320×200 邊界、8-pixel logical cell 對齊、
  單行容量、overflow policy 與畫面群組內不重疊。

## 驗證範圍

本階段已證實的是文字 identity 與譯文目錄，尚未把七筆文字接到 dosgolem runtime overlay，
也尚未建立身體圖示畫面的中文像素 A/B 收據。下一階段應沿用第四十八階段的移動、拒絕與
確認正常路徑，接通 runtime request 後再做 2×／3× 覆繪驗收。

Docker 驗證：`python:3.13-alpine` 內執行 catalog／矩形驗證器；兩組新測試
各有正負向 2 項，加上既有身體圖示收據 2 項，共 6 項通過。本輪產生的
`tools/__pycache__/` 已清除。

主代理另在唯讀掛載倚天來源的 Docker 容器，將本批譯文與其餘十份正式 TSV
共同重建本機字庫；11 份 catalog 聯集為 961 字模，字元清單 SHA-256
`4abe607c8798abc2264b1c7e5dae409cd576019168af1b22eb53ff447e80a529`，
`GOLEMFNT` SHA-256
`7e8f5d0e70cc75505279de0575b3bcc489c0b0901ddc3c39c179124c9e544b18`。
產物僅在忽略版控的 `workplace/phase101-font/`；這證明字模覆蓋，仍不是
身體圖示畫面的執行期覆繪收據。
dosgolem 正式 `fontcheck` 回讀為 `GOLEMFNT 16x16 glyphs=961`；加入新切片後，
專案新增安全矩形測試後的完整 Python 測試為 181 項通過；回讀未以 `-text` 指定文字，故字元覆蓋以
建置器的 11 份 catalog 全字驗證為準。

## 可丟棄 request projection（尚非 runtime watcher）

`workplace/phase101-body-icon-request/body_icon_request_probe.py` 以既有 Phase 48 的
`move-a`／`move-b`、`refuse-a`／`refuse-b`、`exit-a`／`exit-b` 正常收據，依 exact identity
與 source `entry_step` 投影出 request 順序；輸出 `requests.json` 的 SHA-256 為
`42bea1e8d47e98e632c02699ffc489bd9bd45ba2e3d5965058e3beb193e7a514`。三組 A/B 分別得到
1、6、2 筆 request，原收據 hash 對應既有 body-icon receipt：
`f81bbf…982cb`、`fe6ac4…1df019`、`56f36c…4bcc19`。

這是可丟棄的 resolver 相容投影，不是 dosgolem runtime watcher 收據：目前既有
`MenuRequestWatcher` 只觀測 `0763:0424` 高階 dispatcher，而身體圖示四筆圖示列事件位於
`1C41:2708`、`1C41:2729`、`1C41:274A`、`1C41:276B`。因此 projection 證明 catalog／
identity／順序可由既有正常 trace 精確重生，但不證明 runtime request 已接通。
