# 第一百四十八階段：第五頁五行執行期 A/B 與待審負例

日期：2026-09-23
狀態（建立時）：**正式接線與已量同狀態 A/B 通過；規格 014 暫維持 READY，待失敗即關閉矩陣獨立審查。**
2026-09-23 追加稽核後，規格 014 僅在本文固定玩家路徑限縮升 **CONFORMED**；
原始待審結論保留如下，不覆寫形成史。

## 固定輸入與私有證據

從第四頁合法終態 `workplace/phase104-post-return-enter-4/control.state`（SHA-256
`48885cadf2bc51d6c44c09e2f220a3bb80bb23487506c0494eecd977613bf07a`）
於 step `310000000` 送正常 BIOS Enter，執行至 `320000000`。離頁組在同一次執行
再於 step `321000000` 送 Enter，執行至 `330000000`。control、2×、3×使用相同
state 與輸入。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
本機倚天 top-pad GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。
Go 1.26.7 與 dosgolem 本機 branch `buck-rogers-cht-output-overlay` 的 `0f3ea89`，
在有界、無網路、一次性 Docker 容器執行。重建的 runner SHA-256
`f00c9e3b264d29c72e2279cbe860ec1f07bc367f0fee8a1eb4ce93fa6ca34b76`。
原版、state、字型、PNG、完整收據只存在 ignored `workplace/page5-ready-evidence/`，
不進 Git／GitHub／公開包。下列位址均為 dosgolem 實模式 `segment:offset`。

## 穩定第五頁

私有控制組、2×、3×收據 SHA-256 依序為
`dcc11e6a125a8117fb7d2ad80820551725f35558c010892dcfc78e093887bcef`、
`3b90321f1bc95f7e3fa4fb7e1a2f52f189a34869e24aae97d45ecb7b5032a3e1`、
`6f29aba207616d290517e0f7129f7a77c11875749297b858c753312d03927e6a`。
雙倍率五 key 完整啟用、零缺字，中文安全矩形外零像素差；矩形內分別
10663／23103 像素差。兩張 PNG 已抽看，繁中可讀。

扣除唯一輸出層欄位 `story_page5_overlay`、`story_page5_invalidations` 後，
control 與雙倍率原版事件 JSON 逐欄相同。三組 memory SHA-256 均為
`78b33a0dde6a3291fc640453d250b27da16d252a6b5d5b5e53b58890fb3381e8`，
indexed framebuffer 均為
`5869dd6d91d7f0fc84d2204cce43f8e229ce140bd1b0e75aa712bf295e21ecab`。
正規化 state-compare 均 `equal=true`，machine digest
`a8bf6d4013d78b1273c603da14fabec6d9d63862cf7f3e1da39106bf86355eef`，
DOS digest
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。
由本機 `0f3ea89` 重建 runner 後獨立重跑 2×，收據逐 byte 相同。

## 同執行 Enter 離頁

私有 control、2×、3×收據 SHA-256 依序為
`76e6afb1c38ebecc84dbf86477ccba9fed33ebe5a2d99c42c1aa919b6e28f6f3`、
`a4b44092e9ff03d04b97f7774d8498b1e9360375a317d86c1ec65d6612201068`、
`7f169587257eb0b8b6d30df6f813fc473a21e2368ae7d051a42f4917865d203f`。
雙倍率於 step `321118382` 的原版 pre-write `0CF4:1B3A`、
`ES:DI=A000:AA08`、`CX=304` 從 active 五 key 清為零。終態 `drew=false`，
RGBA 與 baseline 完全相同，安全矩形內外像素差均為零。原版 JSON 扣除
輸出層欄位後逐欄等於控制組；memory SHA-256 三組均為
`c48559e27108789330d27e7272476ee07c1dcd2f44e8fb2ed9aaf17ed1b1133e`，
indexed 均為 `e6177505b4f603839c8e72a8e16c4cc1c115a2862368dfdc411e763a48fa0b6a`。
state-compare 兩倍率均 `equal=true`，machine digest
`a16a73299e2c61378d82d6bbd4aa312e28bc6dd1b5b75fad5f3ac6cf450d5236`，
DOS digest 同上。從提交後 runner 使用兩筆同型 `-bios-key-at` 重跑 2×，
收據逐 byte 相同；一次不同輸入旗標造成的 `bios_input` metadata 差異
不當作原版差異，已同型重跑訂正。

## 限制

`go test`、`go vet`、`go test -race` 對相關 Go 套件通過，但現有失敗矩陣
須獨立審查每個 case 是否真正抵達其聲稱的錯誤條件，並補 presenter
invalid-tail、混合 generation、duplicate key 的原子性負例。未完成前規格 014
保持 READY。完整開機玩家路徑、其他離頁與遊戲內存讀檔尚未由本收據驗證。

## 2026-09-23 追加稽核與限縮結論

Terra 在本機 dosgolem `a2dba44` 補 presenter invalid-tail、混合 generation、
duplicate key 的 2×／3×原子拒絕測試。主代理於 `6181e31` 再補完整末字 SHA
mismatch 真正觸發計數、return step、已啟用 group 下未知／非 A000／不相交 write
不得誤清、已量相交 pre-write 清除後 RGBA 無殘留，以及 2×／3×缺字與 DRAFT TSV
拒絕。原有七個 ABI word 非零高位、caller／guard／style／order、return caller／
SS／SP、partial／discontinuity、READY catalog identity 與正式 CLI 負例一併審閱。
主代理從當前程式 Docker 重跑 Go test、vet、race 均通過，並回讀本文六份
control／2×／3×穩定與離頁私有收據，雜湊皆與本文相符。新提交只增加測試，
未改變重生收據所用 runtime 路徑。

因此規格 014 只在同一合法第四頁終態、既有 BIOS Enter 進入第五頁、
再由 Enter 離開的雙倍率五行正常執行鏈升 CONFORMED。完整開機、其他離頁
與遊戲內存讀檔仍未知，不從本收據外推。
