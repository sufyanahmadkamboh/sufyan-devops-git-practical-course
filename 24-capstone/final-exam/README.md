# Final exam

> ⏱ 60 minutes · no reference solution while you work · run from the course folder

A broken repository and ten tasks. Every task is something that happens in real teams; every one was practised in the
course. Work in order (some tasks depend on earlier ones). Use any command you like; do not delete and re-create the
repository.

## Start

<!-- test: contains=exam ready -->
```bash
bash 24-capstone/final-exam/final-exam.sh
cp 24-capstone/final-exam/check-exam.sh ~/git-practice/
cd ~/git-practice/exam
git status | head -2
```

The repository `~/git-practice/exam` has a server at `~/git-practice/exam-server.git`. Only `main` up to "Add
experimental pricing" has been pushed; everything else is local.

## Tasks

| # | Task | Points |
|---|---|---|
| 1 | A commit "Add the winter menu" was made in detached HEAD and left behind. Save it on a branch `winter-menu`. | 1 |
| 2 | The branch `seasonal` was deleted by mistake. Restore it. | 1 |
| 3 | The local commit "Add the meun board" has a typo. Rename it to "Add the menu board" (it is not pushed). | 1 |
| 4 | The last commit, "Add debug log", also committed `debug.log` (200 kB). Remove the file from that commit, keep the commit's other change, and make Git ignore `*.log`. | 1 |
| 5 | Bring back the stashed "WIP: espresso note", commit it, and leave the stash list empty. | 1 |
| 6 | `origin` points to a server that does not exist. Point it to `~/git-practice/exam-server.git`. | 1 |
| 7 | The **pushed** commit "Add experimental pricing" must be undone on `main`, without rewriting shared history. | 1 |
| 8 | Merge `feature-tea` into `main`. The team agreed on a latte price of **3.40**; keep green tea. | 1 |
| 9 | Push `main`. The branch `hotfix` tracks `origin/main` by mistake: push it as `origin/hotfix` and make that its upstream. | 1 |
| 10 | Replace the lightweight tag `v1.0` with an **annotated** tag `v1.0.0` on the commit "Add prices", and push it. | 1 |

## Grade yourself

<!-- test: contains=score: 0 / 10; output -->
```bash
cd ~/git-practice/exam
bash ../check-exam.sh
```

```text
MISSING  1. branch winter-menu has the winter menu commit
MISSING  2. branch seasonal is back
MISSING  3. the typo in 'Add the meun board' is fixed
MISSING  4. debug.log removed from history, *.log ignored
MISSING  5. the stash is committed and the stash list is empty
MISSING  6. origin points to exam-server.git
MISSING  7. the experimental pricing is reverted (not rewritten)
MISSING  8. feature-tea merged, latte at 3.40, green tea on the menu
MISSING  9. main pushed; hotfix pushed and tracking origin/hotfix
MISSING  10. annotated v1.0.0 on 'Add prices' (pushed), no v1.0

score: 0 / 10
```

(The output above is the starting point: nothing solved yet.) Passing grade: 8 / 10.

Stuck? The lessons behind each task: 1 → 78, 2 → 79, 3 → 63, 4 → 31/73, 5 → 35, 6 → 38, 7 → 32, 8 → 27,
9 → 42–43, 10 → 69. The complete solution is in [SOLUTION.md](SOLUTION.md): open it only after you have tried.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/exam ~/git-practice/exam-server.git ~/git-practice/check-exam.sh
```
