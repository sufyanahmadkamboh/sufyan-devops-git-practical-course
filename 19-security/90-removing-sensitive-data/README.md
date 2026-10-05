# Lesson 90 · Removing sensitive data

> Level 19 · Git security · ⏱ 30 minutes

## What are we learning?

How to rewrite a repository's history so that a file (or a string) never existed, with `git filter-repo`, and what
else has to happen for the cleanup to be real: force-pushing, every clone being replaced, and server-side caches. The
credential itself must already be rotated (lesson 89): history rewriting is cleanup, not protection.

## Visual

```text
 before:  A ── B(+.env) ── C ── D(-.env) ── E      every commit after B has a new parent …
 after:   A ── B' ─────── C' ── D' ─────── E'     … so B..E all get NEW IDs; .env exists in none of them

 then:  git push --force (all branches and tags)  →  server has only the new history
        every teammate RE-CLONES (an old clone pushed again brings the secret back)
        GitHub: cached views / PR refs may still show old commits → GitHub Support can purge them
```

## Lab setup

`git filter-repo` is a separate tool (recommended by the Git project and GitHub): `pip install git-filter-repo` (or
your package manager).

<!-- test: contains=git-filter-repo -->
```bash
git filter-repo --version > /dev/null && echo "git-filter-repo available"
bash scripts/new-lab.sh lesson-90 remote
cd ~/git-practice/lesson-90/ada
printf 'DB_PASSWORD=Cafe-2026-not-a-real-password\n' > .env && git add .env && git commit -q -m "Add configuration"
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git rm -q .env && git commit -q -m "Remove .env"
git push -q
(cd ../grace && git pull -q)
git log --oneline
```

## Demonstration

Work on a fresh **mirror** clone (all branches and tags, nothing else), as `filter-repo` recommends:

<!-- test: contains=Add configuration; output -->
```bash
cd ~/git-practice/lesson-90
git clone -q --mirror server/cafe.git cleanup.git
cd cleanup.git
git log --oneline --all -- .env
```

```text
d80d653 (HEAD -> main) Remove .env
61e2249 Add configuration
```

Remove `.env` from every commit:

<!-- test: output -->
```bash
git filter-repo --invert-paths --path .env 2>&1 | grep -v "^Parsed\|^HEAD is now" | tail -3
git log --oneline --all -- .env | wc -l
git log --oneline
```

```text
New history written in 0.18 seconds; now repacking/cleaning...
Repacking your repo and cleaning out old unneeded objects
Completely finished after 0.45 seconds.
0
e1eacde (HEAD -> main) Add green tea
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```

Every commit from "Add configuration" onwards has a new ID, and no commit contains `.env`. Push the new history over
the old one (a mirror push includes all branches and tags):

<!-- test: contains=forced update; output -->
```bash
git push --force --mirror ../server/cafe.git 2>&1 | grep -E "forced|up to date" | head -3
```

```text
 + d80d653...e1eacde main -> main (forced update)
```

(`filter-repo` removes the `origin` remote after rewriting, to prevent an accidental push; push to the URL explicitly.)

## Command breakdown

| Command | Removes |
|---|---|
| `git filter-repo --invert-paths --path FILE` | FILE from every commit |
| `git filter-repo --invert-paths --path-glob '*.pem'` | all matching files |
| `git filter-repo --replace-text replacements.txt` | strings (`OLD==>***REMOVED***` lines) in all files |
| `git filter-repo --analyze` | report of large/deleted files, to decide what to remove |
| BFG Repo-Cleaner | an older alternative (Java) |
| `git filter-branch` | the built-in, slow and error-prone predecessor: avoid |

## Hands-on exercise

**Instructions.** Verify on the **server** that no commit on any branch contains `.env`.

**Expected result.** `0`.

**Verification.**

<!-- test: contains=0 -->
```bash
cd ~/git-practice/lesson-90
git --git-dir=server/cafe.git log --all --oneline -- .env | wc -l
```

## Break it

Grace still has the old history. She makes a commit and does a normal `git pull` + `git push`:

<!-- test: contains=Add configuration; output -->
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

<!-- test: contains=0; output -->
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

## Real-world example

On GitHub, after rewriting and force-pushing: open pull requests and forks still reference old commits, and commit
URLs may stay cached. GitHub's documentation "Removing sensitive data from a repository" describes the remaining
steps: contact GitHub Support to remove cached views and PR references, ask fork owners to delete their forks. All of
this is why rotation comes first: after rotation, the leaked value is useless even if a copy survives.

## Practice challenge

Instead of deleting a whole file, replace one leaked string everywhere in history with `***REMOVED***`.

<details>
<summary>Solution</summary>

<!-- test: contains=REMOVED; absent=Cafe-2026; output -->
```bash
cd ~/git-practice/lesson-90
git init -q text-demo && cd text-demo
printf 'host=db\npassword=Cafe-2026-not-a-real-password\n' > app.conf && git add app.conf && git commit -q -m "Add app.conf"
echo 'Cafe-2026-not-a-real-password==>***REMOVED***' > ../replacements.txt
git filter-repo --force --replace-text ../replacements.txt > /dev/null 2>&1
git show HEAD:app.conf
```

```text
host=db
password=***REMOVED***
```

</details>

## Recap

- Rotate first; rewrite history second.
- `git filter-repo --invert-paths --path FILE` (or `--replace-text`) on a mirror clone, then force-push everything.
- Every clone must be replaced; otherwise the old history comes back with the next push.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-90
```

Next: [Lesson 91 · Commit signing](../91-commit-signing/README.md).
