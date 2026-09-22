# 第一百二十一階段：手冊成功返回 savestate restore 邊界

日期：2026-09-22
狀態：**已確認 dosgolem savestate restore 後不會復活衍生手冊覆繪；遊戲內保存／讀檔仍未驗收。**

## 範圍與輸入

本階段只重載第一百零四階段手冊正確作答後的既有本機終態
`workplace/phase104-manual-correct-return/control.state`，而不是送出新的原版
鍵盤輸入。該輸入 state SHA-256 為
`b99e17c7e2a4affffa746a208637dbec3f315550b64edc0699c044dd21ce99b6`，起點為
dosgolem 虛擬指令步 `280000000`。

原版目錄僅以唯讀 `/orig` 掛載；輸出、state、字型與收據只留在被 Git 忽略的
`workplace/phase120-restored-success-state/`。使用的本機 961 glyph top-pad 字型
SHA-256 為 `7e8f5d0e70cc75505279de0575b3bcc489c0b0901ddc3c39c179124c9e544b18`，與
第一百零四階段相同。收據不保存原版文字、答案、鍵盤排程、原版檔案內容或字型 bytes。

這裡的 **savestate restore** 是 dosgolem 對上述 machine／DOS 快照的重新載入；它
**不是**原版遊戲內「保存」選單寫檔後再「讀檔」的玩家流程，兩者不可互換。

## A/B 結果

以 `tools/manual_runtime_smoke.py` 從該 state 無鍵重播至 `281000000`，各產生無覆繪
control、2× overlay、3× overlay 與完整持久化 state 比較。兩個倍率的結果如下：

| 倍率 | overlay 與 baseline RGBA | 正文內差異 | 安全矩形外差異 | 原始 state 與 control |
| --- | --- | ---: | ---: | --- |
| 2× | SHA-256 相同：`edbbe358…5db9d` | 0 px | 0 px | 相等 |
| 3× | SHA-256 相同：`7a101b0f…b6544` | 0 px | 0 px | 相等 |

兩列均為 `visible=false`，且收據 `original_state_identical=true`。因此，從成功返回
終態重新建構 presenter 時，沒有舊的手冊 generation、style 或文字 stamp 被衍生層帶回；
這個已還原的畫面保持原版 baseline。

既有單元測試
`TestRuntimeManualOverlayFreshAfterRestoreHasNoDerivedLayer` 亦在 Docker 內通過。它驗證
新建的 runtime presenter 沒有 style、active key 或繪製結果，且回傳未覆繪的 baseline；
此測試是純核心補強，不取代上述原版 state A/B。

## 遊戲內保存／讀檔停止線

第一百零四階段已明確記錄：成功返回後只量到連續敘事頁，不能把建角流程的保存／載入
收據拼接成此手冊分支的驗收。其後第一百一十二階段僅有中文手冊明示的數字鍵盤 4／6
輸入；該 pair 沒有證明轉向實際生效，更沒有提供保存入口、讀檔入口或不同可比玩家狀態。

因此目前沒有「手冊成功返回 → 合法遊戲內保存 → 離開／讀檔 → 返回同一畫面」的既有
checkpoint、已證實按鍵或正常玩家收據。不得猜測 scan code、使用 debug／直接寫 state、
繞過手冊判定，或把本階段的 savestate restore 說成遊戲內 save/load 驗收。

下一個窄切片只應追出同一分支的第一個有證據的遊戲內保存入口與對應讀檔返回邊；取得前，
本分支停止。

## catalog／字型現況勘誤

`docs/spec/002-manual-paragraph-overlay-draft.md` 保留的 22 筆／691 glyph 是歷史 DRAFT
閘門。2026-09-22 的現況勘誤已追加至該規格：手冊 catalog 為第一百階段證實的 39／39；
第一百零四與本階段使用 961 glyph 手冊 runtime 字型；第一百一十八階段的 997 glyph 是
故事 DRAFT catalog 聯集，不能拿來改寫手冊 runtime 的來源或驗收範圍。

## 環境與清理

所有重播與單元測試均在一次性、無網路 Docker 容器中執行；原版掛載唯讀，容器使用目前
使用者 UID/GID。確認沒有遺留專案容器、root-owned 產物或誤建的 `.md` 目錄。第一次未掛
`/orig` 的嘗試只建立空的 ignored 輸出目錄，已在重跑前移除；最終收據為上述完整輸出。
