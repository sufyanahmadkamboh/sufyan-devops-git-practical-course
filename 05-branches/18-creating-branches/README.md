# Lesson 18 · Creating branches

> Level 4 · Branches · ⏱ 15 minutes

## What are we learning?

`git branch` lists and creates branches. Creating one does **not** switch to it: a common surprise.

## Visual

```text
 before                          git branch feature-login          (you are still on main)

 A ── B ── C  ← main (HEAD)       A ── B ── C  ← main (HEAD)
                                             ↖ feature-login        a new label on the same commit
```

A branch is a movable label pointing to a commit. Creating one copies nothing: it writes one small file with a commit ID.

## Lab setup

<!-- test: contains=lesson-18 -->
```bash
bash scripts/new-lab.sh lesson-18 basic
cd ~/git-practice/lesson-18
```

## Demonstration

<!-- test: contains=* main; output -->
```bash
git branch
```

```text
* main
```

The `*` marks the current branch. Create a branch:

<!-- test: contains=feature-login; output -->
```bash
git branch feature-login
git branch
git log --oneline -1
```

```text
  feature-login
* main
4267004 (HEAD -> main, feature-login) Add prices
```

Two branches now point to the same commit, and `*` is still on `main`: `git branch NAME` only creates. The branch is a
file containing a commit ID:

<!-- test: output -->
```bash
cat .git/refs/heads/feature-login
git rev-parse main
```

```text
4267004871ae95e12690719f02460f9e3c935cf5
4267004871ae95e12690719f02460f9e3c935cf5
```

Same ID. Branches can also start from an older commit:

<!-- test: contains=hotfix-prices; output -->
```bash
git branch hotfix-prices HEAD~1
git branch -v
```

```text
  feature-login 4267004 Add prices
  hotfix-prices fc345e6 Add the menu
* main          4267004 Add prices
```

## Command breakdown

| Command | What it does |
|---|---|
| `git branch` | list local branches, `*` = current |
| `git branch -v` | with the latest commit of each |
| `git branch NAME` | create NAME at the current commit (no switch) |
| `git branch NAME COMMIT` | create NAME at another commit |
| `git branch -a` | include remote-tracking branches (lesson 40) |
| `git branch -m OLD NEW` | rename a branch |

## Hands-on exercise

**Instructions.** Rename `feature-login` to `feature/login` (slashes are allowed and common for grouping).

**Expected result.** `git branch` lists `feature/login`, not `feature-login`.

<!-- test-run: cd ~/git-practice/lesson-18 && git branch -m feature-login feature/login -->

**Verification.**

<!-- test: contains=feature/login; absent=feature-login -->
```bash
cd ~/git-practice/lesson-18
git branch
```

## Break it

Two classic mistakes: a name that already exists, and an invalid name.

<!-- test: fail; contains=already exists; output -->
```bash
git branch hotfix-prices 2>&1
```

```text
fatal: a branch named 'hotfix-prices' already exists
```

<!-- test: fail; contains=not a valid branch name; output -->
```bash
git branch "fix prices" 2>&1
```

```text
fatal: 'fix prices' is not a valid branch name
hint: See 'git help check-ref-format'
hint: Disable this message with "git config set advice.refSyntax false"
```

## Troubleshoot

`a branch named 'hotfix-prices' already exists`: names are unique. `'fix prices' is not a valid branch name`: no
spaces, no `..`, no `~ ^ : ? * [` or ending in `.lock`. Check a name before using it:

<!-- test: contains=fix-prices -->
```bash
git check-ref-format --branch "fix-prices"
```

## Fix

<!-- test: contains=fix-prices -->
```bash
git branch fix-prices
git branch
```

## Real-world example

Teams agree on branch name patterns so tools can act on them: `feature/JIRA-123-login`, `fix/...`, `release/1.4`,
`hotfix/...`. CI rules then say things like "deploy previews for `feature/*`" or "protect `release/*`" (lesson 59).

## Practice challenge

Create a branch called `before-prices` at the commit **before** prices were added, using the commit message to find it,
not a count like `HEAD~1`.

<details>
<summary>Solution</summary>

<!-- test: contains=before-prices; output -->
```bash
cd ~/git-practice/lesson-18
git branch before-prices "$(git log --format=%h --grep='Add the menu')"
git branch -v
```

```text
  before-prices fc345e6 Add the menu
  feature/login 4267004 Add prices
  fix-prices    4267004 Add prices
  hotfix-prices fc345e6 Add the menu
* main          4267004 Add prices
```

</details>

## Recap

- `git branch NAME` creates a label at the current commit; it does not switch.
- `git branch` lists, `-v` adds the latest commit, `-m` renames.
- A branch is a file with a commit ID: creating one is instant, whatever the project size.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-18
```

Next: [Lesson 19 · Switching branches](../19-switching-branches/README.md).
