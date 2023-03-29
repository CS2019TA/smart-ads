docker buildx build \
    --platform linux/arm64 \
    -t fxdros/fogverse-smart-ads:preprocess \
    -f fog/raspberry/Dockerfile \
    --push .