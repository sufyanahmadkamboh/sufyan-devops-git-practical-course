#!/usr/bin/env bash
# start-capstone.sh: create the broken starting repository of the capstone in ~/git-practice/capstone
#
# It is the cafe DevOps repository from module 21, as a careless team left it: meaningless commit messages, a committed
# .env with a password (fake), a large video in history, no .gitignore, a version mismatch that fails CI, a conflicting
# feature branch, a badly named lightweight tag, and no CI workflows. Run from the course folder:
#
#   bash 24-capstone/start-capstone.sh
set -euo pipefail
course=$(cd "$(dirname "$0")/.." && pwd)
lab="$HOME/git-practice/capstone"
rm -rf "$lab" && mkdir -p "$lab" && cd "$lab"
git init -q -b main

n=0
commit() {  # commit "message": fixed dates, so every learner starts from the same commit IDs
  n=$((n + 1))
  local date; date=$(printf '2026-02-02T10:%02d:00+00:00' "$n")
  GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL="ada@example.com" GIT_COMMITTER_NAME="Ada Lovelace" \
    GIT_COMMITTER_EMAIL="ada@example.com" GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -q -m "$1"
}
if ! git config --global user.name > /dev/null 2>&1; then
  git config user.name "Ada Lovelace" && git config user.email "ada@example.com"
fi

template="$course/21-devops-workflow/devops-project"
cp -r "$template/application" "$template/helm" "$template/kubernetes" "$template/scripts" "$template/docs" \
  "$template/Dockerfile" "$template/VERSION" .
git add . && commit "first commit"

printf '<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <title>Cafe menu</title>\n</head>\n<body>\n  <h1>Our cafe</h1>\n  <p>The menu is served from <code>menu.json</code>.</p>\n</body>\n</html>\n' > application/index.html
printf 'DB_HOST=db.internal\nDB_PASSWORD=Cafe-2026-not-a-real-password\n' > .env
git add . && commit "wip"

mkdir -p assets && head -c 3000000 /dev/zero | tr '\0' 'v' > assets/promo-video.mp4
git add . && commit "asdf"

cp "$template/README.md" README.md
git add . && commit "fix"

git rm -q .env && commit "fix again"
git tag release1

git switch -q -c feature/chai
sed -i 's/{"name": "cappuccino", "price": "3.40"}/{"name": "cappuccino", "price": "3.40"},\n    {"name": "chai", "price": "3.10"}/' application/menu.json
sed -i 's/"latte", "price": "3.20"/"latte", "price": "3.50"/' application/menu.json
git add application/menu.json && commit "chai + latte"
git switch -q main

sed -i 's/tag: "1.0.0"/tag: "1.0.1"/' helm/cafe/values.yaml
sed -i 's/"latte", "price": "3.20"/"latte", "price": "3.30"/' application/menu.json
git add . && commit "changes"

echo "capstone ready: ~/git-practice/capstone"
git log --oneline --graph --all
