docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:base-image \
    -f docker-images/base-image/Dockerfile.base-image \
    --push .