# Module 16 · Advanced recovery · Assessment

> Lessons 79–81 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

Two labs, both damaged on purpose:

<!-- test: contains=labs damaged -->
```bash
bash scripts/new-lab.sh assess-16-practical history
bash scripts/new-lab.sh assess-16-broken basic
(cd ~/git-practice/assess-16-practical &&
  git switch -q -c specials && echo "Friday: chai" > specials.txt && git add specials.txt && git commit -q -m "Add the specials board" &&
  git switch -q main && git branch -q -D specials && git reset -q --hard HEAD~2)
(cd ~/git-practice/assess-16-broken &&
  printf 'flat white 3.60\ncortado 3.10\n' > new-drinks.txt && git add new-drinks.txt && git reset -q --hard)
echo "labs damaged"
```

## Quiz

1. You deleted a branch you had checked out and worked on. Where do you look first?
2. You deleted a branch you only **fetched** and never checked out. Why might the reflog not help, and what does?
3. After `git reset --hard HEAD~3`, which name points to the commit you were on before?
4. Which of these survives `git reset --hard`: committed work, staged work, unstaged work?
5. What does `git fsck --lost-found` write, and where?
6. Why should you avoid running `git gc --prune=now` while recovering?
7. A colleague deleted `release/2.3` on GitHub. Name two places it can be recovered from.

<details>
<summary>Answers</summary>

1. `git reflog`: HEAD was on the branch's commits (lesson 79).
2. HEAD was never on those commits and the remote-tracking reflog was deleted with the ref; `git fsck --unreachable
   --no-reflogs` still finds the commits until garbage collection (lesson 79).
3. `ORIG_HEAD` (and `HEAD@{1}` in the reflog) (lesson 81).
4. Committed: yes (reflog). Staged: yes, as dangling blobs (`fsck --lost-found`). Unstaged: no (lesson 81).
5. Dangling commits and blobs, copied into `.git/lost-found/commit/` and `.git/lost-found/other/` (lesson 81).
6. It deletes unreachable objects immediately, exactly the ones you are trying to recover (lesson 80).
7. Any teammate's clone (`origin/release/2.3`), the "Restore branch" button of its last PR, your own reflog (lesson 79).

</details>

## Practical challenge

In `~/git-practice/assess-16-practical` someone deleted the branch `specials` and then ran `git reset --hard HEAD~2`
on `main`. Requirements:

1. `specials` exists again with the commit "Add the specials board".
2. `main` points again to "Price mocha".
3. Nothing else changed (the working directory is clean).

<details>
<summary>Reference solution</summary>

<!-- test: contains=Price mocha; output -->
```bash
cd ~/git-practice/assess-16-practical
git reflog -4
git branch specials "$(git reflog --format=%h --grep-reflog='commit: Add the specials board' | head -1)"
git reset -q --hard "$(git reflog --format=%h --grep-reflog='commit: Price mocha' | head -1)"
git log --oneline -1
```

```text
269869e (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
ecff18a HEAD@{1}: checkout: moving from specials to main
ea7b281 HEAD@{2}: commit: Add the specials board
ecff18a HEAD@{3}: checkout: moving from main to specials
ecff18a (HEAD -> main) Price mocha
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-16-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "specials has its commit"   'git log --format=%s specials | grep -qx "Add the specials board"'
check "main is at Price mocha"    '[ "$(git log -1 --format=%s main)" = "Price mocha" ]'
check "working directory clean"   '[ -z "$(git status --porcelain)" ]'
```

```text
ok       specials has its commit
ok       main is at Price mocha
ok       working directory clean
```

## Troubleshooting challenge

In `~/git-practice/assess-16-broken`, a colleague wrote `new-drinks.txt`, ran `git add`, and then `git reset --hard`.
"The file is gone, and there was never a commit."

Symptoms:

<!-- test: contains=no new-drinks.txt; output -->
```bash
cd ~/git-practice/assess-16-broken
ls new-drinks.txt 2> /dev/null || echo "no new-drinks.txt"
git reflog -1
```

```text
no new-drinks.txt
4267004 (HEAD -> main) HEAD@{0}: reset: moving to HEAD
```

Investigate and bring the file back.

<details>
<summary>Solution</summary>

`git add` wrote the content as a blob; the reset only removed it from the index. The blob is dangling:

<!-- test: contains=cortado; output -->
```bash
git fsck --lost-found 2> /dev/null
for f in .git/lost-found/other/*; do grep -q cortado "$f" && cp "$f" new-drinks.txt; done
cat new-drinks.txt
```

```text
dangling blob 4e2eb4279996937428e8149a126f85e9bd01b59a
flat white 3.60
cortado 3.10
```

</details>

Verification:

<!-- test: contains=?? new-drinks.txt; output -->
```bash
cd ~/git-practice/assess-16-broken
git status --short
```

```text
?? new-drinks.txt
```

## Real-world scenario

Friday evening, a developer force-pushed a rebased `feature/payments` over a teammate's two commits from the
afternoon; the teammate's laptop is at home. Monday morning, the teammate asks you what to do.

<details>
<summary>Model answer</summary>

Nothing is lost if any clone still has the old commits. The teammate's laptop: `git reflog` (or `origin/feature/payments@{1}`)
shows the branch before the force push; `git branch rescue <sha>`, then compare with `git log rescue..origin/feature/payments`
and re-apply the missing commits (cherry-pick or rebase onto the new branch), push normally. Other sources: the PR's
"force-pushed" timeline entry on GitHub shows the old and new head, CI caches. Prevention: `--force-with-lease`
(which would have refused the push), protected branches, and `gc` defaults that keep unreachable objects for weeks.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-16-practical ~/git-practice/assess-16-broken
```
