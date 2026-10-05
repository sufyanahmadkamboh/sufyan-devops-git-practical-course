# Lesson 03 · Installing Git

> Level 1 · Git fundamentals · ⏱ 15 minutes

## What are we learning?

How to install Git on Linux, macOS and Windows, check which Git you are running, and where it keeps its own files.

## Visual

```text
 you ──► git (the CLI) ──► reads config:  system  →  global (~/.gitconfig)  →  local (.git/config)
                      └──► runs helpers: git-<command> programs in its "exec path"
                      └──► works on:     the repository you are in (.git)
```

## Lab setup

Install Git with your system's package manager or the official installer (from [git-scm.com](https://git-scm.com/downloads)):

<!-- test: skip -->
```bash
# Debian / Ubuntu (for the newest release, first: sudo add-apt-repository ppa:git-core/ppa)
sudo apt-get update && sudo apt-get install -y git

# Fedora / RHEL
sudo dnf install -y git

# macOS (Homebrew; or run "git --version" once and accept the Xcode command line tools)
brew install git

# Windows (winget; or the installer from git-scm.com, which also gives you Git Bash)
winget install --id Git.Git -e
```

This course was tested with Git 2.54 on Windows (Git Bash) and the current Git on Ubuntu 24.04. Anything from Git
2.40 on works; commands such as `git switch` and `git restore` need at least 2.23.

## Demonstration

<!-- test: contains=git version; output -->
```bash
git --version
```

```text
git version 2.54.0.windows.1
```

Which `git` runs, and where are its helper programs?

<!-- test: contains=git; output=head:4 -->
```bash
command -v git
git --exec-path
ls "$(git --exec-path)" | head -5
```

```text
/mingw64/bin/git
C:/Program Files/Git/mingw64/libexec/git-core
Atlassian.Bitbucket.dll
Avalonia.Base.dll
...
```

Each `git <command>` is a built-in or a program called `git-<command>` in the exec path. That is also how extensions
work: install a program named `git-lfs` and `git lfs` becomes a command (lesson 88).

Built-in help works offline:

<!-- test: contains=usage: git commit; output=head:4 -->
```bash
git commit -h 2>&1 | head -4
```

```text
usage: git commit [-a | --interactive | --patch] [-s] [-v] [-u[<mode>]] [--amend]
                  [--dry-run] [(-c | -C | --squash) <commit> | --fixup [(amend|reword):]<commit>]
                  [-F <file> | -m <msg>] [--reset-author] [--allow-empty]
                  [--allow-empty-message] [--no-verify] [-e] [--author=<author>]
```

## Command breakdown

| Command | What it does |
|---|---|
| `git --version` | the installed version |
| `command -v git` | which `git` program runs (the first one on your `PATH`) |
| `git --exec-path` | the folder with Git's helper programs |
| `git <command> -h` | short usage; `git help <command>` opens the full manual |

## Hands-on exercise

**Instructions.** Find out where your Git installation keeps its *system-wide* configuration file.

**Expected result.** A file path (for example `/etc/gitconfig` on Linux), or an empty answer if Git was built without
one.

**Verification.**

<!-- test -->
```bash
git config --system --list --show-origin 2>/dev/null | head -3 || true
git version --build-options | head -3
```

## Break it

Call a Git command that does not exist, the classic typo:

<!-- test: fail; contains=is not a git command; output -->
```bash
git comit -m "test" 2>&1
```

```text
git: 'comit' is not a git command. See 'git --help'.

The most similar command is
	commit
```

## Troubleshoot

Git says it is not a command and usually suggests the closest real one. The same message appears for commands that
come from an extension you have not installed (`git lfs` without Git LFS, `git filter-repo` without filter-repo).

## Fix

Use the right name. To catch typos automatically, Git can run the closest match after a short delay:

<!-- test: contains=autocorrect -->
```bash
git config --global help.autocorrect prompt
git config --global --get-regexp '^help\.'
```

`prompt` asks before running the guess. Many people prefer leaving this off: a typo should fail loudly.

## Real-world example

CI runners, containers and servers all need Git too. In a Dockerfile it is `RUN apt-get install -y git`; on GitHub
Actions runners Git is preinstalled. When a pipeline behaves differently from your laptop, `git --version` in both is
one of the first checks.

## Practice challenge

Without opening a browser or the internet, find in Git's built-in help the `git commit` option that **changes the
last commit** instead of creating a new one, and the one that **stages all modified files** automatically.

<details>
<summary>Solution</summary>

<!-- test: contains=--amend; output -->
```bash
git commit -h 2>&1 | grep -E -- '--amend|-a, --all'
```

```text
usage: git commit [-a | --interactive | --patch] [-s] [-v] [-u[<mode>]] [--amend]
    --[no-]reset-author   the commit is authored by me now (used with -C/-c/--amend)
```

`-h` prints the short usage of any command in the terminal; `git help commit` opens the full manual.

</details>

## Recap

- Install Git with your package manager or the official installer; check with `git --version`.
- `git <command>` maps to built-ins and `git-<command>` programs: that is how extensions plug in.
- Typos produce "is not a git command"; `-h` and `git help` are always available offline.

## Cleanup

<!-- test -->
```bash
git config --global --unset help.autocorrect || true
```

Next: [Lesson 04 · First Git configuration](../04-first-configuration/README.md).
