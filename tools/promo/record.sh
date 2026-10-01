#!/usr/bin/env bash
# 實機錄影：用 buckrogers-play 的自動模式（-frame-dir，規格 049）把固定輸入腳本重播的畫面逐格輸出成 PNG，
# 並以 -wav 輸出同一次執行的音訊。輸出在 workplace/promo-rec/NAME/。
#
#   SCRIPT_FILE=路徑 tools/promo/record.sh NAME FRAMES [額外旗標…]
#
# 環境變數：
#   SCRIPT_FILE  必填。內容是 -script 的單行腳本（`畫格:動作,…`）。腳本含手冊查詢題的作答，
#                只放在 ignored 的 workplace/，不進 Git；題目隨輸入時序而變，換建置或時脈要重新核對。
#   BIN          buckrogers-play 執行檔（須含 -frame-dir；預設 workplace/phase311/bin/buckrogers-play）
#   STAGE        發行包 stage 目錄，取其 text/ 與 font/（預設 workplace/pkg-stage/AppDir）
#   ORIG         原版遊戲目錄（唯讀掛載；預設 workplace/play-e2e/orig）
#   SCALE        輸出倍率，預設 3（腳本不可含 scale 動作）
#   EVERY        每幾格輸出一張，預設 2（30 fps）
# 發行設定：Unifont（-font 指向 stage 的 Unifont 字型），不帶手冊英文列；公開影片不可用倚天字型。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; W=$ROOT/workplace
n=${1:?用法：SCRIPT_FILE=… record.sh NAME FRAMES [旗標…]}; f=${2:?缺 FRAMES}; shift 2
SCRIPT_FILE=${SCRIPT_FILE:?缺 SCRIPT_FILE}
ORIG=${ORIG:-$W/play-e2e/orig}; STAGE=${STAGE:-$W/pkg-stage/AppDir}; BIN=${BIN:-$W/phase311/bin/buckrogers-play}
for p in "$SCRIPT_FILE" "$ORIG/START.EXE" "$STAGE/text" "$STAGE/font/buckrogers-unifont.golemfnt" "$BIN" "$W/play-e2e/exe.sha"; do
  [ -e "$p" ] || { echo "缺 $p" >&2; exit 1; }
done
D=$W/promo-rec/$n; rm -rf "$D"; mkdir -p "$D"
S=$(cat "$SCRIPT_FILE")
timeout "${TMO:-3000}" docker run --rm --name "buck-rec-$n" --network none --memory 4g --cpus 2 --pids-limit 256 \
  --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$STAGE/text:/text:ro" -v "$STAGE/font:/font:ro" -v "$ORIG:/orig:ro" -v "$W/play-e2e/exe.sha:/exe.sha:ro" \
  -v "$BIN:/bin/buckrogers-play:ro" -v "$D:/out" -w /out \
  eob-remake-go:1.26.7-ebiten2.9.9 sh -c "Xvfb :99 -screen 0 1280x1024x24 >/dev/null 2>&1 & X=\$!; trap \"kill \$X\" EXIT; sleep 1; export DISPLAY=:99; \
  /bin/buckrogers-play -original /orig -save /out/save -exe-sha256 \$(cat /exe.sha) -text-dir /text -font /font/buckrogers-unifont.golemfnt -lang-fonts /font \
  -scale ${SCALE:-3} -frames $f -script '$S' -shot /out/shot.rgba -wav /out/out.wav -frame-dir /out/frames -frame-every ${EVERY:-2} $* > /out/log.txt 2>&1; echo exit=\$? >> /out/log.txt"
tail -n 6 "$D/log.txt" | cut -c1-200
