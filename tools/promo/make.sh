#!/bin/sh
# 推廣片合成（規格：Issue #32；方法與素材來源規則見 rulebook 93）。在影片工具容器裡跑：
#
#   tools/promo/run.sh
#
# 輸出 workplace/promo/buckrogers-cht-promo.mp4。
# ⚠ 配樂是 workplace/dosboxx-audio/promo/capture/start_000.wav —— DOSBox-X 跑原版錄下的輸出，
#   不是 dosgolem 的合成結果。使用者 2026-09-28 決定公開影片使用原版音樂，片尾註明權利歸屬。
# ⚠ 畫面全部是發行設定（Unifont、3 倍、無手冊英文列）的實跑截圖；不收手冊查詢題畫面。
#   v1.1.0 起畫面是各語言通道的同狀態輸出（workplace/promo-110/shots，由 tools 之外的 runner 腳本產生，
#   見 docs/re/phase-310-release-v110.md）；v1.0.0 的舊影片用 workplace/play-e2e 的 ps*.png。
set -eu
cd /src

W=1280; H=720; FPS=25
BG_DEEP='#000000'; BG_LITE='#0a1030'
ACCENT='#d8a848'; ACCENT_DIM='#6a5020'   # 遊戲畫框的金色
TEXT='#ffffff'; DIM='#b0b0b0'; GREEN='#55ff55'
FONT_TITLE=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
FONT_BODY=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

SHOT=workplace/promo-110/shots
MUSIC=workplace/dosboxx-audio/promo/capture/start_000.wav
OUT=workplace/promo
TMP=$OUT/tmp
rm -rf "$TMP"; mkdir -p "$TMP" "$OUT"
[ -f "$MUSIC" ] || { echo "缺配樂 $MUSIC"; exit 2; }
for f in "$FONT_TITLE" "$FONT_BODY"; do [ -f "$f" ] || { echo "缺字型 $f"; exit 2; }; done

bg() { convert -size ${W}x${H} "radial-gradient:${BG_LITE}-${BG_DEEP}" "$1"; }

# card：$1 out $2 中標 $3 英標 $4 副標 $5 第二行副標
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

# slide：3 倍截圖（960×600）以原尺寸置中，底部字幕條。$1 out $2 截圖 $3 字幕
slide() {
  bg "$TMP/bg.png"
  convert "$TMP/bg.png" "$SHOT/$2" -gravity north -geometry +0+4 -composite \
    -fill "#000000d0" -draw "rectangle 0,612 ${W},${H}" \
    -stroke "$ACCENT" -strokewidth 1 -draw "line 0,612 ${W},612" -stroke none \
    -font "$FONT_BODY" -fill "$TEXT" -gravity south -pointsize 32 -annotate +0+34 "$3" "$1"
}

clip() {
  fo=$(awk "BEGIN{print $3-0.6}")
  ffmpeg -y -loglevel error -loop 1 -i "$1" -t "$3" -r $FPS \
    -vf "fade=t=in:st=0:d=0.6,fade=t=out:st=$fo:d=0.6,format=yuv420p" \
    -threads 2 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$2"
}

card  "$TMP/00.png" "拯救地球" "BUCK ROGERS: COUNTDOWN TO DOOMSDAY" \
  "SSI 1990 ・ DOS 英文版 ・ 繁體中文／簡體中文／日文／韓文" "原版程式一行不改，在 dosgolem 上執行並即時覆繪"
slide "$TMP/01.png" party-zh-TW.png "隊伍與功能選單：玩家名音譯成「中文(英文)」"
slide "$TMP/02.png" cmdr-zh-TW.png "指揮官登場：人名依印刷手冊譯名"
slide "$TMP/03.png" narr-zh-TW.png "廢棄飛船敘事：玩家名接入句中，原版版面與時機不變"
slide "$TMP/04.png" cmdr-zh-CN.png "F4 切換語言：簡體中文"
slide "$TMP/05.png" party-ja.png "日文：玩家名音譯成片假名（機器輔助譯文）"
slide "$TMP/06.png" narr-ja.png "日文：敘事與選單"
slide "$TMP/07.png" party-ko.png "韓文：玩家名音譯成諺文（機器輔助譯文）"
slide "$TMP/08.png" battle-ko.png "韓文：戰鬥畫面"
card  "$TMP/09.png" "AdLib 音樂 ・ 滑鼠 ・ 三平台" "Windows ・ macOS ・ Linux" \
  "模擬 AdLib 與 PC 喇叭；手冊查詢題顯示中文手冊段落" "需自備合法取得的原版遊戲，程式核對雜湊後匯入"
card  "$TMP/99.png" "拯救地球 繁體中文化" "github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht" \
  "RRSAL-1.0 ・ 非商業免費 ・ 不附原版遊戲" "配樂為原版遊戲音樂（DOSBox-X 錄製），著作權屬原權利人"

LIST="$TMP/list.txt"; : > "$LIST"
for f in 00 01 02 03 04 05 06 07 08 09 99; do
  case "$f" in 00|99) s=5 ;; 09) s=6 ;; *) s=4.8 ;; esac
  clip "$TMP/$f.png" "$TMP/s_$f.mp4" "$s"
  echo "file 's_$f.mp4'" >> "$LIST"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -threads 2 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$TMP/silent.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/silent.mp4")
FO=$(awk "BEGIN{print $DUR-3}")
# 配樂取錄音開頭；第 55 秒起原版有停頓，影片控制在 55 秒內
ffmpeg -y -loglevel error -i "$TMP/silent.mp4" -i "$MUSIC" \
  -filter_complex "[1:a]atrim=0:$DUR,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.5,afade=t=out:st=$FO:d=3[a]" \
  -map 0:v -map "[a]" -threads 2 -c:v libx264 -preset veryfast -c:a aac -b:a 192k \
  -movflags +faststart "$OUT/buckrogers-cht-promo.mp4"
echo "== 產出"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/buckrogers-cht-promo.mp4"
ffprobe -v error -select_streams a -show_entries stream=duration -of csv=p=0 "$OUT/buckrogers-cht-promo.mp4"
ls -la "$OUT/buckrogers-cht-promo.mp4"
