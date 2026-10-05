# Lesson 77 · Branches are references

> Level 15 · Git internals · ⏱ 15 minutes

## What are we learning?

A branch is not a copy of anything: it is a 41-byte file (or a line in `packed-refs`) containing one commit ID. Creating
a branch is instant, deleting one deletes only that pointer, and a "branch's commits" are simply the commits reachable
from it.

## Visual

```text
 .git/refs/heads/main          → 4267004
 .git/refs/heads/feature-tea   → bb67674
 .git/refs/tags/v1.0.0         → 4267004
 .git/refs/remotes/origin/main → 4267004

 main ───────→ Commit C              feature-tea ────→ Commit F
                 └── parent B …                          └── parent C …
```

## Lab setup

<!-- test: contains=lesson-77 -->
```bash
bash scripts/new-lab.sh lesson-77 feature
cd ~/git-practice/lesson-77
```

## Demonstration

<!-- test: contains=refs/heads/feature-tea; output -->
```bash
git for-each-ref --format='%(refname) -> %(objectname:short)'
cat .git/refs/heads/feature-tea 2> /dev/null || grep feature-tea .git/packed-refs
```

```text
refs/heads/feature-tea -> bb67674
refs/heads/main -> 4267004
bb676741936c50ad1f936300a05fc3c2cc0a9675
```

Create a branch by writing the reference yourself; Git sees a normal branch:

<!-- test: contains=experiment; output -->
```bash
git update-ref refs/heads/experiment fc345e6
git branch -v
```

```text
  experiment  fc345e6 Add the menu
  feature-tea bb67674 Add green tea to the menu
* main        4267004 Add prices
```

## Command breakdown

| Command | What it does |
|---|---|
| `git for-each-ref [refs/heads]` | list references with formats |
| `git show-ref` | references and IDs |
| `git update-ref REF ID` | create or move a reference (with a reflog entry) |
| `git update-ref -d REF` | delete a reference |
| `git pack-refs --all` | move loose reference files into `.git/packed-refs` |
| `git branch NAME ID` | the porcelain way to create a branch |

## Hands-on exercise

**Instructions.** Move `experiment` to `main`'s commit with `update-ref`, then list branches pointing at the same
commit as `main`.

**Expected result.** `experiment` and `main`.

<!-- test-run: cd ~/git-practice/lesson-77 && git update-ref refs/heads/experiment main -->

**Verification.**

<!-- test: contains=experiment; contains=main -->
```bash
cd ~/git-practice/lesson-77
git branch --points-at main
```

## Break it

Delete a branch reference and look for "its" commits:

<!-- test: absent=feature-tea; output -->
```bash
git update-ref -d refs/heads/feature-tea
git branch
git log --oneline --all | head -3
```

```text
  experiment
* main
4267004 (HEAD -> main, experiment) Add prices
fc345e6 Add the menu
d6df412 Add README
```

## Troubleshoot

The commit "Add green tea to the menu" no longer appears in `git log --all`: nothing references it. It still exists:
deleting a branch deleted a pointer, not commits.

<!-- test: contains=Add green tea to the menu; output -->
```bash
git cat-file -p bb67674 | tail -1
```

```text
Add green tea to the menu
```

## Fix

Recreate the reference to the same commit (the ID was in the earlier output, or in `git reflog`):

<!-- test: contains=feature-tea; output -->
```bash
git branch feature-tea bb67674
git log --oneline -1 feature-tea
```

```text
bb67674 (feature-tea) Add green tea to the menu
```

## Real-world example

Because branches are just pointers, the cost of creating them is zero: tools such as GitHub create `refs/pull/N/head`
for every pull request, CI systems fetch them directly (`git fetch origin pull/42/head`), and a repository with 10,000
branches is not 10,000 copies of the code.

## Practice challenge

Fetch-style: create a reference outside `refs/heads` (`refs/review/42`) pointing at `feature-tea`, and list it.

<details>
<summary>Solution</summary>

<!-- test: contains=refs/review/42; output -->
```bash
cd ~/git-practice/lesson-77
git update-ref refs/review/42 feature-tea
git for-each-ref refs/review
git branch | grep -c review || true
```

```text
bb676741936c50ad1f936300a05fc3c2cc0a9675 commit	refs/review/42
0
```

It is a valid reference (usable in any command: `git log refs/review/42`), but not a branch, so `git branch` does not
list it.

</details>

## Recap

- A branch is a reference: a name containing a commit ID.
- Creating, moving and deleting branches only changes these pointers.
- Unreferenced commits stay in the object store until garbage collection.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-77
```

Next: [Lesson 78 · Detached HEAD](../78-detached-head/README.md).
