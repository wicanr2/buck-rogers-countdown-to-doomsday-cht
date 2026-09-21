# 第七十五階段：技能配置底部操作列執行期事件

狀態：完成

## 目標

審查 dosgolem spec 213 的 DRAFT 證據，在契約足夠時升為 READY，實作 Buck Rogers
專屬 guarded glyph-event watcher，將職業／技術技能頁底部逐字輸出收旂為 content-safe
typed events。以正常玩家輸入證實 watcher 不改原版 framebuffer、按鍵或技能狀態。

## 範圍

- 復用 `text/skill-action-bar-events.tsv` 的 exact 長度、SHA-256、caller、座標與色彩。
- 建立純核心 collector，明示處理候選序列、完成事件、錨定中斷與失敗即關閉。
- 接入 Buck Rogers runtime watcher，但只輸出 typed event，不建立譯文 request 或覆繪。
- 重生職業 base／Subtract／Done 焦點與技術 base／Subtract／Prev／Next／Done
  焦點收據，每條至少重跑兩次。

## 不在本階段

- 不新增繁中譯文、安全矩形或 renderer；不宣稱操作列已中文化。
- 不把「一般」variant 命名為「可用」，disabled 仍是 unknown。
- 不選定產品預設 2×／3×，不改手冊版面。

## 完成條件

1. spec 213 在實作前具備輸入版本、typed 狀態、邊界、失敗模式及驗收方法，
   通過證據審查後才標示 READY。
2. 純核心測試覆蓋職業三標籤、技術五標籤，並拒絕部分序列、座標跳號、
   跨列、錯誤 caller，repeat 不為 1、未知雜湊與錨定失效。
3. 八條正常玩家路徑產生精確事件數與 identity；雙重播 JSON 決定性一致。
4. watcher 開／關的原版 framebuffer、鍵盤輸入及玩家可見終點一致。
5. spec 213 只在上述範圍內升為 CONFORMED；專案與 dosgolem 測試通過，專案
   `main` 推送並回寫相關 GitHub Issues。

## 退出條件

- 若現有 adapter 無法可靠錨定技能畫面，規格退回 DRAFT，先補錨定證據，不以字元
  內容單獨啟用 watcher。
- 若 runtime 收據暴露新 caller／色彩，保持 miss 並回到清冊審查，不擴張 exact
  catalog。

## 完成收據

- spec 213 實作前先補齊固定輸入、typed 狀態、錨定、失效、失敗模式、驗收與
  權利邊界後升為 READY；三次 runtime 暴露契約缺口時都回到 DRAFT 訂正。
- 純核心已拒絕未錨定內容、部分序列、mode／repeat／row／column／caller／
  SS／SP 漂移、未知雜湊、錯誤共享 key 與錨定失效。
- 八條正常路徑的 action event 累計數為 3、6、9、8、13、18、23、28；每條 watcher
  A/B JSON 一致，全數 0 miss、0 drop。
- watcher A/B/control 的 indexed framebuffer 各自逐 byte 相同；移除 action metadata 後，
  watcher 與 control 的其餘 JSON 也完全相同。
- 專案 142 項 Python 回歸、dosgolem 全部正式套件 test／vet 與相關 race detector
  通過；spec 213 已限定範圍升為 CONFORMED。
- 本階段不含譯文、安全矩形或 renderer，不改 disabled unknown、產品倍率或手冊版面。
- dosgolem 實作已提交於本機 branch `buck-rogers-cht-output-overlay`，commit `356848c`；
  依專案規範未推送 dosgolem 遠端。
