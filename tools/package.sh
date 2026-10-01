#!/usr/bin/env bash
# 發行包（規格 035）：Linux AppImage、Windows zip、macOS zip，產物放 dist-all/。
#
#   tools/package.sh [all|linux|windows|macos]
#   BUCKROGERS_WITH_DATA=1 tools/package.sh all   # 本機自用完整版（內附原版，規格 035 §1.1）
#
# ⚠ -with-data 產物含原版遊戲：只留 dist-all/（已 gitignore），絕不推 git、絕不上傳 Release。
#
# 一律 Docker、--network none。dosgolem 以「已推送的分支 HEAD」git archive 出來建置，
# 版本與 dosgolem commit 以 -ldflags -X 注入。發行包不含任何原版檔案；打包後做外洩掃描，
# 命中即刪除產物並失敗。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TARGET="${1:-all}"

W="$ROOT/workplace"
DG="$W/dosgolem"
DG_BRANCH="buck-rogers-cht-output-overlay"
MODCACHE="$W/dosgolem-clean/workplace/gomodcache"
GOCACHE_DIR="$W/pkg-gocache"
STAGE="$W/pkg-stage"
DIST="$ROOT/dist-all"
UNIFONT="$W/unifont-src/unifont_all-17.0.05.hex.gz"
UNIFONT_SHA="7b182454966046d35482469b979edce7d262fab5c53c2180e9b1fbb5d0b5e574"
UNIFONT_DOC="$W/unifont-src/unifont-17.0.05"
# 規格 050：zh-TW 用台灣來源 unifont_t、zh-CN 用預設 unifont，從官方 tarball 的 font/precompiled/ 解出並核對雜湊（ja、ko 仍用 unifont_all）。
UNIFONT_TAR="$W/unifont-src/unifont-17.0.05.tar.gz"
UNIFONT_TAR_SHA="f287cffb26e22723aa36e6684869b0f3ff3bfb822c4b01008bd847911ec1b631"
UNIFONT_T_SHA="169634258e4037b507beaafad5d72edc2e44b3faeaa856d9669e4657d1eee454"     # unifont_t-17.0.05.hex
UNIFONT_ZH_SHA="fd79af3613ec1b984a98d33428fdd43fcf06018d18059960d78edeb63d958622"    # unifont-17.0.05.hex
RUNTIME_SIZE=944632  # psychicwar-appimage 的 /opt/runtime-x86_64
GO_IMAGE="eob-remake-go:1.26.7-ebiten2.9.9"
PY_IMAGE="python:3.13-bookworm"
MAC_IMAGE="buckrogers-osxcross"
APPIMAGE_IMAGE="psychicwar-appimage"
MAC_MIN="11.0"
# 外洩掃描的禁止來源：原版樹、倚天字型來源與本機產物、手冊英文摘錄。
LEAK_SOURCES=("$W/original/BRcdoom" "/home/anr2/cht/etan_font/ET353S/FILES" "$W/current-font" "$W/manual-english")

# 規格 040／041：發行包帶的語言（每個語言一個 font/buckrogers-<lang>.golemfnt；zh-TW 維持現行檔名
# buckrogers-unifont.golemfnt）。en 是原版，不需要檔案。
LANGS=(zh-TW zh-CN ja ko)
# 只供產生與審閱、不進發行包的 text/ 檔（規格 041 §3.1、042 §3.10）。
TEXT_EXCLUDE=(zh-CN-phrases.tsv zh-CN-overrides.tsv zh-CN-term-review.tsv ja-coverage-exemptions.tsv ja-name-exemptions.tsv ko-coverage-exemptions.tsv ko-name-exemptions.tsv)

