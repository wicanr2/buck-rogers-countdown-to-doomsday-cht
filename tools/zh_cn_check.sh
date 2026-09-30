#!/usr/bin/env bash
# 規格 041 §3.7：簡體（zh-CN）驗證，逐支明列呼叫形式。全部在 buck-zhcn-opencc:1.4.2 內、--network none、
# repo 唯讀掛載。任何一支失敗即非零結束（tools/package.sh 的前置檢查）。
#
#   tools/zh_cn_check.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${ZH_CN_IMAGE:-buck-zhcn-opencc:1.4.2}"
for d in "$ROOT/text" "$ROOT/tools" "$ROOT/font"; do [[ -d "$d" ]] || { echo "[zh_cn_check] 缺 $d" >&2; exit 1; }; done
docker image inspect "$IMAGE" >/dev/null 2>&1 || { echo "[zh_cn_check] 缺映像 $IMAGE（tools/docker/opencc/build.sh）" >&2; exit 1; }

timeout 20m docker run --rm --name "buck-zhcn-check-$$" --network none --memory 3g --cpus 2 --pids-limit 128 \
  --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$ROOT/text:/p/text:ro" -v "$ROOT/tools:/p/tools:ro" -v "$ROOT/font:/p/font:ro" -w /p "$IMAGE" sh -eu -c '
T=text; L="--lang zh-CN"
step() { echo "[zh_cn_check] $*"; "$@" >/tmp/out.txt 2>&1 || { cat /tmp/out.txt; echo "[zh_cn_check] 失敗：$*" >&2; exit 1; }; }
# 1. 產生器：重新產生比對、詞表／覆寫表／帳本、名字、跨家族一致性
step python3 tools/zh_cn_convert.py --check
# 2. 以 --lang zh-CN 呼叫
step python3 tools/menu_events.py $T/menu-events.tsv $T/menu.zh-CN.tsv $L
step python3 tools/gender_events.py $T/gender-events.tsv $T/gender.zh-CN.tsv $T/post-race-events.tsv $T/gender-selection-events.tsv $L
step python3 tools/class_events.py $T/class-events.tsv $T/class.zh-CN.tsv $T/post-gender-events.tsv $T/class-selection-events.tsv $L
step python3 tools/character_sheet_events.py $T/character-sheet-events.tsv $T/character-sheet.zh-CN.tsv $T/post-class-events.tsv $L
step python3 tools/name_prompt_catalog.py $T/name-prompt-events.tsv $T/name-prompt.zh-CN.tsv $T/reroll-no-events.tsv $L
step python3 tools/body_icon_catalog.py $T/body-icon-events.tsv $T/body-icon-affixes.tsv $T/body-icon.zh-CN.tsv $T $L
step python3 tools/career_skill_screen_catalog.py $T/career-skill-screen-events.tsv $T/career-skill-screen.zh-CN.tsv $T/name-confirm-events.tsv $T/career-skill-selection-events.tsv $T/character-sheet.zh-CN.tsv $L
step python3 tools/save_roster_join_catalog.py $L
step python3 tools/technical_skill_screen_catalog.py $T/technical-skill-screen-events.tsv $T/technical-skill-screen.zh-CN.tsv $T/career-skill-exit-events.tsv $T/technical-skill-selection-events.tsv $L
step python3 tools/header_columns.py --text $T --workplace /tmp/none $L
step python3 tools/name_glossary.py $L lint
step python3 tools/catalog_font.py lint $L
step python3 tools/skill_action_bar_catalog.py $T/skill-action-bar-events.tsv $T/skill-action-bar.zh-CN.tsv $L
# 3. 以 *.zh-CN.tsv 路徑呼叫
step python3 tools/story_opening_catalog.py $T/story-opening-events.tsv $T/story-opening.zh-CN.tsv
for n in 2 3 4 5 6 7 8 9; do
  step python3 tools/story_page${n}_catalog.py $T/story-page${n}-events.tsv $T/story-page${n}.zh-CN.tsv
done
step python3 tools/manual_catalog.py $T/manual-questions.tsv $T/manual-source-crosswalk.tsv $T/manual-events.tsv $T/manual.zh-CN.tsv
step python3 tools/manual_overlay_layout.py $T/manual-overlay-layout.tsv $T/manual.zh-CN.tsv
# 4. 字元清單：由正式 zh-CN 譯文（含音譯對照簡體字）重生，須與版控檔逐位元組相同
step python3 tools/catalog_font.py chars $L --out /tmp/characters.zh-CN.txt
cmp /tmp/characters.zh-CN.txt font/characters.zh-CN.txt || { echo "[zh_cn_check] font/characters.zh-CN.txt 未同步" >&2; exit 1; }
echo "[zh_cn_check] 全部通過"
'
