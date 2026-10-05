<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 58 · Git Flow · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A production bug in 1.1.0: the latte price. A **hotfix** goes into `main`, is released as 1.1.1, but the developer
forgets to merge it into `develop`:

```bash
git switch -q -c hotfix/1.1.1 main
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price"
git switch -q main && git merge -q --no-ff --no-edit hotfix/1.1.1 && git tag -a v1.1.1 -m "Release 1.1.1"
git switch -q develop && grep latte prices.txt
```

## Troubleshoot

`develop` still has `latte 3.20`: the next release (1.2.0, cut from `develop`) would **bring the bug back**. Check what
`main` has that `develop` does not:

```bash
git log --oneline develop..main
```

```text
857e449 (tag: v1.1.1, main) Merge branch 'hotfix/1.1.1'
18f4759 (tag: v1.1.0) Merge branch 'release/1.1.0'
c88da4e (hotfix/1.1.1) Fix the latte price
```

## Fix

```bash
git merge -q --no-ff --no-edit hotfix/1.1.1 && git branch -d -q hotfix/1.1.1
grep latte prices.txt
git log --oneline develop..main | wc -l
```

```text
latte 3.30
1
```
