<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 03 · Installing Git · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

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

## Demonstration

```bash
git --version
```

```bash
command -v git
git --exec-path
ls "$(git --exec-path)" | head -5
```

```bash
git commit -h 2>&1 | head -4
```

## Hands-on exercise

```bash
git config --system --list --show-origin 2>/dev/null | head -3 || true
git version --build-options | head -3
```

## Break it

```bash
git comit -m "test" 2>&1
```

## Fix

```bash
git config --global help.autocorrect prompt
git config --global --get-regexp '^help\.'
```

## Practice challenge

```bash
git commit -h 2>&1 | grep -E -- '--amend|-a, --all'
```

## Cleanup

```bash
git config --global --unset help.autocorrect || true
```
