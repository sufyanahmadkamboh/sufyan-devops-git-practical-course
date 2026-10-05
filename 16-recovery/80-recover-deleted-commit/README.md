# Lesson 80 · Recover a deleted commit

> Level 16 · Advanced recovery · ⏱ 20 minutes

## What are we learning?

A commit can disappear from a branch in many ways: an interactive rebase that dropped it, an `--amend` that replaced
it, a reset. We recover one with the reflog and `cherry-pick`, and then see the limit: once the reflog has expired and
garbage collection has run, only another copy (the server, a colleague) can help.

## Visual

```text
 A ── B ── C ── D   ← main           git rebase -i … drop C        A ── B ── D'   ← main
                                                                    C, D: unreachable, still in the reflog
 recovery:   git reflog → find C → git cherry-pick C                A ── B ── D' ── C'

 after git reflog expire --expire=now --all && git gc --prune=now:   C is gone from THIS repository
```

## Lab setup

<!-- test: contains=lesson-80 -->
```bash
bash scripts/new-lab.sh lesson-80 history
cd ~/git-practice/lesson-80
git init -q --bare ../lesson-80-server.git && git remote add origin ../lesson-80-server.git
git log --oneline -4
```

(`lesson-80-server.git` plays the team's GitHub repository; nothing is pushed yet.)

## Demonstration

A cleanup rebase drops the wrong line: "Add mocha" instead of something else.

<!-- test: absent=Add mocha; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i '/Add mocha/s/^pick/drop/'" git rebase -q -i HEAD~3
git log --oneline -4
grep mocha menu.txt || echo "mocha has a price but is not on the menu!"
```

```text
ffc88e8 (HEAD -> main) Price mocha
269869e Price green tea
6833580 Add green tea
4267004 Add prices
mocha has a price but is not on the menu!
```

The reflog lists every commit HEAD has been on, including the dropped one:

<!-- test: contains=Add mocha; output -->
```bash
git reflog | grep "Add mocha"
```

```text
2c389c0 HEAD@{4}: commit: Add mocha
```

Bring its change back on top of the current branch:

<!-- test: contains=mocha; output -->
```bash
dropped=$(git reflog --format=%h --grep-reflog="commit: Add mocha" | head -1)
git cherry-pick "$dropped" > /dev/null
git log --oneline -3
grep mocha menu.txt
```

```text
ccd73e3 (HEAD -> main) Add mocha
ffc88e8 Price mocha
269869e Price green tea
mocha
```

## Command breakdown

| Command | Use |
|---|---|
| `git reflog [--date=iso]` | every position of HEAD, with the action that caused it |
| `git log -g --grep-reflog=TEXT` | search the reflog |
| `git cherry-pick SHA` | re-apply a lost commit on the current branch |
| `git reset --hard HEAD@{N}` | jump the branch back to before the mistake (all of it) |
| `git fsck --unreachable` | unreachable objects, independent of the reflog |

## Hands-on exercise

**Instructions.** An `--amend` replaced a commit's content. Make one, then show the commit **before** the amend.

**Expected result.** The reflog's `commit (amend)` line, and the previous version's message.

<!-- test-run: cd ~/git-practice/lesson-80 && echo "chai" >> menu.txt && git commit -q -am "Add chai" && echo "chai 3.10" >> prices.txt && git commit -q -a --amend -m "Add chai and its price" -->

**Verification.**

<!-- test: contains=Add chai -->
```bash
cd ~/git-practice/lesson-80
git reflog -2
git log -1 --format=%s 'HEAD@{1}'
```

## Break it

Ada pushes her work, then "starts over" on the chai commit and cleans the repository aggressively:

<!-- test: contains=0; output -->
```bash
git push -q -u origin main
git reset -q --hard HEAD~1
git reflog expire --expire=now --all
git gc -q --prune=now
git reflog | wc -l
```

```text
0
```

## Troubleshoot

The reflog is empty and `gc --prune=now` deleted every unreachable object. Locally, the chai commit is gone:

<!-- test: contains=0; output -->
```bash
git fsck --unreachable --no-reflogs 2> /dev/null | wc -l
git log --oneline main | grep -c chai || true
```

```text
0
0
```

Recovery inside this clone is impossible. The question becomes: **where else does this commit exist?** On the server
if it was pushed, in a colleague's clone, in CI caches, in a GitHub PR (`refs/pull/N/head`). Ada pushed it:

<!-- test: contains=Add chai and its price; output -->
```bash
git log --oneline -1 origin/main
```

```text
3685547 (origin/main) Add chai and its price
```

## Fix

<!-- test: contains=chai 3.10; output -->
```bash
git reset -q --hard origin/main
git log --oneline -2
grep chai prices.txt
```

```text
3685547 (HEAD -> main, origin/main) Add chai and its price
ccd73e3 Add mocha
chai 3.10
```

Had the commit never been pushed, it would be lost for good: push work you care about, early.

## Real-world example

`git gc` runs automatically, but with safe defaults: reflog entries live 90 days (30 for unreachable commits), loose
unreachable objects 2 weeks. Commands like `git reflog expire --expire=now` and `git gc --prune=now` appear in
"reduce repository size" guides and in secret-removal procedures (lesson 90); run them only when you are certain
nothing needs recovering, and never as a reflex.

## Practice challenge

Find out how old the oldest entry in this repository's reflog is, and what the configured expiry is.

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-80
git reflog --date=relative | tail -1 | sed -E 's/\{[0-9]+ (seconds?|minutes?) ago\}/{N seconds ago}/'
git config --get gc.reflogExpire || echo "gc.reflogExpire not set: default 90 days"
```

```text
3685547 (HEAD -> main, origin/main) HEAD@{N seconds ago}: reset: moving to origin/main
gc.reflogExpire not set: default 90 days
```

</details>

## Recap

- Dropped, amended or reset commits stay in the reflog: find them, cherry-pick or reset back.
- `reflog expire` + `gc --prune=now` make them unrecoverable locally.
- Then only other copies help: the server, colleagues, PR refs. Push your work.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-80 ~/git-practice/lesson-80-server.git
```

Next: [Lesson 81 · Recover after a hard reset](../81-recover-after-hard-reset/README.md).