VER="$(git describe --tags --always --dirty 2>/dev/null || echo dev)"
WITH_DATA="${BUCKROGERS_WITH_DATA:-}"
ORIG_TREE="$W/original/BRcdoom"
ETEN_SRC="/home/anr2/cht/etan_font/ET353S/FILES"
MANUAL_EXCERPT="$W/manual-english/excerpt.tsv"   # 本機手冊英文摘錄（規格 034，只進完整版）   # 倚天 15 點來源（本機購買，只進完整版）
SUF=""
if [[ "$WITH_DATA" == 1 ]]; then
  SUF="-with-data"
  [[ -f "$ORIG_TREE/START.EXE" ]] || { echo "[package] 缺原版 $ORIG_TREE" >&2; exit 1; }
  [[ -f "$MANUAL_EXCERPT" ]] || { echo "[package] 缺手冊摘錄 $MANUAL_EXCERPT" >&2; exit 1; }
  for f in ASCFONT.15 SPCFONT.15 STDFONT.15; do [[ -f "$ETEN_SRC/$f" ]] || { echo "[package] 缺倚天 $f" >&2; exit 1; }; done
fi
DC="$(git -C "$DG" rev-parse HEAD)"

die() { echo "[package] $*" >&2; exit 1; }
dr() {
  timeout 30m docker run --rm --network none --memory 6g --cpus 4 --pids-limit 512 \
    --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp "$@"
}

# --- 前置檢查 --------------------------------------------------------------------
[[ "$(git config user.email)" == "wicanr2@gmail.com" ]] || die "git 身分不是 wicanr2@gmail.com"
git -C "$DG" fetch -q origin "$DG_BRANCH" 2>/dev/null || true
git -C "$DG" merge-base --is-ancestor "$DC" "origin/$DG_BRANCH" || die "dosgolem $DC 尚未推到公開分支"
[[ -f "$UNIFONT" ]] || die "缺 $UNIFONT"
[[ "$(sha256sum "$UNIFONT" | cut -c1-64)" == "$UNIFONT_SHA" ]] || die "Unifont 雜湊不符"
[[ -f "$UNIFONT_TAR" ]] || die "缺 $UNIFONT_TAR"
[[ "$(sha256sum "$UNIFONT_TAR" | cut -c1-64)" == "$UNIFONT_TAR_SHA" ]] || die "Unifont tarball 雜湊不符"
for f in COPYING OFL-1.1.txt; do [[ -f "$UNIFONT_DOC/$f" ]] || die "缺 Unifont $f"; done
[[ -d "$MODCACHE" ]] || die "缺模組快取 $MODCACHE"
for s in "${LEAK_SOURCES[@]}"; do [[ -d "$s" ]] || die "外洩掃描來源不存在：$s"; done
for i in "$GO_IMAGE" "$PY_IMAGE" "$APPIMAGE_IMAGE"; do docker image inspect "$i" >/dev/null 2>&1 || die "缺映像 $i"; done
# 規格 041 §3.7／§3.8：簡體產生檔、詞表、帳本與各驗證器必須全數通過（漏提交重新產生的 zh-CN 檔也在這裡擋下）。
if [[ " ${LANGS[*]} " == *" zh-CN "* ]]; then
  "$ROOT/tools/zh_cn_check.sh" || die "zh_cn_check.sh 失敗"
fi
# 規格 042 §3.10：日文檢查（含 charset.ja.txt 重生比對，需要 Unifont hex 所在目錄）。
if [[ " ${LANGS[*]} " == *" ja "* ]]; then
  UNIFONT_DIR="$(dirname "$UNIFONT")" "$ROOT/tools/ja_check.sh" || die "ja_check.sh 失敗"
fi
# 規格 043 §3.10：韓文檢查（含 charset.ko.txt 重生比對）。
if [[ " ${LANGS[*]} " == *" ko "* ]]; then
  UNIFONT_DIR="$(dirname "$UNIFONT")" "$ROOT/tools/ko_check.sh" || die "ko_check.sh 失敗"
fi
if [[ "$TARGET" == all || "$TARGET" == macos ]] && ! docker image inspect "$MAC_IMAGE" >/dev/null 2>&1; then
  docker build --network none -t "$MAC_IMAGE" -f tools/docker/osxcross.Dockerfile tools/docker
