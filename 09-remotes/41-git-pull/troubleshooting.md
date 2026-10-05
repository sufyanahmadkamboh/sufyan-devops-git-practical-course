<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 41 · git pull · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Both sides commit: Ada locally, Grace on the server.

```bash
cd ~/git-practice/lesson-41/grace && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" && git push -q
cd ../ada && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git pull 2>&1
```

```text
From ~/git-practice/lesson-41/server/cafe
   520c5c5..4baa03b  main       -> origin/main
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

## Troubleshoot

`fatal: Need to specify how to reconcile divergent branches.`: Git fetched Grace's commit (look: `origin/main` moved)
but refuses to choose between a merge and a rebase for you, because they produce different histories.

```bash
git status | head -3
```

```text
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
```

## Fix

Choose. The two options produce the same files but a different history:

```bash
git pull --no-rebase --no-edit
git log --oneline --graph -4
```

```text
Merge made by the 'ort' strategy.
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
*   91360a6 (HEAD -> main) Merge branch 'main' of ~/git-practice/lesson-41/server/cafe
|\  
| * 4baa03b (origin/main, origin/HEAD) Add mocha
* | e1d3b7e Espresso 2.60
|/  
* 520c5c5 Add chai
```

Or undo that and rebase instead: your commit is replayed on top, a straight line (lesson 61 explains rebase):

```bash
git reset -q --hard HEAD~1
git pull --rebase
git log --oneline --graph -3
```

```text
Rebasing (1/1)
Successfully rebased and updated refs/heads/main.
* e99591c (HEAD -> main) Espresso 2.60
* 4baa03b (origin/main, origin/HEAD) Add mocha
* 520c5c5 Add chai
```

Then set your default once: `git config --global pull.rebase true` (or `false`, or `pull.ff only`).
