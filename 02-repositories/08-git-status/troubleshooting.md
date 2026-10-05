<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 08 · git status · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Read `git status` wrongly and lose work: you think `prices.txt` is staged, commit, and push, but the latte price change
was not in the commit.

```bash
git commit -q -m "Add chai"
git status --short
```

## Troubleshoot

After the commit, `git status` still lists ` M prices.txt` (and the extra `matcha` line in `menu.txt`): those changes
were **not staged**, so they were not committed. The commit contains only what was in *Changes to be committed*:

```bash
git show --stat --format='%s' HEAD
git show HEAD | grep '^[+-][^+-]'
```

```text
Add chai

 menu.txt | 1 +
 1 file changed, 1 insertion(+)
+chai
```

## Fix

Stage the missing change and commit it (or, if the commit is not pushed yet, add it to the last commit with
`git commit --amend`, lesson 11):

```bash
git add prices.txt menu.txt && git commit -q -m "Raise the latte price, add matcha"
rm hours.txt
git status
```
