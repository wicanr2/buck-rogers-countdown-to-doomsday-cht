# 第九十六階段：倚天字型建置與手冊中文執行期整合

狀態：已完成本階段實作切片；#14 全範圍仍開啟。

驗收結果見 [實作與重播收據](../re/phase-96-eten-manual-runtime.md)。

## 交付目標

依使用者要求，由 Terra 子代理並行實作，主代理整合與驗收，將已完成的調查轉成可執行的手冊中文畫面。
沿用已選定的倚天 `top-pad`、保留原題、36×14 正文與 2×／3×；只針對實作遇到的具體缺口補證據。

工作以 GitHub [#15](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/15)、
[#13](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/13)、
[#14](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/14) 為權威。
字型實作契約見 [spec 008](../spec/008-eten-top-pad-local-font-builder-draft.md)，
手冊整合契約見 [spec 005](../spec/005-manual-runtime-presenter-draft.md)。

獨立像素驗證入口：[`tools/manual_rgba_verify.py`](../../tools/manual_rgba_verify.py)，
直接比較原始 RGBA 並檢查正文安全矩形；可另寫本機 PNG 供目視檢查。
整合重播入口：[`tools/manual_runtime_smoke.py`](../../tools/manual_runtime_smoke.py)，
以獨立控制組及 2×／3× 三次執行比較完整存態、記憶體與輸出收據。

## 驗收與退出條件

1. 本機正式工具可由使用者的倚天來源產出 691 字模，通過合成測試、來源驗證與 dosgolem 回讀。
2. 手冊呈現沿用既有事件鏈；前景色來自真實原題輸出，正常重播能顯示中文正文。
3. 2×／3× 的正文區外像素不變，原版狀態不受覆繪影響；抽測換題時舊段落清除。
4. 保存可重跑入口、必要收據及實際通過範圍；未驗證情境保留在 Issue，不以本階段外推全遊戲完成。
5. 文件、GitHub Issue 與程式同步交接；dosgolem 僅提交本機分支，字型與原版素材仍在被忽略的工作區。
