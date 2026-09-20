# 第二十三階段：手冊事件 adapter 規格與正式核心

日期：2026-09-20  
狀態：純核心 READY 且已實作；runtime／renderer 整合仍為 DRAFT。

## 證據審查

第 18 階段的兩次固定狀態重播已證實題首、六筆 fragment、局部 clear 與錯答換題順序；
第 19、20 階段分別用可丟棄 prototype 驗證 generation 狀態機與精確 catalog lookup；
第 21 階段則以原版 consumer 與固定表補齊 1–10 序數橋接。這些證據足以批准不含 hook、
renderer、輸入與版面的純核心，仍不足以批准玩家可見接線。

依 dosgolem 自身的規格驅動開發規則，唯一實作權威建立在其工作分支：
`docs/spec/007-buck-rogers-manual-event-adapter.md`，狀態 READY。規格明列 typed inputs、
狀態轉移、資料 schema、失敗模式、測試矩陣、權利邊界與停止線；「是否涵蓋所有手冊入口」
維持強推論，由未命中不顯示與後續正常玩家路徑 gate 隔離。

## 實作

workplace dosgolem `apps/buckrogers` 新增：

- `Collector`：精確題首建立單調 generation；依 caller 順序收集 page／heading／ordinal；
  亂序、重複、未知 caller、錯誤固定文句及無效頁碼 poison 當前 generation；stale generation
  直接忽略；局部 clear 只清 visible、不破壞 pending。
- `Catalog`：一次性驗證三份嚴格 UTF-8、無 BOM TSV；要求原版序數恰有 1–10、所有鍵唯一、
  event ordinal 存在於橋接表、catalog 無孤兒，再提供 exact-match `Resolve`。
- `DisplayRequest`：固定只有 `Generation`、`EventKey`、`TextKey`、`Translation` 四欄。

核心不 import oracle 或 xlate，不接 hook、不畫圖、不送鍵，也不保存或解析答案。

## 測試與收據

- `go vet ./apps/buckrogers`：通過。
- `go test -race -v ./apps/buckrogers`：所有頂層案例與子案例通過；正式三份 TSV 測試未 skip。
- dosgolem 所有正式 packages（排除 `workplace/`）：通過，含耗時的 `internal/cpu` 完整測試。
- 正式資料正向：`34 / Deimos Prison / tenth` 產生唯一顯示請求。
- 正式資料未命中：`41 / Technical Skills / second` 因未有校訂 catalog 條目而不顯示。
- malformed 反例含 BOM、無效 UTF-8、重複 identity／event key／text key／catalog key、孤兒、
  ordinal 缺號／多對一及 event ordinal 不在原版橋接表，皆拒絕整份載入。

檔案 SHA-256：

- `apps/buckrogers/manual.go`：
  `6d57f99e0ae023c12b9857d894a17209792c3e1d704e9fcbefbc6e20a431b49b`
- `apps/buckrogers/manual_test.go`：
  `a0869557184ae9415752b9c419e6ccef232c9c1fe3ea61f903972ca44dd3ffd4`
- READY 規格：
  `01e96cb28b9291d40362617838b4424a7e58e72a9b2113ffa41f780371daa475`

本機 dosgolem commit：`8ce092f29d000ea7e6765c4f3389fe484aefa555`；分支
`buck-rogers-cht-output-overlay`，未推送遠端。

## 結論與剩餘閘門

第 19、20 階段 prototype 已轉成有 READY 規格與正式 Go 測試的純核心，不再需要 Python
prototype 承擔產品契約。但這不是畫面功能完成：正式 hook guard、2×／3× 選擇、overlay
生命週期、分頁輸入與正常玩家路徑 A/B 尚未完成，因此總體手冊覆繪規格仍為 DRAFT。
