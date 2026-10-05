# Lesson 11 · git commit

> Level 2 · Commits · ⏱ 20 minutes

## What are we learning?

How to record a commit, how to write a good commit message, and how to fix the last commit with `--amend`.

## Visual

```text
 Working Directory ──git add──► Staging Area ──git commit──► new commit
                                                              ├─ snapshot of the staging area
                                                              ├─ author, date
                                                              ├─ message: WHY this change
                                                              └─ parent: the previous commit
```

A good message:

```text
Raise the latte price to 3.30              ← summary: imperative, ≤ 50 characters, no full stop

Milk prices went up 8 % this quarter.     ← body (optional): why, not how; wrap at 72 characters
```

## Lab setup

<!-- test: contains=lesson-11 -->
```bash
bash scripts/new-lab.sh lesson-11 basic
cd ~/git-practice/lesson-11
```

## Demonstration

<!-- test: contains=1 file changed; output -->
```bash
sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add prices.txt
git commit -m "Raise the latte price to 3.30" -m "Milk prices went up 8 % this quarter."
```

```text
[main b9f1597] Raise the latte price to 3.30
 1 file changed, 1 insertion(+), 1 deletion(-)
```

`[main 1a2b3c4]`: the branch and the new commit's short ID; then a summary of what changed. Look at the whole commit:

<!-- test: contains=Milk prices; output -->
```bash
git log -1
```

```text
commit b9f159714f72da1fe83650bedeab8f9bdfc44a49 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Mon Oct 5 02:54:31 2026 +0200

    Raise the latte price to 3.30
    
    Milk prices went up 8 % this quarter.
```

`-m` twice gives a summary and a body. Without `-m`, Git opens your editor (`core.editor`, or `$EDITOR`) for the
message.

**Skipping `git add` for tracked files**: `git commit -a` stages every modified tracked file first. It does not add
new files:

<!-- test: contains=?? specials.txt; output -->
```bash
echo "green tea" >> menu.txt
echo "2 for 1 on Mondays" > specials.txt
git commit -q -a -m "Add green tea"
git status --short
```

```text
?? specials.txt
```

## Command breakdown

| Command | What it does |
|---|---|
| `git commit -m "summary"` | commit the staging area with that message |
| `git commit -m "summary" -m "body"` | summary + body paragraph |
| `git commit` | open the editor for the message |
| `git commit -a -m "..."` | stage modified tracked files first (not new ones) |
| `git commit --amend` | replace the last commit (new message and/or staged changes) |
| `git commit --amend --no-edit` | add staged changes to the last commit, keep the message |

## Hands-on exercise

**Instructions.** Commit `specials.txt` with a summary and a body explaining why.

**Expected result.** `git log -1` shows both paragraphs; `git status` is clean.

<!-- test-run: cd ~/git-practice/lesson-11 && git add specials.txt && git commit -q -m "Add a Monday special" -m "Mondays are our quietest day." -->

**Verification.**

<!-- test: contains=quietest -->
```bash
cd ~/git-practice/lesson-11
git log -1 --format='%s%n%n%b'
git status --short
```

## Break it

A typo in the message, and a forgotten file:

<!-- test: contains=Add hte opening hours -->
```bash
echo "Open 8-18" > hours.txt
echo "Closed on public holidays" > holidays.txt
git add hours.txt
git commit -q -m "Add hte opening hours"
git log --oneline -1
```

## Troubleshoot

The summary has a typo and `holidays.txt` belongs to the same change but is still untracked. The commit has **not**
been pushed (no remote here at all), so it is safe to rewrite it.

## Fix

<!-- test: contains=Add the opening hours; contains=holidays.txt; output -->
```bash
git add holidays.txt
git commit -q --amend -m "Add the opening hours"
git log --oneline -1
git show --stat --format= HEAD
```

```text
b6da377 (HEAD -> main) Add the opening hours
 holidays.txt | 1 +
 hours.txt    | 1 +
 2 files changed, 2 insertions(+)
```

`--amend` replaced the commit: same parent, new snapshot, new message, **new ID**. Never amend a commit that others
already pulled: their copy still has the old one (lesson 32 shows the safe alternative, `git revert`).

## Real-world example

Commit messages are the project's memory: "Fix bug" tells the on-call engineer nothing at 3 a.m.; "Increase the
readiness probe timeout to 5 s, the JVM takes 4.5 s to start" tells them exactly what changed and why. Many teams also
use prefixes (`feat:`, `fix:`, `docs:`, Conventional Commits) so tools can build changelogs and version numbers.

## Practice challenge

Make a commit whose message has a summary line and a two-line body, using only `git commit` with an editor command
that writes the message for you (as Git would with your editor). Hint: `GIT_EDITOR` can be any command that edits the
file passed to it.

<details>
<summary>Solution</summary>

<!-- test: contains=Add a mocha; contains=Customers asked; output -->
```bash
cd ~/git-practice/lesson-11
echo "mocha" >> menu.txt && git add menu.txt
GIT_EDITOR='printf "Add a mocha\n\nCustomers asked for it.\nPrice follows tomorrow.\n" >' git commit -q
git log -1 --format='%s%n---%n%b'
```

```text
Add a mocha
---
Customers asked for it.
Price follows tomorrow.
```

Git writes a template into `.git/COMMIT_EDITMSG` and runs the editor on it; whatever the file contains afterwards
(minus `#` comment lines) becomes the message.

</details>

## Recap

- `git commit` records the staging area as a snapshot with a message, author, date and parent.
- Message: short imperative summary, blank line, a body that explains why.
- `--amend` rewrites the last commit; only for commits nobody else has yet.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-11
```

Next: [Lesson 12 · What actually happens during a commit?](../12-inside-a-commit/README.md).
