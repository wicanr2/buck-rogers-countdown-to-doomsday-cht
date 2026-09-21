# 第七十階段：職業技能配置靜態文字繁中請求

日期：2026-09-21  
狀態：完成

## 結論

職業技能配置畫面的四個標題與八個技能名稱已建立 exact 繁中 request。初始注意力 selected 與
Down 後無重力行動 selected 以不同 identity 命中同一技能 text key；所有動態點數維持原版
事件與 catalog miss。

## 正式資料

- events：14 identities；SHA-256
  `3d0bde60cfe3fb4bc9db9853ca969a9062c8b56a29a7dd147a8f59122b3e0613`。
- 譯文：12 text keys；SHA-256
  `96624a20a2f6e4b90d33d6447066400a137e6574fd82811624962867a97a4161`。
- 八個技能譯名逐筆反查 `character-sheet.zh-TW.tsv`，來源為 `manual-and-runtime`；四個畫面標題
  為 `runtime-interface`。完整英文不存入正式 catalog。

## 正常路徑收據

| 路徑 | events | control requests／misses | catalog requests／misses | framebuffer SHA-256 |
|---|---:|---:|---:|---|
| `A`→Enter base | 226 | 1／225 | 14／212 | `a1cd728c…95f7` |
| base→Down | 234 | 1／233 | 16／218 | `ddf66e0c…c6cbd` |

兩路的 control 與 catalog 都各重播兩次；JSON、64,000-byte framebuffer 各自逐位元一致。
移除 `requests`／`catalog_misses` 後，catalog JSON 完全等於 control。Down 新增的兩筆 request
依序是注意力一般色重畫與無重力行動選取色重畫。

## 邊界

未實測的其他技能 selected variants 不進 catalog；row 1／2 剩餘點數與每列 points／bonus／
total 都保持 miss。底部 ADD／SUBTRACT／DONE 並非本批 dispatcher 事件。本階段不證明安全
矩形、繁中像素覆繪或技能規則。
