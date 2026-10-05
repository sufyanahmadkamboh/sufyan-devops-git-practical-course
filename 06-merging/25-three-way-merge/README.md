# Lesson 25 · Three-way merge

> Level 5 · Merging · ⏱ 20 minutes

## What are we learning?

How Git merges two branches that both changed: it compares **three** snapshots, the two tips and their common
ancestor, the **merge base**.

## Visual

```text
          C  ← feature    (changed menu.txt)
         ╱
 A ─── B                  B = merge base: the last commit both branches share
         ╲
          D  ← main       (changed README.md)

 For every file: compare base→C and base→D.
   changed on one side only  → take that side
   changed on neither        → keep the base
   changed on both sides     → combine; if the same lines changed differently: CONFLICT (lesson 26)
```

## Lab setup

<!-- test: contains=lesson-25 -->
```bash
bash scripts/new-lab.sh lesson-25 diverged
cd ~/git-practice/lesson-25
git log --oneline --graph --all
```

## Demonstration

The three snapshots:

<!-- test: contains=4267004; output -->
```bash
base=$(git merge-base main feature-tea)
git log --oneline -1 "$base"
echo "--- base -> main changed:";        git diff --name-only "$base" main
echo "--- base -> feature-tea changed:"; git diff --name-only "$base" feature-tea
```

```text
4267004 Add prices
--- base -> main changed:
README.md
--- base -> feature-tea changed:
menu.txt
```

Each side changed a different file, so Git can take each change from its side automatically:

<!-- test: contains=Merge made by the 'ort' strategy; output -->
```bash
git merge --no-edit feature-tea
git show --stat --format='%s%nparents: %p' HEAD
```

```text
Merge made by the 'ort' strategy.
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
Merge branch 'feature-tea'
parents: f40d080 bb67674

 menu.txt | 1 +
 1 file changed, 1 insertion(+)
```

## Command breakdown

| Command | Use |
|---|---|
| `git merge-base A B` | the common ancestor of A and B |
| `git diff BASE A` | what A changed since they split |
| `git diff A...B` | B's changes since the merge base (lesson 15) |
| `git merge B` | three-way merge into the current branch |
| `git show --stat MERGE` | what the merge brought in (compared with the first parent) |

## Hands-on exercise

**Instructions.** Make both branches change **the same file in different places** (`menu.txt`: one adds a line at the
top, the other at the bottom) and merge.

**Expected result.** The merge succeeds without a conflict: Git combines changes to different lines of the same file.

<!-- test-run: cd ~/git-practice/lesson-25 && git switch -q -c top main && sed -i '1i ristretto' menu.txt && git commit -q -am "Add ristretto at the top" && git switch -q -c bottom main && echo "chai" >> menu.txt && git commit -q -am "Add chai at the bottom" && git switch -q main && git merge -q --no-edit top && git merge -q --no-edit bottom -->

**Verification.**

<!-- test: contains=ristretto; contains=chai -->
```bash
cd ~/git-practice/lesson-25
cat menu.txt
```

## Break it

Merge a branch that is not related to `main` at all: no merge base.

<!-- test: fail; contains=refusing to merge unrelated histories; output -->
```bash
git switch -q --orphan unrelated && echo "other project" > other.txt && git add other.txt && git commit -q -m "Other project"
git switch -q main
git merge unrelated 2>&1
```

```text
fatal: refusing to merge unrelated histories
```

## Troubleshoot

`refusing to merge unrelated histories`: `unrelated` has no commit in common with `main` (it was started with
`--orphan`), so there is no merge base. In real life this appears when you connect a local project to a GitHub
repository that was created **with** a README (two first commits), or when two different projects are combined.

<!-- test: contains=no merge base -->
```bash
git merge-base main unrelated || echo "no merge base"
```

## Fix

If combining them is really intended, allow it explicitly:

<!-- test: contains=other.txt; output -->
```bash
git merge --allow-unrelated-histories --no-edit unrelated
ls
```

```text
Merge made by the 'ort' strategy.
 other.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 other.txt
README.md
menu.txt
other.txt
prices.txt
```

## Real-world example

Two people edit `values.yaml` of a Helm chart on separate branches: one changes `replicaCount`, the other the image
tag. Different lines: the three-way merge combines them automatically. Only changes to the **same lines** need a human.
That is why small, focused commits and short-lived branches produce fewer conflicts.

## Practice challenge

After the merge, show the changes the merge brought into `main` relative to `main`'s previous tip, using the merge
commit's first parent.

<details>
<summary>Solution</summary>

<!-- test: contains=other.txt; output -->
```bash
cd ~/git-practice/lesson-25
git diff --stat HEAD^1 HEAD
```

```text
 other.txt | 1 +
 1 file changed, 1 insertion(+)
```

`HEAD^1` is the first parent (where `main` was), `HEAD^2` the second (the merged branch).

</details>

## Recap

- A three-way merge compares the two tips with their merge base.
- Changes on one side, or on different lines of the same file, merge automatically.
- No merge base = unrelated histories; `--allow-unrelated-histories` only when you really mean it.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-25
```

Next: [Lesson 26 · Merge conflicts](../26-merge-conflicts/README.md).
