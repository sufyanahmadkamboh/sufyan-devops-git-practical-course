# Lesson 55 · Team Git workflow

> Level 12 · Collaboration · ⏱ 25 minutes

## What are we learning?

What happens when three people work on the same repository at the same time, and the small set of habits that keeps
it calm: short branches, pull before you start, push often, integrate through the shared server.

## Visual

```text
 Developer A (Ada)      Developer B (Grace)      Developer C (Linus)
   feature-tea            fix-latte-price          docs-hours
        │                      │                        │
        └──────── push ────────┼──────── push ──────────┘
                               ▼
                       GitHub (server/cafe.git)
                               │
                 main ◄── merged one after another; everyone pulls
```

## Lab setup

The `remote` scenario has Ada and Grace; Linus joins:

<!-- test: contains=lesson-55 -->
```bash
bash scripts/new-lab.sh lesson-55 remote
cd ~/git-practice/lesson-55
git clone -q server/cafe.git linus
git -C linus config user.name "Linus Torvalds" && git -C linus config user.email "linus@example.com"
ls
```

## Demonstration

Each developer works on a branch and pushes it:

<!-- test: contains=feature-tea; contains=fix-latte-price; contains=docs-hours; output -->
```bash
(cd ada && git switch -q -c feature-tea && echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q -u origin feature-tea)
(cd grace && git switch -q -c fix-latte-price && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price" && git push -q -u origin fix-latte-price)
(cd linus && git switch -q -c docs-hours && echo "Open 8-18" >> README.md && git commit -q -am "Document opening hours" && git push -q -u origin docs-hours)
git --git-dir=server/cafe.git branch
```

```text
  docs-hours
  feature-tea
  fix-latte-price
* main
```

The branches are integrated into `main` one by one (on GitHub: three merged pull requests). Here, Ada merges all
three, as the PR merge button would:

<!-- test: contains=Document opening hours; output -->
```bash
cd ada
git switch -q main && git fetch -q
for b in feature-tea fix-latte-price docs-hours; do git merge -q --no-ff --no-edit "origin/$b"; done
git push -q
git log --oneline --graph -8
```

```text
*   927a05a (HEAD -> main, origin/main, origin/HEAD) Merge remote-tracking branch 'origin/docs-hours'
|\  
| * b9f013b (origin/docs-hours) Document opening hours
* |   7e09982 Merge remote-tracking branch 'origin/fix-latte-price'
|\ \  
| * | a39c66b (origin/fix-latte-price) Fix the latte price
| |/  
* |   8495af2 Merge remote-tracking branch 'origin/feature-tea'
|\ \  
| |/  
|/|   
| * cbe4ea7 (origin/feature-tea, feature-tea) Add green tea
|/  
* 4267004 Add prices
* fc345e6 Add the menu
```

Everyone updates their `main` before starting the next task:

<!-- test: contains=origin/docs-hours; output -->
```bash
cd ../linus && git switch -q main && git pull -q && git log --oneline -1
```

```text
927a05a (HEAD -> main, origin/main, origin/HEAD) Merge remote-tracking branch 'origin/docs-hours'
```

## Command breakdown

| Habit | Commands |
|---|---|
| start from the latest main | `git switch main && git pull` |
| one branch per task | `git switch -c TASK` |
| push early (backup, visibility) | `git push -u origin TASK` |
| integrate through PRs | `gh pr create`, review, merge |
| clean up | `git branch -d TASK`, `git fetch --prune` |

## Hands-on exercise

**Instructions.** As Grace, bring your clone up to date and delete your merged local branch.

**Expected result.** `fix-latte-price` deleted with `-d` (it is merged, so no `-D` needed).

<!-- test-run: cd ~/git-practice/lesson-55/grace && git switch -q main && git pull -q && git branch -d fix-latte-price -->

**Verification.**

<!-- test: absent=fix-latte-price -->
```bash
cd ~/git-practice/lesson-55/grace
git branch
```

## Break it

Two developers commit directly on `main` and push, minutes apart:

<!-- test: fail; contains=[rejected]; output -->
```bash
cd ~/git-practice/lesson-55/grace && git pull -q
echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q
cd ../linus && echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push 2>&1
```

```text
To ~/git-practice/lesson-55/server/cafe.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '~/git-practice/lesson-55/server/cafe.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Troubleshoot

Linus's push is rejected: Grace's commit reached the server first. Both changed the end of `menu.txt`, so integrating
will also conflict. On a team, working directly on `main` turns every push into a race.

## Fix

Linus integrates Grace's work (rebase his commit on top), resolves, and pushes:

<!-- test: contains=Add mocha; output -->
```bash
git pull --rebase > /dev/null 2>&1 || true
printf 'espresso\nlatte\ncappuccino\ngreen tea\nchai\nmocha\n' > menu.txt
git add menu.txt && GIT_EDITOR=true git rebase --continue > /dev/null
git push -q
git log --oneline -3
```

```text
Successfully rebased and updated refs/heads/main.
2941d65 (HEAD -> main, origin/main, origin/HEAD) Add mocha
e8de87a Add chai
927a05a Merge remote-tracking branch 'origin/docs-hours'
```

Prevention: work on branches and merge through PRs (lesson 56), and protect `main` (lesson 59).

## Real-world example

A platform team of five works on one Terraform repository: each change is a short branch and a PR, CI posts the
`terraform plan` as a PR comment, one teammate reviews, the PR is merged, and CI applies it. Nobody pushes to `main`;
when two PRs touch the same module, the second one is updated (`git merge main` or rebase) and its plan re-run.

## Practice challenge

Show, for each developer's clone, how many commits its `main` is behind the server.

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-55
for dev in ada grace linus; do
  git -C "$dev" fetch -q
  echo "$dev: $(git -C "$dev" rev-list --count main..origin/main) behind"
done
```

```text
ada: 2 behind
grace: 1 behind
linus: 0 behind
```

</details>

## Recap

- Many developers, one server: integrate through it, in small pieces.
- Pull before starting, branch per task, push early, merge via PRs.
- Direct commits to a shared `main` cause rejected pushes and conflicts.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-55
```

Next: [Lesson 56 · Feature branch workflow](../56-feature-branch-workflow/README.md).
