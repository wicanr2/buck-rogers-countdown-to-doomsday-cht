#!/usr/bin/env bash
# Windows 發行包的 Wine 驗收（規格 035 §4 第 4 項）：解開 zip、原版放在 exe 旁、
# 自動模式跑到功能選單並輸出截圖；再驗缺原版時立即結束。⚠ Wine 不是 Windows。
#
#   tools/release/verify-windows.sh <輸出目錄> [畫格] [腳本]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="${1:?輸出目錄}"; F="${2:-1250}"; S="${3:-623:Space,779:Space,1100:Escape}"
ZIP="$(ls "$ROOT"/dist-all/BuckRogersCHT-*-win64.zip)"
ORIG="$ROOT/workplace/original/BRcdoom"
[[ -d "$ORIG" ]] || { echo "缺原版 $ORIG" >&2; exit 2; }
rm -rf "$OUT/win"; mkdir -p "$OUT/win"
timeout 120 docker run --rm --network none --memory 512m --cpus 1 --pids-limit 32 --log-opt max-size=10m --log-opt max-file=3 \
  -u "$(id -u):$(id -g)" -v "$ZIP:/z.zip:ro" -v "$OUT:/v" python:3.13-alpine \
  python3 -c "import zipfile; zipfile.ZipFile('/z.zip').extractall('/v/win')"
mkdir -p "$OUT/win/BuckRogersCHT/original"; cp "$ORIG"/* "$OUT/win/BuckRogersCHT/original/"
timeout 1800 docker run --rm --network none --memory 4g --cpus 2 --pids-limit 512 --log-opt max-size=10m --log-opt max-file=3 \
  -u "$(id -u):$(id -g)" -e HOME=/wine -e WINEDEBUG=-all -e WINEDLLOVERRIDES="mscoree,mshtml=" -e BUCKROGERS_NO_DIALOG=1 \
  -e F="$F" -e S="$S" -v "$OUT:/v" --tmpfs "/wine:exec,uid=$(id -u),gid=$(id -g),size=2g" psychicwar-wine bash -c '
export WINEPREFIX=/wine/prefix; WINE=$(command -v wine || command -v wine64)
mkdir -p /tmp/.X11-unix; Xvfb :99 -screen 0 1280x800x24 -nolisten tcp -ac >/dev/null 2>&1 &
i=0; while [ ! -S /tmp/.X11-unix/X99 ] && [ $i -lt 50 ]; do sleep 0.1; i=$((i+1)); done; export DISPLAY=:99
$WINE --version; $WINE wineboot -i >/dev/null 2>&1
cd /v/win/BuckRogersCHT
$WINE ./BuckRogersCHT.exe -frames $F -script "$S" -shot "Z:\\v\\win.rgba" > /v/win.log 2>&1; echo "run exit=$?"
ls /wine/prefix/drive_c/users/*/AppData/Roaming/BuckRogersCHT
mv original /v/win-original.away
rm -rf /wine/prefix/drive_c/users/*/AppData/Roaming/BuckRogersCHT/game
$WINE ./BuckRogersCHT.exe -frames 5 > /v/win-noorig.log 2>&1; echo "noorig exit=$?"
'
