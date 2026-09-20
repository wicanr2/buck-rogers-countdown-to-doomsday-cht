# 第七階段目標：文字 post-call 與 generation 事件

狀態：已完成（post-call、stack 護欄與 generation 順序已有可重生收據）  
日期：2026-09-20  
前置：[第六階段清除路徑與失效 hook 證據](phase-6-clear-path-hook-evidence.md)  
工作追蹤：[GitHub Issue #3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可開始探查。本輪維持 dosgolem 執行期輸出端繁體中文化；使用
被忽略的 `workplace/dosgolem/` 分支 `buck-rogers-cht-output-overlay`。不修改原版 EXE、資料、
規則、手冊驗證或存檔語意，也不把一次性 probe 直接併入 production adapter。

## 目標

找出 `0763:0424` 原版字串 dispatcher 在完成整段英文繪製後可重現的 return／post-call
觀測點，並與 `026F:029C` 矩形失效事件排成有證據的時間序列。成果用來判斷 dosgolem
現有 `OnCall` 能力是否足夠，或是否需要一個通用且可測的 post-call／return hook；本階段
只更新研究證據與 DRAFT，不建立正式中文覆繪。

## 成功定義

1. 由固定輸入與既有功能選單狀態重播至少一條正常玩家路徑，保存 `0763:0424` 的 callsite、
   caller return 位址、stack／暫存器、原文來源與繪製前後的指令序號；地址均標明 dosgolem
   實模式位址空間。
2. 證實 post-call 事件發生時整段原版 glyph 已完成，而非只到 dispatcher 入口；至少用
   一個已知字串的末端 glyph 像素或等價 VRAM 證據支持。
3. 對 Enter 向前或 Escape 返回路徑，把 `026F:029C` 矩形清除、dispatcher entry、post-call
   與下一次文字事件依序列出，判斷 generation 邊界能否形成不殘字的可測契約。
4. 檢查 dosgolem 現有 API／machine step 邊界；若缺 post-call 能力，只提出最小通用設計與
   測試，不在 DRAFT 升為 READY 前寫 production hook。
5. 更新 `docs/re/`、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；完成後做 Docker 衛生檢查，
   推送 `main` 並更新 Issues #3、#4。

## 不屬於本階段

- 不繪製繁中、不決定字型、不建立正式翻譯 catalog。
- 不以 dispatcher entry 冒充整段繪製完成，也不以單一 caller 樣本宣稱涵蓋所有輸出路徑。
- 不修改 dosgolem CPU／DOS／VGA 語意，除非證據顯示通用觀測 API 有獨立缺口；即使如此，
  也先寫 READY 規格與測試契約，不能由探針直接進 production。

## 退出條件

成功定義均由可重生的 dosgolem 收據支持，且 DRAFT 明確記錄已證實順序、未涵蓋 caller 與
下一個最小缺口後結束。若現有 API 無法表達 post-call，必須把缺口與最小介面契約寫清楚，
不得以輪詢畫面穩定、固定延遲或猜測指令數替代。

## 完成收據

[第七階段研究證據](../re/phase-7-text-post-call-generation-event.md)保存第一筆已知字串的
entry／末 glyph／post-call 時序、九筆 entry／return 的 `SS:SP` 配對、自然 fall-through
反例、IDA 9.4 caller 與 dispatcher 尾端，以及不需先擴充 dosgolem API 的 DRAFT 護欄。
