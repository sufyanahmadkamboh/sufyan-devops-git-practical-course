<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 57 · GitHub Flow · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Skip the flow: a "quick fix" pushed straight to `main`, without review or checks, breaks the prices file.

```bash
cd ~/git-practice/lesson-57/ada && git pull -q
sed -i 's/^espresso 2.50/espresso two-fifty/' prices.txt && git commit -q -am "Quick fix" && git push -q
cd .. && bash deploy.sh
```

```text
```

## Troubleshoot

Production's smoke test failed (`deploy.sh` stopped with exit status 1 and printed no `deployed` line): `main` is no
longer deployable, and every later merge is blocked behind it. Find the culprit:

```bash
git -C server/cafe.git log --oneline -3
git -C ada show --format=%s HEAD -- prices.txt | grep -E "^[-+]espresso|Quick"
```

```text
b407c2d (HEAD -> main) Quick fix
e2958c4 Merge branch 'add-mocha'
e9ae25b Add mocha
Quick fix
-espresso 2.50
+espresso two-fifty
```

## Fix

The fastest safe fix on a shared `main`: revert it, **through the same flow** (branch, check, merge), and deploy:

```bash
cd ada
git switch -q -c revert-quick-fix && git revert --no-edit HEAD > /dev/null
grep -q "^espresso [0-9]" prices.txt && echo "check passed"
git switch -q main && git merge -q --no-ff --no-edit revert-quick-fix && git push -q
cd .. && bash deploy.sh
```

```text
check passed
deployed 333283f (HEAD -> main, origin/main, origin/HEAD) Merge branch 'revert-quick-fix'
```
