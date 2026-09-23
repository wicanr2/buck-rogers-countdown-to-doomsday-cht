# 第一百八十七階段：Exit 六步停止點差異的重播勘誤

日期：2026-09-23
狀態：**DRAFT 證據勘誤；不授權 Exit 覆繪或升 READY。**

第一百八十三階段在同一 Y→Y 選項記錄 dosgolem text runner 於 step `125006330`
停止；第一百八十四階段的最小 A000 觀測器則在 `125006324` 停止。先前懷疑
觀測器影響執行，但沒有控制組。這次固定本機 fork commit
`cb3ca77c66e4909c5f513b807840e885ab5cb4a3`、私有 `a-joined.state` SHA-256
`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`、
同一 13 筆 BIOS 鍵盤步點與唯讀原版輸入，在 Docker／Go 1.25.14 重跑兩種
runner。以下位址是 dosgolem 的 8086 實模式 CS:IP，step 是 Machine 指令計數：

| 控制組 | 收據 SHA-256 | 停止點 |
| --- | --- | --- |
| 最小 A000 觀測器 | `990c5a99f141534958ac0f96e4f4fef30215a941914bdcd3ded23ab01810418b` | `125006324`；與第一百八十四階段 `cb-yy.json` 逐位元組相同。 |
| 原 `buckrogers-text-receipt` 工具兩次獨立重跑 | 兩次皆 `9f77ac3462d3fb4c2c47ad0421d17dad806776145212cf82cbe39452aff9ec94` | 兩次皆 `125006324`，JSON 逐位元組相同。 |
| 最後指令窄 trace | `7537d6046ee576c85adf86e1d0374aab3fbe0ee0a3bb4c91ecfe4d6f94a27dc4` | step `125006323` 執行前 `0CF4:0192`、`Exited=false`；執行後 `Exited=true`，停止於 `125006324`。 |

trace 的停止條件是 `m.Steps < 126000000 && !d.Exited`；`125006300` 之後
沒有 A000 寫入。最小 trace 來源是 ignored
`workplace/phase184-exit-drift-probe/dosgolem-cb3ca77-trace/cmd/exit-terminal-trace/main.go`，
SHA-256 `0fe6e3f9108b9b41fa7ead0896f62ca42b84f7c23895703b2533d34ed642f197`。
全部私有收據與重播副本均留在 `workplace/phase184-exit-drift-probe/`，沒有加入 Git。

因此「A000 觀測器讓遊戲提早六步退出」被這個控制組**否定**；目前固定條件下
兩種 runner 都在同一步退出。舊 `125006330` 收據的產生環境與 runner 二進位
沒有完整保存，不能判定其差異到底來自 Go patch 版、未保存的輸入實例，還是
其他執行環境。第一百八十三階段的歷史記錄保留並附本勘誤；不可把舊停止點
當成目前 fork 的可重生值。

這項訂正不改變已量的原版提示或同值 A000 寫入：第一提示文字矩形在
Y→Y 分支第一次相交 pre-write 仍是 step `124906844`、`0763:184D`、
像素 `(0,192)`、`0→0`；row21 是 `124800903`、同一 CS:IP、`15→0`。
中文候選、逐幀失效、真正 runtime A/B 仍待證據審查。Docker 均以 `--rm`、
無網路、資源上限與目前 UID/GID 執行，原版唯讀，沒有留下本案容器或
root-owned 產物。
