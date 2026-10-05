# Lesson 02 · Git vs GitHub

> Level 1 · Git fundamentals · ⏱ 15 minutes

## What are we learning?

The difference between **Git** (a program on your computer) and **GitHub** (a website that hosts Git repositories and
adds collaboration). We prove that Git works with no GitHub at all, then talk to GitHub with plain Git.

## Visual

```text
Git                                          GitHub
↓                                            ↓
a version control SYSTEM                     a HOSTING + COLLABORATION platform
runs on your computer                        a website and a service
works offline, needs no account              stores Git repositories for you and your team
commits, branches, history, merges           + pull requests, reviews, issues, Actions, releases, permissions

        your computer                                    github.com
 ┌─────────────────────────┐   git push / fetch   ┌──────────────────────────┐
 │ repository (.git)        │ ◄──────────────────► │ the same repository      │
 │ all history, all commits │                      │ + PRs, issues, Actions   │
 └─────────────────────────┘                      └──────────────────────────┘
```

GitHub is one host among several (GitLab, Bitbucket, Gitea, Azure Repos, a plain server with SSH). They all store the
same kind of repository; Git is what you use with all of them.

## Lab setup

<!-- test: contains=lesson-02 -->
```bash
bash scripts/new-lab.sh lesson-02 basic
cd ~/git-practice/lesson-02
```

## Demonstration

A complete repository with history, on this computer only. Is there any server?

<!-- test: output -->
```bash
git log --oneline
git remote -v
echo "remotes: $(git remote | wc -l)"
```

```text
4267004 (HEAD -> main) Add prices
fc345e6 Add the menu
d6df412 Add README
remotes: 0
```

Three commits and **zero remotes**: no GitHub, no network, no account. Everything (history, branches, diffs) lives in
the `.git` folder of this directory.

Git can even "host" a repository for others without any website: a *bare* repository is a repository without a working
folder, the same thing GitHub keeps on its servers.

<!-- test: contains=main -> main; output -->
```bash
git init -q --bare -b main ~/git-practice/lesson-02-server/cafe.git
git remote add origin ~/git-practice/lesson-02-server/cafe.git
git push origin main 2>&1
```

```text
To ~/git-practice/lesson-02-server/cafe.git
 * [new branch]      main -> main
```

That push used Git alone, to a folder. GitHub does the same over the network, then adds a website around it. Plain Git
can read from GitHub too, no account needed for a public repository:

<!-- test: timeout=60; contains=refs/heads; output -->
```bash
git ls-remote --heads https://github.com/git/git | head -3
```

```text
165e5ad3169d0fd26637da3383a4514f1a9d1e72	refs/heads/bisect
78cbef44230fd357b15a71b4a6eab4232267bac5	refs/heads/jch
a018953688f1b10bddf91bff8747068f5f4746a4	refs/heads/maint
```

`git ls-remote` asked GitHub which branches the Git project's own repository has: the Git source code is itself in a
Git repository, mirrored on GitHub.

## Command breakdown

| Command | What it does here |
|---|---|
| `git remote -v` | list the remote repositories this one knows (none at first) |
| `git init --bare` | create a repository without a working folder: what a server stores |
| `git remote add origin PATH` | register a remote named `origin` (a path, or an `https://`/`git@` URL) |
| `git push origin main` | send the `main` branch's commits to the remote |
| `git ls-remote --heads URL` | ask a remote which branches it has, without cloning |

## Hands-on exercise

**Instructions.** Make a new commit in `~/git-practice/lesson-02` (any change), then push it to the bare repository.

**Expected result.** The bare "server" has the same latest commit as your local `main`.

<!-- test-run: cd ~/git-practice/lesson-02 && printf 'Open daily.\n' >> README.md && git commit -qam "Add opening note" && git push -q origin main -->

**Verification.**

<!-- test: contains=Add opening note -->
```bash
cd ~/git-practice/lesson-02
git log --oneline -1
git --git-dir ~/git-practice/lesson-02-server/cafe.git log --oneline -1
```

## Break it

Push to a remote that does not exist (a typo in the path, a repository that was never created):

<!-- test: fail; contains=does not appear to be a git repository; output -->
```bash
cd ~/git-practice/lesson-02
git remote add backup ~/git-practice/no-such-server/cafe.git
git push backup main 2>&1
```

```text
fatal: '~/git-practice/no-such-server/cafe.git' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

## Troubleshoot

The error names the remote it tried and says it is not a repository. Check what the remote points to:

<!-- test: contains=no-such-server -->
```bash
git remote -v
```

## Fix

Point the remote at a real repository (here: create it), or remove the wrong remote:

<!-- test: contains=main -> main -->
```bash
git remote remove backup
git remote -v
git push origin main 2>&1 | tail -1 || true
git init -q --bare -b main ~/git-practice/lesson-02-backup.git
git remote add backup ~/git-practice/lesson-02-backup.git
git push backup main 2>&1
```

## Real-world example

Teams often use more than one host: GitHub for collaboration, an internal mirror for build systems, an archive for
compliance. It is all the same Git repository with several remotes. And when GitHub has an outage, everyone can keep
committing locally: Git does not need it to work.

## Practice challenge

Without cloning it, find out which branch the public repository `https://github.com/git/git` uses as its default
(`HEAD`).

<details>
<summary>Solution</summary>

<!-- test: timeout=60; contains=ref: refs/heads/; output -->
```bash
git ls-remote --symref https://github.com/git/git HEAD
```

```text
ref: refs/heads/master	HEAD
8103b446517e0c44e67561b9d0ccce56efa60a71	HEAD
```

`--symref` shows what the remote's `HEAD` points to: its default branch.

</details>

## Recap

- **Git** is the version control program; it works on your computer, offline, with no account.
- **GitHub** hosts Git repositories and adds collaboration: pull requests, reviews, issues, Actions, releases.
- A remote is just "another copy of this repository somewhere": a folder, a server, or GitHub.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-02 ~/git-practice/lesson-02-server ~/git-practice/lesson-02-backup.git
```

Next: [Lesson 03 · Installing Git](../03-installing-git/README.md).
