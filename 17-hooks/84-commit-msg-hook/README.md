# Lesson 84 · Commit message hook

> Level 17 · Git hooks · ⏱ 20 minutes

## What are we learning?

The `commit-msg` hook receives the path of the file holding the commit message and can reject it. We enforce the
**Conventional Commits** format (`feat: …`, `fix(scope): …`), which tools use to generate changelogs and version
numbers.

## Visual

```text
 git commit -m "fixed stuff"
    │
    ▼
 .git/hooks/commit-msg  $1 = .git/COMMIT_EDITMSG  (the message)
    │   first line must match:  type(optional-scope): description   (≤ 72 characters)
    │   types: feat fix docs chore refactor test ci build perf
    ├── no match → exit 1 → commit aborted, message explained
    └── match    → exit 0 → commit created
```

## Lab setup

<!-- test: contains=lesson-84 -->
```bash
bash scripts/new-lab.sh lesson-84 basic
cd ~/git-practice/lesson-84
```

## Demonstration

<!-- test: contains=commit-msg -->
```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/usr/bin/env bash
# commit-msg: require Conventional Commits, e.g. "feat(menu): add green tea"
subject=$(head -n 1 "$1")
case "$subject" in Merge*|Revert*|fixup!*|squash!*) exit 0 ;; esac
pattern='^(feat|fix|docs|chore|refactor|test|ci|build|perf)(\([a-z0-9-]+\))?!?: .{1,72}$'
if ! echo "$subject" | grep -Eq "$pattern"; then
  echo "commit-msg: \"$subject\" does not follow Conventional Commits"
  echo "  expected: type(scope): description   e.g. feat(menu): add green tea"
  exit 1
fi
EOF
chmod +x .git/hooks/commit-msg
ls .git/hooks | grep -v sample
```

A valid message:

<!-- test: contains=feat(menu): add green tea -->
```bash
echo "green tea" >> menu.txt && git commit -q -am "feat(menu): add green tea"
git log --oneline -1
```

## Command breakdown

| Type | For |
|---|---|
| `feat` | a new feature (minor version in semantic-release) |
| `fix` | a bug fix (patch version) |
| `feat!` / `BREAKING CHANGE:` footer | an incompatible change (major version) |
| `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf` | no release by themselves |
| `git commit --no-verify` | skips `commit-msg` too |

## Hands-on exercise

**Instructions.** Commit a price change as a fix with the scope `prices`.

**Expected result.** `fix(prices): …` accepted.

<!-- test-run: cd ~/git-practice/lesson-84 && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "fix(prices): correct the latte price" -->

**Verification.**

<!-- test: contains=fix(prices) -->
```bash
cd ~/git-practice/lesson-84
git log --oneline -1
```

## Break it

<!-- test: fail; contains=does not follow Conventional Commits; output -->
```bash
echo "mocha" >> menu.txt
git commit -am "fixed stuff" 2>&1
```

```text
commit-msg: "fixed stuff" does not follow Conventional Commits
  expected: type(scope): description   e.g. feat(menu): add green tea
```

## Troubleshoot

The hook printed why: no type prefix. The commit was not created and nothing is lost: the change is still staged and
modified, ready for a second try.

<!-- test: contains=M menu.txt; output -->
```bash
git status --short
```

```text
 M menu.txt
```

## Fix

<!-- test: contains=feat(menu): add mocha -->
```bash
git commit -q -am "feat(menu): add mocha"
git log --oneline -1
```

## Real-world example

With Conventional Commits enforced (locally by a hook, centrally by a CI check such as `commitlint` on every PR, or by
requiring squash merges with a conventional PR title), tools like `release-please` or `semantic-release` read the
history since the last tag and decide the next version: any `feat` → minor, only `fix` → patch, `!` → major, and write
the changelog.

## Practice challenge

List the commits since `4267004` grouped by type, as a changelog generator would.

<details>
<summary>Solution</summary>

<!-- test: contains=feat; output -->
```bash
cd ~/git-practice/lesson-84
git log --format=%s 4267004..HEAD | sed -E 's/^([a-z]+).*/\1/' | sort | uniq -c
```

```text
      2 feat
      1 fix
```

</details>

## Recap

- `commit-msg` gets the message file as `$1`; exit 1 rejects the commit.
- Conventional Commits: `type(scope): description`, machine-readable history.
- Enforce it in CI as well; hooks can be skipped.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-84
```

Next: [Lesson 85 · Git hooks in teams](../85-hooks-in-teams/README.md).
