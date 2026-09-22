# 第一百五十二階段：第六頁六行雙倍率執行期同狀態驗收

日期：2026-09-23
狀態：**CONFORMED 僅限合法第五頁終態進入第六頁六行，以及同執行 page6→page7 Enter 離頁。**

## 固定輸入、工具與權利

從私有合法第五頁終態
`workplace/phase123-story-page6-enter/page5.state`（SHA-256
`dcd08e37d9f394d47b1985b5891f0f3c70ba55d2c345bf9296867657f8ee65f6`）
開始。穩定第六頁組在 step `321000000` 送正常 BIOS Enter，停止於
`330000000`；同執行離頁組另於 step `331000000` 送同類 Enter，停止於
`340000000`。control／2×／3×使用完全相同 state 與輸入排程。
原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，
本機倚天 top-pad GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。

本機 dosgolem branch `buck-rogers-cht-output-overlay` HEAD `0ce4948`，
Go 1.26.7／`golang:1.26.7-bookworm` Docker；本次 `cmd/buckrogers-text-receipt`
runner SHA-256
`6039c6d97d57a6cc30efc1e03bee28b2e4a817e5bbae9d1dc2fd982149a35e66`。
執行容器為無網路、有界資源、`--rm`、目前 UID/GID；原版資料唯讀掛於
`/orig`，輸出只在 ignored `workplace/page6-runtime-evidence/`。位址均為
dosgolem 實模式 `segment:offset`，非 IDA 線性位址。原版、state、字型、
RGBA、PNG 及完整收據不入 Git／GitHub／公開包。

首次控制組試跑漏掛 `/orig/GAME.OVR`，restore 失敗且無有效收據；
確認原版檔案實際存在後唯讀掛入 `/orig`，才乾淨重跑以下三組。

## 穩定第六頁 control／2×／3×

私有 `stable-{control,2x,3x}.json` SHA-256 依序為
`0b476c177c4c06d084d146fac79bcc75662a19c104b10913714dfdc52f1277b3`、
`ce5d1781c6b985e482809f7a48c837137306b7c29bc441b18f24bb786c469f11`、
`2345b07cc31d0bb1df1e2a57aa64c7a93da6324d29799e42b7c4b021b890e9a8`。
兩倍率均完整啟用六個 `story.page6.line.001`–`.006` key、`drew=true`、
零缺字；logical `[8,320)×[136,184)` 外零像素差，內部分別 13067／27979
像素差。2×／3× PNG 已抽看：繁中可讀，未侵入右側人物資訊或 row 24。

扣除唯一 output-only 的 `story_page6_overlay` 與
`story_page6_invalidations` 欄位後，兩倍率原版 JSON 與 control 逐欄相等，
包括原版事件、BIOS 輸入、記憶體、indexed framebuffer 與 palette digest。
正規化 `state-compare` 兩倍率均 `equal=true`，machine digest
`a16a73299e2c61378d82d6bbd4aa312e28bc6dd1b5b75fad5f3ac6cf450d5236`、
DOS digest
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。

## 同執行 Enter 離頁

私有 `exit-{control,2x,3x}.json` SHA-256 依序為
`76dfc9593943e867aad0657821f0a31967908fd004a9b9858d98fb8955d39e6e`、
`6f073fe8e1f0fbebdb9223d46d1b1dce7ad10309d6c10c14ac29a61c973b6bbf`、
`38f021750bfdecc86e41bf01d17d972dd6726d3631d0f697b6ab64498fba15df`。
雙倍率均在 step `331026784` 的原版 pre-execution
`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`，記錄
`active_keys_before=6`，立即清空六行。終態 active 空、`drew=false`，
RGBA 與各自 baseline 逐 byte 相同，安全矩形內外差異均為零；原版 JSON
扣除 output-only 欄位後與 control 逐欄相同。正規化
`state-compare` 兩倍率均 `equal=true`，machine digest
`ef146aed0a78772b7471f9c476aa22be0235225f6b285c3e253dfc79e51aae65`，
DOS digest 同上。

## 失敗即關閉與限制

本機 dosgolem `e3e1db1` 接第六頁 strict catalog／watcher／presenter，
`a7304e3` 補真正缺字、mode／repeat、完整 SHA、invalid-tail／mixed／
duplicate 的雙倍率原子負例，`0ce4948` 接正式 CLI 與旗標／輸出拒絕測試。
主代理從當前 HEAD Docker 重跑
`go test ./apps/buckrogers ./cmd/buckrogers-text-receipt`、`go vet`
與 `go test -race` 均通過。負例和同狀態收據只支持上述固定路徑；
完整開機、其他離頁、遊戲內存讀檔及 Linux 正式玩家前端仍未驗。
本頁不能用來宣稱整款遊戲已中文化。
