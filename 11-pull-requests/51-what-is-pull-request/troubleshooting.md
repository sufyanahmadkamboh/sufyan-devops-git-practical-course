<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 51 · What is a pull request? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A branch that conflicts with its base, like a PR GitHub marks "This branch has conflicts that must be resolved":

```bash
cd ~/git-practice/lesson-51b
git merge-tree --write-tree --name-only main feature-tea
```

```text
c1ec90e49d06aa38520744c366604c4ec932383a
prices.txt

Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
```

## Troubleshoot

Exit status 1 and `CONFLICT (content): Merge conflict in prices.txt`: both branches changed the same line. GitHub
cannot merge the PR; the author has to update the branch.

## Fix

The PR author brings `main` into the branch and resolves the conflict there (lesson 27), then pushes; the PR updates
itself:

```bash
git switch -q feature-tea
git merge main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q -m "Merge main into feature-tea"
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts: can be merged automatically"
```

```text
no conflicts: can be merged automatically
```
