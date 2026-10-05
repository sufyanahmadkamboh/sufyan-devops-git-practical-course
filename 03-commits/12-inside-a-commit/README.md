# Lesson 12 · What actually happens during a commit?

> Level 2 · Commits · ⏱ 20 minutes

## What are we learning?

What a commit is made of: a **snapshot** of all files (not a diff), plus an ID, an author, a timestamp and a link to
its **parent** commit. Those parent links are the history.

## Visual

```text
 files ─► changes ─► staging ─► SNAPSHOT ─► COMMIT ─► history

 commit 4267004                          commit fc345e6                     commit d6df412
 ├─ tree   (all files, as they are)      ├─ tree                            ├─ tree
 ├─ parent fc345e6 ─────────────────────►├─ parent d6df412 ────────────────►├─ (no parent: the first commit)
 ├─ author  Ada Lovelace, 09:03          ├─ author ...                      ├─ author ...
 └─ message "Add prices"                 └─ message "Add the menu"          └─ message "Add README"
```

The commit ID is a hash of all of that. Change anything (a file, the message, the parent) and the ID changes.

## Lab setup

The lab's prepared commits have fixed authors and dates, so your IDs are exactly the ones shown here:

<!-- test: contains=4267004; output -->
```bash
bash scripts/new-lab.sh lesson-12 basic
cd ~/git-practice/lesson-12
git log --oneline
```

```text
lab ready: ~/git-practice/lesson-12 (basic)
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```

## Demonstration

The raw commit object of the latest commit:

<!-- test: contains=parent fc345e6; output -->
```bash
git cat-file -p HEAD
```

```text
tree edd9d5aca7be17de9c83a80dc687991f6f56e24d
parent fc345e6b28df7fdfd7f872b37d78b47d0d024103
author Ada Lovelace <ada@example.com> 1767603780 +0000
committer Ada Lovelace <ada@example.com> 1767603780 +0000

Add prices
```

Four parts: `tree` (the snapshot), `parent` (the previous commit), `author`/`committer` (name, e-mail, Unix time and
time zone), and the message. The tree lists **every** file, not just the changed one:

<!-- test: contains=README.md; contains=prices.txt; output -->
```bash
git cat-file -p 'HEAD^{tree}'
```

```text
100644 blob af07f28d5cff41687d90ff3f650baedef059f12e	README.md
100644 blob 6c76265ddb2eef943f09b0eac893294d1827affa	menu.txt
100644 blob 5813ff596a4ca95cdeb8b6777f5e30fa427ee0e8	prices.txt
```

`README.md` and `menu.txt` did not change in this commit, yet the snapshot lists them: Git stores complete snapshots
and reuses unchanged files (the same `blob` ID as in the parent), so it stays small. The diffs you see in `git show`
are computed on the fly by comparing two snapshots.

Now prove that the ID is computed from the content, by committing with the dates pinned (normally they are "now"):

<!-- test: output -->
```bash
echo "green tea" >> menu.txt && git add menu.txt
export GIT_AUTHOR_DATE="2026-01-05T10:00:00+00:00" GIT_COMMITTER_DATE="2026-01-05T10:00:00+00:00"
git commit -q -m "Add green tea";           echo "commit:               $(git rev-parse --short HEAD)"
git commit -q --amend -m "Add green tea";   echo "same everything:      $(git rev-parse --short HEAD)"
git commit -q --amend -m "Add green tea!";  echo "one character more:   $(git rev-parse --short HEAD)"
export GIT_COMMITTER_DATE="2026-01-05T10:01:00+00:00"
git commit -q --amend -m "Add green tea!";  echo "one minute later:     $(git rev-parse --short HEAD)"
unset GIT_AUTHOR_DATE GIT_COMMITTER_DATE
```

```text
commit:               3de709d
same everything:      3de709d
one character more:   7d464fc
one minute later:     3652692
```

The same snapshot, parent, author, time and message always give the same ID; change any of them, even one character
or one minute, and the ID is completely different. That is why your own commits never have the same IDs as someone
else's, even for an identical change: the time and the author differ.

## Command breakdown

| Command | Shows |
|---|---|
| `git cat-file -p COMMIT` | the raw commit: tree, parents, author, committer, message |
| `git cat-file -p 'COMMIT^{tree}'` | the snapshot's top-level files and folders |
| `git rev-parse HEAD` | the full ID of the current commit |
| `git log --format='%H %P'` | each commit's ID and its parents' IDs |

## Hands-on exercise

**Instructions.** Print the first commit's parent list (it has none) and the latest commit's parent.

**Expected result.** The root commit `d6df412` has no parent; every other commit has one.

**Verification.**

<!-- test: contains=d6df412 -->
```bash
cd ~/git-practice/lesson-12
git log --format='%h  parents: %p  %s'
```

## Break it

Try to change an old commit's message "in place" by editing the history directly. You can't: the closest thing,
`--amend`, works only on the **latest** commit, and changes its ID:

<!-- test: contains=Add pricing -->
```bash
before=$(git rev-parse --short HEAD)
git commit -q --amend -m "Add pricing (green tea)"
echo "before: $before  after: $(git rev-parse --short HEAD)"
git log --oneline -2
```

## Troubleshoot

Why can't an old commit simply be edited? Its ID is a hash of its content **including its parent's ID**. Changing a
commit changes its ID, which changes the parent recorded in every later commit, which changes all their IDs. History
is a chain of hashes: tamper with one link and every following link is different. That is what makes Git history
trustworthy, and why rewriting shared history causes trouble.

## Fix

Rewriting older commits is possible, as a deliberate new history, with interactive rebase (lesson 63). For a mistake
in the latest, unpushed commit, `--amend` (above) is the right tool. Put the message back:

<!-- test: contains=Add green tea -->
```bash
git commit -q --amend -m "Add green tea"
git log --oneline -1
```

## Real-world example

Because IDs are content hashes, a commit ID identifies an exact version of the code. Pipelines tag Docker images with
the commit ID (`app:4267004`), deployments record which commit is live, and a security team can say "every version
built from commit `4267004` or later contains the fix". The same ID means the same code, everywhere.

## Practice challenge

Show that two different commits can share an identical file version: find the `blob` ID of `README.md` in the first
commit and in the latest commit.

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-12
git rev-parse "$(git rev-list --max-parents=0 HEAD):README.md"
git rev-parse HEAD:README.md
```

```text
af07f28d5cff41687d90ff3f650baedef059f12e
af07f28d5cff41687d90ff3f650baedef059f12e
```

Same ID: the README never changed, so every snapshot points at the same stored blob.

</details>

## Recap

- A commit = snapshot (tree) + parent(s) + author/committer + message; its ID is a hash of all of it.
- Git stores snapshots and reuses unchanged files; diffs are computed when you ask.
- Changing a commit changes its ID and the IDs of everything after it: history is a hash chain.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-12
```

Next: [Module 04 · Lesson 13 · git log](../../04-history/13-git-log/README.md).
