<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 62 · Rebase vs merge · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Ada pushes `feature-tea`; Grace builds on it; Ada then rebases and force-pushes. Grace pulls with a merge:

```bash
git init -q --bare ../lesson-62-server.git && git remote add origin ../lesson-62-server.git
git push -q origin main feature-tea
git clone -q -b feature-tea ../lesson-62-server.git ../lesson-62-grace
(cd ../lesson-62-grace && git config user.name "Grace Hopper" && git config user.email grace@example.com &&
  echo "green tea is popular" > notes.txt && git add notes.txt && git commit -q -m "Add notes")
git switch -q feature-tea && git rebase -q main && git push -q --force-with-lease origin feature-tea
cd ../lesson-62-grace && git pull -q --no-rebase --no-edit
git log --oneline --graph | head -12
```

```text
*   f448256 (HEAD -> feature-tea) Merge branch 'feature-tea' of ~/git-practice/lesson-62/../lesson-62-server into feature-tea
|\  
| * 507d4af (origin/feature-tea) Price green tea
| * 0dda4da Add green tea to the menu
| * f40d080 (origin/main, origin/HEAD) Add opening hours
* | b2ed916 Add notes
* | b4e37a0 Price green tea
* | bb67674 Add green tea to the menu
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Troubleshoot

"Add green tea to the menu" and "Price green tea" now appear **twice** in Grace's history: the originals (which
Grace's commit is built on) and the rebased copies (from Ada's force push), joined by a merge. Merged into `main`, the
history would carry both.

```bash
git log --oneline | grep -c "Price green tea"
```

```text
2
```

## Fix

Grace undoes her merge and **rebases** her own commit onto the new branch instead. Git recognises that the old copies
are already upstream (same patches) and skips them:

```bash
git reset -q --hard ORIG_HEAD
git rebase origin/feature-tea 2>&1 | grep -v "^hint:" || true
git log --oneline | grep -c "Price green tea"
git log --oneline --graph | head -5
```

```text
warning: skipped previously applied commit bb67674
warning: skipped previously applied commit b4e37a0
Rebasing (1/1)
Successfully rebased and updated refs/heads/feature-tea.
1
* 3b7ba33 (HEAD -> feature-tea) Add notes
* 507d4af (origin/feature-tea) Price green tea
* 0dda4da Add green tea to the menu
* f40d080 (origin/main, origin/HEAD) Add opening hours
* 4267004 Add prices
```

Prevention: do not rebase branches others have pulled; if you must, tell them and have them use `git pull --rebase`.
