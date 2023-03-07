docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:cpu-check \
    -f docker-images/cpu-check/Dockerfile.cpu-check \
    --push .