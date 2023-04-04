docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:preprocess \
    -f docker-images/preprocess/Dockerfile.preprocess \
    --push .