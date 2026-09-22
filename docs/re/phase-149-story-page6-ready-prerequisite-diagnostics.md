# 第一百四十九階段：第六頁六行 READY 前逐字返回與離頁寫入診斷

日期：2026-09-23
狀態：**原版低階證據已補強；第六頁仍為 DRAFT，不授權正式覆繪。**

## 輸入、工具與權利

entry 從合法第五頁私有終態 `workplace/phase123-story-page6-enter/page5.state`
（SHA-256 `dcd08e37d9f394d47b1985b5891f0f3c70ba55d2c345bf9296867657f8ee65f6`）
於 step `321000000` 送正常 BIOS Enter，至 `330000000`。exit 從合法第六頁
私有終態 `workplace/phase123-story-page6-enter/page6.state`（SHA-256
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`）
於 step `331000000` 送 Enter，至 `340000000`。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
位址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址或檔案 offset。

使用本機 dosgolem `buck-rogers-cht-output-overlay` branch、
`cmd/buckrogers-text-receipt` 在有界、無網路 Docker 內雙重重播。
重播當下的 runner binary 雜湊與精確 HEAD 沒有保存，**不能**把後來
`5652f11` 或 `6181e31` 的 HEAD 倒填成此收據版本；`0f3ea89` 是已知包含
所用第五頁 CLI 功能的提交，不是精確 runner 版本證明。重生時應補記
runner SHA-256 與 Go／dosgolem 完整版本。

原版、state、完整逐字事件、手冊與畫面只在 ignored `workplace/`，不得
加入 Git／GitHub 或公開發行包。本文件只保留不可還原原作的定位與摘要。

## 雙重原版收據

`workplace/page6-ready-evidence/entry-{a,b}.json` 逐 byte 相同，SHA-256
`1b137650c25d1f1137815de412b8cc8a722b401e4ac63b29c2f09fd8eabd5030`。
六行逐字返回共 200 筆，row 17–22 分別為 `37/34/36/38/36/19`。
200/200 筆皆記錄 `0763:03D6`、RETF opcode `0xCA`、回到
`0763:04FF`、entry／return 同 SS、相對 SP `+0x12`、mode/repeat `1/1`、
背景／前景 `0/10`，七個 ABI word 的 `high_word_mask` 全為 0。
這些是原版逐字控制流已證實的證據；正式 runtime watcher 與 TSV 審查尚未完成。

`workplace/page6-ready-evidence/exit-{a,b}.json` 逐 byte 相同，SHA-256
`38e9f933e811f77363cdf16e919f2998f3c7ce2e5bb0f68b5d1d72e26c70377f`。
以六列候選安全矩形觀察 48 筆相交的原版 fill；最早一筆在 step
`331026784` 的 pre-execution `0CF4:1B3A`，`ES:DI=A000:AA08`、
`CX=304`。這是第六頁離頁失效的候選錨點；尚未證明正式安全矩形、
完整覆繪生命週期或玩家畫面無殘字。

## READY 前仍需完成

獨立審查 `text/story-page6-events.tsv` 六筆 exact identity 與譯文，建立
六行文字安全矩形及實際字型 2×／3×墨跡 containment；以可丟棄 typed-core
驗證原子提交、七 ABI 高位、return／stack／step、partial／錯序、SHA、
未知／不相交／相交 write、DRAFT catalog、缺字與 discontinuity 負例。
取得精確 runner 身分並雙重重生後才可評估升 READY；其後仍須正式
dosgolem runtime control／2×／3×同狀態 A/B 與已量離頁驗收。

## 2026-09-23 補充：明確 runner 重生與可丟棄核心

上述早期收據的精確 runner 身分仍不可追溯；Terra 後來以本機 dosgolem
`6dcc42794fc8942451f5e584ba60a7d12b4bd106`、Go 1.26.7、
`golang:1.26.7-bookworm` 執行
`go build -trimpath -o /out/buckrogers-text-receipt ./cmd/buckrogers-text-receipt`，
新 runner SHA-256
`bc9d90a38fe5ede2dcfe5cd165f1567e81e2ac5430f25ec8e1b8e36c3b2597c7`。
從本文同一兩份私有 state、同一 Enter 排程分別雙重重播 entry／exit，
新輸出逐 byte 等於舊收據：entry SHA-256
`1b137650c25d1f1137815de412b8cc8a722b401e4ac63b29c2f09fd8eabd5030`、
exit SHA-256
`38e9f933e811f77363cdf16e919f2998f3c7ce2e5bb0f68b5d1d72e26c70377f`。
這補上一條**可重生的現行 runner 證據鏈**，不反向宣稱舊 runner 的確切版本。

ignored `workplace/page6-ready-atomic-core/typed-core-receipt.json` SHA-256
`1d24cf502b6f13d6b76af61dd74b2140ffa5ea72721b2d186fe6456c48cd0638`
記錄完整命令、輸入 TSV／字型雜湊、可丟棄 Python typed-core 三項測試、
正式 DRAFT catalog 五項測試與 2×／3×靜態墨跡 containment。核心已測
六行原子、length／SHA、caller／guard／style／order、七個 ABI word 各自
非零高位、RETF／stack／step、partial／錯序、未知／不相交／相交寫入及
discontinuity；真實 `confirmed/DRAFT` catalog 被拒，僅暫存 in-memory
READY fixture 用於核心正例。當前本機倚天 GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`，
loader 對第六頁譯文回讀零缺字，2×／3×各 4,179 個受控字模墨跡像素未越界。
這仍是靜態與可丟棄證據，不是正式 dosgolem runtime A/B。

第六頁的正式安全矩形與離頁前寫入、譯文目錄及負例尚待獨立 READY
審查；審查前 catalog 與規格保持 DRAFT，不將此原型接 production。

## 2026-09-23 獨立 READY 審查結果

Terra 以本文雙重原版收據、同一 state 的明確 runner 重生、私有
typed-core／字型 containment、正式六筆 catalog 與譯文逐項核對，
確認 `[8,320)×[136,184)` 及已量 step `331026784` 的相交 pre-write
足以定義固定 Enter 離頁的限縮契約。曾因誤讀不存在的 phase149
檔名而暫判證據缺失；重新打開本文件與正確私有收據後訂正，
不將先前誤判當成實際證據缺口。

[規格 015](../spec/015-story-page6-overlay-ready.md)及六筆
`text/story-page6-events.tsv` 已限縮升 READY。這只授權開始正式實作：
第六頁 watcher／presenter、control／2×／3×同狀態 A/B、已量 Enter
離頁與無殘字驗收仍未完成。舊 DRAFT 停止線保留作審查形成史，
不能據本段稱第六頁已中文化或 CONFORMED。
