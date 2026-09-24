# 第一百四十七階段：第四頁六行執行期 A/B 與失敗矩陣待審

日期：2026-09-23
狀態（建立時）：**正式接線與已量同狀態 A/B 通過；規格 013 暫維持 READY，待失敗即關閉矩陣獨立審查。**
2026-09-23 追加稽核後，規格 013 僅在本文固定玩家路徑限縮升 **CONFORMED**；
原始待審結論保留如下，不覆寫形成史。

## 固定輸入、工具與權利

從私有第三頁合法終態 `workplace/phase104-post-return-enter-3/control.state`
（SHA-256 `49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0`）
於 step `301000000` 送一筆正常 BIOS Enter、執行至 `310000000`。離頁測試
使用**同一執行**、同一 state，在 step `310000000` 再送一筆 Enter、執行至
`320000000`，讓第四頁六行先啟用再真正清除。control、2×、3×使用相同
輸入排程。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`
只讀掛於 `/orig`；字型為本機倚天 top-pad GOLEMFNT，SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。

本機 dosgolem branch `buck-rogers-cht-output-overlay` 至 `1cf9ec4`，
`golang:1.26.7-bookworm` Docker、Go 1.26.7、`--rm --network none`；
runner SHA-256 `aa48f8519cc1a4339d74ab390f697eee55128ab4e5391f86da7f6ef3bda46164`。
原版、state、字型、PNG、RGBA、完整收據僅在 ignored
`workplace/page4-ready-evidence/`，不進 Git／GitHub／公開包。原版位址
均為 dosgolem 實模式 `segment:offset`。

## 穩定第四頁

私有 `runtime-{control,2x,3x}/receipt.json` SHA-256 依序為
`8b7c26d5310d261204dfee40fdff341c092e16de86f031c25341b8691edf1a36`、
`ca5869c5bf51195bd9fd184124abe9315bd8a3cc9f964118c0f7595a3ae439da`、
`611b457183a219bd4f7729c2daa168dabcb91d26a467876d4f127a40d28f03e6`。
2×／3×均完整啟用 `.001`–`.006` 六 key，`drew=true`、零缺字；
六行安全矩形 `[8,320)×[136,184)` 外零像素差，內部分別為 12176／25588
像素差。兩張 PNG 已抽看，繁中可讀且未侵入右側人名、數值或 row 24。

移除唯一 output-only 的 `story_page4_overlay`／`story_page4_invalidations` 後，
控制組與雙倍率原版 JSON 逐欄相同，包含原版事件、檔案操作、記憶體、
indexed framebuffer 與 palette 摘要。三組 memory SHA-256 均為
`76f7360c4d973a357c872d9e8531473e3a51ecfac593a9e3c24722920ec40b48`，
indexed 均為 `4f9d1bb280724737ca72599c3e7d387c23c076f7e0a8637d8d3ebc9164514bf2`。
dosgolem `state-compare` control→2×及 control→3×均 `equal=true`，
machine digest `961639c34e16aacc97eacdc6dd984609e784439a5b5be14f9167551a73f20e63`，
DOS digest `8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。

## 已量 Enter 離頁

私有 `runtime-live-exit-{control,2x,3x}/receipt.json` SHA-256 依序為
`88ee06f5d5dec99a63f893cef2b97528b9bb88456207c39269cf73a1e7d14923`、
`37c2f75be19b85c01b31cda2a294b5f590b60628f3fee27dd1d2631981945628`、
`0043bc6dd4ea924d5a7f3972bc59cae8d9f0e5a7f7c30f30bd141ab7dadb5d38`。雙倍率均於
step `310023777` 的原版 pre-execution `0CF4:1B3A`、`ES:DI=A000:AA08`、
`CX=304` 記錄 `active_keys_before=6`，立即清空六行。終態 active 空、
`drew=false`、RGBA 逐 byte 等於 baseline，安全矩形內外差異皆 0；
原版 JSON 除 output-only 欄位外逐欄等於控制組。`state-compare`
兩倍率均 `equal=true`，machine digest
`a8bf6d4013d78b1273c603da14fabec6d9d63862cf7f3e1da39106bf86355eef`，
DOS digest 同上。

