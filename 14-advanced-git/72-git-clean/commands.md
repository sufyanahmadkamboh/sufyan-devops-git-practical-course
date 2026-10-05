<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 72 · Git clean · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-72 basic
cd ~/git-practice/lesson-72
echo ".env" > .gitignore && git add .gitignore && git commit -q -m "Ignore .env"
echo "draft" > notes-draft.txt
mkdir build && echo "binary" > build/app
echo "DB_PASSWORD=local-only" > .env
git status --short --ignored
```

## Demonstration

```bash
git clean 2>&1
```

```bash
git clean -n -d
```

```bash
git clean -f -d
git status --short --ignored
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-72
ls
```

## Break it

```bash
git clean -f -d -x
```

## Troubleshoot

```bash
cat .env 2>&1 | sed 's/.*No such file.*/no such file/'
git log --all --oneline -- .env | wc -l
```

## Fix

```bash
printf 'DB_PASSWORD=change-me\n' > .env.example && git add .env.example && git commit -q -m "Add .env.example"
cp .env.example .env
git clean -n -d -x
```

## Practice challenge

```bash
cd ~/git-practice/lesson-72
echo "my work" > work.txt
git clean -f -X
ls
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-72
```
