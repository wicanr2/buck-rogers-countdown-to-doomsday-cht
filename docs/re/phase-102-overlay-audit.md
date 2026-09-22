# 第一百零二階段：手冊與快捷列覆繪稽核

日期：2026-09-22  
狀態：**已完成靜態與一題執行期稽核；未完成全部玩家路徑驗收。**

## 範圍

本階段獨立核對已補齊的 39 題手冊段落、2×／3× 字形幾何，以及技能操作列的
白色快捷字母契約。它不改動原版 EXE、答案判定、DOS 輸入、VRAM、存檔或規則；
也不把單一固定狀態的收據外推為 39 題或所有畫面的完成聲明。

## 手冊容量與 3× 幾何

- `text/manual-overlay-layout.tsv` 的唯一正式正文矩形為 logical
  `[7,312)×[72,184)`；文字 anchor `(16,72)`，36 欄×14 行，容量 504 個
  Unicode 碼位（code point）。所有 39 段均在此上限內，因此正式契約是單頁顯示，
  **不需要也沒有實作手冊覆繪捲動／分頁控制**。
- 2× 路徑使用原始 16×16 字模。3× 將非 ASCII 中文字模在記憶體最近鄰放大為
  22×22，放在 24×24 的輸出字格 `(1,1)`；每格間保留兩像素，不改字庫來源。
  ASCII 維持 16×16。
- `RuntimeManualOverlay` 建構時會預先驗證整份正式 catalog 的每個字元都在字庫，
  因此以下第一百階段字庫的成功載入同時涵蓋 39 段的字模存在性；這只證明字模覆蓋與
  layout，不證明每題都已在正常遊戲中被抽到。

## 第一百階段字庫的執行期收據

以 `phase12-before-question.state` 的已知第一題重播，載入現行 39 題 catalog 與
10 份 catalog 聯集的本機倚天 top-pad 字庫。原始遊戲、字型、完整存態與 PNG
只存在被忽略的 `workplace/`，不加入 Git 或 GitHub。

| 項目 | 值 |
| --- | --- |
| 初始 state SHA-256 | `8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269` |
| 字庫 SHA-256（959 個字模） | `1c8bc423568b13702e6056bcff302e9497c09c237955acd95593c2bab04018aa` |
| 起訖指令步 | `266399999` → `266557247` |
| 2× 核准正文內變更／正文外變更 | `3776`／`0` 像素 |
| 3× 核准正文內變更／正文外變更 | `6591`／`0` 像素 |
| 2× 覆繪 RGBA SHA-256 | `da3007bc54ecd0e52dd6a7f8979619808e54521ca6e176686403374dcafed5fb` |
| 3× 覆繪 RGBA SHA-256 | `c6e87ba6267ae12f99f7110c02328e0844c32946e7ad8a77cae70a6bb712206e` |

兩倍率與無覆繪控制組的原版完整持久化狀態相等，且原始 indexed framebuffer
未變。可重生收據位於 `workplace/phase101-overlay-audit-first/`。

在一次性、無網路 Docker 容器內的重跑入口如下；掛載 `/orig` 前須確認其為原版
目錄，輸出目錄必須是尚不存在的 `workplace/` 子目錄：

```sh
docker run --rm --network none --memory 2g --cpus 2 --pids-limit 512 \
  -u "$(id -u):$(id -g)" \
  -v "$PWD:/project" \
  -v "$PWD/workplace/original/BRcdoom:/orig:ro" \
  -w /project python:3.12-slim sh -c \
  'python3 tools/manual_runtime_smoke.py \
    --command workplace/dosgolem/workplace/out/buckrogers-text-receipt \
    --state-compare workplace/dosgolem/workplace/out/state-compare \
    --state workplace/probe/phase12-before-question.state \
    --font workplace/phase96-font/buckrogers-ui-eten-top-pad.golemfnt \
    --out-dir workplace/phase102-rerun'
```

## 快捷列視覺契約

正常態文案為 `(A)加點`、`(S)減點`、`(P)上頁`、`(N)下頁`、`(D)完成`。
`HotkeyPreservingActionBarNormalStyle()` 將每個字的前景索引固定為
`[原色, 白色快捷字母, 原色, 原色, 原色]`；焦點狀態則沿用已證實的原版反白色彩，
不猜測 disabled 狀態。既有 3× 收據與 PNG 顯示中文 22×22、字距約兩像素，
2× 保持原有 16×16 路徑。

## 靜態與核心驗證

在 Docker 內，設定 `BUCKROGERS_CHT_ROOT=/project` 後：

- `go test ./apps/buckrogers`、`go vet ./apps/buckrogers ./cmd/buckrogers-text-receipt`、
  `go test -race ./apps/buckrogers` 通過。
- `python3 tools/manual_catalog.py ...` 與
  `python3 tools/manual_overlay_layout.py text/manual-overlay-layout.tsv text/manual.zh-TW.tsv`
  通過；後者輸出 `validated 39 manual paragraphs at 504 characters`。
- `python3 -m unittest discover -s tools -p 'test_*.py'`：177 項通過。

## 明確未驗收項目

- 手冊：實際遊戲內返回、存檔與讀檔後的覆繪失效；以及其餘 38 題的正常玩家路徑
  抽樣。現有 first-question receipt 不可作為這些流程的證明。
- 快捷列：職業技能頁、各焦點變化、技術技能頁的 Prev／Next／Done，以及離開技能頁
  後的清除與返回，尚缺各自的正常玩家路徑收據。
- 互動式 host 前端仍是獨立的未完成能力；本文件的 headless 收據不等於使用者端
  視窗驗收。

本收據執行後，第一百零一階段又新增身體圖示的七筆譯文，11 份 catalog
已重建為 961 字模；該新字庫尚未用於本節的手冊執行期重播，勿將上述像素雜湊
套用到新字庫。新字庫來源與雜湊見[第一百零一階段](phase-101-body-icon-text-catalog.md)。
