# Project 2 · Team collaboration

> Level 24 · Projects · intermediate · ⏱ 90 minutes · lessons 37–43, 51–59

## Brief

Three developers (Ada, Grace and Linus) share one repository. `main` is protected: nobody may push to it directly;
every change arrives as a reviewed branch ("pull request"). Simulate a week of work: three features in parallel, one
review that asks for changes, and every branch kept up to date before merging.

## Requirements

1. The server rejects direct pushes to `main` (a `pre-receive` hook, as in lesson 59); merges are done by a "PR bot"
   identity (`PUSHER=pr-bot`).
2. Three feature branches, one per developer, each pushed to the server.
3. One branch receives review feedback and an extra commit before merging.
4. Each branch is updated with the latest `main` before it is merged (no stale merges).
5. All three features end up in `main` through merge commits; merged branches are deleted on the server.

## Starting point

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh project-2 remote
cd ~/git-practice/project-2
git clone -q server/cafe.git linus
git -C linus config user.name "Linus Torvalds" && git -C linus config user.email "linus@example.com"
```

## Hints

- Protection: lesson 59's hook; a "PR merge" is `git merge --no-ff` done in a clone and pushed with `PUSHER=pr-bot`.
- Updating a branch: `git merge origin/main` on the branch (lesson 56), then push the branch again.
- Review: `git log main..origin/BRANCH`, `git diff main...origin/BRANCH` (lesson 51).

## Reference solution

<details>
<summary>Show the reference solution</summary>

Protect `main`:

<!-- test: contains=protected -->
```bash
cd ~/git-practice/project-2
cat > server/cafe.git/hooks/pre-receive << 'EOF'
#!/usr/bin/env bash
while read -r old new ref; do
  if [ "$ref" = refs/heads/main ] && [ "${PUSHER:-}" != pr-bot ]; then
    echo "error: main is protected: open a pull request"; exit 1
  fi
done
EOF
chmod +x server/cafe.git/hooks/pre-receive
echo "main is protected"
```

Three features in parallel:

<!-- test: contains=feature/opening-hours; output -->
```bash
(cd ada && git switch -q -c feature/green-tea && echo "green tea" >> menu.txt && git commit -q -am "feat(menu): add green tea" && git push -q -u origin feature/green-tea)
(cd grace && git switch -q -c feature/latte-price && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "fix(prices): latte costs 3.30" && git push -q -u origin feature/latte-price)
(cd linus && git switch -q -c feature/opening-hours && printf '\nOpen 8:00-18:00.\n' >> README.md && git commit -q -am "docs: add opening hours" && git push -q -u origin feature/opening-hours)
git --git-dir=server/cafe.git branch
```

```text
  feature/green-tea
  feature/latte-price
  feature/opening-hours
* main
```

A "PR merge" helper for the reviewer: update the branch with `main`, check, merge, delete.

<!-- test: contains=merge-pr -->
```bash
cat > merge-pr.sh << 'EOF'
#!/usr/bin/env bash
# merge-pr.sh BRANCH: what the merge button does, run from a reviewer's clone
set -euo pipefail
branch=$1
git fetch -q origin
git switch -q main && git merge -q --ff-only origin/main
git merge -q --no-ff -m "Merge pull request from $branch" "origin/$branch"
PUSHER=pr-bot git push -q origin main
git push -q origin --delete "$branch"
echo "merged $branch"
EOF
echo "merge-pr.sh ready"
```

Review of Grace's PR asks for the reason in the README; she adds a commit, updates her branch with `main`, and all
three are merged:

<!-- test: contains=merged feature/latte-price; output -->
```bash
cd ~/git-practice/project-2/ada && bash ../merge-pr.sh feature/green-tea
cd ../grace && printf '\nPrices updated for 2026.\n' >> README.md && git commit -q -am "docs: explain the price change"
git fetch -q && git merge -q --no-edit origin/main && git push -q
cd ../ada && bash ../merge-pr.sh feature/latte-price
cd ../linus && git fetch -q && git merge -q --no-edit origin/main 2>/dev/null || {
  printf '# Cafe\n\nThe menu and prices of a small cafe.\n\nOpen 8:00-18:00.\n\nPrices updated for 2026.\n' > README.md
  git add README.md && git commit -q --no-edit; }
git push -q
cd ../ada && bash ../merge-pr.sh feature/opening-hours
```

```text
merged feature/green-tea
merged feature/latte-price
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
merged feature/opening-hours
```

</details>

## Self-check

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/project-2/ada && git switch -q main && git pull -q
check() { if eval "$2" > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "direct push to main is rejected" '! (git commit -q --allow-empty -m "direct" && git push -q origin main); git reset -q --hard origin/main'
check "three merge commits on main"     '[ "$(git rev-list --merges --count origin/main)" -ge 3 ]'
check "feature branches deleted"        '[ -z "$(git ls-remote --heads origin "feature/*")" ]'
check "all three changes in main"       'grep -q "green tea" menu.txt && grep -q "latte 3.30" prices.txt && grep -q "Open 8" README.md'
check "the review fix is in main"       'git log --oneline origin/main | grep -q "explain the price change"'
git log --oneline --graph -12
```

```text
ok       direct push to main is rejected
ok       three merge commits on main
ok       feature branches deleted
ok       all three changes in main
ok       the review fix is in main
*   c9d6fdf (HEAD -> main, origin/main, origin/HEAD) Merge pull request from feature/opening-hours
|\  
| *   b86c07e Merge remote-tracking branch 'origin/main' into feature/opening-hours
| |\  
| |/  
|/|   
* |   d4817d9 Merge pull request from feature/latte-price
|\ \  
| * \   016fd40 Merge remote-tracking branch 'origin/main' into feature/latte-price
| |\ \  
| |/ /  
|/| |   
* | |   cbcec88 Merge pull request from feature/green-tea
|\ \ \  
| * | | ab67749 (feature/green-tea) feat(menu): add green tea
|/ / /  
| * | d025290 docs: explain the price change
| * | 376d9d9 fix(prices): latte costs 3.30
|/ /  
| * 04b8198 docs: add opening hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/project-2
```

Next: [Project 3 · Conflict resolution](project-3-conflict-resolution.md)
