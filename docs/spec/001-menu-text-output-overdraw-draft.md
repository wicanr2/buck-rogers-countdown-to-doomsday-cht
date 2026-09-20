# DRAFT：功能選單文字輸出端覆繪

狀態：DRAFT — 禁止據此實作 production hook  
日期：2026-09-20  
證據：[第二階段文字分派與生命週期追蹤](../re/phase-2-text-dispatch-and-lifecycle.md)、
[第四階段向前轉場](../re/phase-4-menu-interaction-lifecycle.md)、
[第五階段 Escape 返回](../re/phase-5-pick-race-return-lifecycle.md)、
[第六階段清除路徑與 hook 邊界](../re/phase-6-clear-path-hook-evidence.md)、
[第七階段 post-call 與 generation 事件](../re/phase-7-text-post-call-generation-event.md)、
[第八階段字型與版面 prototype](../re/phase-8-menu-font-layout-prototype.md)、
[第二十八階段顯示請求純核心](../re/phase-28-menu-display-request-core.md)、
[第二十九階段執行期顯示請求 watcher](../re/phase-29-menu-runtime-request-watcher.md)、
[第三十階段反白與文字安全矩形](../re/phase-30-race-selection-highlight-lifecycle.md)

## 玩家可見範圍

此規格只描述原版由標題進入功能選單時、以 `0763:0424` 分派的長度前綴 ASCII 字串。
目標方向仍是「保留原版語意，只在原始輸出後覆繪繁中」，不改 EXE、遊戲規則、手冊驗證、
檔名或存檔。它不涵蓋劇情、戰鬥、角色／物品名稱、手冊提示或任何中文內容。

## 已證實輸入與事件形狀

原版輸入、雜湊、dosgolem commit 與地址空間均見研究證據。對此選單樣本，`0763:0424`
接收下列原始資料：

```text
source: far pointer ES:DI → [length:u8][original_bytes:length]
style/page: u8（完整語意未證實）
background_palette_index: u8
foreground_palette_index: u8
row: u8, 0..24
column: u8, 0..39
```

原版會把字串複製到 stack buffer，再逐 byte 呼叫 `0763:026B`，最後由 `0763:1809` 與
`0763:183A..1863` 畫出 8×8 glyph。可測得的原文畫面矩形為：

```text
x = column × 8
y = row × 8
width = length × 8
height = 8
```

`source` 的內容僅能作顯示比對鍵；繁中不得進入原版比較、資源查找、序列化、檔案路徑或
存檔名稱。第 27 階段已用 `text/menu-events.tsv` 定義九筆 content-free identity：穩定
event／text key 加原文長度／SHA-256、caller、色號與文字格座標；repo 不保存原版文字 catalog。

## DRAFT 覆繪生命週期

若未來證據審查通過，候選事件必須按以下順序運作：

1. 原版完整執行 `0763:0424` 的字串繪製；不得提前跳過或替換。
2. 僅在已核准的原文顯示鍵、同一個 row／column 與計算後 text-safe rectangle 上，清除
   原文墨跡並畫出繁中 glyph。
3. 原版的下一次重繪、游標、翻頁、捲動、切換畫面、離開或載入狀態必須使覆繪失效或重建；
   不得留殘字。
4. 同一初始狀態、相同輸入與固定 seed（若該路徑引入 RNG）下，原文與繁中執行的原版狀態
   必須一致；允許差異只可出現在經核准的覆繪像素。

### 已量到的轉場失效證據

由功能選單固定狀態送入 BIOS Enter 時，原版在 #100,010,174 接受輸入，於 #100,010,490
先發生一筆轉場中的 `0763:0424` dispatcher，卻到 #100,031,031 才由 watchpoint 當時標為
`0CF4:1B3C` 的路徑將已證實的
舊選單像素 `A000:838A` 從 `0x0A` 清為 `0x00`。完整收據見
[第四階段選單互動與失效生命週期](../re/phase-4-menu-interaction-lifecycle.md)。

第七階段進一步證實該第一筆內容仍是舊功能選單的 `Create New Character` 重畫；真正的
矩形清除完成後，#100,033,190 才開始下一筆已觀測文字。因此不能把 #100,010,490 稱為
新畫面的第一筆文字。

所以 DRAFT 的保守規則是：在原版接受可造成轉場的輸入時，現有 overlay 必須立即標示為
失效；不得把「首次看到下一筆字串事件」當成原畫面已清除的證據。這只是失效策略候選，
尚未證實哪一個通用 dosgolem hook 可正確辨識所有轉場。

