# Lesson 04 · First Git configuration

> Level 1 · Git fundamentals · ⏱ 20 minutes

## What are we learning?

How to tell Git who you are, and how Git combines settings from three levels: system, global and local.

## Visual

```text
 system   /etc/gitconfig (or the installer's)      every user on this machine
    ▼ overridden by
 global   ~/.gitconfig                              you, in every repository
    ▼ overridden by
 local    REPO/.git/config                          this repository only        ← the most specific wins
```

Your name and e-mail are written into **every commit** you make. They are not a login: GitHub matches the e-mail to an
account to show your avatar, nothing more.

## Lab setup

<!-- test: contains=lesson-04 -->
```bash
bash scripts/new-lab.sh lesson-04 empty
cd ~/git-practice/lesson-04
```

## Demonstration

Set your identity once, globally (use your own name and e-mail):

<!-- test: output -->
```bash
git config --global user.name "Ada Lovelace"
git config --global user.email "ada@example.com"
git config --global init.defaultBranch main
git config --global --list
```

```text
user.name=Ada Lovelace
user.email=ada@example.com
init.defaultbranch=main
```

`init.defaultBranch main` makes every new repository start with a branch called `main` (older Git versions defaulted
to `master`). Where does each setting come from?

<!-- test: contains=user.email; output -->
```bash
git config --list --show-origin --show-scope | grep -E 'user\.|init\.'
```

```text
global	file:~/.gitconfig	user.name=Ada Lovelace
global	file:~/.gitconfig	user.email=ada@example.com
global	file:~/.gitconfig	init.defaultbranch=main
local	file:.git/config	user.name=Ada Lovelace
local	file:.git/config	user.email=ada@example.com
```

(The `local` lines come from the lab script: it gave this repository an identity because none existed globally yet.)

Now a project that needs another identity, for example your work e-mail in a work repository. A local setting
overrides the global one, in this repository only:

<!-- test: contains=local	ada@work.example.com; output -->
```bash
git config user.email "ada@work.example.com"
git config --show-scope --get-all user.email
git config --show-scope --show-origin user.email
```

```text
global	ada@example.com
local	ada@work.example.com
local	file:.git/config	ada@work.example.com
```

The global value still exists; the local one wins. Commits in this repository will carry the work address.

## Command breakdown

| Command | What it does |
|---|---|
| `git config --global KEY VALUE` | set a value in `~/.gitconfig` |
| `git config KEY VALUE` | set it in the current repository (`.git/config`) |
| `git config --list --show-origin --show-scope` | every effective setting, with its file and level |
| `git config --get KEY` | the value that wins |
| `git config --unset KEY` | remove a setting from one level |

## Hands-on exercise

**Instructions.** In the lab repository, remove the local e-mail so the global one applies again.

**Expected result.** `git config user.email` prints `ada@example.com`, with scope `global`.

<!-- test-run: cd ~/git-practice/lesson-04 && git config --unset user.email && git config --unset user.name || true -->

**Verification.**

<!-- test: contains=global	ada@example.com -->
```bash
cd ~/git-practice/lesson-04
git config --show-scope --get user.email
```

## Break it

A fresh machine (or a new CI runner) with no identity at all. Simulate it by hiding the global file for one command:

<!-- test: fail; contains=Please tell me who you are; output=head:6 -->
```bash
cd ~/git-practice/lesson-04
echo "test" > note.txt && git add note.txt
GIT_CONFIG_GLOBAL=/dev/null git -c user.useConfigOnly=true commit -m "First note" 2>&1
```

```text
Author identity unknown

*** Please tell me who you are.

Run

...
```

## Troubleshoot

`Please tell me who you are` / `Author identity unknown`: no `user.name` or `user.email` at any level. Check what Git
can see:

<!-- test: contains=no identity -->
```bash
GIT_CONFIG_GLOBAL=/dev/null git config --show-origin --get user.email || echo "no identity at any level"
```

## Fix

Configure the identity (globally on your own machine; in CI, set it in the job). Then the commit works:

<!-- test: contains=First note; output -->
```bash
git config --global user.email >/dev/null && git commit -q -m "First note" && git log --format='%h %an <%ae> %s'
```

```text
134e755 Ada Lovelace <ada@example.com> First note
```

## Real-world example

A pipeline that commits (a version bump, a generated changelog) fails with "Please tell me who you are" because the
runner has no Git identity. The fix is two lines in the job:
`git config user.name "release-bot"` and `git config user.email "release-bot@example.com"`.
And when you work for two organisations, a local `user.email` per repository (or an `includeIf` rule in
`~/.gitconfig` per folder) keeps the right address on the right commits.

## Practice challenge

Make every repository under `~/git-practice/work/` use the e-mail `ada@work.example.com` automatically, without setting
it in each repository. (Hint: `includeIf "gitdir:..."` in `~/.gitconfig`.)

<details>
<summary>Solution</summary>

<!-- test: contains=ada@work.example.com; output -->
```bash
printf '[user]\n\temail = ada@work.example.com\n' > ~/.gitconfig-work
git config --global includeIf."gitdir:~/git-practice/work/".path '~/.gitconfig-work'
mkdir -p ~/git-practice/work/project && cd ~/git-practice/work/project && git init -q
git config --show-origin --get user.email
```

```text
file:~/.gitconfig-work	ada@work.example.com
```

The conditional include applies the extra file only to repositories inside that folder. Quote `'~/...'` so that
Git, not your shell, expands the `~`: that works the same on every system.

</details>

## Recap

- `user.name` and `user.email` go into every commit; set them before your first commit.
- Three levels: system < global < local. The most specific wins; `--show-origin --show-scope` tells you which.
- `init.defaultBranch main` names the first branch of new repositories.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-04 ~/git-practice/work ~/.gitconfig-work
git config --global --unset-all includeIf.gitdir:~/git-practice/work/.path || true
```

Your global identity stays: every later lesson uses it.

Next: [Module 02 · Lesson 05 · What is a Git repository?](../../02-repositories/05-what-is-a-repository/README.md).
