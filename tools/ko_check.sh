#!/usr/bin/env bash
# 規格 043 §3.3：韓文（ko）驗證，逐支明列呼叫形式。全部在 python:3.12-slim 內、--network none、repo 唯讀掛載。
# 任何一支失敗即非零結束（tools/package.sh 的前置檢查）。Unifont hex 存在時另核對 font/charset.ko.txt。
#
#   tools/ko_check.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${KO_CHECK_IMAGE:-python:3.12-slim}"
UNIFONT_DIR="${UNIFONT_DIR:-$ROOT/workplace/unifont-src}"
for d in "$ROOT/text" "$ROOT/tools" "$ROOT/font"; do [[ -d "$d" ]] || { echo "[ko_check] 缺 $d" >&2; exit 1; }; done
docker image inspect "$IMAGE" >/dev/null 2>&1 || { echo "[ko_check] 缺映像 $IMAGE" >&2; exit 1; }
MOUNT_UNIFONT=()
if [[ -f "$UNIFONT_DIR/unifont_all-17.0.05.hex.gz" ]]; then
  MOUNT_UNIFONT=(-v "$UNIFONT_DIR:/unifont:ro")
fi
# 規格 044 §5：固定名單與例子表（docs/re）；dosgolem 的 testdata 副本在時一併比對雜湊
[[ -d "$ROOT/docs/re" ]] || { echo "[ko_check] 缺 $ROOT/docs/re" >&2; exit 1; }
MOUNT_TRANSLIT=(-v "$ROOT/docs/re:/p/docs/re:ro")
DG_TESTDATA="$ROOT/workplace/dosgolem/xlate/translitjk/testdata"
if [[ -d "$DG_TESTDATA" ]]; then
  MOUNT_TRANSLIT+=(-v "$DG_TESTDATA:/p/workplace/dosgolem/xlate/translitjk/testdata:ro")
fi

timeout 20m docker run --rm --name "buck-ko-check-$$" --network none --memory 3g --cpus 2 --pids-limit 128 \
  --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$ROOT/text:/p/text:ro" -v "$ROOT/tools:/p/tools:ro" -v "$ROOT/font:/p/font:ro" "${MOUNT_UNIFONT[@]}" "${MOUNT_TRANSLIT[@]}" \
  -w /p "$IMAGE" sh -eu -c '
T=text; L="--lang ko"
step() { echo "[ko_check] $*"; "$@" >/tmp/out.txt 2>&1 || { cat /tmp/out.txt; echo "[ko_check] 失敗：$*" >&2; exit 1; }; }
# 1. ko_check.py、合成負例（test_lang_check.py）；ja_check.py 薄包裝仍全綠（規格 043 §5.1）；覆蓋斷言：31 個家族檔 5,414 列、5,406 個不同 key（規格 043 §3.1）
step python3 tools/ko_check.py --expect-rows 5414 --expect-keys 5406
step sh -c "cd tools && python3 -m unittest test_ja_check.py test_lang_check.py test_name_glossary.py test_translit_jk.py"
step python3 tools/ja_check.py --expect-rows 5414 --expect-keys 5406
# 2. 以 --lang ko 呼叫
step python3 tools/menu_events.py $T/menu-events.tsv $T/menu.ko.tsv $L
step python3 tools/gender_events.py $T/gender-events.tsv $T/gender.ko.tsv $T/post-race-events.tsv $T/gender-selection-events.tsv $L
step python3 tools/class_events.py $T/class-events.tsv $T/class.ko.tsv $T/post-gender-events.tsv $T/class-selection-events.tsv $L
step python3 tools/character_sheet_events.py $T/character-sheet-events.tsv $T/character-sheet.ko.tsv $T/post-class-events.tsv $L
step python3 tools/name_prompt_catalog.py $T/name-prompt-events.tsv $T/name-prompt.ko.tsv $T/reroll-no-events.tsv $L
step python3 tools/body_icon_catalog.py $T/body-icon-events.tsv $T/body-icon-affixes.tsv $T/body-icon.ko.tsv $T $L
step python3 tools/career_skill_screen_catalog.py $T/career-skill-screen-events.tsv $T/career-skill-screen.ko.tsv $T/name-confirm-events.tsv $T/career-skill-selection-events.tsv $T/character-sheet.ko.tsv $L
step python3 tools/save_roster_join_catalog.py $L
step python3 tools/technical_skill_screen_catalog.py $T/technical-skill-screen-events.tsv $T/technical-skill-screen.ko.tsv $T/career-skill-exit-events.tsv $T/technical-skill-selection-events.tsv $L
step python3 tools/header_columns.py --text $T --workplace /tmp/none $L
step python3 tools/name_glossary.py $L lint
step python3 tools/catalog_font.py lint $L
# 音譯資料（規格 044、045）：詞典 lint、允許字集檔、例子表、固定名單（含 pending 即失敗）
step python3 tools/translit_jk.py lint $L
step python3 tools/translit_jk.py chars --check $L
step python3 tools/translit_jk.py examples --check $L
step python3 tools/translit_jk.py verify-fixed $L
step python3 tools/skill_action_bar_catalog.py $T/skill-action-bar-events.tsv $T/skill-action-bar.ko.tsv $L
# 3. 以 *.ko.tsv 路徑呼叫（manual_catalog.py 對只有標頭的 manual.ko.tsv 失敗，手冊韓文另訂時再納入）
step python3 tools/story_opening_catalog.py $T/story-opening-events.tsv $T/story-opening.ko.tsv
for n in 2 3 4 5 6 7 8 9; do
  step python3 tools/story_page${n}_catalog.py $T/story-page${n}-events.tsv $T/story-page${n}.ko.tsv
done
step python3 tools/manual_overlay_layout.py $T/manual-overlay-layout.tsv $T/manual.ko.tsv
# 4. 字元清單：由正式 ko 譯文重生，須與版控檔逐位元組相同
step python3 tools/catalog_font.py chars $L --out /tmp/characters.ko.txt
cmp /tmp/characters.ko.txt font/characters.ko.txt || { echo "[ko_check] font/characters.ko.txt 未同步" >&2; exit 1; }
# 5. 允許字集：Unifont hex 存在時重生比對
if [ -f /unifont/unifont_all-17.0.05.hex.gz ]; then
  step python3 tools/ko_charset.py --font /unifont/unifont_all-17.0.05.hex.gz --check
else
  echo "[ko_check] 略過 charset.ko.txt 重生比對（沒有 Unifont hex；打包前置檢查必須提供）"
fi
echo "[ko_check] 全部通過"
'
