# Module 22 · Real-world troubleshooting

> Level 22 · 18 hands-on problems · ⏱ 15–20 minutes each · run every command from the course folder

Each problem creates a broken situation on purpose and walks through it the way an experienced engineer would:

```text
Problem → Symptoms → Investigation → Commands → Understand the output → Root cause → Fix → Verification → Prevention
```

Do them in any order. Each one creates its own lab in `~/git-practice/lesson-tNN` and removes it at the end.

| # | Problem | Typical message | Related lessons |
|---|---|---|---|
| 1 | [Committed on the wrong branch](problem-01-wrong-branch.md) | (none: commits are just in the wrong place) | 17, 21, 31 |
| 2 | [Merge conflict](problem-02-merge-conflict.md) | `CONFLICT (content): Merge conflict in …` | 26–28 |
| 3 | [Accidental commit](problem-03-accidental-commit.md) | (a file that does not belong in the commit) | 30, 31, 73 |
| 4 | [Accidental reset](problem-04-accidental-reset.md) | (commits missing from `git log`) | 31, 33, 81 |
| 5 | [Deleted branch](problem-05-deleted-branch.md) | `fatal: invalid reference: …` | 22, 79 |
| 6 | [Detached HEAD](problem-06-detached-head.md) | `Warning: you are leaving 1 commit behind` | 76, 78 |
| 7 | [Wrong remote](problem-07-wrong-remote.md) | `refusing to merge unrelated histories` | 37, 38 |
| 8 | [Push rejected](problem-08-push-rejected.md) | `! [rejected] main -> main (fetch first)` | 40–42 |
| 9 | [Non-fast-forward error](problem-09-non-fast-forward.md) | `! [rejected] … (non-fast-forward)` | 42, 60, 63 |
| 10 | [Authentication failure](problem-10-authentication-failure.md) | `Permission denied (publickey)` | 48–50 |
| 11 | [Wrong upstream branch](problem-11-wrong-upstream.md) | `The upstream branch of your current branch does not match …` | 43 |
| 12 | [Accidentally committed secret](problem-12-committed-secret.md) | (a scanner or secret-scanning alert) | 83, 89, 90 |
| 13 | [Large file rejected](problem-13-large-file-rejected.md) | `GH001: Large files detected` | 83, 88 |
| 14 | [Rebase conflict](problem-14-rebase-conflict.md) | `could not apply … ` / `interactive rebase in progress` | 64–66 |
| 15 | [Incorrect merge](problem-15-incorrect-merge.md) | (the wrong branch is in `main`) | 23, 32, 54 |
| 16 | [Lost commit](problem-16-lost-commit.md) | (a commit vanished after a rebase) | 33, 80 |
| 17 | [Wrong commit needs to be removed](problem-17-remove-wrong-commit.md) | (a bad commit in the middle of history) | 31, 32, 63 |
| 18 | [Production branch contains an unwanted commit](problem-18-unwanted-commit-production.md) | (production behaves like the next release) | 32, 58, 67 |

## The general method

1. **Stop and look** before typing more commands: `git status`, `git log --oneline --graph --all -10`.
2. **Is it pushed?** `git branch -r --contains <sha>` / `git status` (ahead/behind). Unpushed = rewrite freely;
   pushed = add commits (revert) instead of rewriting.
3. **Find the last good state**: `git reflog`, `ORIG_HEAD`, the server, a teammate's clone.
4. **Mark it** before experimenting: `git branch rescue <sha>`.
5. **Fix, then verify** with the same commands that showed the problem.
6. **Prevent**: a hook, a protection rule, a habit.

Next: [Module 23 · Command reference lab](../docs/command-reference.md) and [Module 23 · Projects](../23-projects/README.md).
