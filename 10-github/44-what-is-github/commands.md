<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 44 · What is GitHub? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-44 empty
cd ~/git-practice/lesson-44
```

## Demonstration

```bash
git ls-remote https://github.com/octocat/Hello-World
```

```bash
git clone -q https://github.com/octocat/Hello-World
cd Hello-World
git log --oneline -3
git remote -v
```

## Hands-on exercise

```bash
git ls-remote --heads https://github.com/octocat/Hello-World | wc -l
```

## Break it

```bash
cd ~/git-practice/lesson-44
git clone https://github.com/octocat/Hello-Wrld 2>&1
```

## Fix

```bash
rm -rf Hello-World
git clone https://github.com/octocat/Hello-World 2>&1
```

## Practice challenge

```bash
gh repo view octocat/Hello-World --json description,defaultBranchRef --jq '.description, .defaultBranchRef.name'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-44
```
