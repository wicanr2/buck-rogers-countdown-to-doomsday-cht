# 第二百零二階段：技能頁離開問句本體的正式執行期 A/B

日期：2026-09-24  
狀態：**僅兩個合法固定起點、兩句問句本體與 Escape→N／Y 的無頭雙倍率路徑限縮 CONFORMED。**

## 輸入與重生邊界

依[規格 020](../spec/020-skill-exit-confirmation-overlay-draft.md)的限縮 READY，
本機 dosgolem fork 已將正式 watcher、presenter 與收據 runner 接線。使用
職業與技術技能頁各一個合法 Escape 前原版 state；兩個 state **不同**，
每頁只在自己的 control／2×／3× 之間比較同狀態。原版遊戲、存態、字型、
RGBA 與完整收據均只留在 ignored `workplace/`，未加入 Git／GitHub。

重生參數與完整私有檔案索引在
`workplace/phase202-skill-exit-ab/README.md`，該 manifest SHA-256 是
`b80ea93ef57b739a39888ccc03f34134a17f9d3d401f34d8f5e29486dccf841a`。
runner binary SHA-256 為
`c426944ffe8358f57738d91e05c8d4679fd674a419ca75d6f9b0bb5c500afbdf`，
Go VCS revision 為 `38380a35814edccd93eda0525b790cc411cef87a`，
`vcs.modified=false`。runner 使用 `debian:bookworm-slim`；建置使用
Go `1.26.7`。職業／技術起始 state SHA-256 分別為
`fd64f35d19c855eef9f8f6e44357ed2aa295b89ff329bc35ee4cefd8eb4fbaa9`、
`2302ceede2daff8df0de42ff3cf7fc2e346ac89f64ff2b715b0be281fddb9a8e`。
倚天本機字型 SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`；
三份版控 TSV 的雜湊及所有 BIOS 步點見私有 manifest。這些雜湊只供辨識
本機輸入，不把原版或字型的散布權轉移給本專案。

Escape 使用 BIOS `01:1b`，N 使用 `31:6e`，Y 使用 `15:79`；錯誤的
`01:00` 不會顯示此提示，不列入驗收。兩頁分別取得 active prompt，
再各自從相同起點跑 N、Y，對每條路徑取 control／2×／3×。
control 與 overlay **都**開啟 `-file-ops -key-trace`。沒有檔案操作的
JSON 會因 `omitempty` 省略空 `file_ops`；不能據此推論未開觀測。

## 觀測結果

| 路徑 | 2× active RGBA 差異像素 | 3× active RGBA 差異像素 | 安全矩形外及尾碼 |
| --- | ---: | ---: | --- |
| 職業問句 | 2071 | 4015 | 零差 |
| 技術問句 | 2196 | 4211 | 零差 |

職業本體 logical 半開矩形為 `[0,264)×[192,200)`，技術本體為
`[0,272)×[192,200)`；2×／3×差異皆非空，逐像素只落在放大後的
本體矩形。其餘畫面與各自六格原版多色選擇尾碼皆為零差。active
control／overlay 的 `memory_sha256`、indexed framebuffer、palette、
BIOS 收據相等；中文只存在輸出端 RGBA 覆繪，不回寫原版畫素或狀態。

四條 N／Y 終態的 control／2×／3× JSON 與 indexed 檔案，在各自
同狀態路徑中逐位元組相等；overlay RGBA 對 baseline 亦全畫面逐位元組
相等。JSON SHA-256 分別為：職業 N
`9cc543726e022b41a2ba5f95c9e63ee272c073229165a035d9a07c27e3afc2fc`、
職業 Y `8a132373d5f505ab82ddea31496d723f823cbd54e8ee5c57c69564b9332e0de9`、
技術 N `334b6ed702f757a9ca5e212739ceed88bdc7ec5aba44048e0ea280df7adee42d`、
技術 Y `f363a1eee7697b74c6bb3924be52a259167091d3514119afa54a657e0dc90603`。
因此已記錄的記憶體、indexed、palette、BIOS 鍵讀取與 FileOps metadata
在覆繪前後不變；技術 Y 的非空 FileOps 也在三組原始 JSON 中完全相同。
返回／離頁的這四個有界停止點均無繁中層殘影。

獨立審查重新核對 runner／state／字型／TSV 身分、BIOS 排程、所有
active 像素矩形，以及四組終態 JSON、indexed、RGBA。正式定向
`go test ./apps/buckrogers ./cmd/buckrogers-text-receipt`、`go vet` 與
定向 race 測試已通過；這些程式測試與上述原版 A/B 是不同證據。

## 限制與後續

此結論**只**證實兩個固定合法 state、兩句問句本體、已量的 Escape→N／Y
和 dosgolem 無頭 2×／3× 收據。不證明冷開機正常玩家全流程、遊戲內
存檔／讀檔、Snapshot／Restore 的正式 bridge、Linux 視窗或輸入焦點，
也不推論原版尾碼逐格重畫語意。runner 的 DOS Exit 清層已接線；
Restore／Discontinuity 在核心有負例測試，但正式 session 事件來源仍須接通
並驗證。Issue #17 因這些剩餘工作維持開啟。
