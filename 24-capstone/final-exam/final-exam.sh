#!/usr/bin/env bash
# final-exam.sh: create the broken repository of the final exam in ~/git-practice/exam
# (and its server in ~/git-practice/exam-server.git). Run from the course folder:
#
#   bash 24-capstone/final-exam/final-exam.sh
set -euo pipefail
base="$HOME/git-practice"
rm -rf "$base/exam" "$base/exam-server.git" "$base/wrong-server.git"
mkdir -p "$base/exam" && cd "$base/exam"
git init -q -b main

n=0
commit() {  # fixed dates: every candidate gets the same commit IDs
  n=$((n + 1))
  local date; date=$(printf '2026-03-01T09:%02d:00+00:00' "$n")
  GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL="ada@example.com" GIT_COMMITTER_NAME="Ada Lovelace" \
    GIT_COMMITTER_EMAIL="ada@example.com" GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -q "$@"
}
if ! git config --global user.name > /dev/null 2>&1; then
  git config user.name "Ada Lovelace" && git config user.email "ada@example.com"
fi

printf '# Cafe\n\nThe menu and prices of a small cafe.\n' > README.md && git add . && commit -m "Add README"
printf 'espresso\nlatte\ncappuccino\n' > menu.txt && git add . && commit -m "Add the menu"
printf 'espresso 2.50\nlatte 3.20\ncappuccino 3.40\n' > prices.txt && git add . && commit -m "Add prices"
prices=$(git rev-parse HEAD)

# a lightweight tag with a poor name on the wrong commit
git tag v1.0 HEAD~1

# the shared history: one experimental commit already pushed
echo "truffle latte 12.00" >> prices.txt && git add . && commit -m "Add experimental pricing"
git init -q --bare "$base/exam-server.git"
git push -q "$base/exam-server.git" main
git remote add origin "$base/exam-server.git" && git fetch -q origin
git branch -q -u origin/main main

# feature branch (from "Add prices"): conflicts with a local latte change
git switch -q -c feature-tea "$prices"
sed -i 's/latte 3.20/latte 3.50/' prices.txt && commit -am "Raise the latte price to 3.50"
echo "green tea" >> menu.txt && commit -am "Add green tea"

# a branch that will be deleted by mistake
git switch -q -c seasonal "$prices"
echo "pumpkin latte" >> menu.txt && commit -am "Add pumpkin latte"

# a commit made in detached HEAD and left behind
git switch -q --detach "$prices"
echo "Winter: hot chocolate" > winter.txt && git add . && commit -m "Add the winter menu"

# hotfix branch created from origin/main: it tracks origin/main (wrong upstream)
git switch -q -c hotfix origin/main
sed -i 's/cappuccino 3.40/cappuccino 3.50/' prices.txt && commit -am "Fix the cappuccino price"

# local, unpushed work on main: a typo in a message, a latte change, a log file committed by mistake
git switch -q main
echo "Today: espresso, latte, cappuccino" > board.txt && git add . && commit -m "Add the meun board"
sed -i 's/latte 3.20/latte 3.30/' prices.txt && commit -am "Raise the latte price to 3.30"
echo "Today: espresso, latte, cappuccino, truffle latte" > board.txt
head -c 200000 /dev/zero | tr '\0' 'x' > debug.log
git add . && commit -m "Add debug log"

# unfinished work in a stash
echo "Espresso: single or double shot." >> README.md && git stash push -q -m "WIP: espresso note"

# and the mistakes of the afternoon
git branch -q -D seasonal
git remote set-url origin "$base/wrong-server.git"

echo "exam ready: ~/git-practice/exam (server: ~/git-practice/exam-server.git)"
