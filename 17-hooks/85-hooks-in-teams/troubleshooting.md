<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 85 · Git hooks in teams · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace pulls the hooks, but her commits are not checked:

```bash
cd ~/git-practice/lesson-85/grace && git pull -q
ls .githooks
echo "mocha" >> menu.txt && git commit -q -am "whatever" && git log --oneline -1
```

```text
commit-msg
739ddf2 (HEAD -> main) whatever
```

## Troubleshoot

The hook files arrived with `git pull`, but Git does not run them: `core.hooksPath` is configuration of Ada's clone, not
part of the repository. Git never enables hooks automatically after a clone or pull (that would let any repository
run code on your machine).

```bash
git config core.hooksPath || echo "core.hooksPath not set in Grace's clone"
```

```text
core.hooksPath not set in Grace's clone
```

## Fix

Grace enables the hooks (in real projects: a documented one-time setup step), then fixes her message before pushing:

```bash
git config core.hooksPath .githooks
git commit -q --amend -m "feat: add mocha"
git log --oneline -1
```

```text
891bba6 (HEAD -> main) feat: add mocha
```

And the check that cannot be skipped runs on the server side, for every pushed commit, for example in CI:

```bash
git log --format=%s origin/main..HEAD | grep -Ev '^(Merge|(feat|fix|docs|chore|refactor|test|ci)(\(.+\))?!?: )' && exit 1 || echo "all commit messages follow the convention"
```

```text
all commit messages follow the convention
```
