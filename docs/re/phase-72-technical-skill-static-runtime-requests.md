# 第七十二階段：技術技能配置靜態繁中請求

日期：2026-09-21  
狀態：完成

## 結論

技術技能配置畫面的兩個專屬標題、13 個技能一般列及前兩列 selected variants 已建立
17 個 content-safe exact identities，並由 dosgolem guarded post-call watcher 產生繁中
`DisplayRequest`。動態剩餘點數、points／bonus／total 與未實測 selected variants 仍是 miss。

## 中文來源

13 個技能譯名都以中文手冊 `SCAN0352_012.jpg` 第 19–20 頁原圖逐字校訂；該掃描圖
SHA-256 為 `dd4cec6e97c8077d59ede60bb9f40a6ff7bf8d73d274b178055a27e7436674be`。
正式 catalog 不保存掃描圖或完整英文。

## 共享 identity 勘誤

首次將四個標題全部收入 technical catalog 時，dosgolem 合併拒絕兩個重複 identity。
查證後確認「單項技能上限」與「點數／加值／總計」在兩個技能頁的長度、hash、caller、
色號與座標全部相同，是同一 exact identity。spec 211 曾退回 DRAFT，修正為共享已
CONFORMED 的 career identities，technical flags 也必須與 career catalog 一起提供。

## 正式收據

| 路徑 | events | control requests／misses | catalog requests／misses | framebuffer SHA-256 |
|---|---:|---:|---:|---|
| base | 289 | 16／273 | 32／257 | `6bf7f9bb…432a` |
| Down | 297 | 16／281 | 34／263 | `8990a6cb…0729e` |

兩路 control／catalog 都各重播兩次；JSON 與 64,000-byte framebuffer 各自逐位元一致。
移除 `requests`／`catalog_misses` 後，catalog JSON 完全等於 control。Down 新增的兩筆請求
依序為第一列 normal 與第二列 selected。

正式 events／譯文 SHA-256 分別為
`d593b4bcc8b05dea1b8c86cbd8024d5e78bd9be846eac1e3f707e6b57e52b57a`、
`7524444a17ff5cb3bc5e2dddbdd21b4ce3bc75ba9774a7d6141d4c2bcb9cece3`。

## 邊界

本階段只完成 request，尚未建立安全矩形或繪製繁中像素；不得據此宣稱技術技能頁
已完成畫面中文化。
