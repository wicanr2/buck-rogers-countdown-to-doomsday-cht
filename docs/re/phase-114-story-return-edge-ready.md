# 第一百一十四階段：首屏字元返回邊與 READY 輸入

日期：2026-09-22
狀態：已確認輸出觀測邊；首屏 runtime A/B 尚未完成。

從本機 `workplace/probe/phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）
沿 phase104 已證實的合法手冊返回排程重播首屏；排程、答案、原版 glyph bytes
均只在被忽略的 `workplace/`，不寫入本文件或 Git。

dosgolem 本機分支 `9dcbc7d` 或後續相容提交的
`--glyph-return-edge-trace` 診斷收據位於
`workplace/phase114-story-return-edge/receipt.json`，SHA-256
`2f4716135c2b8f58c46d5b6d486bba839dfebfb7386d16860683db7f7c107297`。
位址均為 dosgolem 實模式 `segment:offset`，不是檔案偏移或 IDA 線性位址。
收據本身含私有 BIOS 作答排程，故即使 glyph trace 不含原文，整份 JSON 仍不得
加入 Git 或對外散布。
其 160 個完成的 glyph return edge 對應首屏五行長度 `37+38+33+29+23`；
返回指令均為 dosgolem 實模式 `0763:03D6` 的 `RETF imm16`（opcode `0xCA`），
回到 `0763:04FF`。顯示 ABI 的低位元組樣式為 mode `1`、repeat `1`、背景 `0`、
前景 `10`；本次正常首屏高位 mask 全為 `0`。因此本收據證明這條正常路徑的
返回邊與低位顯示條件，不推定所有未觀測路徑的高位一定為零。

此收據使 watcher 可以要求真正的 far-return control-flow edge，而非只因稍後
再次經過同一 caller 位址就提交字元。dosgolem 本機 watcher 仍須把符合五筆
原文長度／SHA-256 的整組事件交給覆繪器；只有 runtime 接線、2×／3× 同狀態
A/B、頁面轉場與存讀檔生命週期驗收通過，才可稱首屏已中文化。
