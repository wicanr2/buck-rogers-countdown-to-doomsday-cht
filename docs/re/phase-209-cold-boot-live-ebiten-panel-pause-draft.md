# 第二百零九階段：冷開機選單的實體視窗回合與面板暫停

日期：2026-09-24
狀態：**DRAFT；ignored 原型的單次實體 X11 收據，不是正式可玩版或同狀態 A/B。**

## 輸入、原型與重生邊界

[第二百零八階段](phase-208-cold-boot-menu-ebiten-prototype-draft.md)已從原版
`START.EXE` 第零步取得繁中選單，但開窗後只重畫預先算好的影格。本次另建
`workplace/cold-boot-live-turn-proto/`，不改舊原型與正式程式：以相同的
本機原版 EXE SHA-256
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`
從第零步安裝選單 watcher，跑至一億步後，將**同一部 machine**交給正式
`frontend/ebiten.Game` 的 `Update` 回呼繼續推進。原版資料唯讀掛載，
`scratch/` 與 `out/` 分別可寫；原版 bytes、字型 bytes、文字與畫面未加入 Git。

`main.go` SHA-256
`acc237dffa27614021745ae2819413eb9abc28ede07970c1457ea2c74967328b`，
`go.mod` SHA-256
`5f45f6595de4d2e3a712693b1c5fa898db08887efb93435bbf11574e345d56c6`；
私有 `out/receipt.json` SHA-256
`457d658a7adbd11fe55fbc476a2e644dc901de94ce53d90df9806947d0d22419`。
沿用 dosgolem fork `674e3e3fcbf8e36d5ac115da9e9b5bf685564339` 與
`eob-remake-go:1.26.7-ebiten2.9.9`。以目前 UID/GID、
`timeout 300s docker run --rm --network none --memory 2g --cpus 2
--pids-limit 256`，專案根唯讀、原型及獨立 out/scratch 可寫；
容器內以有 trap 的 Xvfb :99、`GOPROXY=off GOSUMDB=off` 執行
`/usr/local/go/bin/go run -mod=mod .`。實體點擊由 X11 輸入工具送出；
不是直接呼叫面板核心。掛載前已確認路徑存在與形態。

## 原型量測

| Ebitengine `Update` 回合 | 開始 machine steps | 結束 machine steps | 差分 |
| --- | ---: | ---: | ---: |
| 首個關閉面板回合 | 100000000 | 100000016 | 16 |
| 第二個關閉面板回合 | 100000016 | 100000032 | 16 |
| 實體點擊 Open | 100000448 | 100000448 | 0 |
| 展開期間每個已記錄回合 | 100000448 | 100000448 | 0 |
| 實體點擊 Cancel、收合當回合 | 100000448 | 100000448 | 0 |
| 第一個收合後關閉回合 | 100000448 | 100000464 | 16 |

整次開窗共有 `Advance` 回呼 33 次，machine steps 從 100000000 增至
100000528（差分 528）；`Draw` 與 presentation `Snapshot` 各 69 次，
不把繪圖次數當 DOS 步數。記錄的面板暫停回合同時核對 indexed 影格雜湊
未變；但這**不是**完整 machine／DOS／BIOS／存檔狀態 digest。
watcher drops 0、misses 24；只使用第一個已量選單的 2×作用層。

主代理以唯讀 Docker 獨立核對原型與收據 SHA-256、上述數值和檔案
UID/GID；沒有第二次完整冷開機重播。原型在第一輪因舊 host 字型
缺 `×` 而啟動前拒絕；改載既有 current-font 後成功。此為原型輸入
條件訂正，不是遊戲或正式前端缺陷。原型的 3× host 字型只為滿足
建構器前置檢查，**沒有**進行 3× 視覺或操作驗收。

## 結論與停止線

**已證實（此單次 ignored 原型）**：原版從第零步到已量選單後，正式
`frontend/ebiten.Game.Update` 能在同一 machine 逐回合推進；2×實體
Open／持續展開／Cancel 同回合暫停，下一關閉回合恢復。

**未證實**：正式 composition root／typed session、Apply 切換 3×、
其他繁中作用層、玩家鍵盤／滑鼠正常路徑、完整 DOS 狀態 A/B、
存讀檔、Draw 故障收束及可發行 Linux 入口。規格
[004](../spec/004-dosgolem-host-frontend-draft.md)／
[019](../spec/019-linux-frontend-session-turn-boundary-draft.md) 維持 DRAFT；
Issue #16／#18 均不關閉。
