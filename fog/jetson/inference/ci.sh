docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:inference-jetson \
    -f fog/jetson/inference/Dockerfile \
    --push .