另從已在第四頁的獨立 state `phase104-post-return-enter-4/control.state`
直接送離頁 Enter，沒有清除事件，因新執行的衍生層並未經歷第四頁文字建立；
該組不能證明 active→clear。已以同一次執行的雙 Enter 收據補正，舊嘗試
留在 ignored workspace，不當作通過證據。第一次雙 Enter 命令使用大寫
`1C:0D`，被 CLI 小寫十六進位契約拒絕；以 `1c:0d` 乾淨重跑後才取得上列收據。

## 尚未完成的 CONFORMED 閘門

`go test ./apps/buckrogers ./cmd/buckrogers-text-receipt`、`go vet` 與
`go test -race` 在 Docker 通過；這些與上述正例不能代替完整失敗矩陣。
獨立程式審查曾發現 presenter `Apply` 在逐筆驗證 loop 內就 `layer.Add`：
若後續第 2–6 筆無效，前面的 stamp 可殘留，違反原子失敗即關閉契約。
本機 dosgolem `cad9c3f` 已把「全數驗證」與「一次提交」分成兩個 loop，
並以 2×／3× invalid-tail、mixed generation、duplicate key 驗證零 stamp／
零 RGBA 差異。此勘誤保留，不能讓已修缺陷的成因消失。
本機 `4b07d0c` 另補完整第一行最後 byte 的 SHA mismatch、return
opcode／SS／SP 失敗與不復活負例。尚須獨立驗證 partial／錯序、caller／guard／
style、七欄高位、return caller／step、缺字、非 READY TSV、未知或不相交
寫入，以及相關雙倍率零局部繪製。這些負例通過前，spec 013 **不升
CONFORMED**。
其他離頁、完整開機玩家路徑與遊戲內存讀檔仍是未知，不從本收據外推。

## 2026-09-23 追加稽核與限縮結論

獨立 Terra 在本機 dosgolem `5652f11` 補完七個 ABI word 非零高位、return caller／
predecessor／step、未知與不相交 write 的負例；已存在的完整末字 SHA mismatch、
return opcode／SS／SP、partial、六行原子提交與雙倍率 presenter
invalid-tail／mixed generation／duplicate key 負例一併審閱。主代理於
`6dcc427` 再補正式 loader 的雙倍率 DRAFT catalog 與缺字拒絕，從當前
`6dcc427` Docker 重跑相關 Go test、vet、race 均通過，並回讀本文六份
control／2×／3×穩定與離頁私有收據，雜湊皆與本文相符。程式提交僅增加測試，
未改變重生收據所用的 runtime 路徑；正式 A/B 的範圍仍是同一合法第三頁
終態、既有 BIOS Enter 進入第四頁、再由 Enter 離開的正常執行鏈。

因此規格 013 只在上述雙倍率六行與已量 Enter 離頁升 CONFORMED。這不證明
從完整開機逐步遊玩、其他離頁方式或遊戲內存讀檔；該等項目維持未知，
不能用本頁通過宣稱全遊戲完成。

## 2026-09-24：跨頁引號標點勘誤後重驗

原文 key、事件表、原版遊戲與執行期程式均未修改；僅將正式譯文第六行末尾
`垃圾傾倒場。」` 校為 `垃圾傾倒場。`，使引語留待第五頁結束。
新 TSV SHA-256 為
`c5d8e26d15ea24dc6e464bbf680b89a8deb2d3dd06943bf242a73f51adb46c70`。
使用上文同一合法前態與雙 Enter 排程、原版 `GAME.OVR`、固定 runner，
在無網路 Docker 重生 stable／active→clear 各 control、2×、3×；
本次字型 SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
與本文件早期收據不同，不能宣稱舊畫面逐 byte 不變。

穩定頁雙倍率均啟用六 key、零缺字；文字安全矩形內變動像素為
2× 12,164、3× 25,572，矩形外均為零。控制組與雙倍率的原版 JSON
扣除 output-only 欄位後相同，`state-compare` 均 `equal=true`。
離頁仍在 step `310023777` 由同一 `0CF4:1B3A`／`A000:AA08`／304-byte
原版 pre-write 將 active 6→0；兩倍率 `drew=false`、終態 RGBA
逐 byte 等於 baseline，原版 JSON 與存態比對仍相同。
12 組雙頁完整收據、輸入與 runner 雜湊、逐組結果在 ignored
`workplace/page4-5-punctuation-recheck-20260924/manifest.json`
（SHA-256 `b669b0e887a9ab7ac0e466c70bfc0ccea2679f4dc5c41d5f00426df4316aac23`）。
這只維持原有固定路徑的限縮 CONFORMED，未擴張其他玩家路徑。
