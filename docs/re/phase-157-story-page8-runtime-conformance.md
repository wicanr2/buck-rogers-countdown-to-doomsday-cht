# 第一百五十七階段：第八頁四行 runtime 限縮 CONFORMED

狀態：**只在合法第七頁 Enter 進入第八頁、固定四行及合法 Enter 離頁路徑 CONFORMED。**

## 實作與工具身分

本機 dosgolem 分支 commit
`c0f6d76b0eb60caa72e74a619c1b981c91b340a5` 原子接通第八頁 strict loader、
watcher、verified `RETF`、逐列 pre-write 失效、presenter、RGBA／PNG 與 JSON
receipt。Go 版本為 1.26.7；本輪 runner SHA-256 為
`84fb69fcfbed925757cde1098932b6d13b3aed3449792ed1bab82dfb854a974`。

所有原版 state、畫面、倚天字型與完整收據只保存於 ignored
`workplace/page8-runtime-evidence/`。其
`runtime-evidence-manifest.json` SHA-256 為
`2654b6672f5ea983d338bf1d9fd7b4776566aadbe381999cff4eab88f2e6899b`；
內含完整命令、輸入與輸出雜湊及正規化狀態比較，不加入 Git。

## 同狀態 stable A/B

從合法第七頁終態送出同一筆 Enter，分別重生 control、2×、3×至第八頁穩定畫面。
兩個倍率都啟用四個 `story.page8.line.*` key、缺字為零，且
`diff_outside_story_rect=0`。批准矩形內的 RGBA 差異為 2× 7,332 pixels、
3× 15,816 pixels。兩張 PNG 經人工檢視，原版英文四行均已清除；人物圖、右側
姓名／時間區與故事矩形外未被覆繪。

control 與兩倍率的正規化 machine digest 均為
`07f1729a…2c63`，DOS digest 均為 `8dd5789e…8a59`。這證實覆繪未回寫
原版 machine／DOS 狀態；不能外推未比較的完整開機或其他玩家狀態。

## 同程序 active→clear

同一程序於 step 341,000,000 與 351,000,000 排入兩筆相同 Enter，先建立
第八頁四鍵 active layer，再走合法 page8→page9。2×／3×都在原版最早相交
pre-execution write step `351154334`、`0CF4:1B3A`、
`ES:DI=A000:AA08`、`CX=304` 記錄 `active_keys_before=4` 並清除。

離頁終態兩倍率均為 `active_keys=[]`、`drew=false`、缺字為零，overlay RGBA
與 baseline SHA-256 相同，矩形內外差異皆零。lifecycle control 與兩倍率的
正規化 machine digest 均為 `31296f86…59fe6`，DOS digest 仍為
`8dd5789e…8a59`。

## 獨立失敗即關閉審查

另一代理獨立審查 `ec4dbc3..c0f6d76`：八個 CLI 旗標必須成組出現，倍率只接受
2／3；catalog、譯文、字型、四事件、ABI、verified return、generation、完整英文
清除矩形及輸出均失敗即關閉。2×／3×邊界測試明確接受 `(311,167)`，拒絕
`x=312` 與 `y=168` 的界外差異。定向 `go test`、`go vet`、
`go test -race` 均在 Docker 通過。

合成 active→clear 單元測試只證明核心契約，不單獨證明 CLI hook；本階段上述真實
同程序收據補足此限制。terminal 若停在未完成 glyph 群組中，presenter 維持 inactive／
baseline，屬失敗即關閉，不會產生假陽性覆繪。

## 結論與停止線

規格 017 只在第八頁固定四行及這條已量合法 Enter 進出路徑升 CONFORMED。
完整開機、其他入口／出口、右側動態資訊、存讀檔與第九頁中文化仍未驗，不在本結論內。

## 2026-09-24 標點勘誤重驗

本節追加新收據，不覆寫上文的舊譯文／舊字型結果。第八頁第四行補上跨頁
對話的全形右引號（U+300D）；英文事件 TSV 與原版遊戲維持不變。新版譯文 TSV SHA-256
`4660ef796bd7f2f72d18b6986da04003a02e0aec1f7d1ca7e420fedfe7fc8253`；
本機字型 SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
原版 `GAME.OVR` SHA-256 仍為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，
合法入口 state SHA-256 仍為
`e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`。

在 Go 1.26.7／既有 Docker image 中，以本機 dosgolem fork
`e05bfd304436001c04cee50b41ea289ac27f22bb` 及唯讀原版根，
由同一 state 各重跑 stable 和合法離頁的 control、2×、3×。
stable 四 key 全啟用、零缺字，核准矩形外均零差；矩形內差異為
2× 7,340、3× 15,827 pixels。四組 control／倍率的完整原版 memory、
indexed、palette 與正規化 machine／DOS 比較相等。離頁兩倍率仍在
step `351154334`、`0CF4:1B3A` 的 A000 相交 pre-write 清除四 key，
終態 RGBA 與各自 baseline 完全相同，無殘層。

完整命令、工具與輸入 SHA、六份收據 SHA、同狀態比較及限制記在
ignored `workplace/page8-runtime-revalidation-20260924/revalidation-manifest.json`
（SHA-256 `505e5fd59c676519851972080dfc185f7b8f81e2bc81f8dcca39875ee2b3b742`）。
原版、存態、字型、PNG 與 RGBA 只留本機；所有容器使用 `--rm`，
專案相關容器與 root-owned 產物／誤建 Markdown 目錄查核均無殘留。
此結果只更新第八頁固定四行的既有限縮 CONFORMED，不宣稱其他輸出路徑。
