# Lesson 75 · Git objects

> Level 15 · Git internals · ⏱ 25 minutes

## What are we learning?

We build a commit **by hand** with plumbing commands (`hash-object`, `update-index`, `write-tree`, `commit-tree`,
`update-ref`), to see that `git add` and `git commit` are nothing more than these steps. `git cat-file` lets us
inspect every result.

## Visual

```text
 git add menu.txt      =  git hash-object -w menu.txt            (blob)
                          git update-index --add menu.txt         (staging area = the index)
 git commit -m "msg"   =  git write-tree                          (tree from the index)
                          git commit-tree TREE -p PARENT -m msg   (commit object)
                          git update-ref refs/heads/main COMMIT   (move the branch)
```

## Lab setup

<!-- test: contains=lesson-75 -->
```bash
bash scripts/new-lab.sh lesson-75 basic
cd ~/git-practice/lesson-75
git log --oneline
```

## Demonstration

Change a file and store its content as a blob:

<!-- test: output -->
```bash
echo "green tea" >> menu.txt
blob=$(git hash-object -w menu.txt)
echo "blob $blob: $(git cat-file -t "$blob"), $(git cat-file -s "$blob") bytes"
```

```text
blob cbd8549959e24eb7fa5e0ee03169cb033e6e7877: blob, 36 bytes
```

Stage it and write a tree from the index:

<!-- test: contains=green tea; output -->
```bash
git update-index menu.txt
tree=$(git write-tree)
git cat-file -p "$tree"
git cat-file -p "$tree:menu.txt"
```

```text
100644 blob af07f28d5cff41687d90ff3f650baedef059f12e	README.md
100644 blob cbd8549959e24eb7fa5e0ee03169cb033e6e7877	menu.txt
100644 blob 5813ff596a4ca95cdeb8b6777f5e30fa427ee0e8	prices.txt
espresso
latte
cappuccino
green tea
```

Create the commit object with `main` as parent, then move `main` to it:

<!-- test: contains=Add green tea (by hand); output -->
```bash
tree=$(git write-tree)
commit=$(echo "Add green tea (by hand)" | git commit-tree "$tree" -p main)
git update-ref refs/heads/main "$commit"
git log --oneline -2
git status --short
```

```text
5072f74 (HEAD -> main) Add green tea (by hand)
4267004 Add prices
```

A normal commit, made without `git add` or `git commit`. `git status` is clean: index, working directory and `main`
agree.

## Command breakdown

| Plumbing | Porcelain it is part of |
|---|---|
| `git hash-object -w FILE` | `git add` (store content) |
| `git update-index [--add] FILE` | `git add` (record in the index) |
| `git ls-files --stage` | what the index contains |
| `git write-tree` | `git commit` (snapshot the index) |
| `git commit-tree TREE -p PARENT` | `git commit` (create the commit) |
| `git update-ref REF ID` | `git commit`, `git branch -f`, `git reset` (move a reference) |
| `git cat-file -t / -s / -p ID` | inspect type / size / content |

## Hands-on exercise

**Instructions.** Show the index entry for `menu.txt` (mode, blob ID, stage).

**Expected result.** `100644 <blob> 0	menu.txt`, the same blob ID as in the tree.

**Verification.**

<!-- test: contains=100644 -->
```bash
cd ~/git-practice/lesson-75
git ls-files --stage menu.txt
git rev-parse HEAD:menu.txt
```

## Break it

Create a commit object but forget to move the branch:

<!-- test: absent=Forgotten commit; output -->
```bash
echo "mocha" >> menu.txt && git update-index menu.txt
lost=$(echo "Forgotten commit" | git commit-tree "$(git write-tree)" -p main)
echo "$lost" > ../lesson-75-lost-id.txt
git log --oneline -2
```

```text
5072f74 (HEAD -> main) Add green tea (by hand)
4267004 Add prices
```

## Troubleshoot

The commit exists in the object store, but no reference points to it, so `git log` (which starts from `HEAD`) does not
show it. `git status` shows the staged change as still uncommitted, because `HEAD` did not move:

<!-- test: contains=commit; contains=M  menu.txt; output -->
```bash
git cat-file -t "$(cat ../lesson-75-lost-id.txt)"
git status --short
```

```text
commit
M  menu.txt
```

## Fix

Move the branch to the commit (what `git commit` would have done as its last step):

<!-- test: contains=Forgotten commit; output -->
```bash
git update-ref refs/heads/main "$(cat ../lesson-75-lost-id.txt)"
git log --oneline -2
git status --short
```

```text
32645d5 (HEAD -> main) Forgotten commit
5072f74 Add green tea (by hand)
```

## Real-world example

Plumbing commands are how tools are built on top of Git: CI scripts that read a file from another branch without
checking it out (`git show origin/main:VERSION`), release tools that create tags via `git update-ref`, and
`git commit-tree` in scripts that build a commit with a known tree (for example a `gh-pages` branch generated from
a build folder).

## Practice challenge

Read `prices.txt` as it was in the first commit that had it, without checking anything out.

<details>
<summary>Solution</summary>

<!-- test: contains=latte 3.20; output -->
```bash
cd ~/git-practice/lesson-75
git cat-file -p 4267004:prices.txt
```

```text
espresso 2.50
latte 3.20
cappuccino 3.40
```

</details>

## Recap

- `git add` = store the blob + update the index; `git commit` = write a tree + create a commit + move the branch.
- `git cat-file` inspects any object.
- An object without a reference is invisible to `git log` but still in the store.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-75 ~/git-practice/lesson-75-lost-id.txt
```

Next: [Lesson 76 · HEAD](../76-head/README.md).
