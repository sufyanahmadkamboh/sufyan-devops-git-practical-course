# Lesson 96 · Projects

> Level 20 · GitHub advanced · ⏱ 20 minutes

## What are we learning?

GitHub Projects are planning boards and tables built on top of issues and pull requests, across one or many
repositories: columns such as Todo / In progress / Done, custom fields (priority, estimate, iteration), and views. They
do not change Git at all; they organise the work around it.

## Visual

```text
 Project "Cafe roadmap" (owned by you or an organisation, can span repositories)
 ┌──────────── Todo ────────────┬──────── In progress ────────┬─────────── Done ───────────┐
 │ #42 Update the menu board    │ #45 Seasonal drinks         │ #40 Add chai               │
 │     priority: high · v1.1.0  │     @ada                    │ #41 Price chai             │
 └──────────────────────────────┴─────────────────────────────┴────────────────────────────┘
 items = issues / PRs (or draft notes) · Status, Priority … = project fields · board / table / roadmap = views
```

## Lab setup

<!-- test: github; contains=lesson-96 -->
```bash
bash scripts/new-lab.sh lesson-96 github
cd ~/git-practice/lesson-96
```

Projects need an extra permission for the CLI's token: the `project` scope. Check the current scopes:

<!-- test: github; contains=scopes; output -->
```bash
gh auth status --active 2>&1 | grep -i scopes
```

```text
  - Token scopes: 'gist', 'read:org', 'repo', 'user', 'workflow'
```

## Demonstration

With the `project` scope (see "Fix" below), create a project, add an issue, and move it across the board:

<!-- test: skip -->
```bash
me=$(gh api user --jq .login)
number=$(gh project create --owner "$me" --title "Cafe roadmap" --format json --jq .number)
issue_url=$(gh issue create --title "Update the menu board" --body "New board for v1.1.0." )
gh project item-add "$number" --owner "$me" --url "$issue_url"
gh project item-list "$number" --owner "$me" --format json --jq '.items[] | "\(.content.title): \(.status)"'
```

On the web: your profile or organisation → Projects → New project → Board; then "Add item" and drag cards between
columns. Built-in workflows can set **Status = Done** automatically when an issue is closed or a PR merged.

## Command breakdown

| Command | What it does |
|---|---|
| `gh auth refresh -s project` | give the CLI token access to Projects (browser confirmation) |
| `gh project create --owner OWNER --title T` | create a project |
| `gh project list --owner OWNER` | list projects |
| `gh project item-add N --owner OWNER --url ISSUE_URL` | add an issue/PR |
| `gh project item-list N --owner OWNER` | items with their fields |
| `gh project field-list N --owner OWNER` | fields (Status, custom ones) |
| `gh project link N --owner OWNER --repo REPO` | show the project in a repository's Projects tab |

## Hands-on exercise

**Instructions.** In the web interface, create a board project "Cafe roadmap", link it to `git-practice-cafe`, add the
open issues from lesson 95, and set one to **In progress**.

**Expected result.** The repository's **Projects** tab lists "Cafe roadmap".

**Verification** (needs the `project` scope):

<!-- test: skip -->
```bash
me=$(gh api user --jq .login)
gh project list --owner "$me" --format json --jq '.projects[].title'
```

## Break it

Use the project commands with a token that was created without the `project` scope (the default for `gh auth login`):

<!-- test: github; fail; contains=missing required scopes; output -->
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

<!-- test: skip -->
```bash
gh auth refresh -h github.com -s project
gh project list --owner "$(gh api user --jq .login)"
```

Grant only what you need: `read:project` to read boards, `project` to change them.

## Real-world example

A platform team keeps one organisation project across its Terraform, Helm-charts and CI-templates repositories: every
issue and PR in those repositories is added automatically (a project workflow), the board's columns follow the PR
state, and an "Iteration" field drives two-week planning. Engineers keep working in Git and PRs; the board updates
itself from what happens there.

## Practice challenge

Without the `project` scope, find out from the API which scopes your current token has.

<details>
<summary>Solution</summary>

<!-- test: github; contains=repo; output -->
```bash
gh api -i user 2>/dev/null | grep -i "^x-oauth-scopes"
```

```text
X-Oauth-Scopes: gist, read:org, repo, user, workflow
```

The `X-OAuth-Scopes` response header lists them; `X-Accepted-OAuth-Scopes` says what an endpoint requires.

</details>

## Recap

- Projects organise issues and PRs into boards, tables and roadmaps, across repositories.
- The CLI needs the `project` (or `read:project`) scope: `gh auth refresh -s project`.
- Project workflows keep the board in sync with issue and PR states automatically.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-96
```

Next: [Lesson 97 · Releases](../97-releases/README.md).
