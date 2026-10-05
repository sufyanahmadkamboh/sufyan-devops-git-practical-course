# Lesson 74 · How Git stores data

> Level 15 · Git internals · ⏱ 25 minutes

## What are we learning?

Under every command you have used, Git stores only four kinds of objects in `.git/objects`, each named by the hash of
its content: **blobs** (file contents), **trees** (folders), **commits** (snapshots with history) and **tags**. Plus
**references**: small files with names like `main` pointing to commits.

## Visual

```text
 refs/heads/main ──► commit 4267004                  references: names → commit IDs
                       tree   ─────────────┐
                       parent fc345e6      │
                       author, message     ▼
                                     tree 9a1c…          a folder: names → blob/tree IDs
                                     ├── README.md ──► blob 3f2e…   file content only (no name!)
                                     ├── menu.txt  ──► blob 7b04…
                                     └── prices.txt ─► blob c2a9…

 same content = same hash = stored once. Change one byte → new blob → new tree → new commit.
```

## Lab setup

<!-- test: contains=lesson-74 -->
```bash
bash scripts/new-lab.sh lesson-74 basic
cd ~/git-practice/lesson-74
```

## Demonstration

Follow the chain from `main` down to a file's content:

<!-- test: contains=tree; contains=parent fc345e6; output -->
```bash
cat .git/refs/heads/main 2> /dev/null || git rev-parse main
git cat-file -p main
```

```text
4267004871ae95e12690719f02460f9e3c935cf5
tree edd9d5aca7be17de9c83a80dc687991f6f56e24d
parent fc345e6b28df7fdfd7f872b37d78b47d0d024103
author Ada Lovelace <ada@example.com> 1767603780 +0000
committer Ada Lovelace <ada@example.com> 1767603780 +0000

Add prices
```

The commit points to a tree. The tree lists names and the blobs holding the contents:

<!-- test: contains=blob; contains=menu.txt; output -->
```bash
git cat-file -p 'main^{tree}'
```

```text
100644 blob af07f28d5cff41687d90ff3f650baedef059f12e	README.md
100644 blob 6c76265ddb2eef943f09b0eac893294d1827affa	menu.txt
100644 blob 5813ff596a4ca95cdeb8b6777f5e30fa427ee0e8	prices.txt
```

<!-- test: contains=espresso 2.50; output -->
```bash
git cat-file -p "$(git rev-parse main:prices.txt)"
```

```text
espresso 2.50
latte 3.20
cappuccino 3.40
```

The ID **is** the content's hash: Git computes the same ID for the same bytes, anywhere.

<!-- test: output -->
```bash
git rev-parse main:prices.txt
printf 'espresso 2.50\nlatte 3.20\ncappuccino 3.40\n' | git hash-object --stdin
```

```text
5813ff596a4ca95cdeb8b6777f5e30fa427ee0e8
5813ff596a4ca95cdeb8b6777f5e30fa427ee0e8
```

## Command breakdown

| Command | What it does |
|---|---|
| `git cat-file -t ID` | the object's type: blob, tree, commit, tag |
| `git cat-file -p ID` | pretty-print the object |
| `git rev-parse REV:PATH` | the blob/tree ID of PATH in REV |
| `git hash-object FILE` | compute a file's blob ID (`-w` also stores it) |
| `git count-objects -v` | how many objects, how much space |
| `git ls-tree -r REV` | every file in a commit's snapshot |

## Hands-on exercise

**Instructions.** Count the objects in the repository and explain the number: 3 commits, each with a tree, and how
many distinct blobs?

**Expected result.** `count: 9` loose objects (3 commits + 3 trees + 3 blobs: README, menu, prices).

**Verification.**

<!-- test: contains=count: 9 -->
```bash
cd ~/git-practice/lesson-74
git count-objects -v | head -1
```

## Break it

Corrupt an object file (simulating a disk error), then use the repository:

<!-- test: fail; contains=fatal; output -->
```bash
obj=$(git rev-parse main:menu.txt)
f=".git/objects/${obj:0:2}/${obj:2}"
chmod u+w "$f" && printf 'garbage' > "$f"
git show main:menu.txt 2>&1
```

```text
error: inflate: data stream error (incorrect header check)
error: unable to unpack 6c76265ddb2eef943f09b0eac893294d1827affa header
error: inflate: data stream error (incorrect header check)
error: unable to unpack 6c76265ddb2eef943f09b0eac893294d1827affa header
error: inflate: data stream error (incorrect header check)
error: unable to unpack 6c76265ddb2eef943f09b0eac893294d1827affa header
fatal: loose object 6c76265ddb2eef943f09b0eac893294d1827affa (stored in .git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa) is corrupt
```

## Troubleshoot

The object file no longer decompresses to content whose hash matches its name; Git detects it (every object is
verified by its hash) and refuses to use it. `git fsck` checks the whole repository:

<!-- test: fail; contains=menu; output -->
```bash
obj=$(git rev-parse main:menu.txt)
git fsck --full 2>&1 | head -5 | sed "s/$obj/$obj (menu.txt)/"
test "${PIPESTATUS[0]}" -eq 0
```

```text
error: inflate: data stream error (incorrect header check)
error: unable to unpack header of .git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa
error: 6c76265ddb2eef943f09b0eac893294d1827affa (menu.txt): object corrupt or missing: .git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa
missing blob 6c76265ddb2eef943f09b0eac893294d1827affa (menu.txt)
```

## Fix

A blob is defined by its content: write the same content again and Git recreates exactly the same object. In real
life you get the content back from another clone (`git fetch` from the remote restores missing objects).

<!-- test: contains=latte; output -->
```bash
obj=$(git rev-parse main:menu.txt)
rm -f ".git/objects/${obj:0:2}/${obj:2}"
printf 'espresso\nlatte\ncappuccino\n' | git hash-object -w --stdin
git fsck --full && git show main:menu.txt
```

```text
6c76265ddb2eef943f09b0eac893294d1827affa
espresso
latte
cappuccino
```

## Real-world example

Content addressing is why Git is fast and safe: a clone can verify every byte it received; identical files across
thousands of commits are stored once; comparing two commits starts by comparing tree IDs, so unchanged folders are
skipped instantly. It is also why history cannot be changed silently: editing anything changes every ID after it.

## Practice challenge

Commit a copy of `menu.txt` under another name. How many new blobs does that create?

<details>
<summary>Solution</summary>

<!-- test: contains=same blob; output -->
```bash
cd ~/git-practice/lesson-74
cp menu.txt menu-copy.txt && git add menu-copy.txt && git commit -q -m "Copy the menu"
[ "$(git rev-parse HEAD:menu.txt)" = "$(git rev-parse HEAD:menu-copy.txt)" ] && echo "same blob: no new blob, only a new tree and commit"
```

```text
same blob: no new blob, only a new tree and commit
```

</details>

## Recap

- Objects: blob (content), tree (folder), commit (snapshot + parents + message), tag.
- Every object's name is the hash of its content; same content, same object.
- References (branches, tags, HEAD) are names pointing to commits.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-74
```

Next: [Lesson 75 · Git objects](../75-git-objects/README.md).
