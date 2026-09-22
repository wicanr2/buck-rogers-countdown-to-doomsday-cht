# 第一百三十二階段：第二頁劇情 READY 審查與首屏轉場收據

日期：2026-09-22
狀態：**DRAFT；第二頁四行的進入、穩定 frame、字型／矩形與首屏失效已確認，但不足以授權第二頁 runtime。**

## 範圍與權利邊界

本輪從既有私有、合法手冊成功返回 state（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）重播至 absolute step
`288000000`。私有 BIOS 排程、原版、state、字型、RGBA、PNG、完整 receipt 只留在被忽略的
`workplace/phase131-page2-ready/`；本文件只引用其中的 content-safe summary，沒有原文、答案、
glyph bytes、像素或檔名清單。

本輪只觀測原版及既有 **首屏** READY output-only overlay；沒有載入、實作或試作第二頁
production adapter。第二頁繁中仍絕不進入原版記憶體、輸入、比較、規則、檔案或存檔。

## 同狀態收據

以同一起點和相同私有合法排程重生一份無覆繪 control 與既有首屏覆繪的 2×／3×組。三組在
第 2 頁四行完成後均停在 `288000000`，且完整原版終態相等：

| 項目 | 值／結果 |
| --- | --- |
| machine memory SHA-256 | `941fc5bd027a99e0206ca63b17c97caa4e4fc4b53225baaead39ee4808c49497` |
| indexed framebuffer SHA-256 | `5521a2f5433fd39f58f502f2d5795655822eb14618ec8ccc5792afc1442daf5e` |
| palette SHA-256 | `fa97ee0c556490cc1c64f09cc0d9ead7b9836ff58c7c9ac965cd5e316757242c` |
| control／2×／3×原版終態 | 相等；檔案操作、writes、未實作服務的 content-safe digest 亦相等 |
| 第 2 頁 glyph runs | 四筆完整、guarded，最後一筆 post-call `287243280 < 288000000` |

content-safe review receipt SHA-256 是
`e5c2328b6d4fbdd655792a5c1a22dc568c3149dee7e211b7ff4880ff8fc3326d`；其固定 runner SHA-256 是
`d26f9171c28caf1fc36b74ed0c3d66c126a0d3a795c2ef905102c3950bb9ca5a`。該 summary 重新比對
`text/story-page2-events.tsv` 的 sequence、entry/post step、caller、length、SHA-256、mode/repeat、
色彩與座標，四筆均 exact-hit；它不保存原始文字。

## 首屏作用中 stamp 的最早失效與第 2 頁關係

2×／3×皆只記到一筆已作用中首屏 group 的失效：dosgolem 實模式
`0CF4:1B3A`、pre-execution `ES:DI=A000:AA08`、`CX=304`、step `281020548`。
這是 Mode 13h row 136、x=`8..311` 的 video span，與首屏 READY rectangle 相交；當時完整五個
active keys 仍存在，故 watcher 在原版 write 前清除它們。兩倍率終態皆 `active_keys=[]`、
`drew=false`、缺字零，且 overlay RGBA SHA-256 等於同 frame baseline，故事 rectangle 內外差異均為零。

因此「第 1 頁覆繪留下英文／中文殘字而污染第 2 頁」已被本次延伸至四行穩定 frame 的同狀態
收據排除。這是**首屏** lifecycle 證據，不能偷換成「第二頁已具 lifecycle」。

## 第二頁 identity、幾何與字型

第二頁固定區只包含 `story.page2.line.001` 至 `.004`：
`0763:04FF → 0763:026B`、mode/repeat `1/1`、背景／前景 `0/10`、column `1`、rows `17..20`。
row 24 狀態列和所有右側動態欄位都未命中 catalog，仍排除。

future output-only presenter 的 logical safe rectangle 是
`[8,320)×[136,168)`：四個 8×8 cell rows、每行 39 cells，overflow 固定
`single-line-reject`。本輪以目前本機倚天 subset 的正式 `xlate.LoadFont` 回讀譯文：40 required
runes、0 missing；16×16 source ink 最大 extent 為 15×15。依既有首屏 2×／3× renderer 的相同
cell contract，2× 16×16 glyph 位於 16×16 output cell，3× CJK 22×22 bitmap 以 `(1,1)` 放入
24×24 cell，兩者均 contained。content-safe font geometry receipt SHA-256 為
`436a0a12fa602a095f6b03f30c2c357b7ed5cd776499deacbdfacf5f243c6e44`。

