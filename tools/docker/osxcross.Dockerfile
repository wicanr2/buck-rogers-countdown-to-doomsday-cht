# macOS 交叉編譯映像 buckrogers-osxcross（規格 035 §3.5）：
#
#   docker build -t buckrogers-osxcross -f tools/docker/osxcross.Dockerfile tools/docker
#
# 以本機既有的 psychicwar-osxcross（osxcross、SDK 15.5、lipo）為底，把 Go 換成與 Linux／Windows
# 同一份的 eob-remake-go 1.26.7。兩個來源映像只讀取，不修改也不清理；建置不需網路。
# ⚠ SDK 授權只允許在 Apple 硬體上使用：本映像只留本機，不上傳、不散布。
FROM eob-remake-go:1.26.7-ebiten2.9.9 AS gobase
FROM psychicwar-osxcross
RUN rm -rf /usr/local/go
COPY --from=gobase /usr/local/go /usr/local/go
ENV PATH="/osxcross/bin:/usr/local/go/bin:${PATH}"
