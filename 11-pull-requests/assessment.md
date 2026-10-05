# Module 11 · Pull requests · Assessment

> Lessons 51–54 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

Two labs: one for the practical challenge, one already broken for the troubleshooting challenge.

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-11-pr diverged
bash scripts/new-lab.sh assess-11-broken conflict
(cd ~/git-practice/assess-11-pr && git switch -q feature-tea && echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea" && git switch -q main)
```

## Quiz

1. Which command shows the commits a pull request from `feature` into `main` would bring in?
2. Why does the "Files changed" tab correspond to `git diff main...feature` (three dots) and not `git diff main feature`?
3. How can you check, without touching any file, whether a branch would merge into `main` without conflicts?
4. What is the difference between a "Comment", an "Approve" and a "Request changes" review?
5. Why can't you approve your own pull request, and what does that mean for a protected `main` that requires one
   approval?
6. Name the three merge strategies of the GitHub merge button and the history each leaves on `main`.
7. After a squash merge, `git branch -d feature` says "not fully merged". Why, and what do you check before using
   `-D`?
8. A PR's branch was pushed again with three new commits. Do you need to open a new PR?

<details>
<summary>Answers</summary>

1. `git log --oneline main..feature`: commits on `feature` not on `main` (lesson 51).
2. Three dots diff against the merge base, so only the branch's own changes appear, not what `main` did meanwhile (51).
3. `git merge-tree --write-tree main feature`: exit status 0 = clean, 1 = conflicts (51).
4. Comment has no verdict; Approve says ready to merge; Request changes blocks merging where reviews are required (53).
5. A review is a second person's check; GitHub refuses the author's approval, so someone else with write access must
   approve before the PR can be merged (53, 59).
6. Merge commit (all commits + a merge commit), squash (one new commit per PR), rebase (commits replayed, linear) (54).
7. The squash commit has a new ID; the branch's commits are not reachable from `main`. Compare the content
   (`git diff main feature -- FILES`) before `-D` (54).
8. No: pushing to the PR's branch updates the existing PR (52).

</details>

## Practical challenge

In `~/git-practice/assess-11-pr`, `feature-tea` has two commits ("Add green tea to the menu", "Price green tea"); `main`
has moved on ("Add opening hours").

Requirements:

1. Produce the PR's "commits" and "files changed" views from the command line.
2. Confirm the branch merges without conflicts.
3. Squash-merge it into `main` as **one** commit named `Green tea (#1)`.
4. Delete `feature-tea` after verifying its content is on `main`.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Green tea (#1); output -->
```bash
cd ~/git-practice/assess-11-pr
git log --oneline main..feature-tea
git diff --stat main...feature-tea
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts"
git merge -q --squash feature-tea && git commit -q -m "Green tea (#1)"
git diff --quiet main feature-tea -- menu.txt prices.txt && git branch -D feature-tea
git log --oneline -3
```

```text
549f46a (feature-tea) Price green tea
bb67674 Add green tea to the menu
 menu.txt   | 1 +
 prices.txt | 1 +
 2 files changed, 2 insertions(+)
no conflicts
Automatic merge went well; stopped before committing as requested
Squash commit -- not updating HEAD
Deleted branch feature-tea (was 549f46a).
719ff28 (HEAD -> main) Green tea (#1)
f40d080 Add opening hours
4267004 Add prices
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-11-pr
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "one squash commit 'Green tea (#1)' on main" '[ "$(git log -1 --format=%s main)" = "Green tea (#1)" ]'
check "green tea on the menu and priced"           'grep -q "green tea" menu.txt && grep -q "green tea 2.80" prices.txt'
check "no merge commits on main"                   '[ "$(git rev-list --merges --count main)" -eq 0 ]'
check "feature-tea deleted"                        '! git rev-parse -q --verify refs/heads/feature-tea'
check "opening hours kept"                         'grep -q "Open every day" README.md'
```

```text
ok       one squash commit 'Green tea (#1)' on main
ok       green tea on the menu and priced
ok       no merge commits on main
ok       feature-tea deleted
ok       opening hours kept
```

## Troubleshooting challenge

In `~/git-practice/assess-11-broken`, the reviewer says: "This PR cannot be merged: the branch has conflicts."

Symptoms:

<!-- test: fail; contains=CONFLICT; output -->
```bash
cd ~/git-practice/assess-11-broken
git merge-tree --write-tree --name-only main feature-tea
```

```text
c1ec90e49d06aa38520744c366604c4ec932383a
prices.txt

Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
```

Make the PR mergeable the way its author would: on the branch, without changing `main`. The team agreed the latte
costs **3.40**.

<details>
<summary>Solution</summary>

The author brings `main` into the branch and resolves there (lessons 27, 51):

<!-- test: contains=no conflicts; output -->
```bash
cd ~/git-practice/assess-11-broken
git switch -q feature-tea
git merge main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q -m "Merge main into feature-tea; latte at 3.40"
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts"
```

```text
no conflicts
```

</details>

Verification: the "PR" merges cleanly, and `main` was not touched by the fix.

<!-- test: contains=latte 3.40; output -->
```bash
cd ~/git-practice/assess-11-broken
git log --oneline -1 main
git switch -q main && git merge -q --no-ff --no-edit feature-tea && grep latte prices.txt
```

```text
594657b (main) Raise the latte price to 3.30
latte 3.40
```

## Real-world scenario

You review a PR titled "Update stuff": 41 files changed, 3 unrelated topics (a Helm value, a dependency bump, a new
endpoint), one commit "wip". CI is green. What do you do?

<details>
<summary>Model answer</summary>

Do not approve just because CI is green. Leave a "Request changes" review explaining why: the PR mixes three changes, so
it cannot be reviewed properly or reverted independently. Ask the author to split it into three focused PRs with
descriptive titles (Conventional Commits, lesson 84) and a description of why, what and how it was tested (lesson 52).
Offer to review the smallest one first. If the team keeps seeing this, add a PR template and agree on a size guideline.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-11-pr ~/git-practice/assess-11-broken
```
