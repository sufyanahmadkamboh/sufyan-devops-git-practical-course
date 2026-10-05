# Problem 18 · Production branch contains an unwanted commit

> Troubleshooting lab · run every command from the course folder · related lessons: [32](../07-undoing/32-git-revert/README.md), [58](../12-collaboration/58-git-flow/README.md), [67](../14-advanced-git/67-cherry-pick/README.md)

## Problem

The team deploys from a `production` branch. A commit meant for the **next** release (a new price list) was
cherry-picked into `production` by mistake, pushed, and deployed. It must leave production now, and stay on `main` for
the next release.

<!-- test: contains=lesson-t18 -->
```bash
bash scripts/new-lab.sh lesson-t18 remote
cd ~/git-practice/lesson-t18/ada
git switch -q -c production
echo "environment=production" > deploy.conf && git add deploy.conf && git commit -q -m "Add production deploy settings"
git push -q -u origin production
git switch -q main
echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q
sed -i 's/espresso 2.50/espresso 2.70/; s/cappuccino 3.40/cappuccino 3.60/' prices.txt && git commit -q -am "New price list for March" && git push -q
git switch -q production
git cherry-pick "$(git log --format=%h -1 --grep='green tea' main)" "$(git log --format=%h -1 --grep='March' main)" > /dev/null
git push -q
```

## Symptoms

Production charges the March prices too early:

<!-- test: contains=espresso 2.70; output -->
```bash
git show origin/production:prices.txt | head -1
```

```text
espresso 2.70
```

## Investigation

What is on `production` that should not be? Compare it with the last release and with `main`:

<!-- test: contains=New price list for March; output -->
```bash
git log --oneline origin/main..origin/production
git log --oneline 4267004..origin/production
git cherry -v origin/main origin/production
```

```text
9c933af (HEAD -> production, origin/production) New price list for March
333b168 Add green tea
4e6f254 Add production deploy settings
9c933af (HEAD -> production, origin/production) New price list for March
333b168 Add green tea
4e6f254 Add production deploy settings
+ 4e6f25443bb8262920d9219dcff1a485273caace Add production deploy settings
- 333b1682beb0428a26652086b36dbeacd305aec7 Add green tea
- 9c933af2fa0c098a1f4f0ec9e863589989a472b1 New price list for March
```

## Commands

| Command | Shows |
|---|---|
| `git log A..B` | commits on B that are not on A |
| `git cherry -v main production` | production commits with an equivalent on main (`-`) or not (`+`) |
| `git log --oneline 4267004..production` | everything production received since the last release |

## Understand the output

`production` has its own deploy settings plus two cherry-picked commits: "Add green tea" (wanted) and "New price
list for March" (not wanted). `git cherry` marks the two copies with `-` (an equivalent patch exists on `main`) and the
deploy settings with `+` (only on production). The copies have different IDs from the `main` originals, so
`main..production` lists them too.

## Root cause

Too much was cherry-picked into the production branch, and nothing (review, protection) checked it before the push.

## Fix

Production is shared and deployed: **revert** the unwanted commit on `production` (never reset a deployed branch),
push, and redeploy. `main` is not touched, so the price list still ships in March:

<!-- test: contains=Revert "New price list for March"; output -->
```bash
git revert --no-edit "$(git log --format=%h -1 --grep='March' production)" 2>&1 | head -1
git push -q
git log --oneline -3 production
```

```text
[production c8831c5] Revert "New price list for March"
c8831c5 (HEAD -> production, origin/production) Revert "New price list for March"
9c933af New price list for March
333b168 Add green tea
```

## Verification

<!-- test: contains=espresso 2.50; contains=espresso 2.70; output -->
```bash
echo "production: $(git show origin/production:prices.txt | head -1)"
echo "main:       $(git show origin/main:prices.txt | head -1)"
git show origin/production:menu.txt | tail -1
```

```text
production: espresso 2.50
main:       espresso 2.70
green tea
```

Production is back to the current prices but keeps green tea; `main` still has the March price list.

## Prevention

- Protect `production` (and release branches): changes only via reviewed PRs, and tag every deployment.
- Release from tags (Module 21): a deployment is "tag vX.Y.Z", and rolling back is redeploying the previous tag.
- Record backports with `git cherry-pick -x` so every production commit points to its origin.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t18
```

Back to the [troubleshooting index](README.md).
