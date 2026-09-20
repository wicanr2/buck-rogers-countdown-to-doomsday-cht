# 第二十一階段：手冊序數詞橋接證據

日期：2026-09-20  
狀態：原版 1–10 表、consumer 與 22 筆 catalog 覆蓋均已證實；正式 runtime 尚未實作。

## 問題與輸入

第二十階段確認 runtime 題目輸出英文序數詞，而事件 TSV 保存數字。本階段回到原版資料與
consumer，避免用一般英文常識猜出對照。

- `START.EXE` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`
- `GAME.OVR` SHA-256：
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`
- runtime `0EC0:0000` 64 KiB dump SHA-256：
  `28a0563b647ebe75a70e19648502e3fb9dc9379ada35bd397d99b104a4ce7c60`
- runtime `2A33:0000` 8 KiB overlay dump SHA-256：
  `7a2d9a3806d6ae49e5f8aa47a36767a38a0c1d1cbe744400e0525a98c4c2682c`
- IDA Pro 9.4 image ID：
  `sha256:6f6d59af49d0008c4109a5295b5f374bdc007e2d1ab28cb9de08779584de2780`
- IDA processor `pc`、database bitness 16。database EA 是本輪合成空間：`0x00000` 對應
  runtime `0EC0:0000`，`0x10000` 對應 runtime `2A33:0000`；不得把兩者當同一實模式 segment。

本機非破壞性 IDA 收據位於被忽略的 `workplace/phase21/`：

- JSON SHA-256：`21e87218582abaa140247338fe80c28442d2df797201292fcd263bbcd1e56d40`
- `.i64` SHA-256：`445a5d3ec35a23289698466fef7f046e1d66356fadc15258806c3edc3f252864`
- 匯出腳本 SHA-256：`fd5ad6b40cfadc4af084ca8fcfc458938417b0bade4e14b6f3905baa3168ec7f`

IDA database 中保留原始位址與 bytes，語意只以 `[已證實]` repeatable comment 附加，沒有以
推測性名稱覆蓋原始定位。

## Consumer 控制流

IDA Pro 9.4 對 runtime `2A33:02B7..02D2` 的原始指令為：

```text
2A33:02B7  C4 BE F7 FD        les  di,[bp-209h]
2A33:02BB  26 8A 45 14        mov  al,es:[di+14h]
2A33:02BF  30 E4              xor  ah,ah
2A33:02C1  BA 13 00           mov  dx,0013h
2A33:02C4  F7 E2              mul  dx
2A33:02C6  8B F8              mov  di,ax
2A33:02C8  81 C7 9B 33        add  di,339Bh
2A33:02CC  1E                 push ds
2A33:02CD  57                 push di
2A33:02CE  9A 2A 06 F4 0C     call far 0CF4:062A
```

`[record+14h]` 已由第十二階段證實是範圍 1–10 的 ordinal 數字。上述 consumer 將它乘以
19，再加 `DS:339B`，把結果傳給原版字串複製常式。因此公式為：

`slot_address = 0EC0:(0x339B + ordinal * 0x13)`。

這條資料流同時提供表的索引、stride、segment 與 consumer，不是只靠掃描 ASCII 字串的猜測。

## 原版表格

每個 slot 固定 19 bytes：`length:u8 + ASCII[length] + zero padding`。原版 bytes 為：

| 數字 | runtime 位址 | 長度 | 可見字串（去尾端空白） | 19-byte slot |
| ---: | --- | ---: | --- | --- |
| 1 | `0EC0:33AE` | 7 | `first` | `07666972737420200000000000000000000000` |
| 2 | `0EC0:33C1` | 7 | `second` | `077365636f6e64200000000000000000000000` |
| 3 | `0EC0:33D4` | 7 | `third` | `07746869726420200000000000000000000000` |
| 4 | `0EC0:33E7` | 7 | `fourth` | `07666f75727468200000000000000000000000` |
| 5 | `0EC0:33FA` | 7 | `fifth` | `07666966746820200000000000000000000000` |
| 6 | `0EC0:340D` | 7 | `sixth` | `07736978746820200000000000000000000000` |
| 7 | `0EC0:3420` | 7 | `seventh` | `07736576656e74680000000000000000000000` |
| 8 | `0EC0:3433` | 7 | `eighth` | `07656967687468200000000000000000000000` |
| 9 | `0EC0:3446` | 5 | `ninth` | `056e696e746800000000000000000000000000` |
| 10 | `0EC0:3459` | 5 | `tenth` | `0574656e746800000000000000000000000000` |

所有 padding 均為零。`second` 與 `tenth` 分別由第十八、十一階段的 dosgolem 正常輸出事件
交叉驗證；其餘八筆由同一已證實 consumer、同一固定表與原始 bytes 證實，不需操弄亂數逐題
抽樣。

## 可重生正式資料

`tools/manual_ordinals.py` 由上述 64 KiB dump 重生 `text/manual-ordinals.tsv`，逐 slot 驗證：

- input 長度、length 界線與固定 19-byte stride；
- ASCII 小寫字、去除尾端顯示 padding 後非空且唯一；
- slot 剩餘 bytes 全零；
- 1–10 恰有十筆；
- `manual-events.tsv` 的每個 ordinal 都存在於 bridge。

正式 TSV SHA-256 為
`fbf643ff2eecb1d5747f6d07d8845d2f67ed2e908ea060b8152dcb10bf0b538e`；工具與測試 SHA-256
分別為 `a3f105a6bf2ad239b8ea14dd0d8f64187f540f26fc9dcb4ad300569c4441a1e9`、
`fc959f5fac1db33f50693cb2955b9e5035ee7d0f2ad3eda17678234a3de120fd`。

7 項單元測試涵蓋正常十筆、截斷、長度越界、非 ASCII、非零 padding、重複字串與事件未涵蓋
ordinal。現有 22 筆事件使用 2–10，全部命中；數字 1 雖暫無 catalog 事件，仍保留為原版完整表。

## 結論與邊界

第二十階段的 ordinal bridge 缺口已由原版表與 consumer 解決，不再只是兩筆動態白名單。
這只完成題目身分到數字序數的資料橋接；尚未授權正式 adapter 或 renderer。2×／3×、正式
hook、繁中同狀態 A/B 與分頁互動仍未完成，因此手冊覆繪規格維持 DRAFT。
