# 第一百五十四階段：雙倍率面板空白點擊與滑鼠釋放原型

日期：2026-09-23  
狀態：**僅 ignored Linux／Xvfb／Ebitengine 原型；MouseBridge 與正式前端仍為 DRAFT。**

Terra 在 `workplace/phase118-game-ebiten-active-story/` 以真實 X11／Ebitengine
事件重播 2×／3× 的面板 Open 命中、面板一般命中與面板空白 miss 的
Down／Up。私有 `out/phase151-open-panel-all-pointer-2x-v3/mouse-receipt.json`
SHA-256 為 `e8301562ec2c469efbb7b6816da7870e3c3d4e47ee774f5faf2c686f78d6a727`；
3× 對應收據為 `7ae7ea321bab4a0723afba448c57d7eb9dfd4e3cd3f8db83d2ab8b42f6fdfca8`。
六事件對 DOS mouse API 呼叫均為空，按鍵及座標維持 `(160,100,b0)`，
BIOS pending／鍵盤 IRQ／indexed 畫面在 API 邊界不變。

已命中的事件之面板核心與整合路由都回 `{consumed:true,forward:false}`；
**空白 miss 的面板核心仍回 `{false,false}`**，只有可丟棄整合政策把它改成
`{true,false}`。正式契約必須讓面板開啟時空白 pointer miss 也由 host
消費，不能依賴原型局部補丁。這是規格與接線缺口，不是 DOS 已收到點擊。

閉面板畫布內 Down／Up 亦重跑：2×／3× 收據 SHA-256 分別為
`66bd323ad5ac88866b2130e99053f39b051a8c67d4727d8995bdbc630d9bd6e0`、
`e825b2600f81b722220d0c1e352d88d5c18fa8c02ca8adcc15af27e9ff8964d7`，
均記錄 `Move(100,82)→Press→Move(100,82)→Release`。

依使用者已定案的離界清理規則，再重播 2×／3×各四種
canvas-out／chrome／panel／focus-loss。每案都恰為
`Move(100,82)→Press→Release`，不在 release 前再次 Move；終態
`(100,82,b0)`。私有 `out/phase152-cleanup-<scale>x-<case>/mouse-receipt.json`
的 SHA-256：2×依序為
`98bdbdf0ba8a2d5945a62e063e8ca7d521a75e80584134e2a7a5a2dbd23be1ab`、
`f04c02991f818889d4bdf85c72fade3bbbc616eb4a53aa768420bc3244c23f90`、
`3a8583b8db71e316c7fbfecdb6a935fa95d29bf56faca02113c990f298125af9`、
`804c0ecd920c7bdc7f992bc5d531ba40c37966e3fa74860cd2aa9503d9fd7001`；
3×依序為
`f8c03ffeea6aec1c3add824b0c4bfbc6f12beae39f88c08529d9ecfa24090158`、
`0fa07ea16aee7acdbe13268b2eaa7d97b114b687a8eed43a7f247303ae60cadd`、
`bb409148c754d6ad9811ccd6bf13a3579aa4f8cd7da676cb787a9b8d56f682d7`、
`4fd6bb515cd0def8d445a41e25e647eb6868a4bf961f08edf0757d92d765f3e5`。
focus-loss 是真實 `ebiten.IsFocused` true→false。原型 `go test -race -count=1 ./...`
通過。

限制：panel cleanup 是原型先接受 Down、再開面板的人工前提；
未驗正式視窗的 pointer capture、多鍵或觸控。面板展開可能在同一次
實體點擊的 Up 前改變 layout 高度，使 Ebitengine 重映射座標；正式
host route 應按已按下的 host target 消費 Up，不能依新座標轉送 DOS。
50k step 後 machine-memory hash 曾變，但尚未歸因滑鼠；本收據只主張
上述 API 邊界，不宣稱正常玩家路徑已可用滑鼠操作。
