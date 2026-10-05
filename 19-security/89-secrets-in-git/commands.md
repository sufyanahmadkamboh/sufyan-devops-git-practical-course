<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 89 · Secrets in Git · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-89 remote
cd ~/git-practice/lesson-89/ada
```

## Demonstration

```bash
printf 'DB_HOST=db.internal\nDB_PASSWORD=Cafe-2026-not-a-real-password\nAPI_TOKEN=cafe_token_0123456789abcdef\n' > .env
git add .env && git commit -q -m "Add app configuration"
git push 2>&1 | tail -1
```

```bash
git rm -q .env && git commit -q -m "Remove secrets" && git push 2>&1 | tail -1
ls -a | grep -c "^.env$" || true
```

```bash
cd .. && git clone -q server/cafe.git eve && cd eve
git log --oneline -- .env
git show HEAD~1:.env
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-89/eve
git grep -n "PASSWORD=" $(git rev-list --all) | head -3
```

## Break it

```bash
git log --all --format=%h -- .env | while read -r c; do git show "$c:.env" 2> /dev/null | grep -q PASSWORD && echo "$c: password still readable"; done
```

## Fix

```bash
cd ~/git-practice/lesson-89/ada
printf 'DB_HOST=db.internal\nDB_PASSWORD=\nAPI_TOKEN=\n' > .env.example
echo ".env" >> .gitignore
git add .env.example .gitignore && git commit -q -m "Add .env.example; ignore .env"
git ls-files
```

## Practice challenge

```bash
cd ~/git-practice/lesson-89/eve
git log --oneline -S "cafe_token_" --all
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-89
```
