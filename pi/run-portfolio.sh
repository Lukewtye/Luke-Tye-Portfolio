#!/bin/sh
# Recreate the nginx container that serves luketye.dev.
#
# The container was originally created by a bare `docker run` with no compose
# file and no Portainer stack, so its definition existed only inside the Docker
# daemon and could not be reproduced after a `docker rm`. This script is that
# definition.
#
# The image tag is pinned. `nginx:alpine` resolves at pull time, so it is not
# evidence of currency: the previously running image was built 2026-07-15 and
# had drifted a full mainline release behind by September.
set -eu

IMAGE=nginx:1.31.4-alpine
NAME=portfolio

docker pull "$IMAGE"
docker rm -f "$NAME" 2>/dev/null || true

# Port is bound to loopback only. Public reachability comes from the Cloudflare
# tunnel, which fronts 127.0.0.1:8081; nothing here listens on a LAN address.
# Both mounts are read-only, so a compromised nginx cannot alter the served
# page, the health snapshot, or anything else on the host.
docker run -d \
    --name "$NAME" \
    --restart unless-stopped \
    -p 127.0.0.1:8081:80 \
    -v "$HOME/sites/portfolio.conf:/etc/nginx/conf.d/default.conf:ro" \
    -v "$HOME/sites/luketye.dev:/usr/share/nginx/html:ro" \
    "$IMAGE"

docker exec "$NAME" nginx -v
curl -fsS -o /dev/null -w 'origin check: %{http_code}\n' http://127.0.0.1:8081/
