<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 57 · GitHub Flow · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-57 remote
cd ~/git-practice/lesson-57
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh: put the server's main into production/, and run the smoke test
set -e
rm -rf production && git clone -q server/cafe.git production
grep -q "^espresso [0-9]" production/prices.txt && echo "deployed $(git -C production log --oneline -1)"
EOF
bash deploy.sh
```

## Demonstration

```bash
cd ada
git switch -q -c add-chai
echo "chai" >> menu.txt && echo "chai 3.10" >> prices.txt && git commit -q -am "Add chai"
git push -q -u origin add-chai
git diff --stat main...add-chai
```

```bash
grep -q "^espresso [0-9]" prices.txt && echo "check passed"
git switch -q main && git merge -q --no-ff --no-edit add-chai && git push -q
git push -q origin --delete add-chai && git branch -d add-chai
cd .. && bash deploy.sh
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-57
bash deploy.sh
```

## Break it

```bash
cd ~/git-practice/lesson-57/ada && git pull -q
sed -i 's/^espresso 2.50/espresso two-fifty/' prices.txt && git commit -q -am "Quick fix" && git push -q
cd .. && bash deploy.sh
```

## Troubleshoot

```bash
git -C server/cafe.git log --oneline -3
git -C ada show --format=%s HEAD -- prices.txt | grep -E "^[-+]espresso|Quick"
```

## Fix

```bash
cd ada
git switch -q -c revert-quick-fix && git revert --no-edit HEAD > /dev/null
grep -q "^espresso [0-9]" prices.txt && echo "check passed"
git switch -q main && git merge -q --no-ff --no-edit revert-quick-fix && git push -q
cd .. && bash deploy.sh
```

## Practice challenge

```bash
cd ~/git-practice/lesson-57
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh: test the server's main in a staging folder, and only then replace production/
set -e
rm -rf staging && git clone -q server/cafe.git staging
if grep -q "^espresso [0-9]" staging/prices.txt; then
  rm -rf production && mv staging production && echo "deployed $(git -C production log --oneline -1)"
else
  echo "smoke test failed: kept $(git -C production log --oneline -1)"; exit 1
fi
EOF
(cd ada && sed -i 's/^espresso 2.50/espresso broken/' prices.txt && git commit -q -am "Another quick fix" && git push -q)
bash deploy.sh || true
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-57
```
