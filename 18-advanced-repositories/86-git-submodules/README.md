# Lesson 86 · Git submodules

> Level 18 · Advanced repositories · ⏱ 25 minutes

## What are we learning?

A submodule embeds another Git repository inside yours, pinned to **one exact commit**. Useful for sharing a library,
a chart or a set of templates between repositories; also a source of confusion, because cloning, updating and
committing need extra steps. We go through all of them.

## Visual

```text
 cafe (main repository)
 ├── menu.txt
 ├── .gitmodules              path = shared  url = ../shared.git   (committed)
 └── shared/  ──────────────► shared repository, at commit 1a2b3c4 (the "gitlink": the main repo stores only this ID)

 main repo commit ─► tree ─► shared: commit 1a2b3c4      (not the files: a pointer to the other repo's commit)
```

## Lab setup

A shared repository (common price rules used by several shops) and the cafe repository:

<!-- test: contains=lesson-86 -->
```bash
bash scripts/new-lab.sh lesson-86 basic
cd ~/git-practice
git init -q --bare lesson-86-shared.git
git clone -q lesson-86-shared.git lesson-86-shared-work 2> /dev/null
cd lesson-86-shared-work
echo "VAT 19%" > tax.txt && git add tax.txt && git commit -q -m "Add the tax rule" && git push -q origin HEAD:main
cd ../lesson-86
```

In this course the "remote" repositories are local paths. Since Git 2.38, submodules from local paths need an explicit
`-c protocol.file.allow=always` (a security default); with `https://` or `git@` URLs you will not need it.

## Demonstration

Add the shared repository as a submodule:

<!-- test: contains=shared; output -->
```bash
git -c protocol.file.allow=always submodule add -q ../lesson-86-shared.git shared
cat .gitmodules
git status --short
```

```text
[submodule "shared"]
	path = shared
	url = ../lesson-86-shared.git
A  .gitmodules
A  shared
```

<!-- test: contains=160000; output -->
```bash
git commit -q -m "Add the shared rules as a submodule"
git ls-tree HEAD shared
cat shared/tax.txt
```

```text
160000 commit 9f5499c23790a88afc8019f40aa29d69100d256d	shared
VAT 19%
```

Mode `160000` and type `commit`: the main repository stores a **commit ID** of the other repository, not its files.

## Command breakdown

| Command | What it does |
|---|---|
| `git submodule add URL PATH` | add a submodule, create/extend `.gitmodules` |
| `git clone --recurse-submodules URL` | clone including submodules |
| `git submodule update --init [--recursive]` | check out the pinned commits after a plain clone |
| `git submodule update --remote` | move submodules to their remote branch's latest commit |
| `git submodule status` | pinned commit of each submodule (`-` = not initialised) |
| `git config submodule.recurse true` | let `pull`/`switch` update submodules automatically |

## Hands-on exercise

**Instructions.** The shared repository gets a new rule. Update the cafe's submodule to it and commit the new pin.

**Expected result.** `git diff` of the main repository shows the submodule moving to a new commit; after committing,
`shared/` contains the new rule.

<!-- test-run: cd ~/git-practice/lesson-86-shared-work && echo "Service included" >> tax.txt && git commit -q -am "Add the service rule" && git push -q origin HEAD:main -->

**Verification.**

<!-- test: contains=Service included -->
```bash
cd ~/git-practice/lesson-86
git -c protocol.file.allow=always submodule update -q --remote shared
git diff --submodule=log | head -3
git commit -q -am "Update the shared rules"
cat shared/tax.txt
```

## Break it

Grace clones the cafe repository the usual way:

<!-- test: contains=-; output -->
```bash
git init -q --bare ../lesson-86-cafe.git && git push -q ../lesson-86-cafe.git main
cd .. && git clone -q lesson-86-cafe.git lesson-86-grace && cd lesson-86-grace
ls shared/ | wc -l
git submodule status
```

```text
0
-009710344304d0ac962666fbf91812d01aa6506f shared
```

## Troubleshoot

`shared/` is empty and `git submodule status` shows a leading `-`: the submodule is registered but not initialised. A
plain `git clone` does not fetch submodules. Anything that needs `shared/tax.txt` (a build, a deployment) fails.

## Fix

<!-- test: contains=Service included; output -->
```bash
git -c protocol.file.allow=always submodule update --init
git submodule status
cat shared/tax.txt
```

```text
Submodule 'shared' (~/git-practice/lesson-86-shared.git) registered for path 'shared'
Cloning into '~/git-practice/lesson-86-grace/shared'...
done.
Submodule path 'shared': checked out '009710344304d0ac962666fbf91812d01aa6506f'
 009710344304d0ac962666fbf91812d01aa6506f shared (heads/main)
VAT 19%
Service included
```

Next time: `git clone --recurse-submodules`.

## Real-world example

Submodules fit when the embedded project has its own life and releases (a shared Terraform module repository, a
vendored library) and you want to pin an exact version. Costs: every developer and CI job must init/update them
(`actions/checkout` with `submodules: true`), updates need two commits in two repositories, and detached HEADs inside
submodules confuse people. Alternatives: package managers, Helm chart dependencies, Terraform module sources with
`?ref=v1.2.0`, or a monorepo.

## Practice challenge

Make `git pull` in Grace's clone update the submodule automatically.

<details>
<summary>Solution</summary>

<!-- test: contains=true; output -->
```bash
cd ~/git-practice/lesson-86-grace
git config submodule.recurse true
git config --get submodule.recurse
```

```text
true
```

</details>

## Recap

- A submodule = another repository pinned to one commit (`.gitmodules` + a gitlink, mode 160000).
- Clone with `--recurse-submodules`, or `git submodule update --init` afterwards.
- Updating means: move the submodule, then commit the new pin in the main repository.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-86 ~/git-practice/lesson-86-shared.git ~/git-practice/lesson-86-shared-work ~/git-practice/lesson-86-cafe.git ~/git-practice/lesson-86-grace
```

Next: [Lesson 87 · Git worktrees](../87-git-worktrees/README.md).
