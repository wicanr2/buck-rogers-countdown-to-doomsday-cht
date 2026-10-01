#!/bin/sh
# 實機錄影版推廣片合成：把 tools/promo/record.sh 逐格輸出的畫格依 play-segments.tsv 剪成影片。
# 在影片工具容器裡跑（tools/promo/play-run.sh）。
#
#   FRAMES  畫格目錄（預設 workplace/phase311/runs/rec1/frames，3 倍、每 2 格一張）
#   BAN     手冊題畫面的遊戲畫格範圍 A-B（預設 3040-4040）
#   OUT     輸出檔（預設 workplace/promo/buckrogers-cht-gameplay.mp4）
#
# ⚠ 畫面是 dosgolem 逐格輸出的實機執行（發行設定：Unifont、3 倍、無手冊英文列），輸入由固定腳本重播；
#   不是螢幕錄影，也不是互動遊玩。手冊查詢題畫面不在分鏡內。
# ⚠ 配樂是 workplace/dosboxx-audio/promo/capture/start_000.wav —— DOSBox-X 跑原版錄下的輸出（rulebook 93），
#   不是 dosgolem 的合成結果；影片與遊戲音訊不同步，配樂只是背景。使用者 2026-09-28 決定公開影片使用原版音樂。
set -eu
cd /src

W=1280; H=720; FPS=30
BG_DEEP='#000000'; BG_LITE='#0a1030'
ACCENT='#d8a848'; ACCENT_DIM='#6a5020'
TEXT='#ffffff'; DIM='#b0b0b0'
FONT_TITLE=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
FONT_BODY=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

FRAMES=${FRAMES:-workplace/phase311/runs/rec1/frames}
BAN=${BAN:-3040-4040}   # 手冊題畫面的遊戲畫格範圍（rec1 的值）；分鏡不可與它重疊
SEGS=tools/promo/play-segments.tsv
MUSIC=workplace/dosboxx-audio/promo/capture/start_000.wav
OUT=${OUT:-workplace/promo/buckrogers-cht-gameplay.mp4}
TMP=workplace/promo/tmp-play
rm -rf "$TMP"; mkdir -p "$TMP" "$(dirname "$OUT")"
for f in "$FONT_TITLE" "$FONT_BODY" "$MUSIC" "$SEGS"; do [ -f "$f" ] || { echo "缺 $f"; exit 2; }; done
[ -d "$FRAMES" ] || { echo "缺畫格目錄 $FRAMES"; exit 2; }

bg() { convert -size ${W}x${H} "radial-gradient:${BG_LITE}-${BG_DEEP}" "$1"; }

card() {
  bg "$TMP/bg.png"
  convert "$TMP/bg.png" -gravity center \
    -font "$FONT_TITLE" -fill "$ACCENT_DIM" -pointsize 80 -annotate +4-126 "$2" \
    -fill "$ACCENT" -pointsize 80 -annotate +0-130 "$2" \
    -font "$FONT_BODY" -fill "$TEXT" -pointsize 34 -annotate +0-10 "$3" \
    -fill "$DIM" -pointsize 26 -annotate +0+70 "$4" \
    -fill "$DIM" -pointsize 26 -annotate +0+115 "$5" \
    -stroke "$ACCENT" -strokewidth 2 -fill none -draw "rectangle 36,36 $((W-36)),$((H-36))" "$1"
}

# layer：底圖加字幕條（畫格 960×600 疊在 160,4，不蓋到字幕條）
layer() {
  bg "$TMP/bg.png"
  convert "$TMP/bg.png" \
    -fill "#000000d0" -draw "rectangle 0,612 ${W},${H}" \
    -stroke "$ACCENT" -strokewidth 1 -draw "line 0,612 ${W},612" -stroke none \
    -font "$FONT_BODY" -fill "$TEXT" -gravity south -pointsize 32 -annotate +0+34 "$2" -depth 8 "PNG24:$1"
}

clip_card() {
  fo=$(awk "BEGIN{print $3-0.6}")
  ffmpeg -y -loglevel error -loop 1 -i "$1" -t "$3" -r $FPS \
    -vf "fade=t=in:st=0:d=0.6,fade=t=out:st=$fo:d=0.6,format=yuv420p" \
    -threads 2 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p "$2"
}

