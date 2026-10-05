<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 25 · Three-way merge · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-25 diverged
cd ~/git-practice/lesson-25
git log --oneline --graph --all
```

## Demonstration

```bash
base=$(git merge-base main feature-tea)
git log --oneline -1 "$base"
echo "--- base -> main changed:";        git diff --name-only "$base" main
echo "--- base -> feature-tea changed:"; git diff --name-only "$base" feature-tea
```

```bash
git merge --no-edit feature-tea
git show --stat --format='%s%nparents: %p' HEAD
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-25
cat menu.txt
```

## Break it

```bash
git switch -q --orphan unrelated && echo "other project" > other.txt && git add other.txt && git commit -q -m "Other project"
git switch -q main
git merge unrelated 2>&1
```

## Troubleshoot

```bash
git merge-base main unrelated || echo "no merge base"
```

## Fix

```bash
git merge --allow-unrelated-histories --no-edit unrelated
ls
```

## Practice challenge

```bash
cd ~/git-practice/lesson-25
git diff --stat HEAD^1 HEAD
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-25
```