Docker 中 `tools/story_page2_catalog.py` 及四項單元測試也通過；它們拒絕 row 24、overflow、
identity 與 Unicode／TSV drift。

## READY 審查結論

已完成的 READY 前置：

- [x] 正常私有 state 上第 2 頁四筆 exact glyph-run identity、穩定 frame 與 control／2×／3×終態對照。
- [x] 首屏 active stamp 在進入第 2 頁前的最早可觀測 video-span 失效，且第 2 頁四行終態無殘留。
- [x] 第 2 頁四行 TSV 的 strict schema、雙向 key、來源分級、NFC、控制字元、容量與本機字型 coverage。
- [x] 明示四行 safe rectangle，並以實際 font bitmap／2×／3× cell contract 驗證 containment。

## 第 2 頁 → 第 3 頁的實際失效邊（追加）

從本階段剛建立的私有第 2 頁穩定 `2x/final.state`（SHA-256
`a81f40951ca3694df7af58c785870477991f4dee26e108d255c8c8b0133ca6c9`）開始，僅在 step
`291000000` 排入已證實合法 BIOS Enter，至 `298000000` 停止。一次性的 source 副本只加入
`-page2-active-stamp-probe`：它假定起點有一個 page2 active stamp，但只讀 `ES:DI`、`CX` 並在
第一次與 `[8,320)×[136,168)` 相交時記錄 metadata 後使 probe inactive；它不建立 RGBA layer、
不讀原文、不寫 VRAM，且未修改正式 dosgolem checkout。

probe 與無 probe control 的原版 memory、indexed framebuffer、palette、FileOps、writes、未實作
服務 content-safe digest 完全相同。最早相交 pre-write 為 dosgolem 實模式
`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`、step `291020464`；其 span 是 row 136 的
x=`8..311`，與 page2 safe rectangle 相交。第 3 頁第一筆 guarded glyph run 直到 step
`291022040` 才進入，五筆皆在 `297287594` 前完成，故這不是 row 24 或「下一筆文字」proxy。

content-safe receipt SHA-256 為
`9997bf106571e09387b52eaa948e4c911059ac69363bbee9f45348e3abdf403e`；其中記錄 disposable runner
SHA-256 `d2dacc0048d212ef2d92d600c7c51c6767f2fea402062ef01dd43a113f36c92b`、source SHA-256
`9f84e8dde77791ab7c0c2a89f845cd1e3c630affd1251bf991ed76517c95784b`、base dosgolem commit
`b4e1fb74b93fddabcde20c7ac07132604de04471` 與 control／probe receipt hashes；完整私有收據、
state 和一次性 runner 留在 ignored `workplace/phase132-page2-exit/`。

## 第 2 頁 DRAFT atomic 純核心（追加）

ignored `workplace/phase133-page2-atomic-core/` 建立可丟棄、content-safe 的 watcher／presenter core；
它只讀版控 `text/story-page2-events.tsv` 的四筆 confirmed／DRAFT identity，不保存英文或 glyph bytes，
也沒有 dosgolem runtime、VRAM、renderer、font、input 或檔案依賴。`go vet ./...` 與
`go test ./... -count=1 -v` 在無網路、`--rm`、UID/GID `1000:1000` 的
`eob-remake-go:1.26.7-ebiten2.9.9` Docker 均 exit 0。

原先錯把 1→2→3→4 的合法完整 sequence 當作 wrong-order 的測試已撤回，不能當綠燈證據。訂正後的
pure core 在同一 Docker 命令重新通過：partial 後 row drift、從第 2 行起的 true order inversion、
hash miss、caller／guard／mode mismatch、`RETF` previous address／opcode／return caller mismatch、
relative SS／SP+`0x12` mismatch、相對 step 倒退、重複、restore、unknown video write 與 page3
non-revival 全部 fail-closed。四行只能一次建立 group。fixed original receipt 的 absolute entry／post
step 僅用作可回查 anchor；runtime identity 改以 length／SHA-256、caller／guard、mode／repeat、style、
row／column、sequence、verified far-return 和 `entry < post < next entry` 相對順序判定，故不會因正常
玩家路徑的不同絕對 instruction count 誤拒。

