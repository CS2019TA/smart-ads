docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:preprocess-jetson \
    -f fog/jetson/preprocess/Dockerfile \
    --push .