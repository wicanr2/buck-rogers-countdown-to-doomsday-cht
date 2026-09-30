# 規格 041 §3.1：簡體（zh-CN）產生器的固定版本 image（buck-zhcn-opencc:1.4.2）。
# OpenCC 1.4.2（PyPI 官方 Python 綁定，Apache-2.0），wheel 只有 x86_64。
# 建置不開網路：wheel 由 build.sh 預先下載到 workplace/opencc-wheels/（唯一需要網路的步驟），
# 以 requirements.txt 的 SHA-256 鎖定、--no-index 安裝。基底以 digest 鎖定。
FROM python:3.13-slim@sha256:6771159cd4fa5d9bba1258caf0b82e6b73458c694d178ad97c5e925c2d0e1a91
COPY requirements.txt opencc-1.4.2-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl /wheels/
RUN pip install --no-cache-dir --no-index --find-links /wheels --require-hashes -r /wheels/requirements.txt \
 && rm -rf /wheels \
 && python -c "import opencc; assert opencc.__version__ == '1.4.2', opencc.__version__"
