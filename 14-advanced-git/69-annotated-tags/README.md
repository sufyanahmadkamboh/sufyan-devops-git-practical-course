# Lesson 69 · Annotated tags

> Level 14 · Advanced Git · ⏱ 15 minutes

## What are we learning?

Git has two kinds of tags. A **lightweight** tag is just a name for a commit. An **annotated** tag is an object of its
own, with a tagger, a date and a message (and optionally a signature, lesson 91). Releases should use annotated tags.

## Visual

```text
 lightweight:  refs/tags/v0.9.0 ──────────────────────────► commit fc345e6

 annotated:    refs/tags/v1.0.0 ──► tag object                ──► commit 4267004
                                    tagger: Ada <ada@…>, date
                                    message: "Release 1.0.0 …"
```

## Lab setup

<!-- test: contains=lesson-69 -->
```bash
bash scripts/new-lab.sh lesson-69 history
cd ~/git-practice/lesson-69
git tag v0.9.0 fc345e6
```

## Demonstration

<!-- test: contains=Tagger: Ada Lovelace; output -->
```bash
git tag -a v1.0.0 4267004 -m "Release 1.0.0: the first menu with prices"
git show v1.0.0 --stat | head -8
```

```text
tag v1.0.0
Tagger: Ada Lovelace <ada@example.com>
Date:   Mon Oct 5 03:49:35 2026 +0200

Release 1.0.0: the first menu with prices

commit 4267004871ae95e12690719f02460f9e3c935cf5 (tag: v1.0.0)
Author: Ada Lovelace <ada@example.com>
```

The two kinds, side by side:

<!-- test: contains=v1.0.0 tag; contains=v0.9.0 commit; output -->
```bash
for t in v0.9.0 v1.0.0; do echo "$t $(git cat-file -t "$t")"; done
git tag -n
```

```text
v0.9.0 commit
v1.0.0 tag
v0.9.0          Add the menu
v1.0.0          Release 1.0.0: the first menu with prices
```

`git tag -n` shows each tag's message (a lightweight tag shows the commit's subject instead).

## Command breakdown

| Command | What it does |
|---|---|
| `git tag -a NAME -m "msg" [COMMIT]` | annotated tag |
| `git tag -s NAME -m "msg"` | annotated and signed (lesson 91) |
| `git show NAME` | tag details + the commit |
| `git cat-file -t NAME` | `tag` (annotated) or `commit` (lightweight) |
| `git describe` | name HEAD relative to the nearest annotated tag: `v1.0.0-4-gecff18a` |
| `git push --follow-tags` | push commits and the annotated tags pointing at them |

## Hands-on exercise

**Instructions.** Use `git describe` to name the current commit.

**Expected result.** `v1.0.0-4-g…`: 4 commits after v1.0.0, at commit `g` + abbreviated ID.

**Verification.**

<!-- test: contains=v1.0.0-4-g -->
```bash
cd ~/git-practice/lesson-69
git describe
```

## Break it

In a repository with **only lightweight** tags, the build script calls `git describe`:

<!-- test: fail; contains=No annotated tags can describe; output -->
```bash
git tag -d v1.0.0 > /dev/null
git describe 2>&1
```

```text
fatal: No annotated tags can describe 'ecff18af63d0d85da66114f18c12b06e2ae9888b'.
However, there were unannotated tags: try --tags.
```

## Troubleshoot

`No annotated tags can describe '…'. However, there were unannotated tags: try --tags.`: `git describe` uses only
annotated tags by default, because lightweight tags are often temporary, personal markers. The version a build
reports must come from a real release tag.

## Fix

Create the release as an annotated tag (or, if lightweight tags are intentional, `git describe --tags`):

<!-- test: contains=v1.0.0-4-g; output -->
```bash
git tag -a v1.0.0 4267004 -m "Release 1.0.0"
git describe
git describe --tags --abbrev=0 HEAD~4
```

```text
v1.0.0-4-gecff18a
v1.0.0
```

## Real-world example

Build pipelines stamp versions with `git describe --tags --always --dirty`: `v2.3.1` on a release commit,
`v2.3.1-7-g1a2b3c4` on a commit after it, `-dirty` if the working tree had changes. Note: CI clones are often shallow
(lesson 39); without the tags and history, `git describe` fails, so release jobs fetch with `fetch-depth: 0`.

## Practice challenge

Who created `v1.0.0`, and when? Print only the tagger name and date.

<details>
<summary>Solution</summary>

<!-- test: contains=Ada Lovelace; output -->
```bash
cd ~/git-practice/lesson-69
git for-each-ref refs/tags/v1.0.0 --format='%(taggername) %(taggerdate:short)'
```

```text
Ada Lovelace 2026-10-05
```

</details>

## Recap

- Lightweight tag = a name; annotated tag = an object with tagger, date, message.
- Use annotated (or signed) tags for releases; `git describe` relies on them.
- `git cat-file -t TAG` tells the kinds apart.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-69
```

Next: [Lesson 70 · Git bisect](../70-git-bisect/README.md).