fi

echo "[package] 版本 $VER，dosgolem $DC"
rm -rf "$STAGE"
mkdir -p "$STAGE/src" "$STAGE/common/font" "$STAGE/common/text" "$STAGE/out" "$GOCACHE_DIR" "$DIST"
git -C "$DG" archive "$DC" | tar -x -C "$STAGE/src"

LDFLAGS="-s -w -X main.version=$VER -X main.dosgolemCommit=$DC"
GOENV=(-e GOMODCACHE=/gomodcache -e GOCACHE=/gocache -e GOFLAGS=-mod=mod -e GOPROXY=off -e GOSUMDB=off -e GOTOOLCHAIN=local)
GOMOUNT=(-v "$STAGE/src:/src" -v "$MODCACHE:/gomodcache" -v "$GOCACHE_DIR:/gocache" -v "$STAGE/out:/out")

# --- 共同內容：譯文、字型、授權文件 ------------------------------------------------
for f in text/*.tsv; do
  [[ " ${TEXT_EXCLUDE[*]} " == *" $(basename "$f") "* ]] && continue
  cp "$f" "$STAGE/common/text/"
done
# 規格 044 §3.7：玩家名音譯器讀 CMU 發音詞典（BSD 式授權，全文隨包）與音譯表（CC BY-SA 4.0）的授權說明；
# 這些不是 text/*.tsv，上面的迴圈不會帶。缺任一項就打包失敗，不在發行包裡安靜地停用玩家名。
mkdir -p "$STAGE/common/text/cmudict"
for f in cmudict.dict LICENSE README; do cp "text/cmudict/$f" "$STAGE/common/text/cmudict/$f"; done
cp text/LICENSE-translit-table.md "$STAGE/common/text/LICENSE-translit-table.md"
TRANSLIT_FILES=(cmudict/cmudict.dict cmudict/LICENSE LICENSE-translit-table.md translit-table.tsv translit-arpabet.tsv translit-names.tsv translit-chars.zh-TW.tsv)
for lang in ja ko; do
  [[ " ${LANGS[*]} " == *" $lang "* ]] && TRANSLIT_FILES+=("translit-$lang-names.tsv" "translit-chars.$lang.tsv")
done
for f in "${TRANSLIT_FILES[@]}"; do [[ -f "$STAGE/common/text/$f" ]] || die "發行包缺 text/$f（玩家名音譯器需要）"; done
# 規格 050：從官方 tarball 解出 zh-TW 與 zh-CN 的字形來源並核對解壓後內容的雜湊（任何不符即失敗）。
mkdir -p "$STAGE/unifont"
dr -v "$UNIFONT_TAR:/u.tar.gz:ro" -v "$STAGE:/stage" "$PY_IMAGE" sh -c '
  tar -xzf /u.tar.gz -C /stage/unifont --strip-components=3 \
    unifont-17.0.05/font/precompiled/unifont_t-17.0.05.hex unifont-17.0.05/font/precompiled/unifont-17.0.05.hex'
[[ "$(sha256sum "$STAGE/unifont/unifont_t-17.0.05.hex" | cut -c1-64)" == "$UNIFONT_T_SHA" ]] || die "unifont_t 雜湊不符"
[[ "$(sha256sum "$STAGE/unifont/unifont-17.0.05.hex" | cut -c1-64)" == "$UNIFONT_ZH_SHA" ]] || die "unifont（預設）雜湊不符"
dr -v "$ROOT:/p:ro" -v "$UNIFONT:/u.hex.gz:ro" -v "$STAGE:/stage" -w /p "$PY_IMAGE" sh -c '
  python3 tools/catalog_font.py build text/*.zh-TW.tsv --font /stage/unifont/unifont_t-17.0.05.hex --out /stage/common/font/buckrogers-unifont.golemfnt &&
  for s in 256 512; do python3 tools/appicon.py /stage/common/font/buckrogers-unifont.golemfnt /stage/icon-$s.png $s; done'
for lang in "${LANGS[@]}"; do
  [[ "$lang" == zh-TW ]] && continue
  case "$lang" in
    zh-CN) FONTSRC=/stage/unifont/unifont-17.0.05.hex ;;  # 規格 050：簡體用預設（文泉驛），不用日文優先的 unifont_all
    *)     FONTSRC=/u.hex.gz ;;                           # ja、ko 維持 unifont_all
  esac
  dr -v "$ROOT:/p:ro" -v "$UNIFONT:/u.hex.gz:ro" -v "$STAGE:/stage" -w /p "$PY_IMAGE" \
    python3 tools/catalog_font.py build --lang "$lang" --font "$FONTSRC" --out "/stage/common/font/buckrogers-$lang.golemfnt"
done
# 規格 044 §3.7：以發行包的 text/ 與 font/ 實跑各語言通道（唯讀掛載 common/）。測試必須真的執行：
# 輸出要有 --- PASS 且不得有 --- SKIP，否則打包失敗。dosgolem 取已推送分支 HEAD，測試先進該 commit。
smoke_lanes() {
  local out
  out="$(dr "${GOENV[@]}" -v "$STAGE/src:/src" -v "$MODCACHE:/gomodcache" -v "$GOCACHE_DIR:/gocache" \
    -v "$STAGE/common:/pkg:ro" -e BUCKROGERS_PKG_ROOT=/pkg -e "BUCKROGERS_PKG_LANGS=${LANGS[*]}" -w /src "$GO_IMAGE" \
    go test ./apps/buckrogers -run 'TestPackagedLanes$' -count=1 -v 2>&1)" || { echo "$out" >&2; die "TestPackagedLanes 失敗"; }
  grep -q -- '--- PASS: TestPackagedLanes' <<<"$out" || { echo "$out" >&2; die "TestPackagedLanes 沒有 PASS"; }
  ! grep -q -- '--- SKIP' <<<"$out" || { echo "$out" >&2; die "TestPackagedLanes 被略過（BUCKROGERS_PKG_ROOT 沒生效）"; }
}
smoke_lanes
if [[ "$WITH_DATA" == 1 ]]; then
  # 倚天字型依現行譯文重建（與 Unifont 同一份字元聯集），只放進完整版。
  # eten_font.py 只准輸出到 repo 的 workplace/，所以另把 workplace 可寫掛上。
  dr -v "$ROOT:/p:ro" -v "$W:/p/workplace" -v "$ETEN_SRC:/eten:ro" -w /p "$PY_IMAGE" sh -c '
    python3 tools/eten_font.py build text/*.zh-TW.tsv --asc /eten/ASCFONT.15 --spc /eten/SPCFONT.15 --std /eten/STDFONT.15 \
      --out workplace/pkg-stage/eten.golemfnt --manifest-out workplace/pkg-stage/eten.json >/dev/null'
fi
cp "$UNIFONT_DOC/OFL-1.1.txt" "$STAGE/common/font/OFL-1.1.txt"
cp "$UNIFONT_DOC/COPYING" "$STAGE/common/font/COPYING-unifont"
cp LICENSE "$STAGE/common/LICENSE"
cp "$STAGE/src/LICENSE" "$STAGE/common/LICENSE-dosgolem"
cp "$STAGE/src/audio/nukedopl/COPYING.LGPL" "$STAGE/common/COPYING.LGPL"
cp "$STAGE/src/audio/nukedopl/SOURCE.md" "$STAGE/common/nukedopl-SOURCE.md"
cp docs/release/讀我.txt "$STAGE/common/讀我.txt"

# Linux 執行檔也拿來產生 THIRD-PARTY（三平台連結的模組以 Linux 版為準，另外各自核對）。
build_linux() {
  dr "${GOENV[@]}" "${GOMOUNT[@]}" -w /src "$GO_IMAGE" sh -c "
    go build -trimpath -ldflags '$LDFLAGS' -o /out/linux/buckrogers-play ./cmd/buckrogers-play &&
    go version -m /out/linux/buckrogers-play > /out/modinfo-linux.txt &&
    cp \$(go env GOROOT)/LICENSE /out/go-LICENSE && go version > /out/go-version.txt"
}
third_party() {
  dr -v "$ROOT:/p:ro" -v "$MODCACHE:/gomodcache:ro" -v "$STAGE:/stage" "$PY_IMAGE" \
    python3 /p/tools/release/third_party.py "/stage/out/modinfo-$1.txt" /gomodcache /stage/common
}
build_linux
third_party linux
cp "$STAGE/out/go-LICENSE" "$STAGE/common/licenses/go-LICENSE"
printf '另含 Go 標準程式庫與執行期（%s，BSD-3-Clause，licenses/go-LICENSE）。\n' "$(cut -d' ' -f3 "$STAGE/out/go-version.txt")" >> "$STAGE/common/THIRD-PARTY.md"

# payload <目標目錄>：完整版放入原版與本機自用說明；一般版什麼都不放。
payload() {
  [[ "$WITH_DATA" == 1 ]] || return 0
  mkdir -p "$1/original" "$1/font"
  cp -r "$ORIG_TREE"/. "$1/original/"
  cp "$STAGE/eten.golemfnt" "$1/font/buckrogers-eten-top-pad.golemfnt"
  mkdir -p "$1/local"
  cp "$MANUAL_EXCERPT" "$1/local/manual-english.tsv"
  printf '%s\n' "本機自用完整版：內含原版遊戲《Buck Rogers: Countdown to Doomsday》，著作權屬原權利人。" \
    "內附倚天中文字型（購買授權，限本機使用），預設優先使用；刪除 font/buckrogers-eten-top-pad.golemfnt 即改用 GNU Unifont。" \
    "內附本機手冊英文摘錄 local/manual-english.tsv：手冊查詢題會在中文段落下方顯示英文原文與字序。" \
    "請勿散布、上傳或分享本檔案。" > "$1/本機自用-請勿散布.txt"
}
# check <目錄>：一般版做外洩掃描；完整版改為確認原版確實在包內。
check() {
  if [[ "$WITH_DATA" == 1 ]]; then
    [[ -f "$(find "$1" -path '*original/START.EXE' | head -1)" ]] || die "完整版缺 original/START.EXE"
    [[ -f "$(find "$1" -path '*font/buckrogers-eten-top-pad.golemfnt' | head -1)" ]] || die "完整版缺倚天字型"
  else
    scan "$1"
  fi
}
# prune <樣式>：只清同一變體的舊產物
prune() {
  local f
  for f in $DIST/$1; do
    [[ -e "$f" ]] || continue
    case "$f" in *-with-data-*) [[ "$WITH_DATA" == 1 ]] || continue ;; *) [[ "$WITH_DATA" == 1 ]] && continue ;; esac
    rm -f "$f"
  done
}

scan() {  # scan <解開目錄>
  local mounts=() args=() i=0
  for s in "${LEAK_SOURCES[@]}"; do mounts+=(-v "$s:/leak$i:ro"); args+=("/leak$i"); i=$((i + 1)); done
  dr -v "$ROOT:/p:ro" -v "$1:/pkg:ro" "${mounts[@]}" "$PY_IMAGE" python3 /p/tools/release/leak_scan.py /pkg "${args[@]}"
}

pack_linux() {
  local app="$STAGE/AppDir" out="$DIST/BuckRogersCHT-$VER$SUF-x86_64.AppImage"
  mkdir -p "$app/usr/share/doc/buckrogers-cht"
  cp -r "$STAGE/common/." "$app/"
  cp "$STAGE/out/linux/buckrogers-play" "$app/buckrogers-play"
  cp LICENSE "$app/usr/share/doc/buckrogers-cht/LICENSE"
  cp "$STAGE/icon-256.png" "$app/buckrogers-cht.png"
  cp "$STAGE/icon-256.png" "$app/.DirIcon"
  cat > "$app/AppRun" <<'SH'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/buckrogers-play" "$@"
SH
  chmod +x "$app/AppRun" "$app/buckrogers-play"
  cat > "$app/buckrogers-cht.desktop" <<'DESK'
[Desktop Entry]
Type=Application
Name=拯救地球（繁中）
Name[en]=Buck Rogers CHT
Exec=buckrogers-play
Icon=buckrogers-cht
Categories=Game;RolePlaying;
Terminal=false
DESK
  payload "$app"
  check "$app"
  prune 'BuckRogersCHT-*-x86_64.AppImage'
  timeout 15m docker run --rm --network none --memory 2g --cpus 2 --pids-limit 64 \
    --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$STAGE:/stage" -v "$DIST:/dist" --entrypoint sh "$APPIMAGE_IMAGE" -c "
      set -eu
      [ \$(stat -c %s /opt/runtime-x86_64) = $RUNTIME_SIZE ]
      mksquashfs /stage/AppDir /tmp/app.squashfs -root-owned -noappend -no-progress -comp zstd -Xcompression-level 19 >/dev/null
      cat /opt/runtime-x86_64 /tmp/app.squashfs > '/dist/$(basename "$out")'
      chmod +x '/dist/$(basename "$out")'
      rm -rf /stage/check-appimage
      unsquashfs -q -o $RUNTIME_SIZE -d /stage/check-appimage '/dist/$(basename "$out")' >/dev/null"
  check "$STAGE/check-appimage" || { rm -f "$out"; die "AppImage 檢查失敗"; }
  echo "[package] $out"
}

pack_windows() {
  local dir="$STAGE/win/BuckRogersCHT" out="$DIST/BuckRogersCHT-$VER$SUF-win64.zip"
  dr "${GOENV[@]}" "${GOMOUNT[@]}" -e GOOS=windows -e GOARCH=amd64 -e CGO_ENABLED=0 -w /src "$GO_IMAGE" sh -c "
    go build -trimpath -ldflags '$LDFLAGS -H windowsgui' -o /out/win/BuckRogersCHT.exe ./cmd/buckrogers-play &&
    go version -m /out/win/BuckRogersCHT.exe > /out/modinfo-windows.txt"
  mkdir -p "$dir"
  cp -r "$STAGE/common/." "$dir/"
  cp "$STAGE/out/win/BuckRogersCHT.exe" "$dir/"
  payload "$dir"
  check "$dir"
  prune 'BuckRogersCHT-*-win64.zip'
  dr -v "$ROOT:/p:ro" -v "$STAGE:/stage" -v "$DIST:/dist" "$PY_IMAGE" \
    python3 /p/tools/release/zipdir.py /stage/win/BuckRogersCHT "/dist/$(basename "$out")"
  echo "[package] $out"
}

pack_macos() {
  local top="$STAGE/mac/BuckRogersCHT" app="$STAGE/mac/BuckRogersCHT/BuckRogersCHT.app" out="$DIST/BuckRogersCHT-$VER$SUF-macos.zip"
  mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources" "$STAGE/out/mac"
  dr "${GOENV[@]}" "${GOMOUNT[@]}" -e "MIN=$MAC_MIN" -w /src "$MAC_IMAGE" bash -c "
    set -euo pipefail
    eval \"\$(osxcross-conf)\"
    export CGO_ENABLED=1 GOOS=darwin GOPATH=/tmp/gopath MACOSX_DEPLOYMENT_TARGET=\$MIN
    for arch in arm64 amd64; do
      case \$arch in arm64) pre=arm64-apple-\$OSXCROSS_TARGET ;; amd64) pre=x86_64-apple-\$OSXCROSS_TARGET ;; esac
      env GOARCH=\$arch CC=\$pre-clang CXX=\$pre-clang++ CGO_CFLAGS=-mmacosx-version-min=\$MIN CGO_LDFLAGS=-mmacosx-version-min=\$MIN \
        go build -trimpath -ldflags '$LDFLAGS' -o /out/mac/buckrogers-play-\$arch ./cmd/buckrogers-play
    done
    x86_64-apple-\$OSXCROSS_TARGET-lipo -create /out/mac/buckrogers-play-arm64 /out/mac/buckrogers-play-amd64 -output /out/mac/buckrogers-play
    x86_64-apple-\$OSXCROSS_TARGET-lipo -archs /out/mac/buckrogers-play > /out/mac/archs.txt"
  [[ "$(cat "$STAGE/out/mac/archs.txt")" == *x86_64*arm64* || "$(cat "$STAGE/out/mac/archs.txt")" == *arm64*x86_64* ]] || die "lipo 架構不齊：$(cat "$STAGE/out/mac/archs.txt")"
  cp "$STAGE/out/mac/buckrogers-play" "$app/Contents/MacOS/buckrogers-play"
  chmod +x "$app/Contents/MacOS/buckrogers-play"
  cp -r "$STAGE/common/." "$app/Contents/Resources/"
  for f in 讀我.txt LICENSE; do cp "$STAGE/common/$f" "$top/$f"; done
  dr -i -v "$STAGE:/stage" "$PY_IMAGE" python3 - <<'PY'
import struct
body = b""
for size, tag in ((256, b"ic08"), (512, b"ic09")):
    png = open(f"/stage/icon-{size}.png", "rb").read()
    body += tag + struct.pack(">I", len(png) + 8) + png
open("/stage/mac/BuckRogersCHT/BuckRogersCHT.app/Contents/Resources/buckrogers-cht.icns", "wb").write(b"icns" + struct.pack(">I", len(body) + 8) + body)
PY
  local short
  short="$(printf '%s' "$VER" | sed -n 's/^v\{0,1\}\([0-9][0-9.]*\).*/\1/p')"
  [[ -n "$short" ]] || short="0.0.0"
  cat > "$app/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key><string>zh_TW</string>
	<key>CFBundleDisplayName</key><string>拯救地球（繁中）</string>
	<key>CFBundleExecutable</key><string>buckrogers-play</string>
	<key>CFBundleIconFile</key><string>buckrogers-cht</string>
	<key>CFBundleIdentifier</key><string>io.github.wicanr2.buckrogerscht</string>
	<key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
	<key>CFBundleName</key><string>BuckRogersCHT</string>
	<key>CFBundlePackageType</key><string>APPL</string>
	<key>CFBundleShortVersionString</key><string>$short</string>
	<key>CFBundleVersion</key><string>$VER</string>
	<key>LSApplicationCategoryType</key><string>public.app-category.role-playing-games</string>
	<key>LSMinimumSystemVersion</key><string>$MAC_MIN</string>
	<key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST
  payload "$app/Contents/Resources"
  [[ "$WITH_DATA" == 1 ]] && cp "$app/Contents/Resources/本機自用-請勿散布.txt" "$top/"
  check "$top"
  prune 'BuckRogersCHT-*-macos.zip'
  dr -v "$ROOT:/p:ro" -v "$STAGE:/stage" -v "$DIST:/dist" "$PY_IMAGE" \
    python3 /p/tools/release/zipdir.py /stage/mac/BuckRogersCHT "/dist/$(basename "$out")"
  echo "[package] $out"
}

case "$TARGET" in
  linux) pack_linux ;;
  windows) pack_windows ;;
  macos) pack_macos ;;
  all) pack_linux; pack_windows; pack_macos ;;
  *) die "目標須為 all、linux、windows 或 macos" ;;
esac
ls -l "$DIST"
