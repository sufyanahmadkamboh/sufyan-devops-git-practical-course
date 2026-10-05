#!/usr/bin/env bash
# release.sh VERSION: set the version everywhere it appears, commit, and create an annotated tag
set -euo pipefail
cd "$(dirname "$0")/.."
version="${1:?usage: scripts/release.sh MAJOR.MINOR.PATCH}"
echo "$version" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' || { echo "not a semantic version: $version" >&2; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "the working tree is not clean" >&2; exit 1; }

echo "$version" > VERSION
sed -i.bak "s/^appVersion: .*/appVersion: \"$version\"/; s/^version: .*/version: $version/" helm/cafe/Chart.yaml
sed -i.bak "s/^\( *tag:\) .*/\1 \"$version\"/" helm/cafe/values.yaml
rm -f helm/cafe/Chart.yaml.bak helm/cafe/values.yaml.bak

bash scripts/ci.sh > /dev/null
git commit -q -am "chore(release): $version"
git tag -a "v$version" -m "Release $version"
echo "released v$version: push with  git push --follow-tags"
