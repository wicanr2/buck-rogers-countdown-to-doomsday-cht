# 第九十九階段：技能操作列 3× 中文密度

更新：2026-09-22。這是使用者檢視 3× PNG 後要求「中文字更大、字距更緊；2× 維持」的
操作列切片，不改原版程式、文字判定或技能規則。專案仍以 dosgolem 本機分支
`buck-rogers-cht-output-overlay` 執行，原版與倚天字庫均留在忽略版控的 `workplace/`。

`cmd/buckrogers-text-receipt` 已將既有 READY 的操作列 request catalog 與
`RuntimeActionBarOverlay` 接至正常玩家角色建立→技術技能頁。五個動作文案只在
已確認的底部文字矩形覆繪；熱鍵 ASCII 字母仍用原 16 像素字模與原版白色，
中文取原版對應前景色，focus 的白底黑字配色不推測 disabled 狀態。

3× 中文字模由 16×16 倚天字模在記憶體以最近鄰轉為 22×22，放在原 24×24
字格 `(1,1)`；中文字之間空白由 8 像素縮為 2 像素。2× 路徑不變，與前一版
操作列 RGBA 逐位元相同，SHA-256
`33fba0901492843516d74af5766bcf65f52710b3af0202675ce185ed61e16f93`。

本機收據 `workplace/phase99-actionbar-3x/` 由同一已驗證起點
`phase66/fixed-after-bios-space-100m.state`，輸入正常角色建立鍵序，停於
`103500000` 指令步。控制組與 2×／3× 的非覆繪 JSON、indexed framebuffer、
完整機器與 DOS 存態皆相等；中文覆繪僅落在核准矩形，2×／3× 分別變更
1,586／3,377 像素，矩形外皆為 0。`3x.png` SHA-256
`e88e6a29e575debbc42a2e82810eeed26a46c30dad666871f09624d791647e5a`。
該 PNG 經目視確認中文較大、較緊，熱鍵字母仍可辨且為白色。原版和字型
來源未入 GitHub。

dosgolem 本機 branch 提交 `0c2ca91273d560f3dbc715a8f41556981639393c`。
Docker 內完整 `go test`、`go vet` 與 race detector（`apps/buckrogers`、
`cmd/buckrogers-text-receipt`）通過；手冊 catalog 固定測試已精確更新為
第 31 題 Technical Skills 的 event/text key，沒有放寬未命中的防線。

目前僅驗證技術技能頁正常進入時的五個操作列文案；職業技能頁各焦點、技術頁
Prev／Next／Done、離頁與返回仍待各自正常路徑收據，不以本收據外推完成。
