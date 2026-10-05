# Lesson 13 · git log

> Level 3 · Git history · ⏱ 20 minutes

## What are we learning?

How to read the history: the full log, the one-line view, the graph of branches, and how to filter it by author,
message, date and file.

## Visual

```text
git log                      git log --oneline           git log --oneline --graph --all
──────────────────────       ─────────────────           ───────────────────────────────
commit 4c3f… (HEAD -> main)  4c3f9a1 Price mocha         * 4c3f9a1 (HEAD -> main) Price mocha
Author: Ada …                9b2e7c0 Add mocha           | * 1d8e2f3 (feature-tea) Add green tea
Date:   …                    …                           |/
    Price mocha                                          * 4267004 Add prices
```

## Lab setup

<!-- test: contains=lesson-13 -->
```bash
bash scripts/new-lab.sh lesson-13 history
cd ~/git-practice/lesson-13
```

## Demonstration

The full log, newest first (only the last two here):

<!-- test: contains=Author: Ada Lovelace; output -->
```bash
git log -2
```

```text
commit ecff18af63d0d85da66114f18c12b06e2ae9888b (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Mon Jan 5 09:07:00 2026 +0000

    Price mocha

commit 2c389c05c38cabc31d37906c2bb6b6d938959226
Author: Ada Lovelace <ada@example.com>
Date:   Mon Jan 5 09:06:00 2026 +0000

    Add mocha
```

One line per commit:

<!-- test: contains=d6df412 Add README; output -->
```bash
git log --oneline
```

```text
ecff18a (HEAD -> main) Price mocha
2c389c0 Add mocha
269869e Price green tea
6833580 Add green tea
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```

With a side branch, `--graph --all` draws the shape of the history:

<!-- test: contains=feature-tea; output -->
```bash
git switch -q -c feature-tea HEAD~2
echo "matcha" >> menu.txt && git commit -q -am "Add matcha"
git switch -q main
git log --oneline --graph --all
```

```text
* 5b84357 (feature-tea) Add matcha
| * ecff18a (HEAD -> main) Price mocha
| * 2c389c0 Add mocha
|/  
* 269869e Price green tea
* 6833580 Add green tea
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

`--all` shows every branch, not only the current one; `--graph` draws the lines; the labels in brackets are
references: `HEAD -> main` is where you are, `feature-tea` is another branch.

Filtering: which commits touched `prices.txt`, and which mention "mocha"?

<!-- test: contains=Price mocha; output -->
```bash
echo "--- commits that changed prices.txt"
git log --oneline -- prices.txt
echo "--- commits whose message mentions mocha"
git log --oneline --grep=mocha
```

```text
--- commits that changed prices.txt
ecff18a (HEAD -> main) Price mocha
269869e Price green tea
4267004 Add prices
--- commits whose message mentions mocha
ecff18a (HEAD -> main) Price mocha
2c389c0 Add mocha
```

## Command breakdown

| Command | Shows |
|---|---|
| `git log` | every commit reachable from `HEAD`, full format |
| `git log --oneline` | short ID + summary |
| `git log --oneline --graph --all` | all branches, with the branch structure drawn |
| `git log -N` | only the last N commits |
| `git log -- FILE` | commits that changed FILE |
| `git log --grep=TEXT` / `--author=NAME` / `--since=DATE` | filter by message, author, date |
| `git log -p` | each commit with its diff |
| `git log --format='%h %an %ar %s'` | your own format (hash, author, relative date, subject) |

## Hands-on exercise

**Instructions.** List the commits on `feature-tea` that are not on `main`.

**Expected result.** Exactly one commit: `Add matcha`.

<!-- test-run: true -->

**Verification.**

<!-- test: contains=Add matcha -->
```bash
cd ~/git-practice/lesson-13
git log --oneline main..feature-tea
```

`A..B` means "reachable from B but not from A": what B has that A does not.

## Break it

Look for a commit you know exists, and see nothing:

<!-- test: absent=matcha; output -->
```bash
git log --oneline --grep=matcha
```

```text
```

## Troubleshoot

Plain `git log` follows only the **current branch** (`HEAD`). The matcha commit is on `feature-tea`, which `main`
does not contain. When a commit seems to be missing, ask: which branch am I on, and is the commit on another branch?

<!-- test: contains=On branch main -->
```bash
git status | head -1
git branch
```

## Fix

<!-- test: contains=Add matcha; output -->
```bash
git log --oneline --all --grep=matcha
git branch --contains "$(git log --all --format=%h --grep=matcha)"
```

```text
5b84357 (feature-tea) Add matcha
  feature-tea
```

`--all` searches every branch, and `git branch --contains` names the branch that has the commit.

## Real-world example

Incident review: "what was deployed between Tuesday and today, and who changed the Helm values?"
`git log --since=tuesday --oneline -- helm/values-prod.yaml` answers in one line. In CI, `git log -1 --format=%H`
gives the exact commit being built, used to tag images and releases.

## Practice challenge

Print the history as `<short id> | <author> | <relative date> | <subject>`, only for commits that changed `menu.txt`.

<details>
<summary>Solution</summary>

<!-- test: contains=| Ada Lovelace |; output -->
```bash
cd ~/git-practice/lesson-13
git log --format='%h | %an | %ar | %s' -- menu.txt
```

```text
2c389c0 | Ada Lovelace | 9 months ago | Add mocha
6833580 | Ada Lovelace | 9 months ago | Add green tea
fc345e6 | Ada Lovelace | 9 months ago | Add the menu
```

</details>

## Recap

- `git log` shows the current branch's history, newest first; `--oneline`, `--graph`, `--all` change the view.
- Filter with `-- FILE`, `--grep`, `--author`, `--since`; compare branches with `A..B`.
- "Missing" commits are often on another branch: add `--all`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-13
```

Next: [Lesson 14 · git show](../14-git-show/README.md).
