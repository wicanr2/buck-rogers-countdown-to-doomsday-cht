# 第一百零四階段：手冊正確作答後的遊戲內返回

日期：2026-09-22  
狀態：**已確認一條手冊成功返回的正常玩家路徑；存檔／讀檔仍未驗收。**

## 範圍與權利邊界

本階段從既有正常玩家路徑產生的本機 state
`workplace/probe/phase12-before-question.state` 重播。輸入 state 的 SHA-256 為
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`，起訖絕對
指令步為 `266399999` 至 `280000000`。

玩家依其本機、唯讀原版手冊查得答案後，以三筆正常 BIOS 鍵輸入並按 Enter。
答案、字元、ASCII 值及排程只留在被 Git 忽略的
`workplace/phase104-manual-correct-return/` 收據，未寫入本文件、catalog、程式或
原版輸入。此流程不改寫原版 EXE、資料、答案判定、VRAM、DOS 存檔或遊戲規則。

字庫為本機 top-pad 產物（961 glyph），SHA-256：
`7e8f5d0e70cc75505279de0575b3bcc489c0b0901ddc3c39c179124c9e544b18`。

## 已確認證據

- 手冊題目完成於 dosgolem 執行期位址 `2A33:0309` 的 guarded post-call
  `266557246`；此位址採實模式 `segment:offset`，不是 IDA 線性位址。
- 玩家輸入的兩個字元由原版在 `0753:09AF` 的字串輸出路徑回顯，之後原版於
  `267025068` 開始輸出後續遊戲畫面。這是成功通過驗證的返回，不是 Escape 的錯答重抽。
- 2× 與 3× 終態的手冊覆繪均完全失效：核准正文內外的覆繪差異皆為 0 像素，且
  overlay RGBA 分別逐 byte 等於同 frame／palette 的 baseline。這表示先前可見的
  中文段落不會殘留到返回後的原版遊戲畫面。
- 每個覆繪倍率的原始 indexed framebuffer 皆等於無覆繪控制組；`state-compare`
  正規化後的完整 machine／DOS state 亦相等。2× 的 machine／DOS SHA-256 為
  `7dcaafdb979d749e906c78c8fb2b5226f9d50e7817157a13ec7a5f1ad485aac1`／
  `8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`；3× 比較
  同樣相等。

私有收據 `verification.json` 另保存兩倍率的 RGBA 雜湊、完整狀態比較、原版
indexed framebuffer 與原始 FileOps metadata；原始遊戲、手冊、字型、state 與畫面
均只在 `workplace/`。

## 可重播界線

以一次性、無網路 Docker 容器執行 `tools/manual_runtime_smoke.py`，載入本機
`phase12-before-question.state`、本機字庫及現有 `buckrogers-text-receipt`／
`state-compare` 命令，即可重生此收據。鍵盤排程必須由操作者從其合法本機手冊
取得，且輸出目錄必須位於 `workplace/`；不得把答案或其可還原排程加入版本控制。

Escape 的獨立負向探針顯示它不是返回鍵：原版把它當作錯答並重抽下一題。該私人
收據位於 `workplace/phase104-manual-escape-probe/`，不將錯答流程誤列為返回驗證。

這一條收據**不**驗收原版遊戲內的保存、讀檔，亦不外推其他手冊題目或 host 前端。

## 後續有界探測與存讀檔停止點

從上述成功返回終態繼續正常按 Enter，三次各自可重生的停止點仍為連續敘事頁，
尚未進入可操作的遊戲指令迴圈。每次換頁都有 `026F:029C` 原版矩形清除，
手冊覆繪 `active_keys=[]`，輸出 RGBA 等於同幀 baseline；本機收據位於
`workplace/phase104-post-return-enter-{2,3,4}/`。先前的
`phase11-begin-adventure-360m` 實際是建角 `PICK RACE`，不是本成功返回分支，
不能把第 52 階段的建角保存／載入收據拼接成本節的手冊後存讀檔驗收。
下一個最小缺口是量測敘事頁的正常結束點、第一個 command loop 及其保存入口；
在此之前不猜按鍵，也不宣稱存讀檔 gate 已通過。
