docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:input-jetson \
    -f input/Dockerfile \
    --push .