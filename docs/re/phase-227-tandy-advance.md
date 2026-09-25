# 第二百二十七階段：TANDY 橫幅的按鍵推進首證

狀態：**DRAFT 單次重播。** 證明按鍵造成畫面推進，不辨識新畫面語意，
不定量、不逐位元驗收。

## 實驗

`cmd/probe`（BDA `PushKey`、指令數排程、決定性），唯讀原版＋
scratch 覆寫層，無網路 Docker，終點 200M 步並 `-dump-vram`：

- 對照（無鍵）：VRAM SHA-256 `9fe56b0e…`（TANDY 橫幅區）。
- 實驗（120M 起、每 2M 一空白鍵、緩衝空才送）：VRAM SHA-256
  `b08623d2…`；與對照逐 byte 比對，64,000 中 16,095 不同，
  差異包絡 x[0,318]×y[0,199] 全屏——不是單字重畫，是新視覺狀態，
  與離開 TANDY 橫幅一致。

收據（PNG＋VRAM＋SHA256SUMS）只留 ignored
`workplace/phase227-tandy-advance/`，不入 Git。

## 限制

- 各一次重播：未做雙重決定性確認，不得作 CONFORMED 收據。
- 只證「畫面變了」：新畫面是 logo／title／選單中的哪個未辨識；
  TANDY 橫幅的確切離開步數未二分。
- 按鍵經 BDA 環（phase-226 結論）；`d.Keys` 路徑仍過不了此關。
