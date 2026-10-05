#!/usr/bin/env bash
# deploy.sh SERVER_REPO TAG ENVIRONMENT_DIR: deploy a released version
#
# In real life this runs in CI after a release: build and push the image (docker build, docker push ghcr.io/...),
# then "helm upgrade --install cafe helm/cafe --set image.tag=$VERSION". Here the "cluster" is a folder, so the whole
# flow can be practised without Docker or Kubernetes: the release tag is checked out into ENVIRONMENT_DIR.
set -euo pipefail
server="${1:?usage: deploy.sh SERVER_REPO TAG ENVIRONMENT_DIR}"
tag="${2:?tag}"
env_dir="${3:?environment folder}"

git ls-remote --exit-code --tags "$server" "refs/tags/$tag" > /dev/null || { echo "tag $tag is not on the server" >&2; exit 1; }
rm -rf "$env_dir.new"
git clone -q --depth 1 --branch "$tag" "$server" "$env_dir.new" 2> /dev/null
bash "$env_dir.new/scripts/ci.sh" > /dev/null || { echo "release $tag fails its checks: not deployed" >&2; rm -rf "$env_dir.new"; exit 1; }
rm -rf "$env_dir" && mv "$env_dir.new" "$env_dir"
echo "deployed cafe $(cat "$env_dir/VERSION") ($tag) to $(basename "$env_dir")"
