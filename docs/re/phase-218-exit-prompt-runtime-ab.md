# 第二百一十八階段：真正 Exit 問句本體正式無頭 A/B

日期：2026-09-24
狀態：**固定合法加入角色存態的 N／Y→Y、2×／3× 無頭路徑與已量生命週期，經主代理及獨立審查限縮 CONFORMED。**

## 範圍與輸入

依[規格 021](../spec/021-post-join-exit-prompt-body-only-draft.md)及
[第二百一十七階段](phase-217-exit-prompt-full-body-writer-review.md)的限縮 READY，
正式程式只在輸出 RGBA 上覆繪 row 24 兩句問句的本體。原版六格多色尾碼、
原版 indexed framebuffer、palette、BIOS 輸入及 DOS 狀態不由譯文更動。
本次不驗 Linux 實體視窗、其他加入角色狀態或完整存讀檔路徑。

- `START.EXE` SHA-256：`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；`GAME.OVR`：`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 合法 `workplace/phase54/a-joined.state`：`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`；本機 `workplace/current-font/buckrogers-eten-top-pad.golemfnt`：`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
- dosgolem 工作樹基底 HEAD `674e3e3fcbf8e36d5ac115da9e9b5bf685564339`，本階段正式程式與測試已保存於 workplace 分支 `buck-rogers-cht-output-overlay` 的本地 commit `a01e34253fa59cc92c3fde1bf4b33577e318e9e7`；未推送 dosgolem 遠端。容器 `golang:1.25.0-bookworm`，實際 Go `go1.25.0 linux/amd64`。
- 正式 TSV 為 `text/post-join-exit-prompt-events.tsv` 及 `text/post-join-exit-prompt.zh-TW.tsv`。兩句只接 exact 原文長度／SHA-256、caller、style、row／column 及 guarded Return；譯文不進 DOS 記憶體或原版判定。

位址空間：`37F1:101E` 與 `0763:184D`／`0763:1854` 均為 dosgolem 8086 實模式 `segment:offset`；`machine.VideoWrite.Offset` 是 A000 **段內** offset，先正規化成 `0xA0000+Offset`，再以 320-pixel 行寬判斷 `[0,width)×[192,200)` 八列。`GAME.OVR` offset 是檔案位置，三者不可混用。正式 watcher 僅在同世代 exact pending Entry→Return、已量時窗內接受兩筆初畫 writer；作用中問句遇本體相交 pre-write（含同值）先清層，未知 writer／錯序／越界失敗即關閉。q2 pending 可與 q1 active 短暫共存。

## 固定重播與私有收據

從同一合法 state 的 step `122400000`，固定送 `Right`、`Enter`、七次 `Down`、`Enter` 進真正 row 21 Exit。以 `cmd/buckrogers-text-receipt` 的 `-bios-key-at STEP:SCAN_HEX:ASCII_HEX` 明示排程：

```text
122600000:4d:00  122800000:1c:0d
123300000:50:00  123500000:50:00  123700000:50:00  123900000:50:00
124100000:50:00  124300000:50:00  124500000:50:00  124700000:50:00
124800000:1c:0d
```

| 收據前綴 | 加送鍵 | `-until` | 觀測點 |
| --- | --- | ---: | --- |
| `q1` | 無 | `124850000` | q1 guarded Return 後作用中 |
| `n` | `124900000:31:4e` | `125300000` | N 返回 row 21，q1 已在同值 A000 首寫清層 |
| `yy` | `124900000:15:59` | `124950000` | q2 guarded Return 後作用中 |
| `yystop` | `124900000:15:59`、`125000000:15:59` | `125006324` | DOS `Exited`，owner terminal `Closed` 且零層 |

每個觀測點各跑 control、2×、3× 兩次。所有原版、state、字型唯讀掛載；輸出只在被 Git 忽略的 `workplace/phase188-exit-prompts-draft/`。**權威**收據每點第一輪檔名 `runtime-fops-<表中前綴>-{control,2x,3x}.json`，第二輪於 mode 後加 `-b`。2×／3×另有同前綴 `.rgba` 與 `-baseline.rgba`。先前沒有 `-file-ops` 的 `runtime-<表中前綴>-…` 收據保留作歷程，不拿來支持 FileOps 驗收；不將任何 JSON、RGBA、原版檔或字型加入 Git。

以下是第一輪 q1 2× 的完整命令模式；其餘依表替換 `-until`、加送鍵與輸出前綴，control 省略所有 `-post-join-exit-prompt-*` 旗標，3×改 `-scale 3`。第二輪輸出前綴加 `-b`。`yy` 啟用 `-expect-active`；`yystop` 改用 `-expect-stopped`，要求 DOS 已退出、owner `Closed` 且零層。四組 control／overlay **都保留 `-file-ops`**，讓收據明示追蹤已啟用及零筆數量。每個掛載來源先確認存在且型態正確。

```bash
set -euo pipefail
PROJECT_DIR=/home/anr2/cht/golden_box/拯救地球
FORK_DIR="$PROJECT_DIR/workplace/dosgolem"
OUT_DIR="$PROJECT_DIR/workplace/phase188-exit-prompts-draft"
ORIG_DIR="$PROJECT_DIR/workplace/original/BRcdoom"
test -d "$PROJECT_DIR" && test -d "$FORK_DIR" && test -d "$OUT_DIR" && test -d "$ORIG_DIR" &&
test -d "$FORK_DIR/workplace/gocache" && test -d "$FORK_DIR/workplace/gomodcache" &&
test -f "$PROJECT_DIR/workplace/phase54/a-joined.state" &&
test -f "$PROJECT_DIR/workplace/current-font/buckrogers-eten-top-pad.golemfnt" &&
test -f "$PROJECT_DIR/text/post-join-exit-prompt-events.tsv" &&
test -f "$PROJECT_DIR/text/post-join-exit-prompt.zh-TW.tsv"
timeout 180s docker run --rm --network none --memory 2g --cpus 2 --pids-limit 128 \
  -u "$(id -u):$(id -g)" \
  -v "$FORK_DIR:/src" -v "$PROJECT_DIR:/project:ro" -v "$ORIG_DIR:/orig:ro" \
  -v "$OUT_DIR:/out" -v "$FORK_DIR/workplace/gocache:/gocache" \
  -v "$FORK_DIR/workplace/gomodcache:/gomodcache" \
  -e GOCACHE=/gocache -e GOMODCACHE=/gomodcache -e HOME=/tmp -w /src \
  golang:1.25.0-bookworm go run ./cmd/buckrogers-text-receipt \
  -file-ops -state /project/workplace/phase54/a-joined.state -until 124850000 \
  -bios-key-at 122600000:4d:00 -bios-key-at 122800000:1c:0d \
  -bios-key-at 123300000:50:00 -bios-key-at 123500000:50:00 \
  -bios-key-at 123700000:50:00 -bios-key-at 123900000:50:00 \
  -bios-key-at 124100000:50:00 -bios-key-at 124300000:50:00 \
  -bios-key-at 124500000:50:00 -bios-key-at 124700000:50:00 \
  -bios-key-at 124800000:1c:0d \
  -post-join-exit-prompt-events /project/text/post-join-exit-prompt-events.tsv \
  -post-join-exit-prompt-translations /project/text/post-join-exit-prompt.zh-TW.tsv \
  -post-join-exit-prompt-font /project/workplace/current-font/buckrogers-eten-top-pad.golemfnt \
  -post-join-exit-prompt-scale 2 \
  -post-join-exit-prompt-rgba-out /out/runtime-fops-q1-2x.rgba \
  -post-join-exit-prompt-baseline-rgba-out /out/runtime-fops-q1-2x-baseline.rgba \
  -post-join-exit-prompt-expect-active -receipt-out /out/runtime-fops-q1-2x.json
