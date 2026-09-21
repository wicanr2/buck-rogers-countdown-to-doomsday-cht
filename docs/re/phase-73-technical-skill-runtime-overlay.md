# 第七十三階段：技術技能配置執行期繁中覆繪

日期：2026-09-21  
狀態：完成

## 結論

技術技能頁的 17 個專屬 exact identities 已建立安全矩形，並與兩個 career 共享標題矩形合併
接入 dosgolem 長存 runtime overlay。base 與 Down 的 2×／3× 收據都只改輸出 RGBA；原版
framebuffer、events、BIOS keys 與動態技能點數不變。

## 穩定 frame 訂正

首次沿用第 72 階段 request 收據的停止點時，selected stamp 已進 active keys、但仍處於
`Pending`，PNG 因尚未跨過垂直回掃而露出英文。規格隨即退回 DRAFT。將 base／Down 停止點
分別延後至 103,500,000／103,800,000 後，沒有新增文字事件，selected stamp 進入 `Shown`，
繁中正常顯示。這是測試觀測點錯誤，不是通用 renderer 或清除 hook 缺陷。

因此覆繪驗收不能只看 active keys 與 containment；必須停在下一個穩定 frame 並目視輸出。

## 正式收據

| 路徑 | events／requests／misses | 2× 矩形內差異 | 3× 矩形內差異 | 矩形外／動態欄 |
|---|---:|---:|---:|---:|
| base | 289／32／257 | 16,611 px | 34,423 px | 0／0 px |
| Down | 297／34／263 | 16,611 px | 34,423 px | 0／0 px |

正式 verifier 為 `tools/technical_skill_runtime_overlay_receipt.py`；本機收據保存在忽略版控的
`workplace/phase73/`。字型 SHA-256 為
`2a9c858becca4b65d30f1bc8f337d83aea7f2df8ad6cc7bebf4ddb43fadf7b99`。

## 人工檢查與邊界

四張 2×／3× base／Down PNG 均確認 selected 色隨選取列移動，沒有英文殘字、裁切、重疊或
數值污染。底部 ADD／SUBTRACT／PREV／NEXT／DONE 仍不是本階段 dispatcher catalog 的一部分；
產品預設倍率與手冊版面仍待使用者決策。