`InvalidateFromFutureMeasuredTransition` 只是測試 page3 non-revival 的 placeholder：它不是本段已量到
`0CF4:1B3A` span 的正式 wiring，更不是 production hook。unknown write 不會被 prototype 自行當成轉場。
因此此純核心只補齊 DRAFT 的資料與失敗模式證據；它不能把 disposable exit probe、placeholder 或 synthetic
tests 變成 READY／runtime 授權。

## Page2 glyph guarded far-return 與 span callback 時點（追加）

本輪先讀既有首屏 watcher 的 return-edge 契約，沒有將它直接接至 page2。現有 receipt runner 僅會在
pending `0763:026B` glyph 的前一指令為 `0763:03D6`／opcode `0xCA`（`RETF imm16`），且當前
`CS:IP` 回到記錄 caller、`SS` 相同、`SP = entry SP + 0x12` 時，才記錄 content-safe return edge。
這是 page2 可採用的已確認 RE shape，不是 production 實作。

以既有私有 page2 control trace（SHA-256
`e89a185a5d1edadf2bf902db9ab77c400e41ec0ecc4edcc1c957dd857a10f7b0`）逐 glyph 匯總：

| event | glyphs | mode/repeat | actual far-return | stack guard | 分級 |
| --- | ---: | --- | --- | --- | --- |
| `story.page2.line.001` | 37 | 1／1 | `0763:03D6` / `CA` → `0763:04FF` | `1841h`, `3D66h → 3D78h` | confirmed |
| `story.page2.line.002` | 31 | 1／1 | 同上 | 同上 | confirmed |
| `story.page2.line.003` | 38 | 1／1 | 同上 | 同上 | confirmed |
| `story.page2.line.004` | 37 | 1／1 | 同上 | 同上 | confirmed |

各行 first entry 與 last actual return 精確等於版控 TSV 的 entry/post receipt anchor；caller、style、
row／column 亦 exact-match。絕對 step 只供本次可重播收據比對，**不**是 runtime identity。由同一
content-safe audit 可確認 page2 最後 post-call `287243280`，接著 pre-execution span callback 在
`291020464` 取得 `0CF4:1B3A`／`A000:AA08`／304 bytes，早於第 3 頁 first glyph entry
`291022040`；故 callback 可在原版 write 前失效 page2 stamp，而非以 row24 或下一筆文字代理。

content-safe audit 為 ignored
`workplace/phase132-page2-exit/page2-glyph-return-content-safe.json`，SHA-256
`6767fdd7d8f6c32009004b78fdeaefb48ced665aea16324773d427cf6ba12e36`。它僅保存 aggregate control-flow、
位址、雜湊與分級；不保存原文、glyph bytes、stack words、輸入、像素或檔名。此 slice 的確認範圍
只限該合法重播；其他離頁／restore 仍為 unknown。

仍缺、因此**不得升 READY**：

1. DRAFT core 尚未是 READY typed contract：雖然本輪已量到 glyph entry→actual far-return、SS／SP
   stack guard、mode／repeat 與 page2→page3 pre-write callback，仍須把這些證據審查為正式 adapter
   contract；`InvalidateFromFutureMeasuredTransition` 不得直接接線。其他合法離頁與 restore 仍需明示
   fail-closed boundary。
2. 只有上述契約經審查升 READY，才可實作；之後仍須以 2×／3×、同 state A/B、page2→page3 lifecycle、
   restore／unknown input 與原版 state non-interference 做 CONFORMED 驗收。

## 環境與清理

所有重播、font loader 與 catalog test 皆為 `--rm --network none` 的 Docker container，使用 UID/GID
`1000:1000`，原版與輸入唯讀掛載、只有 ignored `workplace/phase131-page2-ready/` 與
`workplace/phase132-page2-exit/` 及 `workplace/phase133-page2-atomic-core/` 可寫。產物抽查均為
目前使用者所有，未建立長駐容器或 root-owned 專案檔案。
