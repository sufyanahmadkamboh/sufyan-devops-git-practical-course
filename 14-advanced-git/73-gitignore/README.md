# Lesson 73 · .gitignore

> Level 14 · Advanced Git · ⏱ 20 minutes

## What are we learning?

`.gitignore` lists files Git should not track: dependencies, build output, logs, local configuration and secrets. We
write patterns, test them with `git check-ignore`, and fix the classic problem: a file that is already tracked is not
affected by `.gitignore`.

## Visual

```text
 .gitignore                     matches
 node_modules/                  the folder node_modules anywhere (trailing / = only directories)
 .env                           .env in any folder
 *.log                          app.log, logs/error.log
 !keep.log                      exception: do track keep.log
 /build                         build at the repository root only

 untracked + matches .gitignore → ignored (not shown, not added by git add .)
 ALREADY TRACKED                → .gitignore has NO effect: git rm --cached first
```

## Lab setup

<!-- test: contains=lesson-73 -->
```bash
bash scripts/new-lab.sh lesson-73 basic
cd ~/git-practice/lesson-73
mkdir -p node_modules/left-pad logs
echo "module" > node_modules/left-pad/index.js
echo "error" > logs/error.log && echo "keep" > keep.log
echo "API_TOKEN=local-secret" > .env
git status --short
```

## Demonstration

<!-- test: absent=.env; contains=.gitignore; output -->
```bash
printf 'node_modules/\n.env\n*.log\n!keep.log\n' > .gitignore
git status --short
```

```text
?? .gitignore
?? keep.log
```

Only `.gitignore` and `keep.log` are left as untracked. Which rule matches what?

<!-- test: contains=.gitignore:3:*.log; output -->
```bash
git check-ignore -v logs/error.log .env node_modules/left-pad/index.js
git check-ignore -v keep.log || echo "keep.log is not ignored"
```

```text
.gitignore:3:*.log	logs/error.log
.gitignore:2:.env	.env
.gitignore:1:node_modules/	node_modules/left-pad/index.js
.gitignore:4:!keep.log	keep.log
```

<!-- test: contains=2 files changed -->
```bash
git add .
git commit -m "Add .gitignore and keep.log"
```

## Command breakdown

| Command / file | Use |
|---|---|
| `.gitignore` (any folder) | shared rules, committed |
| `.git/info/exclude` | personal rules for this clone, not committed |
| `git config --global core.excludesFile ~/.gitignore_global` | personal rules for every repository (`.DS_Store`, `.idea/`) |
| `git check-ignore -v PATH` | which file and line ignore PATH |
| `git status --ignored` | show ignored files too |
| `git rm --cached FILE` | stop tracking FILE, keep it on disk |

## Hands-on exercise

**Instructions.** Ignore your editor's folder `.vscode/` only for yourself (not in the shared `.gitignore`).

**Expected result.** `git check-ignore -v` points to `.git/info/exclude`.

<!-- test-run: cd ~/git-practice/lesson-73 && mkdir -p .vscode && echo "{}" > .vscode/settings.json && echo ".vscode/" >> .git/info/exclude -->

**Verification.**

<!-- test: contains=.git/info/exclude -->
```bash
cd ~/git-practice/lesson-73
git check-ignore -v .vscode/settings.json
```

## Break it

A config file was committed long ago; now someone adds it to `.gitignore`:

<!-- test: contains=M config.local; output -->
```bash
echo "debug=false" > config.local && git add config.local && git commit -q -m "Add config"
echo "config.local" >> .gitignore && git commit -q -am "Ignore config.local"
echo "debug=true" > config.local
git status --short
```

```text
 M config.local
```

## Troubleshoot

`M config.local`: still tracked, still showing changes. `.gitignore` only affects **untracked** files; Git keeps
tracking every file that is already in the index.

<!-- test: contains=config.local; output -->
```bash
git ls-files | grep config
```

```text
config.local
```

## Fix

Remove it from the index (not from disk), commit, and it becomes an ignored file:

<!-- test: contains=!! config.local; output -->
```bash
git rm -q --cached config.local
git commit -q -m "Stop tracking config.local"
git status --short --ignored | grep config
cat config.local
```

```text
!! config.local
debug=true
```

If the file contained **secrets**, this is not enough: they are still in the history (lesson 90), so rotate them.

## Real-world example

Start every repository with a `.gitignore` for its stack (GitHub's templates: `gh repo create --gitignore Go`, or
github.com/github/gitignore): `.terraform/`, `*.tfstate`, `node_modules/`, `__pycache__/`, `.env`, `*.pem`,
`kubeconfig`. Secrets in Git are one of the most common causes of breaches; `.gitignore` plus a pre-commit secret
scanner (lesson 89) prevents most of them.

## Practice challenge

Ignore everything in `logs/` except a `README.md` that explains the folder.

<details>
<summary>Solution</summary>

<!-- test: contains=logs/README.md; absent=error.log; output -->
```bash
cd ~/git-practice/lesson-73
echo "Application logs are written here." > logs/README.md
printf 'logs/*\n!logs/README.md\n' >> .gitignore
git add . && git commit -q -m "Keep logs/README.md"
git ls-files logs
```

```text
logs/README.md
```

`logs/*` (not `logs/`) ignores the contents but not the folder, so the `!` exception can work.

</details>

## Recap

- `.gitignore` patterns keep dependencies, build output, logs and secrets out of Git.
- `git check-ignore -v` explains which rule applies.
- Tracked files are not affected: `git rm --cached`, commit, and rotate any secret that was committed.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-73
```

Next: [Module 15 · Lesson 74 · How Git stores data](../../15-git-internals/74-how-git-stores-data/README.md).
