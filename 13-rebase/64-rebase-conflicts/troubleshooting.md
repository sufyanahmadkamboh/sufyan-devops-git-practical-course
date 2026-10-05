<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 64 · Rebase conflicts · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Recreate the conflict (`ORIG_HEAD` is the branch before the rebase), edit the file, and continue **without** `git add`:

```bash
git reset -q --hard ORIG_HEAD
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git rebase --continue 2>&1
```

```text
prices.txt: needs merge
You must edit all merge conflicts and then
mark them as resolved using git add
```

## Troubleshoot

Git does not look at the file content to decide whether you are done; it looks at the index. Until `git add` marks
the file resolved, it is still "unmerged":

```bash
git status --short
git status | grep "both modified"
```

```text
UU prices.txt
	both modified:   prices.txt
```

## Fix

```bash
git add prices.txt
git rebase --continue
```

```text
[detached HEAD cff42b7] Raise the latte price to 3.50
 1 file changed, 1 insertion(+), 1 deletion(-)
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
```