反向返回亦有相同順序：Escape 在 #100,310,138 被原版取走，#100,310,464 已發生第一筆
dispatcher，但 `PICK RACE` 標題像素到 #100,316,673 才由相同路徑清除；終點
逐位元回到既有功能選單基線。這使保守失效規則同時有進入與返回兩個正常玩家路徑支持，
但仍不能僅憑兩個像素樣本把該寫入端宣稱為通用清畫面 hook。

### 已證實的矩形失效候選

第六階段訂正 watchpoint 地址：實際寫入指令是 `0CF4:1B3A REP STOSB`，`1B3C` 是下一個 IP；
`0CF4:1B2B` 函式只是任意 far pointer 的 byte-fill，已排除為正式 hook。兩條路徑真正共用的
上層事件是 `026F:029C`：在 `DS:3C78 == 3` 的 Mode 13h 分支，它把四個邏輯文字格參數
換算成像素矩形，再逐列填 0。

DRAFT 候選契約因此縮小為：固定輸入雜湊與 runtime bytes 簽章均相符時，在
`026F:029C` 進入點讀取 `bottom/right/top/left` 四個低 byte；若範圍合法且模式為 3，將
`[left×8, top×8, (right+1)×8, (bottom+1)×8)` 內相交的既有 overlay 標為失效，然後讓原版
函式完整執行。Enter 樣本矩形為 `x=8..311, y=16..183`；Escape 返回為
`x=0..311, y=0..183`。第七階段已在 DRAFT 事件層接上 post-call 重建候選；尚未由 adapter
prototype 與 A/B 像素收據驗證。

### 已證實的 post-call 候選

第七階段由已知 `Create New Character` 樣本證實：`0763:0424` entry 位於
#100,010,490，最後一個 glyph 的 64 個像素到 #100,025,833 全部寫完，caller return
`37F1:1856` 則在 #100,025,943 才成為下一道指令。dispatcher 以 `RETF 0Ch` 返回，因此
entry `SS:SP` 到 post-call 固定增加 `0x10`；該 Enter 畫面的九筆樣本全部符合。

但 return address 不可單獨作事件：`37F1:15BD` 曾在沒有相應 pending dispatcher 的情況下
自然 fall-through。DRAFT 的 guarded post-call 契約為：entry 時立即複製顯示輸入，以
`Caller()`、entry `SS:SP` 建立 pending frame；return hook 只有在 address、`SS` 與
`SP == entry SP + 0x10` 同時符合時，才可送出這一筆原文已完成的覆繪事件。每個 return
address 只註冊一次，其餘自然命中必須忽略。

同一路徑的 generation 順序已量到：舊選單 post-call #100,025,943 → 矩形失效 entry
#100,028,739 → 清除返回 #100,032,997 → 新畫面 dispatcher #100,033,190 → 新畫面 post-call
#100,040,266。故矩形清除負責使相交 overlay 失效，各文字 post-call 負責重建；不能用任意
dispatcher entry 或固定延遲切 generation。

### 已證實的種族選單反白生命週期

第三十階段在穩定種族選單送入正常 BIOS Down：原 Terran 先由 `37F1:1856` 以
`bg/fg=0/10`、row/col `3,3` 重畫完成，再由 `37F1:175D` 以 `15/0`、`4,3` 反白
Martian。Up 先 normal redraw Martian，再 selected redraw Terran。相同終點下，Down 只改
`(24,24)–(79,39)` 的兩列；Up 後逐位元回到 steady。

因此 selection overlay 不能只在畫面進入時建立；每筆 exact normal／selected post-call 都是
同一列中文覆繪重建候選。`text/menu-text-safe-rects.tsv` 已把原文清除矩形與中文 draw anchor
分離：一般選項清除 col 1 起的含縮排原文，但中文從 col 3 畫。第三十一階段已將三筆新
variant 納入正式 exact catalog；固定 Enter→Down→Up 路徑的 13 筆 post-call 全數產生
request 且零 miss，仍不得用座標或 text key 模糊接線。

第三十三階段又在 #100,220,000–#109,990,000 每 10,000 steps 取樣：完整 palette 全程
唯一，色號 0 與 15 的 RGB 都固定為黑色；selected Terran／Martian 完成重畫後，其 region
hash 直到窗口終點都不再變。故本窗口內 selected row 是穩定黑底黑字，而非 palette blink
或週期性 pixel redraw。忠實覆繪候選必須保留這項不可見 selection style；不得擅自換成
白底、反色或現代游標。窗口外仍未知，正式 adapter 需用連續 runtime A/B 限定完成聲明。

### 已符合的倍率中立純覆繪核心

