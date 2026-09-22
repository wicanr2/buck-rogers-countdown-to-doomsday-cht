# 第一百一十八階段：故事 DRAFT 字型重建與 loader 回讀

日期：2026-09-22
狀態：**DRAFT 字型涵蓋驗證完成；不代表 page2／page3／page4 已接通或通過 runtime A/B。**

本階段承接 page2／page3／page4 繁中 DRAFT 譯文校訂，以本機使用的倚天
`ET353S/FILES/` 15 點字模，在 Docker 內重建全部正式與 DRAFT
`text/*.zh-TW.tsv` 的 16×16 top-pad `GOLEMFNT` 子集。生成檔與完整 manifest
只留在被 Git 忽略的 `workplace/phase118-font/`，不可提交、散布或放入公開封包。

## 可追溯雜湊

倚天來源檔案：

- `ASCFONT.15`（3,840 bytes）：
  `1d0cf09d0a319a9e7039190688c6a905ba4370bd369fbfcfa43b2078480d6918`
- `SPCFONT.15`（12,240 bytes）：
  `f32049ba2a7a21db908878a488a2c1d93c389d17398cf46db1390ba89e247605`
- `STDFONT.15`（392,820 bytes）：
  `39ba9c8519d75fe11d5988a8a27e6daa5794ad2ea215108390b0d7e9e53ff701`

本次重建結果：

- 字元清單 SHA-256：
  `64245a389503bb2ee1479a36c8bdb98534c4b8a09b011812a95af3736b3a27f6`
- `buckrogers-eten-top-pad.golemfnt`（997 glyph）SHA-256：
  `15f091f5c0090b3453ca69a16ed0eedd5d0fd2d68d1bc0156712e6e8de8837ef`
- `buckrogers-eten-top-pad.json` SHA-256：
  `674986182b157cea4585f0b684729af74ca853f9a18b459737e110f4082de4c5`

## 正式 loader 回讀

以 dosgolem `cmd/fontcheck` 的正式 `xlate.LoadFont` loader 回讀同一份字型：

- page2：44 個 Unicode 字元，缺字 0。
- page3：47 個 Unicode 字元，缺字 0。
- page4：58 個 Unicode 字元，缺字 0。
- 全部正式與 DRAFT catalog：6,106 個文字字元，997 glyph，缺字 0。

這只證明翻譯資料可由目前倚天來源建立，且正式 loader 能讀取並覆蓋這些字元；
不證明 page2／page3／page4 的 caller、清除矩形、runtime adapter、頁面轉場、
正常玩家路徑或 2×／3× A/B。三頁仍維持 DRAFT，page4 的 caller／glyph guard／
步數仍為未知。
