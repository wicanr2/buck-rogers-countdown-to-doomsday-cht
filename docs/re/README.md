# 原版觀測證據索引

此目錄保存 dosgolem 的原版行為收據與推論分級，不保存原版遊戲、手冊、可還原素材或
其完整輸出。所有位址均須標明使用的位址空間；不可把 IDA 線性位址與 dosgolem 執行期
段位址混用。

| 文件 | 職責 |
| --- | --- |
| [第一階段輸入與啟動收據](phase-1-input-and-startup.md) | 輸入雜湊、權利邊界、dosgolem 能力與正常重播 |
| [第一階段選單文字輸出追蹤](phase-1-menu-text-trace.md) | 一條可觀測文字像素輸出鏈、位址與未知項目 |
| [第二階段文字分派與生命週期追蹤](phase-2-text-dispatch-and-lifecycle.md) | 長度前綴 ASCII 字串、字元 renderer、glyph primitive 與生命週期邊界 |
| [第三階段中文手冊輸入清冊](phase-3-manual-input-inventory.md) | RAR 完整性、解壓成員雜湊與僅 metadata 的頁面定位 |
| [第四階段選單互動與失效生命週期](phase-4-menu-interaction-lifecycle.md) | BIOS Enter 正常路徑、轉場字串輸出與舊文字清除時機 |
| [第五階段種族選擇返回生命週期](phase-5-pick-race-return-lifecycle.md) | BIOS Escape 正常返回、逐位元功能選單重建與反向清除時機 |
| [第六階段清除路徑與失效 hook 證據](phase-6-clear-path-hook-evidence.md) | byte-fill 勘誤、Mode 13h 矩形清除例程、Enter／Escape 動態範圍與 hook 邊界 |
| [第七階段文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md) | 末 glyph 完成證據、guarded return、自然落入反例與轉場事件順序 |
| [第八階段功能選單繁中字型與版面 prototype](phase-8-menu-font-layout-prototype.md) | 九筆來源、手冊譯名、字型授權邊界、2×／3× 整數覆繪與 containment |
| [第九階段 dosgolem 通用繁中覆繪基礎](phase-9-dosgolem-xlate-foundation.md) | `xlate` 來源、移植 commit、能力邊界、測試收據與倍率限制 |
| [第十階段繁中 catalog 與字型建置](phase-10-catalog-font-build-pipeline.md) | TSV 驗證、決定性字元清單、GOLEMFNT builder 與 dosgolem 回讀收據 |

`workplace/` 是被 Git 忽略的原始輸入與可重生收據存放處；其檔名與雜湊由上述文件引用。
