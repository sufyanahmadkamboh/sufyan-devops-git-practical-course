<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 90 · Removing sensitive data · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
git filter-repo --version > /dev/null && echo "git-filter-repo available"
bash scripts/new-lab.sh lesson-90 remote
cd ~/git-practice/lesson-90/ada
printf 'DB_PASSWORD=Cafe-2026-not-a-real-password\n' > .env && git add .env && git commit -q -m "Add configuration"
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git rm -q .env && git commit -q -m "Remove .env"
git push -q
(cd ../grace && git pull -q)
git log --oneline
```

## Demonstration

```bash
cd ~/git-practice/lesson-90
git clone -q --mirror server/cafe.git cleanup.git
cd cleanup.git
git log --oneline --all -- .env
```

```bash
git filter-repo --invert-paths --path .env 2>&1 | grep -v "^Parsed\|^HEAD is now" | tail -3
git log --oneline --all -- .env | wc -l
git log --oneline
```

```bash
git push --force --mirror ../server/cafe.git 2>&1 | grep -E "forced|up to date" | head -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-90
git --git-dir=server/cafe.git log --all --oneline -- .env | wc -l
```

## Break it

```bash
cd ~/git-practice/lesson-90/grace
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git pull -q --no-rebase --no-edit 2>&1 | tail -1
git push -q 2>&1 | tail -1
git --git-dir=../server/cafe.git log --oneline --all -- .env
```

## Fix

```bash
cd ~/git-practice/lesson-90
rm -rf cleanup.git && git clone -q --mirror server/cafe.git cleanup.git
(cd cleanup.git && git filter-repo --invert-paths --path .env > /dev/null 2>&1 && git push -q --force --mirror ../server/cafe.git 2> /dev/null)
rm -rf grace && git clone -q server/cafe.git grace
git --git-dir=server/cafe.git log --oneline --all -- .env | wc -l
git -C grace log --oneline -3
```

## Practice challenge

```bash
cd ~/git-practice/lesson-90
git init -q text-demo && cd text-demo
printf 'host=db\npassword=Cafe-2026-not-a-real-password\n' > app.conf && git add app.conf && git commit -q -m "Add app.conf"
echo 'Cafe-2026-not-a-real-password==>***REMOVED***' > ../replacements.txt
git filter-repo --force --replace-text ../replacements.txt > /dev/null 2>&1
git show HEAD:app.conf
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-90
```
