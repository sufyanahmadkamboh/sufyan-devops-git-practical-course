<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 51 · What is a pull request? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-51b conflict
bash scripts/new-lab.sh lesson-51 diverged
cd ~/git-practice/lesson-51
git log --oneline --graph --all
```

## Demonstration

```bash
git log --oneline main..feature-tea
```

```bash
git diff main...feature-tea
```

```bash
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts: can be merged automatically"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-51
git diff --name-only main...feature-tea
```

## Break it

```bash
cd ~/git-practice/lesson-51b
git merge-tree --write-tree --name-only main feature-tea
```

## Fix

```bash
git switch -q feature-tea
git merge main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q -m "Merge main into feature-tea"
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts: can be merged automatically"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-51
git rev-list --left-right --count main...feature-tea | awk '{print "behind", $1, "ahead", $2}'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-51 ~/git-practice/lesson-51b
```
