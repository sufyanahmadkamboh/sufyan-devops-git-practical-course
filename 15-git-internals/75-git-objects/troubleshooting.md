<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 75 · Git objects · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Create a commit object but forget to move the branch:

```bash
echo "mocha" >> menu.txt && git update-index menu.txt
lost=$(echo "Forgotten commit" | git commit-tree "$(git write-tree)" -p main)
echo "$lost" > ../lesson-75-lost-id.txt
git log --oneline -2
```

```text
5072f74 (HEAD -> main) Add green tea (by hand)
4267004 Add prices
```

## Troubleshoot

The commit exists in the object store, but no reference points to it, so `git log` (which starts from `HEAD`) does not
show it. `git status` shows the staged change as still uncommitted, because `HEAD` did not move:

```bash
git cat-file -t "$(cat ../lesson-75-lost-id.txt)"
git status --short
```

```text
commit
M  menu.txt
```

## Fix

Move the branch to the commit (what `git commit` would have done as its last step):

```bash
git update-ref refs/heads/main "$(cat ../lesson-75-lost-id.txt)"
git log --oneline -2
git status --short
```

```text
32645d5 (HEAD -> main) Forgotten commit
5072f74 Add green tea (by hand)
```
