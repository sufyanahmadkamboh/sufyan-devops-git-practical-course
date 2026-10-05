# Lesson 58 · Git Flow

> Level 12 · Collaboration · ⏱ 25 minutes

## What are we learning?

Git Flow is a branching model with two long-lived branches (`main` for releases, `develop` for integration) and
short-lived `feature/*`, `release/*` and `hotfix/*` branches. We run a full cycle with plain Git commands and discuss
where it helps and where it is unnecessary complexity.

## Visual

```text
 main      ●────────────────────●─────────●──────►   only releases (tagged v1.0.0, v1.0.1 …)
           │                   ╱ ╲       ╱ ╲
 hotfix/*  │                  │   └─●───┘   │        from main, merged into main AND develop
 release/* │           ●──●──┘              │        from develop: stabilise, version, then into main + develop
 develop   ●──●───●───●──────────────●──────●───►    integration of finished features
 feature/*     ╲─●─╱                                  from develop, back into develop
```

## Lab setup

<!-- test: contains=lesson-58 -->
```bash
bash scripts/new-lab.sh lesson-58 basic
cd ~/git-practice/lesson-58
git tag -a v1.0.0 -m "Release 1.0.0" && git switch -q -c develop
git log --oneline --decorate --all
```

## Demonstration

**Feature**: from `develop`, back into `develop`:

<!-- test: contains=Merge branch 'feature/green-tea' into develop -->
```bash
git switch -q -c feature/green-tea develop
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git switch -q develop && git merge -q --no-ff --no-edit feature/green-tea && git branch -d -q feature/green-tea
git log --oneline -1
```

**Release**: from `develop`; only stabilisation commits; merged into `main` (tagged) and back into `develop`:

<!-- test: contains=v1.1.0; output -->
```bash
git switch -q -c release/1.1.0 develop
echo "1.1.0" > VERSION && git add VERSION && git commit -q -m "Bump version to 1.1.0"
git switch -q main && git merge -q --no-ff --no-edit release/1.1.0 && git tag -a v1.1.0 -m "Release 1.1.0"
git switch -q develop && git merge -q --no-ff --no-edit release/1.1.0 && git branch -d -q release/1.1.0
git log --oneline --graph --all | head -12
```

```text
*   86e1fcd (HEAD -> develop) Merge branch 'release/1.1.0' into develop
|\  
| | *   18f4759 (tag: v1.1.0, main) Merge branch 'release/1.1.0'
| | |\  
| | |/  
| |/|   
| * | b7c047e Bump version to 1.1.0
|/ /  
* |   796ceef Merge branch 'feature/green-tea' into develop
|\ \  
| |/  
|/|   
```

## Command breakdown

| Branch | From | Into | Lifetime |
|---|---|---|---|
| `main` | — | — | permanent; every commit is a release |
| `develop` | `main` | — | permanent; next release in progress |
| `feature/*` | `develop` | `develop` | days |
| `release/*` | `develop` | `main` + `develop` | until the release ships |
| `hotfix/*` | `main` | `main` + `develop` | hours |

## Hands-on exercise

**Instructions.** List the tags and the commit each one points to.

**Expected result.** `v1.0.0` and `v1.1.0`.

**Verification.**

<!-- test: contains=v1.1.0 -->
```bash
cd ~/git-practice/lesson-58
git tag -n --format='%(refname:short) %(*objectname:short) %(contents:subject)'
```

## Break it

A production bug in 1.1.0: the latte price. A **hotfix** goes into `main`, is released as 1.1.1, but the developer
forgets to merge it into `develop`:

<!-- test: contains=latte 3.20 -->
```bash
git switch -q -c hotfix/1.1.1 main
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price"
git switch -q main && git merge -q --no-ff --no-edit hotfix/1.1.1 && git tag -a v1.1.1 -m "Release 1.1.1"
git switch -q develop && grep latte prices.txt
```

## Troubleshoot

`develop` still has `latte 3.20`: the next release (1.2.0, cut from `develop`) would **bring the bug back**. Check what
`main` has that `develop` does not:

<!-- test: contains=Fix the latte price; output -->
```bash
git log --oneline develop..main
```

```text
857e449 (tag: v1.1.1, main) Merge branch 'hotfix/1.1.1'
18f4759 (tag: v1.1.0) Merge branch 'release/1.1.0'
c88da4e (hotfix/1.1.1) Fix the latte price
```

## Fix

<!-- test: contains=latte 3.30; output -->
```bash
git merge -q --no-ff --no-edit hotfix/1.1.1 && git branch -d -q hotfix/1.1.1
grep latte prices.txt
git log --oneline develop..main | wc -l
```

```text
latte 3.30
1
```

## Real-world example

Git Flow fits software that ships **versions** to customers and maintains several at once: installers, mobile apps,
on-premise products, libraries. For a web service deployed many times a day, it mostly adds ceremony: `develop` and
`release/*` delay every change, and GitHub Flow (lesson 57) or trunk-based development is usually the better choice.
Use the simplest model that fits how you release.

## Practice challenge

Which commits would go into the next release (1.2.0) if it were cut now? Start a new feature first.

<details>
<summary>Solution</summary>

<!-- test: contains=Add mocha; output -->
```bash
cd ~/git-practice/lesson-58
git switch -q -c feature/mocha develop && echo mocha >> menu.txt && git commit -q -am "Add mocha"
git switch -q develop && git merge -q --no-ff --no-edit feature/mocha
git log --oneline --no-merges main..develop
```

```text
8718abb (feature/mocha) Add mocha
```

</details>

## Recap

- Git Flow: `main` (releases) + `develop` (integration) + feature, release, hotfix branches.
- Hotfixes go into `main` **and** `develop`; check with `git log develop..main`.
- Good for versioned products; often unnecessary for continuously deployed services.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-58
```

Next: [Lesson 59 · Branch protection](../59-branch-protection/README.md).
