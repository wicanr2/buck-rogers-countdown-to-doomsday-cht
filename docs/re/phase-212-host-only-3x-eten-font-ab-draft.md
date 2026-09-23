# 第二百一十二階段：3× 設定面板倚天字型 A/B 原型

日期：2026-09-24
狀態：**DRAFT 視覺決策前置；未選方案、未改正式前端、未執行 3× Apply。**

## 為何先停在 host 字型

[第二百零九階段](phase-209-cold-boot-live-ebiten-panel-pause-draft.md)
已在 2×真實視窗驗到暫停／恢復；3× 的正式
`frontend/ebiten.Game.New` 目前要求 `HostFont3` 為 22×22，
但本案現有的倚天 host/current GOLEMFNT 是 16×16。先前 ignored
原型曾用 16→22 衍生字型滿足建構器，不能當成使用者已核准的
3×字型品質。正式 3× Apply 在本階段**未執行**。

使用者指定的本機倚天來源有原生 24 點字型：

| 本機唯讀輸入 | SHA-256 | 已驗形態 |
| --- | --- | --- |
| `ET353S/FILES/STD.24M` | `347ae2655807fc250a18673e6634a363dfba7feee6c3355b886a0810d2d9c030` | ETUNPACK 壓縮明體；用既有解壓器還原 13,094 個 24×24、942,768 bytes，未截斷 |
| `ET353S/FILES/SPCFONT.24` | `da7574d2eee10b9d3b2a2d90bbc39e2ba482b9b2b73a9803f1e4dbefdd91a92a` | 408 個 24×24 符號 |
| `ET353S/FILES/ASCFONT.24` | `7e69f74bfedf57579fad41a1bc2f0c3a6da873cba1734fd30a1c4afc64893ada` | 256 個 16×24 ASCII |
| 既有 `psychic-war/tools/font/etunpack.py` | `738e491f65a52e6c716269b5e78b4937510547647615985c1d60b00ec2a4bac6` | ETUNPACK 解壓器，未修改 |

六個面板中文字元的原生字模全有墨跡。把 24×24 直接裁到 22×22
不是無損方案：九種整數偏移全部會削掉六字筆畫，最好偏移仍損失
合計 57 個墨點。本機 ignored
`workplace/cold-boot-3x-apply-gap/receipt.json` SHA-256
`c9524423326adcae8157ec4321da4520b92b936d793026e8f9ab7154cd31fea1`
保存這個數值前置檢查，不含字模或影像。

## 不載原版遊戲的並列原型

ignored `workplace/host-only-3x-panel-ab/render.py` SHA-256
`f9f4422f602e077f4915f0c02993977c57db9bb71cd1573b23fc22ee4dd232c3`；
`receipt.json` SHA-256
`2b3128a2487fb3d376fc3034b4a8ed03376cfb2dba1baf353bf03da28d94c48a`。
只用本機倚天字型與 host 控制列的既有座標、顏色，生成 960px 寬
的設定面板／關閉按鈕圖；**沒有**載入 DOS、原版遊戲畫面或執行
`Game.Update`。圖片只在 ignored 本機工作區：

- A：`workplace/host-only-3x-panel-ab/A-native24-open.png`、
  `A-native24-closed.png`。漢字／符號用原生 24×24，數字用原生
  16×24；開啟面板 PNG SHA-256
  `56736c7da70949cec8bd9ed14f7aa508b863f9ad2610cf4590412b17d153adfd`。
- B：`workplace/host-only-3x-panel-ab/B-current22-open.png`、
  `B-current22-closed.png`。沿用既有原型的 16→22 衍生方式作視覺
  對照，**不是**已核准的正式 3× 字型；開啟面板 PNG SHA-256
  `8ef9aecfbbea1cf64ae547e8d72d31a8d739e3edbca87da160f8c0f832bd7dd4`。

A／B 的九個相異 host 字元都不缺字，五項文字的 advance 與墨跡
都在控制項安全矩形內。A 的 `2×`／`3×` advance 各 40px，
中文字標籤各 48px；B 分別為 44px、44px。兩案左邊距沿用既有
控制項起點，沒有移動遊戲畫布或 host hit rectangle。

上述幾何只證 host-only 字形擺放。A 的原生 24 點目前仍不符合
正式 `Game.New` 固定的 22×22 `HostFont3` 契約；若使用者選 A，
須另走 READY 審查、正式 validator／字型資產接線與 3×實體 Apply
驗收。若選 B，也須先明確認可衍生字型的外觀，再做正式接線與
同狀態驗證。**目前兩者都不是已完成的 3× Linux 前端。**

主代理以唯讀 Docker 核對工具／輸入／收據／開啟面板 PNG 的雜湊
和數值欄位，沒有將字型、PNG 或原版畫面送入工具通道。原始
倚天檔與生成圖片只留本機，不進 GitHub 或公開包；本階段不記錄
尚未由使用者作出的視覺選擇。
