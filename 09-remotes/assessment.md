# Module 09 · Remote repositories · Assessment

> Lessons 37–43 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-09-practical remote
bash scripts/new-lab.sh assess-09-broken remote
```

## Quiz

1. What is `origin/main`, and when does it move?
2. What is the difference between `git fetch` and `git pull`?
3. Which command lists the commits that a pull would bring in?
4. Your push is rejected with `(fetch first)`. What happened, and what is the fix?
5. When is `git push --force-with-lease` acceptable?
6. What does `git push -u origin feature` set up?
7. A branch was deleted on the server but `git branch -r` still shows it. Why, and how do you clean up?
8. What does `git clone --depth 1` give you, and when is it a problem?

<details>
<summary>Answers</summary>

1. A remote-tracking branch: your clone's memory of the server's `main`; it moves on fetch, pull and push (lesson 37).
2. `fetch` only downloads and updates `origin/*`; `pull` = fetch + merge or rebase into your branch (lessons 40–41).
3. `git log main..origin/main` (after a fetch) (lesson 40).
4. Someone pushed first; integrate with `git pull --rebase` (or merge), then push (lesson 42).
5. On your own branch after rewriting it, when nobody else builds on it (lesson 42).
6. The upstream: plain `git push`/`git pull` and ahead/behind refer to `origin/feature` (lesson 43).
7. Fetch never deletes remote-tracking branches; `git fetch --prune` (lesson 40).
8. Only the latest commit; history-based commands (`git log`, `git describe`) lack history (lesson 39).

</details>

## Practical challenge

In `~/git-practice/assess-09-practical` (Ada and Grace share `server/cafe.git`):

1. Ada creates `feature-chai` with one commit and pushes it with upstream.
2. Grace gets the branch and works on it locally (a local `feature-chai` tracking `origin/feature-chai`), adds a
   commit and pushes.
3. Ada brings Grace's commit into her branch.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Price chai; output -->
```bash
cd ~/git-practice/assess-09-practical/ada
git switch -q -c feature-chai && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push -q -u origin feature-chai
cd ../grace && git fetch -q && git switch -q feature-chai
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai" && git push -q
cd ../ada && git pull -q
git log --oneline -2
```

```text
5c87e72 (HEAD -> feature-chai, origin/feature-chai) Price chai
817f986 Add chai
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-09-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "feature-chai on the server"          'git --git-dir=server/cafe.git rev-parse --verify feature-chai'
check "Ada tracks origin/feature-chai"      '[ "$(git -C ada rev-parse --abbrev-ref feature-chai@{u})" = origin/feature-chai ]'
check "Grace tracks origin/feature-chai"    '[ "$(git -C grace rev-parse --abbrev-ref feature-chai@{u})" = origin/feature-chai ]'
check "Ada has Grace's commit"              'git -C ada log --format=%s feature-chai | grep -qx "Price chai"'
check "both clones match the server"        '[ "$(git -C ada rev-parse feature-chai)" = "$(git --git-dir=server/cafe.git rev-parse feature-chai)" ]'
```

```text
ok       feature-chai on the server
ok       Ada tracks origin/feature-chai
ok       Grace tracks origin/feature-chai
ok       Ada has Grace's commit
ok       both clones match the server
```

## Troubleshooting challenge

In `~/git-practice/assess-09-broken`, both developers committed on `main`:

<!-- test: contains=Espresso 2.60; output -->
```bash
cd ~/git-practice/assess-09-broken/grace
echo "Open 8-18" >> README.md && git commit -q -am "Add opening hours" && git push -q
cd ../ada
sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git log --oneline -1
```

```text
485602b (HEAD -> main) Espresso 2.60
```

Symptoms:

<!-- test: fail; contains=Need to specify how to reconcile divergent branches; output -->
```bash
git push 2>&1 | grep -E "rejected"
git pull 2>&1
```

```text
 ! [rejected]        main -> main (fetch first)
hint: Updates were rejected because the remote contains work that you do not
From ~/git-practice/assess-09-broken/server/cafe
   4267004..cbef06c  main       -> origin/main
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

Get Ada's commit onto the server with a linear history.

<details>
<summary>Solution</summary>

The push was rejected because the server has Grace's commit; `git pull` then refuses to guess between merge and
rebase. Rebase Ada's local commit on top, then push:

<!-- test: contains=main -> main; output -->
```bash
git pull --rebase 2>&1 | tail -1
git push 2>&1 | tail -1
```

```text
Rebasing (1/1)
Successfully rebased and updated refs/heads/main.
   cbef06c..fa4ab2a  main -> main
```

</details>

Verification:

<!-- test: contains=up to date with 'origin/main'; output -->
```bash
git log --oneline --graph -3
git status | sed -n 2p
```

```text
* fa4ab2a (HEAD -> main, origin/main, origin/HEAD) Espresso 2.60
* cbef06c Add opening hours
* 4267004 Add prices
Your branch is up to date with 'origin/main'.
```

## Real-world scenario

A new teammate cloned the repository yesterday. Today they say "the branch `release/2.4` doesn't exist", although you
can see it on GitHub. What is going on?

<details>
<summary>Model answer</summary>

Their clone's remote-tracking branches are a snapshot from the last fetch; the branch was pushed after they cloned.
`git fetch` updates `origin/*`, then `git switch release/2.4` creates the local tracking branch (lessons 37, 39–40).
If it still does not appear, check `git remote -v` (the right repository?) and `git ls-remote origin` (what the server
really has).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-09-practical ~/git-practice/assess-09-broken
```
