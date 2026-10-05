#!/usr/bin/env bash
# Create a fresh practice repository for a lesson, with a known starting history.
#
#   bash scripts/new-lab.sh NAME SCENARIO
#
# The lab is created in ~/git-practice/NAME (an existing one is replaced). The prepared commits use fixed authors and
# dates, so their commit IDs are the same on every computer: your `git log` shows the same hashes as the lesson.
# The commits YOU make in a lesson get your own name and the current time, so their IDs differ.
#
# Scenarios
#   empty        an initialised repository, no commits
#   basic        3 commits on main: README.md, menu.txt, prices.txt
#   feature      basic + branch "feature-tea" with 1 commit (main unchanged): a fast-forward merge
#   diverged     main and feature-tea each have 1 new commit, different files: a three-way merge
#   conflict     main and feature-tea change the same line of prices.txt: a merge conflict
#   history      basic + 4 more commits on main (for reset, revert, reflog, rebase -i)
#   remote       server/cafe.git (a bare "GitHub"), ada/ and grace/ clones of it
#   bisect       10 commits; one of them breaks the price calculator (check.sh tells good from bad)
#   github       a clone of YOUR practice repository on GitHub (lesson 45: git-practice-cafe; needs gh, logged in)
set -euo pipefail

name="${1:?usage: new-lab.sh NAME SCENARIO}"
scenario="${2:?usage: new-lab.sh NAME SCENARIO}"
lab="$HOME/git-practice/$name"
rm -rf "$lab"
mkdir -p "$lab"
cd "$lab"

# --- helpers ---------------------------------------------------------------------------------------------------
n=0
# commit "message" [author]  (author: ada | grace), with a fixed date one minute after the previous commit
commit() {
  n=$((n + 1))
  local who="${2:-ada}" date
  date=$(printf '2026-01-05T09:%02d:00+00:00' "$n")
  case "$who" in
    ada)   set -- "$1" "Ada Lovelace" "ada@example.com" ;;
    grace) set -- "$1" "Grace Hopper" "grace@example.com" ;;
  esac
  GIT_AUTHOR_NAME="$2" GIT_AUTHOR_EMAIL="$3" GIT_COMMITTER_NAME="$2" GIT_COMMITTER_EMAIL="$3" \
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -q -m "$1"
}

init_repo() {
  git init -q -b main "${1:-.}"
  # an identity for the commits you make in this lab, unless you configured one globally (lesson 04)
  if ! git config --global user.name > /dev/null 2>&1; then
    git -C "${1:-.}" config user.name "Ada Lovelace"
    git -C "${1:-.}" config user.email "ada@example.com"
  fi
}

basic() {
  printf '# Cafe\n\nThe menu and prices of a small cafe.\n' > README.md
  git add README.md && commit "Add README"
  printf 'espresso\nlatte\ncappuccino\n' > menu.txt
  git add menu.txt && commit "Add the menu"
  printf 'espresso 2.50\nlatte 3.20\ncappuccino 3.40\n' > prices.txt
  git add prices.txt && commit "Add prices"
}

# --- scenarios ------------------------------------------------------------------------------------------------
case "$scenario" in
  empty)
    init_repo
    ;;
  basic)
    init_repo && basic
    ;;
  feature)
    init_repo && basic
    git switch -q -c feature-tea
    printf 'green tea\n' >> menu.txt
    git add menu.txt && commit "Add green tea to the menu"
    git switch -q main
    ;;
  diverged)
    init_repo && basic
    git switch -q -c feature-tea
    printf 'green tea\n' >> menu.txt
    git add menu.txt && commit "Add green tea to the menu"
    git switch -q main
    printf '\nOpen every day from 8:00 to 18:00.\n' >> README.md
    git add README.md && commit "Add opening hours"
    ;;
  conflict)
    init_repo && basic
    git switch -q -c feature-tea
    sed -i.bak 's/^latte 3.20$/latte 3.50/' prices.txt && rm -f prices.txt.bak
    git add prices.txt && commit "Raise the latte price to 3.50"
    git switch -q main
    sed -i.bak 's/^latte 3.20$/latte 3.30/' prices.txt && rm -f prices.txt.bak
    git add prices.txt && commit "Raise the latte price to 3.30" grace
    ;;
  history)
    init_repo && basic
    printf 'green tea\n' >> menu.txt;              git add -A && commit "Add green tea"
    printf 'green tea 2.80\n' >> prices.txt;       git add -A && commit "Price green tea"
    printf 'mocha\n' >> menu.txt;                  git add -A && commit "Add mocha"
    printf 'mocha 3.90\n' >> prices.txt;           git add -A && commit "Price mocha"
    ;;
  remote)
    git init -q --bare -b main server/cafe.git
    init_repo seed && (cd seed && basic && git remote add origin ../server/cafe.git && git push -q origin main)
    rm -rf seed
    git clone -q server/cafe.git ada
    git clone -q server/cafe.git grace
    git -C ada config user.name "Ada Lovelace";   git -C ada config user.email "ada@example.com"
    git -C grace config user.name "Grace Hopper"; git -C grace config user.email "grace@example.com"
    ;;
  bisect)
    init_repo
    cat > price.sh <<'EOF'
#!/usr/bin/env bash
# price.sh ITEM... : the total price of an order, from prices.txt
total=0
for item in "$@"; do
  p=$(grep "^$item " prices.txt | awk '{print $2 * 100}')
  total=$((total + p))
done
printf '%d.%02d\n' $((total / 100)) $((total % 100))
EOF
    cat > check.sh <<'EOF'
#!/usr/bin/env bash
# check.sh: exit 0 if an espresso and a latte cost 5.70 (the correct total), 1 otherwise
[ "$(bash price.sh espresso latte 2>/dev/null)" = "5.70" ]
EOF
    printf 'espresso 2.50\nlatte 3.20\n' > prices.txt
    git add -A && commit "Add the price calculator and its check"
    for item in cappuccino mocha "green-tea" chai flat-white americano macchiato cortado; do
      case $item in
        mocha) # the bug: mocha's line sneaks in a second latte price, and grep then matches two lines
               printf 'mocha 3.90\nlatte 3.60\n' >> prices.txt ;;
        *) printf '%s 3.%d0\n' "$item" $(( ${#item} % 10 )) >> prices.txt ;;
      esac
      git add -A && commit "Add $item"
    done
    printf '\nPrices include tax.\n' > NOTES.md
    git add -A && commit "Add notes"
    ;;
  github)
    cd "$HOME/git-practice" && rm -rf "$lab"
    me=$(gh api user --jq .login)
    gh repo clone "$me/git-practice-cafe" "$lab" -- -q
    cd "$lab"
    if ! git config --global user.name > /dev/null 2>&1; then
      git config user.name "Ada Lovelace" && git config user.email "ada@example.com"
    fi
    ;;
  *)
    echo "unknown scenario: $scenario" >&2
    exit 1
    ;;
esac

echo "lab ready: ~/git-practice/$name ($scenario)"
