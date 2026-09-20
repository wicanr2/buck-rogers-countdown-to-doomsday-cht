# 第十階段：繁中 catalog 與 GOLEMFNT 建置收據

日期：2026-09-20  
證據等級：工具契約已證實；正式字型與輸出倍率仍待決策

## 輸入與權利邊界

- 正式顯示資料：`text/menu.zh-TW.tsv`，UTF-8、三欄 TSV，共 8 筆。
- 測試字型：本機 `/home/anr2/cht/sangokushi/fonts/unifont.hex.gz`，SHA-256
  `20e8b505f602488697979eefc69857f7f6106bceab702f5ac559f4f84e0e7494`。
- 隨附授權文字 SHA-256：
  `1e74cb82bf476843e97c2596297b04219b1a7e51f7238944a8c031cb9401fa87`。全文載明
  GNU GPL 2+ 字型嵌入例外及 SIL Open Font License 1.1 條款；本階段未複製授權檔或字型
  到儲存庫，也不宣告 GNU Unifont 為正式產品選擇。

## 已證實的建置契約

`tools/catalog_font.py` 失敗即關閉地檢查 UTF-8、BOM、精確標頭／欄數、空 key／譯文、
重複 key、`runtime`／`manual-and-runtime` 來源枚舉、Unicode 控制／格式字元及 NFC。
字元需求只取 `translation` 欄，依碼點升冪去重，輸出固定的
`U+XXXX<TAB>字元<LF>`。目前 8 筆譯文共有 24 個唯一字元，清單 SHA-256 為
`6094ce0c721cdaf04936eab69c32b4e8529b44c60763a9af0158c8502fac9b6f`。

Unifont builder 接受 `.hex`／`.hex.gz`：16×16 字模保持原位；8×16 每列左移 4 bit，置中
到 16×16。輸出固定為 `GOLEMFNT`、小端 `16×16`、依碼點排序、來源 byte `1`，缺字、重複
字模、非十六進位或非 8×16／16×16 一律中止。6 組 Python 單元測試涵蓋正反向 catalog、
排序、兩種字模、檔頭、來源 byte、輸出長度、決定性與缺字。

## 實際回讀收據

生成物 `workplace/font/menu-unifont16.golemfnt`（不入 Git）為 904 bytes，SHA-256：
`553df09b6accd101995a2781819ba9bee84a6220f0db5bba4437df1ccc458fe7`。workplace dosgolem
分支 commit `8a224601a7d09fc8d0f63ab65828eb7f64fa0200` 加入 `cmd/fontcheck`，直接呼叫
production `xlate.LoadFont`；隔離容器回報：

```text
GOLEMFNT 16x16 glyphs=24 coverage=29
```

`coverage=29` 是 8 筆譯文合併後（含重複字）的碼點數；24 是實際去重字模數。這項收據只
證明檔案格式、載入與現有譯文覆蓋，不能證明畫面倍率、正式字型美術或 runtime adapter。

## 工具與環境註記

- Python：`python:3.13-bookworm`，無網路、限資源、UID/GID 1000:1000。
- Go：`golang:1.26.7-bookworm`，無網路、限資源、UID/GID 1000:1000。
- Go 映像在 `sh -lc` 下由登入 shell 重設 `PATH`，造成兩次 `gofmt: not found`；明確指定
  `PATH=/usr/local/go/bin:...` 並改用 `sh -c` 後，同一測試乾淨通過。這是容器環境問題，
  不是 dosgolem 或字型缺陷。

## 尚未證實

- 2× 填滿格或 3× 置中的玩家可見取捨仍待使用者決定。
- GNU Unifont 是否作正式字型、散布時採用的授權告知與包裝仍未決定。
- 本階段沒有 adapter、hook 或原文／繁中同狀態畫面收據，DRAFT 不升級。