```

## 同狀態比對結果

兩輪的 12 對 JSON、八對 overlay RGBA 與八對 baseline RGBA 均逐位元組相同。每個觀測點的 control／2×／3× JSON 亦逐位元組相同，包含原版事件、鍵盤排程、記憶體、indexed framebuffer、palette 與 FileOps 追蹤狀態。24 份權威 JSON 均明示 `file_ops_tracking_enabled:true`、`file_ops_count:0`、`writes_count:0`；原版在這些存態之後沒有檔案操作，零筆不是未開追蹤。相較舊收據，移除這三個新欄後 12 組 JSON 均逐位元組相同，全部 RGBA 也完全相同，證明觀測旗標沒有改變本次固定重播結果。下表 SHA-256 是各組三份權威 JSON 共同雜湊，兩輪相同：

| 觀測點 | JSON SHA-256 | 2×／3× RGBA 相對同 frame baseline 的異位 bytes | 本體外／六格尾碼 |
| --- | --- | ---: | --- |
| q1 active | `6747184d99791960ab80ec03a9bc1d2af3066e0071b5aa25e7234332588dd67e` | `2208`／`4188` | `0`／`0` |
| N 返回 | `f92956c265b13652767602451850e8ea5d0ae03daea0ffce496e720148a9dcf4` | `0`／`0` | `0`／`0` |
| q2 active | `7a0d19097c9e79024d2b2191f9838350ee83f8858b0011900320e39f23ecb07a` | `5316`／`10287` | `0`／`0` |
| DOS Stop | `09b178aa30eb2cf50b0e213ba398f48ecddc2adfb65213173d57d16c4da0791a` | `0`／`0` | `0`／`0` |

q1 的准許本體是 `[0,96)×[192,200)`；q2 是 `[0,240)×[192,200)`。異位 byte 的 `(x,y)` 由 `cmp -l` 的 1-based byte index `n` 換算：`pixel=floor((n-1)/4)`、`x=pixel mod (320×scale)`、`y=floor(pixel/(320×scale))`；兩個 active 畫面的每筆差異皆在其本體內，保護尾碼 `[width,width+48)×[192,200)` 零差。N／DOS Stop 兩倍率 overlay RGBA 與 baseline 逐位元組相同。`-expect-stopped` 另於兩輪 2×／3× runner 驗證 `d.Exited`、terminal `Closed` 和 presenter 零層；單元測試驗證同 owner 不能 rearm。

容器內 `go test ./apps/buckrogers ./cmd/buckrogers-text-receipt -count=1` 通過，涵蓋 exact catalog 漂移、非 Exit row24 路由、q2 pending／q1 active 交疊、八列同值 pre-write、Stop／Restore／Discontinuity／Fault、未知 writer、越界與雙倍率尾碼 sentinel。另以實際 runner 核對關閉 `-file-ops` 時三個追蹤欄均省略、開啟且零筆時明示 `true/0/0`。這些測試只證程式內部契約；上述固定原版收據才支持本節的限縮同狀態結論。

本節未證其他角色／其他時間路徑、正式 Snapshot／Restore 事件來源、Linux 視窗或手冊以外的玩家流程。私有輸出不進版控；本批一次性容器均以 `--rm` 收尾，未新增本專案殘留容器或 root 擁有產物。

## 獨立生命週期軌跡

端點 A/B 本身不能證明中途交疊與同值寫入，因此正式 runner 另提供可選的
`-post-join-exit-prompt-lifecycle-case n|yy|stop` 及
`-post-join-exit-prompt-lifecycle-out /out/<檔名>.json`。它在既有 owner 的
Entry、guarded Return、A000 pre-write 與 DOS Stop 接點取樣；單獨輸出
`post-join-exit-prompt-lifecycle-v1`，**不改上述 control／overlay 收據**。
欄位只含事件種類、step、q1／q2 層狀態、writer `CS:IP`、A000 段內 offset
及 old／new indexed 色碼，不含原文字串、字模或可還原畫面。使用上節相同
固定 state、鍵盤排程、字型與 2× runner；N／Y→Y／Stop 的 `-until`、加送鍵與
`-expect-*` 亦完全沿用表格，只新增這兩個軌跡旗標。每路徑做 `a`／`b`
雙輪，私有輸出位於 `workplace/phase188-exit-prompts-draft/`：

| 路徑 | 私有檔名 | 雙輪共同 SHA-256 |
| --- | --- | --- |
| N | `runtime-life-n-{a,b}.json` | `9c3a19ebf0911ad80e52be1f483e4f8cb475ea5bc3c780dcf541bf85335a36b1` |
| Y→Y | `runtime-life-yy-{a,b}.json` | `184ecb115825273b49cf439ad73a5bf75a2be8a8d6007da96125f54f26abec8e` |
| Y→Y→Stop | `runtime-life-stop-{a,b}.json` | `2357f4959b768f19e3d34da069dd787366661de0d48cb9f469314fb6f1757b59` |

三組雙輪皆逐位元組相同；正式軌跡驗證器要求 q2 Entry **前** q1 active、
**後** q1 active 與 q2 pending 同時成立；q1 本體首筆 A000 pre-write 的
old/new 同值且立即清 q1、不清 q2 pending；q2 guarded Return 才作用 q2；
N 首筆同值 pre-write 清 q1 而不生 q2；Stop 後 terminal Closed／零層。
單元負例另拒絕失去交疊、不同值、錯 writer、落在尾碼、錯序、漏 Return、
N 意外保留 q2 pending 及 Stop 後仍有 active 層。這是限縮於所列固定存態和
時窗的生命週期證據，不能外推到未測路徑。

主代理另在唯讀、無網路 Docker 中重跑
`go test -count=1 ./apps/buckrogers ./cmd/buckrogers-text-receipt` 通過，
獨立驗算 24 份 FileOps 權威 JSON 的四組 SHA-256、六份正式生命週期軌跡的
三組 SHA-256、跨倍率／雙輪逐位元組同狀態，以及每個 RGBA 異位 byte 的
本體 containment。另一名代理唯讀審查正式 dispatcher、guarded Return、
VGA pre-write、DOS Stop hook 與 validator，支持上述**固定路徑**限縮
CONFORMED；相同原文雜湊但錯 caller／row／column 的外層候選事件目前
只保證不啟用層，不宣稱全域 terminal poison。Restore 後重入、異境路徑、
Linux 實體視窗、存讀檔仍未驗。
