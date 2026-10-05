<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 75 · Git objects · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-75 basic
cd ~/git-practice/lesson-75
git log --oneline
```

## Demonstration

```bash
echo "green tea" >> menu.txt
blob=$(git hash-object -w menu.txt)
echo "blob $blob: $(git cat-file -t "$blob"), $(git cat-file -s "$blob") bytes"
```

```bash
git update-index menu.txt
tree=$(git write-tree)
git cat-file -p "$tree"
git cat-file -p "$tree:menu.txt"
```

```bash
tree=$(git write-tree)
commit=$(echo "Add green tea (by hand)" | git commit-tree "$tree" -p main)
git update-ref refs/heads/main "$commit"
git log --oneline -2
git status --short
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-75
git ls-files --stage menu.txt
git rev-parse HEAD:menu.txt
```

## Break it

```bash
echo "mocha" >> menu.txt && git update-index menu.txt
lost=$(echo "Forgotten commit" | git commit-tree "$(git write-tree)" -p main)
echo "$lost" > ../lesson-75-lost-id.txt
git log --oneline -2
```

## Troubleshoot

```bash
git cat-file -t "$(cat ../lesson-75-lost-id.txt)"
git status --short
```

## Fix

```bash
git update-ref refs/heads/main "$(cat ../lesson-75-lost-id.txt)"
git log --oneline -2
git status --short
```

## Practice challenge

```bash
cd ~/git-practice/lesson-75
git cat-file -p 4267004:prices.txt
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-75 ~/git-practice/lesson-75-lost-id.txt
```
