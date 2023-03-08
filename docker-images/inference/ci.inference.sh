docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:inference \
    -f docker-images/inference/Dockerfile.inference \
    --push .