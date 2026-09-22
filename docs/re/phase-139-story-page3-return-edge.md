# 第一百三十九階段：第三頁五行 glyph 的真實 far-return

日期：2026-09-22
狀態：**原版 control-flow shape 已證實；第三頁規格仍 DRAFT，未接 runtime。**

## 輸入、工具與可重生性

起點為私有第二頁合法終態 `workplace/phase104-post-return-enter-2/control.state`，SHA-256
`b15abdf487f59d982657d1d097c0b38fe3668ca3fd6d15e49c310a5486e238e2`；原版
`GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0` 只讀掛載。
在 step `291000000` 排入一筆正常 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至
`300000000`。工具為本機 dosgolem branch `buck-rogers-cht-output-overlay` commit `f6579d9`，
Docker image `golang:1.26.7-bookworm`／Go 1.26.7，以
`cmd/buckrogers-text-receipt -glyph-trace -glyph-return-edge-trace -story-pixel-trace` 重播。

兩次私有 receipt `workplace/page3-return-probe/page3-{a,b}.json` 逐 byte 相同，SHA-256
`76c275be1d54499e14452440302d7e0a119db237163d199d1fc80c7c3b45c220`。
位址皆是 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址；receipt 只保存 caller、
guard、樣式、座標、步數、控制流與雜湊，不保存原文 glyph bytes。

## 已證實的 return edge

只篩選固定故事 caller `0763:04FF`、rows 17–21；144 個 glyph 全部有一筆真正的
`0763:026B` guarded entry → 緊前 `0763:03D6`、opcode `0xCA`（`RETF imm16`）→
返回 `0763:04FF`。每筆都為 mode／repeat `1/1`、背景／前景 `0/10`、column 依行遞增。
五行 return edge 數依序為 `34/37/31/37/5`，與
[`story-page3-events.tsv`](../../text/story-page3-events.tsv) 的 original length 相同；
首筆 entry step `291022040`，末筆 post-call step `297287594`。右側動態欄位與 row 24
不在此集合，不得加入第三頁 catalog。

另在首個 glyph 周圍開啟最多 1000 筆有界 instruction trace，私有收據
`workplace/page3-return-probe/first-glyph-stack.json` SHA-256
`7a835e423a7a4dcdac19bb7cf05380c868df1bd824ea602722635de15d43db36`。
entry step `291022040` 的 `SS=1841h,SP=3D66h`；緊前 RETF step `291022781`
仍為相同 SS/SP；下一步 `291022782` 實際回到 caller，`SS=1841h,SP=3D78h`，
因此 `SP` 增加 `0x12`。這些絕對 SS/SP 只屬本次收據，**不可**寫成 runtime
身份常數；runtime 只能比 entry-time SS 及相對 `SP+0x12`。

本階段連同[第一百三十八階段](phase-138-story-page3-exit-prewrite.md)補齊第三頁的
far-return 與已量 Enter 離頁前寫入證據，但不單獨授權 production watcher；仍須審查
五行 exact identity、譯文與安全矩形、字型覆蓋、負例與同狀態驗收設計，通過 READY
後才能實作。

## 補充：全部 144 筆 entry／return stack 直接對照

獨立 READY 審查指出上述原始 return-edge JSON 只含 return SS/SP，首筆有界指令
trace 不能證明其餘 143 筆的相對 stack。故本機 dosgolem commit `a9f2afd` 為
`glyph_return_edges` 增加 content-safe `entry_ss`／`entry_sp`，不輸出 stack words
或原文，再從同一 state、同一 Enter 排程雙重重播。

私有 `workplace/page3-return-probe/page3-entry-stack-{a,b}.json` 逐 byte 相同，
SHA-256 `11427a055910594f3ecce309a3d0f6d7802e93ad728113c0adf5c13be5531943`。
固定故事 caller／rows 篩出的 144 筆仍為 `34/37/31/37/5`；每一筆均有
`entry_ss == return_ss`、`(return_sp-entry_sp) mod 65536 == 0x12`、緊前
`0763:03D6` opcode `0xCA` 及實際返回 `0763:04FF`，反例數為零。首末筆同為
entry `SS:SP=1841:3D66`、return `1841:3D78`；這些絕對值仍只作收據錨點。
這次訂正把「首筆支持相對 guard」提高為「144 筆直接驗證」，保留先前收據，
不改寫原歷史；第三頁 typed core 的負例審查仍未完成，規格維持 DRAFT。
