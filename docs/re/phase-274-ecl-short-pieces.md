# 第二百七十四階段：ECL 敘事窗的組句碎片

日期：2026-09-27

## 1. 執行期（已證實）

以探索紀錄（`workplace/phase257-text-window-trace/cp/*.tsv`，631 則不同的 `0763:056C` 整串）
對 ECL catalog 與引擎片段查表：545 則命中，86 則未命中。扣掉玩家名、數字與標點，剩下：

| 字串 | 次數 | 情境（強推論，依前後整串） |
|---|---|---|
| ` ATTACKS.` | 5 | `<名字>` 之後，戰鬥觸發句 |
| `BELOW` | 1 | `HORRID GENNIES SLIP INTO THE AIRSHAFT FROM ` 之後，接 `. `、名字、`WILL HAVE TO FACE …` |
| `HIM`、`GIRL`、`SELF` | 各 1 | 對話中的代名詞碎片 |
| `AAAAAAAAAAAHHHHHHHHHHH!!!!!'` | 1 | 慘叫 |
| `AUTHORIZED PERSONNEL` 接名字 | 1 | 門禁句尾 |

另有開場三句（`AFTER HEARING …`、`AS NEW RECRUITS …`、`YOU SETTLE …`）與 `LAUNCH...`：
由開場故事家族處理，不屬本項。

## 2. 靜態原因（已證實）

`tools/ecl_text_catalog.py` 只收去頭尾空白後長度 > 3 且含空白的候選。上表碎片不含空白（或只有
前導空白、去掉後不含空白）而被排除。放寬為「長度 ≥ 2、不要求空白」後新增 289 則；前幾名是
`EXIT`（32 處）、`STAY`、`ATTACK`、`LEAVE`、`UP`、`DOWN`、`FLEE`、`PORT`、`IT`，也有 `DA`、`(B` 這類雜訊。

## 3. 相鄰譯文

`HORRID GENNIES … FROM ` 的現行譯文是「可怕的基改人，從第」，翻譯時以為後面接層數；實際接
`BELOW`（本次紀錄）。第 2 層翻譯要連同相鄰句一起看。
