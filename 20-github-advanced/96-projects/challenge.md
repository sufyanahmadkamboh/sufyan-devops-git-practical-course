<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 96 · Projects · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without the `project` scope, find out from the API which scopes your current token has.

<details>
<summary>Solution</summary>

```bash
gh api -i user 2>/dev/null | grep -i "^x-oauth-scopes"
```

```text
X-Oauth-Scopes: gist, read:org, repo, user, workflow
```

The `X-OAuth-Scopes` response header lists them; `X-Accepted-OAuth-Scopes` says what an endpoint requires.

</details>
