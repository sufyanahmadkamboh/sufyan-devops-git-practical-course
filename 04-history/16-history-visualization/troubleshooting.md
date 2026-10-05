<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 16 · Commit history visualization · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Draw the graph without `--all` from the side branch and conclude, wrongly, that `main` has nothing new:

```bash
git switch -q feature-tea
git log --oneline --graph
```

```text
* bb67674 (HEAD -> feature-tea) Add green tea to the menu
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Troubleshoot

Without `--all`, `git log` draws only what is reachable from `HEAD`. From `feature-tea`, the opening hours and the
merge on `main` are invisible, although they exist. Same lesson as lesson 13: a view is not the whole repository.

## Fix

```bash
git log --oneline --graph --all
git switch -q main
```
