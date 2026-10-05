# Lesson 76 · HEAD

> Level 15 · Git internals · ⏱ 15 minutes

## What are we learning?

`HEAD` is the answer to "where am I?". Normally it points to a **branch**, and the branch points to a commit. That
indirection is why committing moves the branch you are on, and switching branches changes what `HEAD` points to.

## Visual

```text
 .git/HEAD:  ref: refs/heads/main
                    │
                    ▼
 .git/refs/heads/main:  4267004…
                    │
                    ▼
             commit 4267004 "Add prices"

 git commit       → new commit; main moves to it; HEAD still says "ref: refs/heads/main"
 git switch tea   → HEAD becomes "ref: refs/heads/tea"
```

## Lab setup

<!-- test: contains=lesson-76 -->
```bash
bash scripts/new-lab.sh lesson-76 feature
cd ~/git-practice/lesson-76
```

## Demonstration

<!-- test: contains=ref: refs/heads/main; output -->
```bash
cat .git/HEAD
git symbolic-ref HEAD
git rev-parse HEAD
```

```text
ref: refs/heads/main
refs/heads/main
4267004871ae95e12690719f02460f9e3c935cf5
```

Switch: only `HEAD` changes.

<!-- test: contains=ref: refs/heads/feature-tea; output -->
```bash
git switch -q feature-tea
cat .git/HEAD
git rev-parse --short HEAD
```

```text
ref: refs/heads/feature-tea
bb67674
```

Commit: the branch moves, `HEAD` still names the branch.

<!-- test: contains=ref: refs/heads/feature-tea; output -->
```bash
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
cat .git/HEAD
echo "feature-tea: $(git rev-parse --short feature-tea), HEAD: $(git rev-parse --short HEAD)"
```

```text
ref: refs/heads/feature-tea
feature-tea: be4d094, HEAD: be4d094
```

## Command breakdown

| Expression / command | Meaning |
|---|---|
| `HEAD` | the current commit (through the current branch) |
| `HEAD~1`, `HEAD~2` | first parent, grandparent |
| `HEAD^2` | second parent (of a merge) |
| `git symbolic-ref HEAD` | which branch HEAD points to (fails if detached) |
| `git branch --show-current` | the same, friendlier |
| `@` | shorthand for `HEAD` |

## Hands-on exercise

**Instructions.** Print the subject of the commit two before `HEAD`, using `HEAD~2`.

**Expected result.** "Add prices".

**Verification.**

<!-- test: contains=Add prices -->
```bash
cd ~/git-practice/lesson-76
git log -1 --format=%s HEAD~2
```

## Break it

Edit `.git/HEAD` to point to a branch that does not exist (as a broken script or typo would):

<!-- test: contains=No commits yet; output -->
```bash
echo "ref: refs/heads/mian" > .git/HEAD
git status 2>&1 | head -3
```

```text
On branch mian

No commits yet
```

## Troubleshoot

`On branch mian … No commits yet`: Git believes you are on a brand-new, empty branch, because `HEAD` names a branch
that has no commit. Nothing is lost: your branches are untouched.

<!-- test: contains=feature-tea; output -->
```bash
git branch
```

```text
  feature-tea
  main
```

## Fix

Point `HEAD` back to a real branch (the safe way, with the command instead of editing the file):

<!-- test: contains=refs/heads/feature-tea -->
```bash
git symbolic-ref HEAD refs/heads/feature-tea
git symbolic-ref HEAD
git status --short | wc -l
```

## Real-world example

The same idea exists on remotes: `refs/remotes/origin/HEAD` points to the server's default branch (`origin/main`).
When a team renames `master` to `main`, clones keep the old value until `git remote set-head origin --auto` updates
it; scripts that rely on `origin/HEAD` then pick the right default branch.

## Practice challenge

Clone the lab repository and show what the clone's `origin/HEAD` points to. Why that branch?

<details>
<summary>Solution</summary>

<!-- test: contains=refs/remotes/origin/feature-tea; output -->
```bash
cd ~/git-practice
git clone -q lesson-76 lesson-76-clone
git -C lesson-76-clone symbolic-ref refs/remotes/origin/HEAD
git -C lesson-76-clone branch --show-current
```

```text
refs/remotes/origin/feature-tea
feature-tea
```

`origin/HEAD` records the **source's** `HEAD` at clone time: the lab was on `feature-tea`, so the clone checked out
`feature-tea` and considers it the default branch. On GitHub, the source's `HEAD` is the repository's default branch.

</details>

## Recap

- `HEAD` → branch → commit; committing moves the branch, switching moves `HEAD`.
- `HEAD~N`, `HEAD^2`, `@` navigate from there.
- `git symbolic-ref` reads and sets `HEAD` safely.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-76 ~/git-practice/lesson-76-clone
```

Next: [Lesson 77 · Branches are references](../77-branches-are-references/README.md).
