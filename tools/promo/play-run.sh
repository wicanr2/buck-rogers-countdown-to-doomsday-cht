#!/usr/bin/env bash
# 在借用的影片工具映像（ffmpeg＋ImageMagick＋Noto CJK）裡跑 play-make.sh；只執行，不清理、不覆寫該映像。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
IMAGE="${BUCKROGERS_VIDEO_IMAGE:-psychicwar-video}"
exec timeout 30m docker run --rm --network none --memory 2g --cpus 2 --pids-limit 256 \
  --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp \
  ${FRAMES:+-e FRAMES="$FRAMES"} ${OUT:+-e OUT="$OUT"} ${BAN:+-e BAN="$BAN"} \
  -v "$ROOT:/src" -w /src "$IMAGE" sh tools/promo/play-make.sh
