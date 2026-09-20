# 第三十五階段：選定種族後的下一畫面文字路徑清冊

## 結論

由既有 #99,999,999 固定 state 先正常 Enter 進入種族選單，再於 #100,240,000 以第二次
正常 BIOS Enter 選定預設種族，原版於 #100,250,787 開始輸出下一個玩家可見畫面。該畫面
恰有四筆新的 `0763:0424` guarded post-call：一筆性別選擇提示、兩筆 normal 選項，以及
一筆 selected 第一選項。

兩次完整重播的 14-event JSON 與終點 64,000-byte indexed framebuffer 均逐 byte 相同；
命令兩次皆成功退出，零 pending／drop。這證實單一預設種族路徑，但不外推其他種族、
方向鍵 selection lifecycle、確認性別後的畫面或完整角色建立流程。

## 固定輸入與工具

- state：`workplace/probe/after-bios-space-100m.state`，SHA-256
  `cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`，起點
  #99,999,999。
- `START.EXE`／`GAME.OVR` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`／
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- dosgolem 基準 commit：`64b15779edc9d5be35e1acba0f854ba022008511`；本階段本機 commit：
  `7009315c5a04981eb1b048e7bba34a0b932fbf6d`，未推其遠端。
- `cmd/buckrogers-text-receipt/main.go` SHA-256：
  `8ce3a79a791659f72f4fa4190274155462ce701431bf11c8d7da7ee8ae291506`。
- dosgolem spec `016-buck-rogers-post-race-text-receipt` 已依 READY→實作→真實重播順序達
  CONFORMED。

所有 caller 都採 dosgolem runtime `segment:offset`，不是 IDA 線性位址或檔案偏移。原版
完整文字只在被忽略的 probe 中用 bytes／候選雜湊核對；正式 TSV 與 JSON 不保存全文。

## 正常輸入與事件時間線

- #100,010,000：排入第一個 Enter，進入既有 `PICK RACE` 路徑。
- #100,240,000：排入第二個 Enter，選定當下預設種族。
- #100,240,522 → #100,245,301：原選取列先以 normal style 重畫，沿用既有
  `race.selection.normal.terran` identity。
- #100,250,787 起：下一畫面開始輸出。
- #100,334,602：第四筆新事件 guarded post-call 完成。
- #101,000,000：固定停止；其間沒有更多完成事件。

## 四筆新事件

`text/post-race-events.tsv` 保存完整 content-free identity：

| event key | entry → post-call | caller | len／SHA-256 | bg/fg | row,col |
| --- | --- | --- | --- | --- | --- |
| `gender.screen.prompt` | 100250787 → 100259380 | `37F1:158C` | 11／`d6359f6f…6a91e` | 0/13 | 2,1 |
| `gender.option.male` | 100277753 → 100282556 | `37F1:15BD` | 6／`b261705c…8116d` | 0/10 | 3,1 |
| `gender.option.female` | 100304303 → 100310629 | `37F1:15BD` | 8／`8e30eb57…08183` | 0/10 | 4,1 |
| `gender.selection.selected.male` | 100331347 → 100334602 | `37F1:175D` | 4／`03f8c127…f73a1` | 15/0 | 3,3 |

前三個文字 key 只是穩定語意識別；本階段沒有建立繁中 catalog。normal 選項從 col 1 起並
含兩格縮排，selected 第一選項從 col 3 起，形狀與種族選單相同；但方向鍵重畫與返回生命
週期尚未量測，不能因此直接套用種族選單結論。

## 決定性收據與驗證

- 兩份 JSON 逐 byte 相同，SHA-256 均為
  `0c24a9fa56f5815bfed35b9ebff1ca219d10931beafaed16ed57a99eabbb7dab`。
- 兩份 framebuffer 逐 byte 相同，SHA-256 均為
  `dcf947d18c85b051ec85e1bc968f30cec5c315a9158d598055d14ebfe82a715c`。
- `tools/post_race_receipt.py` 固定 state／原版／命令 hash、兩鍵排程、前十筆既有 inventory、
  四筆新 inventory、14 組 exact step／identity、終點尺寸與 framebuffer hash。
- 新 inventory／verifier／verifier 測試 SHA-256：`168e978f…311c`／`d897d6ea…e61b`／
  `e356c888…eca2`。
- 專案 47 項 Python 測試通過；dosgolem 排除既有非正式 `workplace/` 後，全部正式
  packages test／vet，以及 `apps/buckrogers`／receipt command race detector 通過。

收據位於被 Git 忽略的 `workplace/phase35/`。因本階段只有原版證據，尚未建立譯文、字型
覆蓋、文字安全矩形或 A/B 畫面，不能把這四筆稱為已中文化。

## 證據等級與下一步

- **已證實**：固定預設種族路徑、兩鍵排程、14 筆事件順序、四筆新 identity 與終點畫面。
- **已證實**：下一畫面是性別選擇，第一選項在固定終點為 selected style。
- **強推論**：normal／selected 的 col 1→3 幾何可能沿用種族選單的兩格縮排；仍需正常
  Down／Up 實驗才能升格。
- **未知**：性別選單方向鍵、Escape、確認後畫面、其他種族是否同路徑，以及正式繁中版面。

下一個最小切片應先量性別選單 Down／Up／Escape lifecycle，再決定能否把四筆 identity
併入正式 catalog；不得只憑相似 caller 與座標直接接 production renderer。
