<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 96 · Projects · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Use the project commands with a token that was created without the `project` scope (the default for `gh auth login`):

```bash
gh project list --owner "$(gh api user --jq .login)" 2>&1
```

```text
error: your authentication token is missing required scopes [read:project]
To request it, run:  gh auth refresh -s read:project
```

## Troubleshoot

`your authentication token is missing required scopes [read:project]`: OAuth tokens carry **scopes**, the list of
things they may do (lesson 48). `repo` covers code, issues and PRs, but Projects are a separate permission, so the same
token that pushes and opens issues cannot read projects. GitHub tells you exactly which scope is missing.

## Fix

Grant the scope (opens the browser to confirm), then retry:

```bash
gh auth refresh -h github.com -s project
gh project list --owner "$(gh api user --jq .login)"
```

Grant only what you need: `read:project` to read boards, `project` to change them.
