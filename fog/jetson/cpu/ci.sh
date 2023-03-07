docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:cpu-jetson \
    -f fog/jetson/cpu/Dockerfile \
    --push .