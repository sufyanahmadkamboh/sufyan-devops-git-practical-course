# Lesson 71 · Git blame

> Level 14 · Advanced Git · ⏱ 15 minutes

## What are we learning?

`git blame FILE` shows, for every line, the commit that last changed it, who made it and when. It answers "why is
this line like this?", by leading you to the commit and its message. It is a research tool, not a tool to blame people.

## Visual

```text
 git blame prices.txt
 4267004 (Ada Lovelace 2026-01-05 09:03) espresso 2.50      ← last changed in "Add prices"
 7f3a2c1 (Grace Hopper 2026-01-05 09:05) latte 3.30         ← last changed in "Raise the latte price"
 4267004 (Ada Lovelace 2026-01-05 09:03) cappuccino 3.40
           │
           └── git show 7f3a2c1   →  the commit message explains WHY
```

## Lab setup

<!-- test: contains=lesson-71 -->
```bash
bash scripts/new-lab.sh lesson-71 conflict
cd ~/git-practice/lesson-71
```

## Demonstration

<!-- test: contains=Grace Hopper; output -->
```bash
git blame prices.txt
```

```text
42670048 (Ada Lovelace 2026-01-05 09:03:00 +0000 1) espresso 2.50
594657b3 (Grace Hopper 2026-01-05 09:05:00 +0000 2) latte 3.30
42670048 (Ada Lovelace 2026-01-05 09:03:00 +0000 3) cappuccino 3.40
```

Only some lines? `-L`. Then read the commit:

<!-- test: contains=Raise the latte price to 3.30; output -->
```bash
git blame -L 2,2 prices.txt
git show --stat "$(git blame -L 2,2 --porcelain prices.txt | head -1 | cut -c1-7)" | head -6
```

```text
594657b3 (Grace Hopper 2026-01-05 09:05:00 +0000 2) latte 3.30
commit 594657b3b1f6fa082b531b3baebe668cffe1c98a (HEAD -> main)
Author: Grace Hopper <grace@example.com>
Date:   Mon Jan 5 09:05:00 2026 +0000

    Raise the latte price to 3.30
```

## Command breakdown

| Command | What it does |
|---|---|
| `git blame FILE` | last commit per line |
| `git blame -L 10,20 FILE` | only lines 10–20 |
| `git blame -w FILE` | ignore whitespace-only changes |
| `git blame --ignore-rev C FILE` | skip commit C (e.g. a reformatting) |
| `git config blame.ignoreRevsFile .git-blame-ignore-revs` | skip the commits listed in a file, always |
| `git log -L 2,2:prices.txt` | the full history of a line range |

## Hands-on exercise

**Instructions.** Show the complete history of the latte line, not only the last change.

**Expected result.** Two commits: "Raise the latte price to 3.30" and "Add prices".

**Verification.**

<!-- test: contains=Raise the latte price to 3.30; contains=Add prices -->
```bash
cd ~/git-practice/lesson-71
git log --oneline -L 2,2:prices.txt | grep -E "^[0-9a-f]{7} "
```

## Break it

A teammate aligns the price column for readability, touching every line:

<!-- test: contains=Align the prices; output -->
```bash
awk '{printf "%-12s %s\n", $1, $2}' prices.txt > p.tmp && mv p.tmp prices.txt
git commit -q -am "Align the prices"
git log --oneline -1
git blame prices.txt
```

```text
4a8b468 (HEAD -> main) Align the prices
4a8b4686 (Ada Lovelace 2026-10-05 03:49:42 +0200 1) espresso     2.50
4a8b4686 (Ada Lovelace 2026-10-05 03:49:42 +0200 2) latte        3.30
4a8b4686 (Ada Lovelace 2026-10-05 03:49:42 +0200 3) cappuccino   3.40
```

## Troubleshoot

Every line now points to "Align the prices": blame shows who touched the line last, even if the change was only
formatting. The real history of the latte price is hidden behind the reformatting commit.

## Fix

Tell blame to ignore that commit (and record it for everyone in `.git-blame-ignore-revs`):

<!-- test: contains=Raise the latte price to 3.30; output -->
```bash
git rev-parse HEAD > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
git blame prices.txt
git log --oneline -1 "$(git blame -L 2,2 --porcelain prices.txt | head -1 | cut -c1-40)"
```

```text
42670048 (Ada Lovelace 2026-01-05 09:03:00 +0000 1) espresso     2.50
594657b3 (Grace Hopper 2026-01-05 09:05:00 +0000 2) latte        3.30
42670048 (Ada Lovelace 2026-01-05 09:03:00 +0000 3) cappuccino   3.40
594657b Raise the latte price to 3.30
```

GitHub's blame view honours `.git-blame-ignore-revs` in the repository root too.

## Real-world example

Appropriate: "this timeout is 37 seconds, why?" → blame → commit "Raise the timeout: the payment provider takes up to
30 s at peak (#812)" → the PR discussion. Inappropriate: counting whose lines broke the build, or using blame in
performance reviews. Blame shows the last editor, not the author of the idea, nor whoever caused the bug.

## Practice challenge

Show only the authors' names and how many lines of `prices.txt` each last changed, ignoring the reformatting.

<details>
<summary>Solution</summary>

<!-- test: contains=Ada Lovelace; output -->
```bash
cd ~/git-practice/lesson-71
git blame --line-porcelain prices.txt | sed -n 's/^author //p' | sort | uniq -c
```

```text
      2 Ada Lovelace
      1 Grace Hopper
```

</details>

## Recap

- `git blame` = last commit per line; follow it to the commit message and PR for the "why".
- `-L` for a range, `git log -L` for a line's whole history.
- Ignore formatting commits with `--ignore-rev` / `.git-blame-ignore-revs`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-71
```

Next: [Lesson 72 · Git clean](../72-git-clean/README.md).
