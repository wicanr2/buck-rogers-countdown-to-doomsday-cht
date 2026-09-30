#!/usr/bin/env bash
# 建立規格 041 的 OpenCC image（buck-zhcn-opencc:1.4.2）。
#
#   tools/docker/opencc/build.sh
#
# 1. wheel 不在 workplace/opencc-wheels/ 時，才以 pip download 下載（唯一開網路的步驟）；
# 2. 核對 wheel SHA-256（requirements.txt 的 --hash）；
# 3. docker build --network none，pip --no-index --require-hashes 安裝。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
D="$ROOT/tools/docker/opencc"
CACHE="$ROOT/workplace/opencc-wheels"
IMAGE="${IMAGE:-buck-zhcn-opencc:1.4.2}"
WHEEL="opencc-1.4.2-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl"
WANT="$(sed -n 's/.*--hash=sha256:\([0-9a-f]\{64\}\).*/\1/p' "$D/requirements.txt")"
[[ ${#WANT} -eq 64 ]] || { echo "requirements.txt 缺 SHA-256" >&2; exit 1; }
mkdir -p "$CACHE"
if [[ ! -f "$CACHE/$WHEEL" ]]; then
  # 只有這一步開網路；以同一個 python 基底下載，不安裝。
  timeout 10m docker run --rm --name buck-zhcn-opencc-dl --memory 1g --cpus 2 --pids-limit 128 \
    --log-opt max-size=10m --log-opt max-file=3 -u "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$CACHE:/dl" -v "$D:/req:ro" \
    python:3.13-slim@sha256:6771159cd4fa5d9bba1258caf0b82e6b73458c694d178ad97c5e925c2d0e1a91 \
    pip download --no-deps --only-binary=:all: --platform manylinux2014_x86_64 --python-version 3.13 \
      --require-hashes -r /req/requirements.txt -d /dl
fi
GOT="$(sha256sum "$CACHE/$WHEEL" | cut -c1-64)"
[[ "$GOT" == "$WANT" ]] || { echo "wheel SHA-256 不符：$GOT" >&2; exit 1; }
cp "$D/requirements.txt" "$CACHE/requirements.txt"
docker build --network none -t "$IMAGE" -f "$D/Dockerfile" "$CACHE"
docker image inspect "$IMAGE" --format '{{.Id}}'