第三十四階段已把第 32 階段診斷命令中的 stamp 建構、ink rectangle 與 containment 規則，
依 dosgolem `015-buck-rogers-menu-overlay-core` READY 子規格移入 `apps/buckrogers`。核心只接受
明示倍率，沒有產品預設值；2×／3× 四組真實 framebuffer 重生的繁中 PNG、base PNG 與
JSON 全部逐 byte 等於既有基線。診斷命令已改用正式核心，不再保存第二套相同行為。

這只使 `DisplayRequest → typed overlay entry → xlate.Layer` 的純建構段達 CONFORMED；尚未
把 runtime watcher、矩形失效與 frame lifecycle 接到玩家路徑，也沒有選定 2×／3×，因此
本整體規格仍為 DRAFT。

### 已證實的選定種族後下一畫面

第三十五階段由相同 #99,999,999 state 排入 Enter #100,010,000 與 Enter #100,240,000，
正常選定預設種族後於 #100,250,787 進入性別選擇畫面。兩次完整重播各得到相同 14-event
JSON 與終點 framebuffer；後四筆是提示、兩筆 normal 選項及 selected 第一選項，完整
identity 保存於 `text/post-race-events.tsv`。

normal 選項從 col 1 起、selected 第一選項從 col 3 起，與種族選單呈現相同兩格縮排形狀。
第 36 階段已由正常 Down／Up 證實 normal→selected 重畫及兩格縮排，Escape 則先取消男性
反白再返回功能選單；訂正第 35 階段「方向鍵與 Escape 未知」。第 37 階段又把七個唯一
identity 接入正式繁中 catalog 與 runtime request。第 38 階段又以第三個正常 Enter 證實
接受預設性別後進入五選項的職業選擇畫面，新增七筆 content-safe identity；訂正「確認性別
後畫面未知」。職業選單生命週期、text-safe rectangle 及玩家可見 renderer 仍未知／未接，
因此本整體規格仍是 DRAFT。

## 未知與 READY 閘門

下列項目未達 READY，故禁止 production 實作：

- 第 4–7 階段已證實本功能選單進入／返回的矩形清除與 guarded post-call，但訊息捲動、
  存讀檔及其他畫面的失效時機仍未知；種族選單鍵盤反白已由第 30 階段 Down／Up 證實，
  且其三筆新增 identity 已接入 exact catalog；overlay 重建與畫面繪製仍未接入；
- 第 27 階段 `TextRecorder` 已由九筆真實事件與自然 fall-through／錯誤 guard regression
  驗證純觀測契約；第 28 階段 READY `MenuCatalog` 已把九筆真實收據精確解析成繁中
  `DisplayRequest`。第 29 階段又以 CONFORMED runtime watcher 在 guarded post-call 直接
  產生九筆 request；第 31 階段把 selection variants 擴充為正常 Down／Up 路徑的 13 筆
  exact request。繁中 `Stamp` 的倍率中立純核心與離線 A/B 已完成，但矩形失效、frame
  lifecycle 與 runtime watcher 尚未接成玩家路徑 adapter；
- GNU Unifont 已證實可作有授權的 prototype 字型，且現有 8 筆譯文已由正式 TSV 決定性
  導出 24 個字模並經 `xlate.LoadFont` 回讀；正式採 2× 填滿格或 3× 置中仍待使用者決定，
  後續畫面的換行與 overflow 策略仍未知；
- 選單每一行的完整 text-safe rectangle，以及非靜態畫面的適用性；
- 上游字串表定位仍未知；九筆已用完整 identity 區分同譯文的不同顯示事件，其他畫面的
  collision 策略不得由此樣本外推。
- 選定預設種族後的性別畫面已有初始、Down／Up 與 Escape 證據，七個唯一 identity 亦已
  產生 exact runtime request；Enter 確認性別後的職業初始畫面已有七筆 identity，但其
  Down／Up／Escape、確認職業後畫面、性別／職業 text-safe rectangle 仍未知，且尚未接 renderer。

升為 READY 前，至少須以 dosgolem 取得一條正常互動路徑，明確量到上述生命週期事件，並
完成原文／繁中 A/B 同狀態收據與中文 glyph containment 驗證。沒有達成這些條件時，DRAFT
只能引導後續量測，不能成為程式碼、測試期望或「已中文化」的依據。

第九階段已在本機 dosgolem 專用分支移植並測試通用 `xlate` package；第 22 階段又把
`xlate.Draw` 擴充為支援所有正整數倍率。這只解決 GOLEMFNT、stamp、定色、失效、捲動與
快照等遊戲無關能力，不構成本作 adapter 實作，也不代表使用者已在 2×／3× 間做出選擇。
