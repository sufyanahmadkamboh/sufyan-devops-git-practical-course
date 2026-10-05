# Final exam · solution

> Open this only after attempting the [final exam](README.md). Every step is run and checked like the lessons.

## Start

<!-- test: contains=exam ready -->
```bash
bash 24-capstone/final-exam/final-exam.sh
cp 24-capstone/final-exam/check-exam.sh ~/git-practice/
cd ~/git-practice/exam
```

First, look before touching anything:

<!-- test: contains=hotfix; output -->
```bash
git status | head -3
git log --oneline --graph --all
git stash list
git remote -v
git branch -vv
```

```text
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)
*   5d71a91 (refs/stash) On main: WIP: espresso note
|\  
| * 3738a19 index on main: d65dd52 Add debug log
|/  
* d65dd52 (HEAD -> main) Add debug log
* 58a9c52 Raise the latte price to 3.30
* a49643e Add the meun board
| * c579de0 (hotfix) Fix the cappuccino price
|/  
* e97be76 (origin/main, origin/HEAD) Add experimental pricing
| * 6df269e (feature-tea) Add green tea
| * f03fd86 Raise the latte price to 3.50
|/  
* ae3b636 Add prices
* b5a3c6c (tag: v1.0) Add the menu
* cd90b3e Add README
stash@{0}: On main: WIP: espresso note
origin	~/git-practice/wrong-server.git (fetch)
origin	~/git-practice/wrong-server.git (push)
  feature-tea 6df269e Add green tea
  hotfix      c579de0 [origin/main: ahead 1] Fix the cappuccino price
* main        d65dd52 [origin/main: ahead 3] Add debug log
```

## 1 · Save the detached commit (lesson 78)

<!-- test: contains=Add the winter menu; output -->
```bash
git branch winter-menu "$(git reflog --format=%h --grep-reflog='commit: Add the winter menu' | head -1)"
git log --oneline -1 winter-menu
```

```text
b7af354 (winter-menu) Add the winter menu
```

## 2 · Restore the deleted branch (lesson 79)

<!-- test: contains=Add pumpkin latte; output -->
```bash
git branch seasonal "$(git reflog --format=%h --grep-reflog='commit: Add pumpkin latte' | head -1)"
git log --oneline -1 seasonal
```

```text
2a56433 (seasonal) Add pumpkin latte
```

## 3 · Fix the typo in an unpushed commit (lesson 63)

<!-- test: contains=Add the menu board; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i 's/^pick \([0-9a-f]*\) # Add the meun board$/reword \1 # Add the meun board/'" \
  GIT_EDITOR="sed -i '1s/meun/menu/'" git rebase -q -i origin/main
git log --oneline origin/main..main
```

```text
[detached HEAD 36a0485] Add the menu board
 Date: Sun Mar 1 09:10:00 2026 +0000
 1 file changed, 1 insertion(+)
 create mode 100644 board.txt
b1dc33f (HEAD -> main) Add debug log
f3d3e75 Raise the latte price to 3.30
36a0485 Add the menu board
```

`origin/main` still refers to the real server's state (the URL is wrong, but the remote-tracking branch is correct), so
the rebase touches only the unpushed commits.

## 4 · Remove the log file from the last commit (lessons 31, 73)

<!-- test: contains=board.txt; absent=debug.log; output -->
```bash
git rm -q --cached debug.log
echo "*.log" > .gitignore && git add .gitignore
git commit -q --amend --no-edit
git show --stat --format=%s HEAD
```

```text
Add debug log

 .gitignore | 1 +
 board.txt  | 2 +-
 2 files changed, 2 insertions(+), 1 deletion(-)
```

## 5 · Commit the stash (lesson 35)

<!-- test: contains=0; output -->
```bash
git stash pop -q
git commit -q -am "Add an espresso note"
git stash list | wc -l
```

```text
0
```

## 6 · Fix the remote (lesson 38)

<!-- test: contains=exam-server.git; output -->
```bash
git remote set-url origin ~/git-practice/exam-server.git
git ls-remote --heads origin | sed 's/^[0-9a-f]*\t//'
git remote get-url origin | sed "s|$HOME|~|"
```

```text
refs/heads/main
~/git-practice/exam-server.git
```

## 7 · Revert the pushed commit (lesson 32)

<!-- test: contains=Revert "Add experimental pricing"; output -->
```bash
git revert --no-edit "$(git log --format=%h -1 --grep='^Add experimental pricing$')" > /dev/null
git log --oneline -1
grep -c truffle prices.txt || true
```

```text
bddbd8e (HEAD -> main) Revert "Add experimental pricing"
0
```

## 8 · Merge feature-tea and resolve the conflict (lesson 27)

<!-- test: contains=latte 3.40; output -->
```bash
git merge feature-tea > /dev/null 2>&1 || true
git status --short
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q --no-edit
cat prices.txt menu.txt
```

```text
M  menu.txt
UU prices.txt
espresso 2.50
latte 3.40
cappuccino 3.40
espresso
latte
cappuccino
green tea
```

## 9 · Push main; fix the hotfix upstream (lessons 42–43)

<!-- test: contains=[origin/hotfix]; output -->
```bash
git push -q origin main 2>&1
git push -q -u origin hotfix 2>&1
git branch -vv | grep -E "hotfix|main"
```

```text
  hotfix      c579de0 [origin/hotfix] Fix the cappuccino price
* main        f9c9ad9 [origin/main] Merge branch 'feature-tea'
```

## 10 · Replace the tag (lessons 68–69)

<!-- test: contains=refs/tags/v1.0.0; output -->
```bash
git tag -d v1.0
git tag -a v1.0.0 -m "Release 1.0.0" "$(git log --format=%h -1 --grep='^Add prices$')"
git push -q origin v1.0.0
git ls-remote --tags origin
```

```text
Deleted tag 'v1.0' (was b5a3c6c)
c75f2f4b42fb6c5fe80454b0af765adabe7d8f4b	refs/tags/v1.0.0
ae3b6365bd1d215294bc9acaaf69fd0d70b031c3	refs/tags/v1.0.0^{}
```

## Grade

<!-- test: contains=score: 10 / 10; output -->
```bash
bash ../check-exam.sh
```

```text
ok       1. branch winter-menu has the winter menu commit
ok       2. branch seasonal is back
ok       3. the typo in 'Add the meun board' is fixed
ok       4. debug.log removed from history, *.log ignored
ok       5. the stash is committed and the stash list is empty
ok       6. origin points to exam-server.git
ok       7. the experimental pricing is reverted (not rewritten)
ok       8. feature-tea merged, latte at 3.40, green tea on the menu
ok       9. main pushed; hotfix pushed and tracking origin/hotfix
ok       10. annotated v1.0.0 on 'Add prices' (pushed), no v1.0

score: 10 / 10
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/exam ~/git-practice/exam-server.git ~/git-practice/check-exam.sh
```
