<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 21 · Branch visualization · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Commit on the wrong branch: you meant to add the chai recipe to `feature`, but you are on `main`.

```bash
echo "chai: black tea, spices, milk" > chai.txt && git add chai.txt && git commit -q -m "Add chai"
git log --oneline --graph --all | head -4
```

## Troubleshoot

The graph shows `Add chai` under the `HEAD -> main` label: the label that moved is the one `HEAD` was on. Committing
always moves the current branch.

## Fix

Move the commit: put it on `feature` (cherry-pick, lesson 67), then take it off `main` (reset, lesson 31; safe here
because `main` was never pushed):

```bash
git switch -q feature
git cherry-pick main > /dev/null
git switch -q main
git reset -q --hard HEAD~1
git log --oneline --graph --all
```

```text
* 63edaa0 (feature) Add chai
* 85afb8e Add green tea
| * 21c291f (HEAD -> main) Add hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```
