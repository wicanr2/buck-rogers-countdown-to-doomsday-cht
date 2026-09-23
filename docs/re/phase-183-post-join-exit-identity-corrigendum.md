# 第一百八十三階段：功能選單 Exit 身分與舊清除收據勘誤

狀態：**DRAFT 原版證據；不授權新增覆繪或改寫選單流程。**  
日期：2026-09-23

## 問題與固定輸入

[第一百六十一階段](phase-161-post-join-menu-selection-and-exit.md)曾把 step
`125100053` 的 Enter 及 step `125119490` 的全選單清除解讀成 `Exit to DOS`
離頁；[規格 018](../spec/018-post-join-menu-overlay-draft.md)沿用了這項語意。
但同一份原版事件表顯示：Enter 前最後選到的是 row 12，不是 row 21。
本次重新核對兩列的原始字串與事件順序，並另以合法輸入重播真正的
row 21 Enter、確認與取消分支；這些新分支仍只是 DRAFT 原版證據。

- 原版 `START.EXE` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
  `GAME.OVR` SHA-256：
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 合法 `workplace/phase54/a-joined.state` SHA-256：
  `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
- 權威原版重播使用 dosgolem fork `1dafb0a857c42fbda7058157b7615e214a64ec64`、
  Docker 內 Go 1.24.13；ignored
  `workplace/phase161-post-join-menu-selection/cycle-exit-a.json`／`-b.json`
  均為 SHA-256
  `5b4c8f66ffd72651344c0dbb45de5946d273276b933dc9d4b902d69297841c36`。
  原版檔案、完整事件與畫面留在 ignored `workplace/`。
- 下表 `START.EXE` 位址是**檔案 offset**；`37F1:...` 與 `026F:...` 是 dosgolem
  8086 實模式 `segment:offset`，不可混為同一位址空間。

## 已證實的原始身分與時間順序

主代理在唯讀 Docker 中對 `START.EXE` 每一個定長 byte window 計算 SHA-256：
row 12 的 20 bytes 在 offset `0xE2E9` 唯一對上事件 SHA-256
`ac461667a825d608971320c5e9a9b0c3beddba13cdf3a659b5d03dd578a13fa7`，
短標籤為 `Create New Character`；row 21 的 11 bytes 在 offset `0xE421`
唯一對上 SHA-256
`622af18ec40b9e50d8ee66ca0da3e2071c85104b5fe4e3f07ea3b7ff116a7b4e`，
短標籤為 `Exit to DOS`。兩個 digest 在 `GAME.OVR` 均無同長度匹配。
這是原始 bytes、檔案 offset 與雙重原版顯示事件一致的**已證實**身分；
大小寫屬原文比對鍵，不得正規化成全大寫。

| 原版 step | dosgolem caller | 事件 | row／column | 背景／前景 |
| ---: | --- | --- | --- | --- |
| `123116863` | `37F1:15BD` | row 21 初畫普通 | `21／9` | `0／10` |
| `124714336` | `37F1:175D` | row 21 反白選取 | `21／9` | `15／0` |
| `124900535` | `37F1:1856` | row 21 回復普通 | `21／9` | `0／10` |
| `124909479` | `37F1:175D` | row 12 反白選取 | `12／9` | `15／0` |
| `125100053` | `INT 16h AH=00` | Enter 被原版消費 | row 12 仍為最後已量選取 | 不適用 |
| `125100369` | `37F1:1856` | row 12 回復普通 | `12／9` | `0／10` |
| `125119490` | `026F:029C` | 全選單清除 | 格 `[1,39)×[2,23)` | 不適用 |

由事件順序可**已證實**原先的 Enter 並非在 row 21 選取狀態發生；
把後續清除命名為「Exit to DOS Enter clear」因此被推翻。
該清除的 step、原始 caller、範圍與雙收據本身沒有錯，仍可作「選到 row 12 後
Enter」的清除證據。是否進入建角的完整狀態轉移仍未量；row 21 的新分支收據如下。

## row 21 真正 Enter 的 DRAFT 分支收據

以下均從上述合法加入角色存態，以 Right→Enter→七次 Down 選取 row 21，
再排程 Enter（step `124800000`），雙重重播均逐 byte 相同。收據留在 ignored
`workplace/`，不把原版可還原內容加入 Git。短提示的檔案位址是
`GAME.OVR` **檔案 offset**，輸出 caller `37F1:101E` 是 dosgolem 8086
實模式 `segment:offset`；兩者不能互換。
這四組新收據以 dosgolem fork
`cb3ca77c66e4909c5f513b807840e885ab5cb4a3`、
`golang:1.25.0-bookworm` 內 Go 1.25.0 執行
`go run ./cmd/buckrogers-text-receipt`；原版唯讀掛在 `/orig`，
使用 `--rm --network none --memory 2g --cpus 2 --pids-limit 256` 及目前使用者 UID/GID。

| 輸入分支 | 雙收據 SHA-256 | 已量輸出與結果 |
| --- | --- | --- |
| 只按 Enter | `4f10d8144cf764eeb2f1e33fadaa7bb2628abdc6bf6625c76391a8358cd7d8a6` | row 21 普通回寫 step `124800641`；row 24／column 0 的 12-byte `Quit to DOS ` 提示在 step `124811496` 輸出，原始 SHA-256 `c38a515358859a10e7a2104cab69fe10ee2d492d94024b7d8f17d69b1a409032`；至上限 `126000000` 未退出。 |
| 再按 Y（step `124900000`） | `f1157b2b9dcdab551e431c0b7999646e3cdbda718e8b17594559a916b9539a46` | BIOS 於 `124900053` 消費 Y；row 24 的 30-byte `Game NOT saved.  Quit anyway? ` 在 step `124906585` 輸出，原始 SHA-256 `35023ac3208312fb1c932ec15a737aae88817925d6cabb26d83281bf755bdcb8`；至上限仍未退出。 |
| 改按 N（step `124900000`） | `776f2ded2cd6d0edc42edc78a12fb2a934c2183f7b1be4112c40707971bc9d86` | BIOS 於 `124900053` 消費 N；step `124905852` 清掉選單區，之後重畫原選單，step `125241457` row 21 再反白；至上限仍在遊戲中。 |
| 連按兩次 Y（第二次 step `125000000`） | `d2e4ccba17048518e706762cd6a0b04b3851fb120c270dd14ff2ae79fbcb3a4f` | 第二個 Y 於 `125000111` 被 BIOS 消費；當時的 dosgolem runner 記錄在 step `125006330` 停止，早於 `126000000` 上限。runner 主迴圈條件為 `m.Steps < until && !d.Exited`，該次無執行錯誤，故可判定 DOS `Exited`。收據沒有顯示此前全選單清除，不能虛構一筆 Exit clear。後續同 fork 重播訂正見[第一百八十七階段](phase-187-exit-stop-six-step-corrigendum.md)。 |

兩個提示的短 bytes 經對 `GAME.OVR` 全檔定長 SHA-256 掃描，各自唯一對上
offset `0x17B0D` 與 `0x17B1A`；這證實提示身分，不授權將英文提示原文放入正式
catalog，更不授權跳過任何確認。新收據使用同一原版輸入與本機 runner 的
臨時鍵盤追蹤欄；其 `stopped_at`、提示與 BIOS 消費均可重生。

另以 ignored、可丟棄的 `cmd/row21-a000` 觀測器，從 row 21 selected
post-call step `124722949` 起，精確監測其半開像素矩形
`[72,160)×[168,176)`；線性 A000 範圍逐 byte `WatchWrite` 在寫入前回報，
連同值寫入也納入候選。觀測器檔案 SHA-256
`0633a6229ebe3facdf5749df0492482a65e1a165bc058b55e89a93bf8c9b00b7`，
雙收據 `workplace/.row21-final-a/b.json` 均為 SHA-256
`d0742be6b547f635c4546908ebd9b110ad261a23a47a7489edf245fd1c965117`。
原版最早相交 pre-write **已證實**為 step `124800903`、dosgolem 實模式
caller `0763:184D`、線性 A000 位址 `709192`（像素 x=`72`、y=`168`），
old `15`→new `0`；它落在 row 21 Enter 後普通回寫期間，早於 row 24
第一個提示。這僅證明 Enter 分支的原版覆寫邊界；N 返回選單、兩次 Y 退出、
中文候選字型 containment、逐幀覆繪失效及 control／2×／3× 同狀態 A/B
尚未完成，不能因此升 READY 或 CONFORMED。

## DRAFT 翻譯候選與幾何

低階翻譯代理在確認大小寫與原文後，為 row 21 建議「返回 DOS」；另有
「離開至 DOS」「退出至 DOS」。這只是顯示層候選，不進原版比較或正式 TSV。
row 21 原文單列安全矩形為邏輯像素 `[72,160)×[168,176)`；候選字型覆蓋、
2×／3× raster containment、反白顏色、逐幀失效尚未正式驗證，不能升 READY。
同一低階翻譯工序為兩個 row 24 提示提出「返回 DOS」（6 字元，對應 12-byte
第一問）與「遊戲尚未儲存。仍要離開？」（12 字元，對應 30-byte 第二問）；
其中第一問與選單項同譯並不表示它們可共用同一輸出 identity 或生命週期。
這些仍只是 DRAFT 候選；要先審查 row 24 的安全矩形、倚天字型覆蓋、
2×／3×色彩與提示更新，再另建正式 TSV。若原畫面另有 Y／N 鍵位提示，
必須保留原字母與白色，不得被提示譯文覆蓋；原版的 Y／N 判定不變。

## 回填與下一門檻

不可變定位鍵為 `DOS／START.EXE@0xE2E9`、`DOS／START.EXE@0xE421`，
並以原版重播 `37F1:175D` 的 row／SHA／style 連到玩家畫面。
此勘誤須回填 phase 161、spec 018、phase 182 runtime 收據、`CONTEXT.md` 與
研究索引；舊清除收據保留，不能重新命名成新的 Exit 收據。
下一個最小可丟棄實驗是補量 N 返回選單與兩次 Y 離開的
最早相交 A000 pre-write，確認覆繪生命週期；然後審查中文候選幾何及 guard。
只有證據審查通過、另行更新
READY 範圍後才能把 row 21 加入正式 watcher 或用其清除驗收。
