<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 68 · Git tags · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-68 remote
cd ~/git-practice/lesson-68/ada
git log --oneline
```

## Demonstration

```bash
git tag v1.0.0
git tag v0.9.0 fc345e6
git tag
git log --oneline --decorate
```

```bash
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git log --oneline --decorate -2
```

```bash
git switch -q --detach v1.0.0
cat menu.txt
git switch -q main
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-68/ada
git tag -l "v1.*"
git log --oneline -1 v0.9.0
```

## Break it

```bash
git push -q
git ls-remote --tags origin | grep . || echo "no tags on the server"
```

## Fix

```bash
git push origin v1.0.0 2>&1
git ls-remote --tags origin
```

## Practice challenge

```bash
cd ~/git-practice/lesson-68/ada
git tag v1.0.1 d6df412
git tag -d v1.0.1
git tag
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-68
```
