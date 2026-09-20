# 第二階段目標：文字分派與生命週期證據

狀態：已完成（DRAFT 前置證據已建立；production 覆繪仍未授權）  
日期：2026-09-20  
前一階段：[可觀測的原版啟動與文字輸出基線](phase-1-observable-original.md)  
工作追蹤：[GitHub Issue #3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後須先被讀回，才可作為本輪工作範圍。開工前已載入專案 `AGENTS.md`、
`CONTEXT.md`、第一階段收據、復古遊戲路由、`reverse-engineer-retro-game-remake` 與
`grilling` 的入口規範。

## 目標

在不改動原版 EXE、資料、規則、存檔或手冊判定的前提下，從第一階段的功能選單收據
追出高層文字／glyph 分派與畫面生命週期的最小充分原版證據，讓下一份「輸出端繁中
覆繪」DRAFT 規格能以可審查欄位描述 hook、原文顯示鍵、繪製範圍與失效時機。

專案的既定產品定位是 dosgolem 輸出端繁中覆繪，**不是 clean-room remake**。目前活躍
目標中「完成 remake」一詞與此定位衝突；本階段不自行把它改成重寫引擎的授權，只做
兩種方向都需要的原版證據與 DRAFT 前置工作，並把方向決策保留給使用者。

## 成功定義

1. 以第一階段的固定狀態與 BIOS BDA 輸入，建立文字 primitive 以上至少一層的可重生
   分派證據，或精確記錄 dosgolem 所缺的最小觀測能力。
2. 對字元／字串資料來源、編碼、座標／矩形、字型、色彩、清除與捲動至少逐項更新為
   已證實、強推論、假說或未知；不以推測位址命名取代原始定位。
3. 若證據足夠，新增一份只屬 DRAFT 的覆繪規格；若不足，文件化阻擋它成為 READY 的
   最小未知與下一個 probe。
4. 本輪完成後驗證工作樹、Docker 衛生與文件連結，推送 `main`，並在相關 GitHub Issue
   留下證據連結與真實狀態。

## 不屬於本階段

- 不寫中文譯文、字型、adapter、遊戲引擎或任何 production hook。
- 不把 RAR 手冊內容未解的部分假裝成可用段落。
- 不以 DOSBox／DOSBox-X 取代 dosgolem 原版收據。
- 不決定「輸出端中文化」是否改為「完整 remake」；這是使用者的範圍決策。

## 退出條件

當上述成功定義均以 dosgolem 可重生收據與分級研究文件佐證後，本階段結束。若 first
blocker 是 dosgolem 通用觀測缺口，必須先把缺口與 DRAFT 寫清楚；不得修改正式路徑來
繞過它。

## 完成收據

- [文字分派與生命週期追蹤](../re/phase-2-text-dispatch-and-lifecycle.md) 證實長度前綴
  ASCII 資料、字元 renderer、glyph primitive、色彩與 40×25 文字格座標。
- [功能選單文字輸出端覆繪 DRAFT](../spec/001-menu-text-output-overdraw-draft.md) 定義正式
  實作前仍須解開的生命週期與中文字型閘門。
