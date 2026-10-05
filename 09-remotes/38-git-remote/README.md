# Lesson 38 · git remote

> Level 8 · Remote repositories · ⏱ 15 minutes

## What are we learning?

Managing remotes: add, rename, change the URL, remove. And working with two remotes, the common `origin` + `upstream`
setup of a fork.

## Visual

```text
   upstream  (the original project, read-only for you)
       │ fetch
       ▼
   your clone ──push──► origin  (your fork, or the team repository)

   git remote add NAME URL      git remote rename OLD NEW
   git remote set-url NAME URL  git remote remove NAME
```

## Lab setup

<!-- test: contains=lesson-38 -->
```bash
bash scripts/new-lab.sh lesson-38 remote
cd ~/git-practice/lesson-38
git clone -q --bare server/cafe.git upstream.git
cd ada
```

`upstream.git` plays the original project; `server/cafe.git` is Ada's fork (`origin`).

## Demonstration

Add the second remote and fetch from it:

<!-- test: contains=upstream; output -->
```bash
git remote add upstream ../upstream.git
git remote -v
git fetch -q upstream
git branch -r
```

```text
origin	~/git-practice/lesson-38/server/cafe.git (fetch)
origin	~/git-practice/lesson-38/server/cafe.git (push)
upstream	../upstream.git (fetch)
upstream	../upstream.git (push)
  origin/HEAD -> origin/main
  origin/main
  upstream/HEAD -> upstream/main
  upstream/main
```

The server moved to a new address (the team renamed the repository). Update the URL instead of re-cloning:

<!-- test: contains=cafe-shop.git; output -->
```bash
mv ../server/cafe.git ../server/cafe-shop.git
git remote set-url origin ../server/cafe-shop.git
git remote -v | grep origin
git fetch origin && echo "fetch ok"
```

```text
origin	../server/cafe-shop.git (fetch)
origin	../server/cafe-shop.git (push)
fetch ok
```

## Command breakdown

| Command | What it does |
|---|---|
| `git remote add NAME URL` | add a remote |
| `git remote set-url NAME URL` | change its address (e.g. HTTPS → SSH, lesson 49) |
| `git remote rename OLD NEW` | rename it (remote-tracking branches follow) |
| `git remote remove NAME` | remove it and its remote-tracking branches |
| `git remote get-url NAME` | print the URL |

## Hands-on exercise

**Instructions.** Rename `upstream` to `original`, then check the remote-tracking branches.

**Expected result.** `original/main` instead of `upstream/main`.

<!-- test-run: cd ~/git-practice/lesson-38/ada && git remote rename upstream original -->

**Verification.**

<!-- test: contains=original/main; absent=upstream -->
```bash
cd ~/git-practice/lesson-38/ada
git branch -r
```

## Break it

Add `origin` again, as you would after copying a "connect this repository" snippet from GitHub:

<!-- test: fail; contains=remote origin already exists; output -->
```bash
git remote add origin ../server/cafe-shop.git 2>&1
```

```text
error: remote origin already exists.
```

## Troubleshoot

`error: remote origin already exists.`: a clone already has `origin`. The snippet assumes a fresh `git init`. Check what
`origin` currently is before deciding:

<!-- test: contains=cafe-shop.git -->
```bash
git remote get-url origin
```

## Fix

If the URL is what you wanted, there is nothing to do. If not, change it (`set-url`), never add a second `origin`:

<!-- test: contains=cafe-shop.git -->
```bash
git remote set-url origin ../server/cafe-shop.git
git remote -v
```

## Real-world example

Moving from HTTPS to SSH (lesson 49), or after a GitHub repository is renamed or transferred to another organisation:
`git remote set-url origin git@github.com:org/new-name.git`. GitHub redirects old URLs for a while, but updating the
remote avoids surprises when the redirect stops.

## Practice challenge

Remove the `original` remote and prove its remote-tracking branches are gone too.

<details>
<summary>Solution</summary>

<!-- test: absent=original; output -->
```bash
cd ~/git-practice/lesson-38/ada
git remote remove original
git remote
git branch -r
```

```text
origin
  origin/HEAD -> origin/main
  origin/main
```

</details>

## Recap

- `git remote add / set-url / rename / remove` manage the list of remotes.
- One `origin`; change its URL instead of adding it again.
- Forks usually have `origin` (your fork) and `upstream` (the original).

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-38
```

Next: [Lesson 39 · git clone](../39-git-clone/README.md).
