# 第二百零四階段：技能操作列完整清底的正式執行期 A/B

日期：2026-09-24
狀態：**僅八條已量技能操作路徑、技術技能頁 Escape→Y 離頁及 2×／3× 無頭輸出限縮 CONFORMED。**

## 問題與勘誤

[第九十九階段](phase-99-action-bar-3x-density.md)確認 3× 中文字體較大、字距較緊，
但當時只驗差異落在核准矩形，沒有驗證原版英文是否完全清除。這次檢查正式 PNG
發現較短的 `(S)減點` 等譯文之後仍有原版 `SUBTRACT` 等尾字。
舊 `RuntimeActionBarOverlay.Draw` 只在譯文 28 logical-pixel 寬度內覆畫，
未清除原版標籤的剩餘寬度；因此先前「矩形外零差」不能作為無英文殘字的證據。

本機 dosgolem fork 現於繪製前，以已核准的**完整原版標籤矩形**及該標籤
normal／focus 背景色清底，再繪製五字混合寬度譯文。只有整組 stamp 均達
`Shown` 才清底、顯示；不完整組合失敗即關閉。indexed framebuffer、
原版記憶體與 DOS 輸入均不寫回。此修正與回歸測試在本機 fork commit
`674e3e3fcbf8e36d5ac115da9e9b5bf685564339`，正式契約見其
`docs/spec/215-buck-rogers-skill-action-bar-runtime-overlay.md`。

## 固定輸入與收據

從同一合法角色建立 state `workplace/phase66/fixed-after-bios-space-100m.state`
起跑，其 SHA-256 為
`209a78934d9936fd9b6a9e28cd5e51da294dd459b4ce6abab47a36a284aa2cc5`。
八條操作路徑沿第七十五階段已固定的 BIOS 鍵序；第九條 technical-exit
沿第二百零二階段已證實的 Escape→Y 路徑。每條各取 control、2×、3×
兩次重播，開啟 `-file-ops -key-trace`。原版遊戲、state、字型、PNG、
indexed 與完整 JSON 均只在 ignored `workplace/phase204-actionbar-ab/`，
不進 Git／GitHub。

乾淨建置的 runner SHA-256 為
`ccb6f8cb761f0265c9d881bf7f81087e4a9985050cd92d1b7857680b53c40a1d`，
Go VCS revision 為上述 fork commit、`vcs.modified=false`；本機倚天
字型 SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
私有 `README.md`、`run.sh`、`verify.py` 分別釘在 SHA-256
`cebe060e1f9488c559ff29ed2daca0635d72a43ad1346d5f5d0b463adea322dc`、
`83a462f5f86a6fe1b6f623c8171722a739d0999a15e83ebedc698c0d2b916dc6`、
`10979385ad74df5098ab451e80d3def35364b9031f306a5afb66c5009298e0a9`。
這些雜湊只供本機重生辨識，不轉移原版、手冊或字型的散布權。

## 同狀態觀測

| 固定路徑 | 原版文字事件 | 2× 差異像素 | 3× 差異像素 |
| --- | ---: | ---: | ---: |
| career-base | 3 | 1,377 | 3,026 |
| career-subtract | 6 | 1,185 | 2,562 |
| career-done | 9 | 1,189 | 2,567 |
| technical-base | 8 | 2,014 | 4,340 |
| technical-subtract | 13 | 1,822 | 3,876 |
| technical-prev | 18 | 1,822 | 3,876 |
| technical-next | 23 | 1,826 | 3,881 |
| technical-done | 28 | 1,826 | 3,881 |
| technical-exit | — | 0 | 0 |

各路徑兩次重播的原始 JSON、indexed、RGBA 與 PNG 逐位元組相同。
control 與覆繪組的 JSON 除 `action_bar_overlay` 呈現欄外相同，
indexed framebuffer 完全相同。active 畫面只在已核准 row 24
操作列矩形內有 RGBA 差異；較長原版標籤的譯文後尾段皆為單一背景色。
修正前 runner 在相同 verifier 的尾段檢查中如預期失敗；修正前後
新增的像素變更亦只在這些英文尾段。兩張代表性 2×／3× PNG 已目視核對：
無殘英文、無裁字或底框侵入；normal 僅括號內助記字母白色，
括號與繁中保持原版配色，focus 保持白底黑字。3× 中文使用
22×22 字模、兩字距兩像素，2× 配置不變。

技術技能頁 Escape→Y 離頁後 action group 數為零，覆繪 RGBA
逐位元組等於 control；這只覆蓋該固定離頁，不代表所有轉場。
正式 Go 定向 test、vet、race 均通過；獨立審查核對清底只在 RGBA、
相鄰矩形不重疊、未全數顯示的群組失敗即關閉及同狀態負控制。

## 限制與後續

本階段只證實上述固定原版路徑、正常／焦點狀態和 2×／3× 輸出。
disabled 標籤、未量的焦點／重入、完整冷開機、遊戲內存讀檔、
Restore bridge 及 Linux 玩家視窗仍未知或待驗。原版助記字母的
直接鍵盤功能未由本覆繪收據證實，保留原樣而不改輸入語意。
因此相關 Issue 仍應開啟；不能把操作列的限縮驗收當作整個遊戲中文化完成。