card "$TMP/c00.png" "拯救地球" "BUCK ROGERS: COUNTDOWN TO DOOMSDAY" \
  "實機遊玩錄影 ・ 繁體中文／簡體中文／日文／韓文" "畫面是遊戲實際執行的逐格輸出，輸入以固定腳本重播"
card "$TMP/c99.png" "拯救地球 繁體中文化" "github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht" \
  "RRSAL-1.0 ・ 非商業免費 ・ 不附原版遊戲" "配樂為原版遊戲音樂（DOSBox-X 錄製），著作權屬原權利人"
clip_card "$TMP/c00.png" "$TMP/s_000.mp4" 3.5
echo "file 's_000.mp4'" > "$TMP/list.txt"

# 分鏡：每段先列出畫格，再疊上字幕層

grep -v "^#" "$SEGS" > "$TMP/segs.txt"
while IFS="$(printf '\t')" read -r id a b k join cap; do
  [ -n "$id" ] || continue
  # 手冊查詢題的畫面（含輸入的作答）不得入片：BAN 是該次錄影的遊戲畫格範圍 A-B，與分鏡重疊就中止
  if [ "$a" -lt "${BAN#*-}" ] && [ "$b" -gt "${BAN%-*}" ]; then echo "分鏡 $id（$a-$b）與手冊題範圍 $BAN 重疊"; exit 5; fi
  L="$TMP/f_$id.txt"; : > "$L"; cnt=0; f=$a
  while [ "$f" -lt "$b" ]; do
    p=$(printf '%s/frame-%08d.png' "$FRAMES" "$f")
    [ -f "$p" ] || { echo "缺畫格 $p（分鏡 $id）"; exit 3; }
    printf "file '/src/%s'\nduration 0.0333333\n" "$p" >> "$L"
    cnt=$((cnt+1)); f=$((f + 2*k))
  done
  last=$(printf '%s/frame-%08d.png' "$FRAMES" $((f - 2*k)))
  printf "file '/src/%s'\n" "$last" >> "$L"
  dur=$(awk "BEGIN{printf \"%.4f\", $cnt/$FPS}")
  layer "$TMP/l_$id.png" "$cap"
  if [ "$join" = fade ]; then
    fo=$(awk "BEGIN{print $dur-0.12}"); FADE=",fade=t=in:st=0:d=0.12,fade=t=out:st=$fo:d=0.12"
  else FADE=""; fi
  ffmpeg -nostdin -y -loglevel error -filter_threads 2 -filter_complex_threads 2 -f concat -safe 0 -i "$L" -loop 1 -i "$TMP/l_$id.png" \
    -filter_complex "[0:v]fps=$FPS,format=rgba[g];[1:v]format=rgb24[b];[b][g]overlay=160:4:shortest=1,format=yuv420p$FADE" \
    -r $FPS -threads 2 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p "$TMP/s_$id.mp4"
  echo "file 's_$id.mp4'" >> "$TMP/list.txt"
  echo "$id $cnt 張 $dur 秒"
done < "$TMP/segs.txt"
clip_card "$TMP/c99.png" "$TMP/s_999.mp4" 4.5
echo "file 's_999.mp4'" >> "$TMP/list.txt"

ffmpeg -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -threads 2 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r $FPS "$TMP/silent.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/silent.mp4")
FO=$(awk "BEGIN{print $DUR-3}")
# 配樂取錄音開頭；第 55 秒起原版有停頓，影片須在 55 秒內
awk "BEGIN{exit !($DUR <= 55.5)}" || { echo "影片 $DUR 秒超過配樂可用的 55 秒"; exit 4; }
ffmpeg -y -loglevel error -i "$TMP/silent.mp4" -i "$MUSIC" \
  -filter_complex "[1:a]atrim=0:$DUR,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.5,afade=t=out:st=$FO:d=3[a]" \
  -map 0:v -map "[a]" -threads 2 -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k \
  -movflags +faststart "$OUT"
echo "== 產出"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
ffprobe -v error -select_streams a -show_entries stream=duration -of csv=p=0 "$OUT"
ls -la "$OUT"
