<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 47 · GitHub repository structure · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Use `gh` outside a repository folder:

```bash
cd ~/git-practice/lesson-47
gh issue list 2>&1
```

```text
no git remotes found
```

## Troubleshoot

`no git remotes found`: `gh` picks the repository from the current folder's Git remotes. The lab folder is a Git
repository, but without a GitHub remote, so `gh` cannot know which repository you mean. (Outside any repository the
message is `not a git repository`.)

## Fix

Name it explicitly with `-R OWNER/REPO`, or `cd` into the clone:

```bash
me=$(gh api user --jq .login)
gh issue list -R "$me/git-practice-cafe" > /dev/null && echo OK
```
