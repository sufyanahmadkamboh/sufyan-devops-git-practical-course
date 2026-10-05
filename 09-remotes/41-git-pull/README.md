# Lesson 41 · git pull

> Level 8 · Remote repositories · ⏱ 20 minutes

## What are we learning?

`git pull` = `git fetch` + integrate (merge or rebase) `origin/<branch>` into the current branch. We see the easy case,
the "divergent branches" error, and how to configure the behaviour you want.

## Visual

```text
 git pull  =  git fetch  +  git merge origin/main      (pull.rebase false)
                         or git rebase origin/main     (pull.rebase true)
                         or fast-forward only          (pull.ff only)

 diverged:   A ── B ── X        ← main (your commit X)
                   ╲
                    C           ← origin/main (Grace's C)
             Git asks you to choose: merge (M joins X and C) or rebase (X' replayed after C)
```

## Lab setup

<!-- test: contains=lesson-41 -->
```bash
bash scripts/new-lab.sh lesson-41 remote
cd ~/git-practice/lesson-41/grace
echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q
cd ../ada
```

## Demonstration

Ada has no local commits: the pull is a fast-forward.

<!-- test: contains=Fast-forward; output -->
```bash
git pull
git log --oneline -2
```

```text
From ~/git-practice/lesson-41/server/cafe
   4267004..1b60e79  main       -> origin/main
Updating 4267004..1b60e79
Fast-forward
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
1b60e79 (HEAD -> main, origin/main, origin/HEAD) Add green tea
4267004 Add prices
```

## Command breakdown

| Command | What it does |
|---|---|
| `git pull` | fetch + integrate according to configuration |
| `git pull --ff-only` | only if no merge is needed |
| `git pull --no-rebase` | fetch + merge |
| `git pull --rebase` | fetch + rebase your local commits on top |
| `git config pull.rebase true` / `pull.ff only` | set the default |

## Hands-on exercise

**Instructions.** Grace pushes another commit; pull it into Ada's clone with `--ff-only`.

**Expected result.** `Fast-forward`.

<!-- test-run: cd ~/git-practice/lesson-41/grace && git pull -q && echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q -->

**Verification.**

<!-- test: contains=Add chai -->
```bash
cd ~/git-practice/lesson-41/ada
git pull --ff-only
git log --oneline -1
```

## Break it

Both sides commit: Ada locally, Grace on the server.

<!-- test: fail; contains=Need to specify how to reconcile divergent branches; output -->
```bash
cd ~/git-practice/lesson-41/grace && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" && git push -q
cd ../ada && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git pull 2>&1
```

```text
From ~/git-practice/lesson-41/server/cafe
   0562a80..6bbab0d  main       -> origin/main
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

<!-- test: contains=have diverged; output -->
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

<!-- test: contains=Merge branch 'main'; output -->
```bash
git pull --no-rebase --no-edit
git log --oneline --graph -4
```

```text
Merge made by the 'ort' strategy.
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
*   59d74a6 (HEAD -> main) Merge branch 'main' of ~/git-practice/lesson-41/server/cafe
|\  
| * 6bbab0d (origin/main, origin/HEAD) Add mocha
* | 0c3438b Espresso 2.60
|/  
* 0562a80 Add chai
```

Or undo that and rebase instead: your commit is replayed on top, a straight line (lesson 61 explains rebase):

<!-- test: contains=Espresso 2.60; absent=Merge branch; output -->
```bash
git reset -q --hard HEAD~1
git pull --rebase
git log --oneline --graph -3
```

```text
Rebasing (1/1)
Successfully rebased and updated refs/heads/main.
* 251ba29 (HEAD -> main) Espresso 2.60
* 6bbab0d (origin/main, origin/HEAD) Add mocha
* 0562a80 Add chai
```

Then set your default once: `git config --global pull.rebase true` (or `false`, or `pull.ff only`).

## Real-world example

Many teams standardise `pull.rebase true` for feature branches, so `git pull` never creates "Merge branch 'main' of
github.com:..." commits that clutter the history, and protect `main` so that it is only changed through pull requests
(lesson 59). Whatever your team uses, configure it explicitly, and use `git pull --ff-only` on `main`.

## Practice challenge

Set up Ada's clone so that `git pull` always rebases and automatically stashes uncommitted changes before doing so.

<details>
<summary>Solution</summary>

<!-- test: contains=true; output -->
```bash
cd ~/git-practice/lesson-41/ada
git config pull.rebase true
git config rebase.autoStash true
git config --get pull.rebase && git config --get rebase.autoStash
```

```text
true
true
```

</details>

## Recap

- `git pull` = fetch + merge or rebase.
- Diverged branches need a decision: `--no-rebase` (merge commit) or `--rebase` (linear history).
- Configure `pull.rebase` / `pull.ff` once; use `--ff-only` on shared branches.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-41
```

Next: [Lesson 42 · git push](../42-git-push/README.md).
