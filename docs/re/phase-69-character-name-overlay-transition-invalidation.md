# 第六十九階段：角色姓名覆繪轉場失效生命週期

日期：2026-09-21  
狀態：完成

## 結論

Enter 確認姓名後，原版通用清除矩形已使 `character.name.prompt` stamp 失效，技能配置頁沒有
繁中殘留。Escape 並非取消；它重印同一提示並留在姓名畫面，runtime 以同 key replace，終態
只保留一份 stamp。

## 正常路徑收據

| 分支 | events／requests／misses | 終態 active keys | drew | 2× JSON | 3× JSON |
|---|---:|---|---|---|---|
| `A`→Enter | 226／1／225 | 空 | false | `18be6427…5f0a` | `d77d7e18…3851` |
| Escape | 184／2／182 | `character.name.prompt` 一筆 | true | `220087a2…ddb1` | `562afa6f…0442` |

兩分支的 control、2×、3× 都各重跑兩次；JSON、RGBA、baseline、raw framebuffer 逐位元一致，
且 presentation 欄位外的 JSON 等於 control。Enter 的 2×／3× RGBA 完全等於 baseline；Escape
仍只有核准提示矩形內 941／2,038 pixels 差異，矩形外與玩家輸入欄皆為 0。

## 原版行為與實作邊界

- Enter 終態 raw framebuffer SHA-256：
  `a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7`。
- Escape 終態 raw framebuffer SHA-256：
  `55da7c0e296b882f99c7c8ba2550743debe93a8bc480d1a0fc8fbb1dc514a6bb`。
- 首次正式 overlay 重播因命令把合法空終態的 `drew=false` 當錯誤而停止。spec 208 只訂正
  收據表示：有 presenter 時明示 drew true／false，且它必須與 active keys 是否為空一致。
- 沒有依姓名 event key 新增清除；失效仍由已證實的 `026F:029C` 原版矩形 hook 驅動。

原始解析度圖已人工確認 Enter 顯示乾淨技能配置頁，Escape 留在角色資料／姓名畫面並只顯示
一份繁中提示。本階段沒有翻譯技能頁文字或選定產品倍率。
