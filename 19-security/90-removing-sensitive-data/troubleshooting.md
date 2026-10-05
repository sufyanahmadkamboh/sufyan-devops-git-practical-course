<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 90 · Removing sensitive data · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace still has the old history. She makes a commit and does a normal `git pull` + `git push`:

```bash
cd ~/git-practice/lesson-90/grace
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git pull -q --no-rebase --no-edit 2>&1 | tail -1
git push -q 2>&1 | tail -1
git --git-dir=../server/cafe.git log --oneline --all -- .env
```

```text
d80d653 Remove .env
61e2249 Add configuration
```

## Troubleshoot

The old commits, `.env` included, are back on the server: Grace's merge connected her old history (which still
contains "Add configuration") to the rewritten one, and her push uploaded it. A rewrite only works if **every** copy
switches to the new history.

## Fix

Rewrite the server again, then Grace replaces her clone instead of merging (keeping her new work as a patch):

```bash
cd ~/git-practice/lesson-90
rm -rf cleanup.git && git clone -q --mirror server/cafe.git cleanup.git
(cd cleanup.git && git filter-repo --invert-paths --path .env > /dev/null 2>&1 && git push -q --force --mirror ../server/cafe.git 2> /dev/null)
rm -rf grace && git clone -q server/cafe.git grace
git --git-dir=server/cafe.git log --oneline --all -- .env | wc -l
git -C grace log --oneline -3
```

```text
0
81f4587 (HEAD -> main, origin/main, origin/HEAD) Merge branch 'main' of ~/git-practice/lesson-90/server/cafe
4776ba7 Price chai
e1eacde Add green tea
```

In a team: announce the rewrite, freeze pushes, rewrite, then everyone deletes their clone and clones again.
