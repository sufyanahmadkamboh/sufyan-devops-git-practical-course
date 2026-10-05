#!/usr/bin/env bash
# ci.sh: the checks every pull request must pass (run by .github/workflows/ci.yml, and locally before pushing)
set -uo pipefail
cd "$(dirname "$0")/.."
failed=0
check() { if eval "$2"; then echo "ok    $1"; else echo "FAIL  $1"; failed=1; fi; }

version=$(tr -d '[:space:]' < VERSION)
chart_version=$(sed -n 's/^appVersion: *"\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' helm/cafe/Chart.yaml)
image_tag=$(sed -n 's/^ *tag: *"\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' helm/cafe/values.yaml)

check "menu.json is valid JSON" "python3 -m json.tool application/menu.json > /dev/null 2>&1 || python -m json.tool application/menu.json > /dev/null 2>&1"
check "every menu item has a price with two decimals" "! grep -E '\"price\"' application/menu.json | grep -vqE '\"price\": \"[0-9]+\.[0-9]{2}\"'"
check "VERSION is semantic (MAJOR.MINOR.PATCH)" "echo '$version' | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'"
check "Chart appVersion matches VERSION ($version)" "[ '$chart_version' = '$version' ]"
check "image tag matches VERSION ($version)" "[ '$image_tag' = '$version' ]"
check "no secrets in tracked files" "! git grep -nIE '(PASSWORD|SECRET|TOKEN)[A-Z_]*=[^ ]+|-----BEGIN [A-Z ]*PRIVATE KEY' -- ':!scripts/ci.sh' > /dev/null"

[ $failed -eq 0 ] && echo "all checks passed" || { echo "checks failed"; exit 1; }
