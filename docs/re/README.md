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

`workplace/` 是被 Git 忽略的原始輸入與可重生收據存放處；其檔名與雜湊由上述文件引用。
