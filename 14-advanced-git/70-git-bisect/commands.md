<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 70 · Git bisect · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-70 bisect
cd ~/git-practice/lesson-70
git log --oneline
```

## Demonstration

```bash
bash price.sh espresso latte 2>&1 || true
bash check.sh && echo good || echo bad
```

```bash
first=$(git rev-list --max-parents=0 HEAD)
git bisect start
git bisect bad HEAD
git bisect good "$first"
```

```bash
while true; do
  if bash check.sh; then result=$(git bisect good); else result=$(git bisect bad); fi
  echo "$result" | head -1
  case "$result" in *"is the first"*) break ;; esac
done
```

```bash
git bisect reset
git branch --show-current
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-70
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh > /dev/null 2>&1
git log -1 --format='first bad commit: %h %s' refs/bisect/bad
git bisect reset > /dev/null 2>&1
```

## Break it

```bash
git bisect start
git bisect good HEAD
git bisect bad "$(git rev-list --max-parents=0 HEAD)" 2>&1
```

## Fix

```bash
git bisect reset > /dev/null 2>&1
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh 2>&1 | grep "is the first"
git bisect reset > /dev/null 2>&1
```

## Practice challenge

```bash
cd ~/git-practice/lesson-70
git show "$(git log --format=%h --grep='^Add mocha$')" -- prices.txt
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-70
```
