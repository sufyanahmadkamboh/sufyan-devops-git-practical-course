# Lesson 70 · Git bisect

> Level 14 · Advanced Git · ⏱ 25 minutes

## What are we learning?

`git bisect` finds the commit that introduced a bug by binary search: you mark a known good and a known bad commit,
Git checks out the middle, you test, and it halves the range until one commit remains. Ten commits take about 3–4
tests; a thousand take about 10.

## Visual

```text
 known good                                                           known bad
 ●──────●──────●──────●──────●──────●──────●──────●──────●──────●
 1      2      3      4      5      6      7      8      9      10
                             ▲ test: bad  → the bug is in 2..5
               ▲ test: good  → the bug is in 4..5
                      ▲ test: bad → commit 4 is the first bad commit
```

## Lab setup

The lab has a tiny price calculator, `price.sh`, and a check, `check.sh` (exit 0 = correct, 1 = wrong):

<!-- test: contains=lesson-70 -->
```bash
bash scripts/new-lab.sh lesson-70 bisect
cd ~/git-practice/lesson-70
git log --oneline
```

## Demonstration

The bug: an espresso and a latte should cost 5.70.

<!-- test: output -->
```bash
bash price.sh espresso latte 2>&1 || true
bash check.sh && echo good || echo bad
```

```text
price.sh: line 6: 320
360: arithmetic syntax error in expression (error token is "360")
2.50
bad
```

The first commit was fine. Start bisecting:

<!-- test: contains=Bisecting; output -->
```bash
first=$(git rev-list --max-parents=0 HEAD)
git bisect start
git bisect bad HEAD
git bisect good "$first"
```

```text
status: waiting for both good and bad commits
status: waiting for good commit(s), bad commit known
Bisecting: 4 revisions left to test after this (roughly 2 steps)
[1a2385cb587a5c03380dfd5ceb0a36bd51305324] Add chai
```

Git checked out a commit in the middle. Test it and tell Git, until it names the culprit:

<!-- test: contains=is the first; output -->
```bash
while true; do
  if bash check.sh; then result=$(git bisect good); else result=$(git bisect bad); fi
  echo "$result" | head -1
  case "$result" in *"is the first"*) break ;; esac
done
```

```text
Bisecting: 1 revision left to test after this (roughly 1 step)
Bisecting: 0 revisions left to test after this (roughly 0 steps)
3ceea031d6f34d67cc8f33c993ea0784c54ae95f is the first bad commit
```

Finish: return to where you were.

<!-- test: contains=main -->
```bash
git bisect reset
git branch --show-current
```

## Command breakdown

| Command | What it does |
|---|---|
| `git bisect start` | begin |
| `git bisect bad [C]` / `git bisect good [C]` | mark the current (or C) commit |
| `git bisect run CMD` | automate: CMD exit 0 = good, 1–124 = bad, 125 = skip |
| `git bisect skip` | the current commit cannot be tested |
| `git bisect log` / `visualize` | what was marked so far |
| `git bisect reset` | finish, back to the original branch |

## Hands-on exercise

**Instructions.** Let Git do the whole search with `git bisect run`.

**Expected result.** The first bad commit is "Add mocha".

**Verification.**

<!-- test: contains=Add mocha -->
```bash
cd ~/git-practice/lesson-70
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh > /dev/null 2>&1
git log -1 --format='first bad commit: %h %s' refs/bisect/bad
git bisect reset > /dev/null 2>&1
```

## Break it

Mark the commits the wrong way round:

<!-- test: fail; contains=Maybe you mistook; output -->
```bash
git bisect start
git bisect good HEAD
git bisect bad "$(git rev-list --max-parents=0 HEAD)" 2>&1
```

```text
status: waiting for both good and bad commits
status: waiting for bad commit, 1 good commit known
Some good revs are not ancestors of the bad rev.
git bisect cannot work properly in this case.
Maybe you mistook good and bad revs?
```

## Troubleshoot

`Some good revs are not ancestors of the bad rev … Maybe you mistook good and bad revs?` (newer Git versions
quote the terms: `'good'`, `'bad'`): bisect searches for the
commit where things went from good to bad, so the good commit must be older than the bad one. Here it is reversed.

## Fix

Start over with the right order:

<!-- test: contains=is the first; output -->
```bash
git bisect reset > /dev/null 2>&1
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh 2>&1 | grep "is the first"
git bisect reset > /dev/null 2>&1
```

```text
3ceea031d6f34d67cc8f33c993ea0784c54ae95f is the first bad commit
```

(If you are looking for when something was **fixed**, use other words: `git bisect start --term-old=broken
--term-new=fixed`.)

## Real-world example

"Deployments of the chart started failing sometime in the last 200 commits." `git bisect run helm template ./chart`,
or `git bisect run make test`, finds the commit in 8 builds without anyone reading 200 diffs. The better the check
script (fast, deterministic, exit code 125 for "cannot build"), the more useful bisect is.

## Practice challenge

Show the change that introduced the bug, and explain it.

<details>
<summary>Solution</summary>

<!-- test: contains=+latte 3.60; output -->
```bash
cd ~/git-practice/lesson-70
git show "$(git log --format=%h --grep='^Add mocha$')" -- prices.txt
```

```text
commit 3ceea031d6f34d67cc8f33c993ea0784c54ae95f
Author: Ada Lovelace <ada@example.com>
Date:   Mon Jan 5 09:03:00 2026 +0000

    Add mocha

diff --git a/prices.txt b/prices.txt
index 88ea474..63b4ce4 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,5 @@
 espresso 2.50
 latte 3.20
 cappuccino 3.00
+mocha 3.90
+latte 3.60
```

The mocha commit also added a second `latte` line. `price.sh` greps `^latte `, gets two prices, and the sum breaks.

</details>

## Recap

- Bisect = binary search through history between a good and a bad commit.
- Automate with `git bisect run SCRIPT` (0 good, 1–124 bad, 125 skip).
- Always `git bisect reset` at the end.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-70
```

Next: [Lesson 71 · Git blame](../71-git-blame/README.md).
