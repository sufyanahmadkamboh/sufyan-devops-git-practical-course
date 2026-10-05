# Module 14 · Advanced Git · Assessment

> Lessons 67–73 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-14-adv basic
bash scripts/new-lab.sh assess-14-bisect bisect
(cd ~/git-practice/assess-14-adv && git switch -q -c feature-specials &&
  echo "Monday: mocha" > specials.txt && git add specials.txt && git commit -q -m "Start the specials board" &&
  sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Fix the espresso price" &&
  git switch -q main && echo "debug output" > debug.log && echo "scratch" > scratch.tmp)
```

## Quiz

1. What does `git cherry-pick C` copy, and what does it **not** bring along?
2. What does `-x` add to a cherry-picked commit, and when is it useful?
3. Lightweight vs annotated tag: what is the difference, and which one does `git describe` use by default?
4. Are tags pushed by `git push`? How do you publish `v1.0.0`?
5. What exit codes does a `git bisect run` script use for good, bad and "cannot test"?
6. A teammate reformatted a whole file; `git blame` now shows them on every line. How do you see the real history?
7. Why should `git clean` always be run with `-n` first, and what does `-x` add?
8. A file is listed in `.gitignore` but still shows as modified. Why, and how do you fix it?

<details>
<summary>Answers</summary>

1. The change of that one commit, as a new commit; not the commits it depends on (lesson 67).
2. A line "(cherry picked from commit …)": traceability for backports (67).
3. Lightweight = a name for a commit; annotated = a tag object with tagger, date, message. `describe` uses annotated
   tags (68, 69).
4. No: `git push origin v1.0.0` (or `--follow-tags`) (68).
5. 0 good, 1–124 (except 125) bad, 125 skip (70).
6. `git blame --ignore-rev SHA` or a `.git-blame-ignore-revs` file; `git log -L` for a line's history (71).
7. Deleted untracked files cannot be recovered; `-n` previews. `-x` also deletes ignored files such as `.env` (72).
8. It was already tracked; `.gitignore` only affects untracked files. `git rm --cached FILE` and commit (73).

</details>

## Practical challenge

In `~/git-practice/assess-14-adv` (on `main`; `feature-specials` has an unfinished specials board and a fix):

1. Bring **only** the espresso fix to `main`, recording where it came from.
2. Ignore `*.log` files with a committed `.gitignore`; `debug.log` must stay on disk.
3. Remove the stray `scratch.tmp` with `git clean` (preview first), without touching `debug.log`.
4. Create an annotated tag `v1.1.0` on the new `main`.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Would remove scratch.tmp; output -->
```bash
cd ~/git-practice/assess-14-adv
git cherry-pick -x "$(git log --format=%h -1 --grep='Fix the espresso' feature-specials)" > /dev/null
echo "*.log" > .gitignore && git add .gitignore && git commit -q -m "Ignore log files"
git clean -n
git clean -q -f
git tag -a v1.1.0 -m "Release 1.1.0"
git log --oneline --decorate -3
```

```text
Would remove scratch.tmp
0a81af2 (HEAD -> main, tag: v1.1.0) Ignore log files
38ad0c0 Fix the espresso price
4267004 Add prices
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-14-adv
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "espresso fix on main"                 'git show main:prices.txt | grep -q "espresso 2.60"'
check "the fix records its origin"           'git log --format=%B main | grep -q "cherry picked from commit"'
check "no specials board on main"            '! git cat-file -e main:specials.txt'
check "debug.log ignored but still on disk"  'git check-ignore -q debug.log && [ -f debug.log ]'
check "scratch.tmp removed"                  '[ ! -e scratch.tmp ]'
check "annotated tag v1.1.0 on main"         '[ "$(git cat-file -t v1.1.0)" = tag ] && [ "$(git rev-parse "v1.1.0^{commit}")" = "$(git rev-parse main)" ]'
```

```text
ok       espresso fix on main
ok       the fix records its origin
ok       no specials board on main
ok       debug.log ignored but still on disk
ok       scratch.tmp removed
ok       annotated tag v1.1.0 on main
```

## Troubleshooting challenge

In `~/git-practice/assess-14-bisect`, the order total is wrong. It was correct in the very first commit; there are ten
commits since.

<!-- test: output -->
```bash
cd ~/git-practice/assess-14-bisect
bash price.sh espresso latte 2>&1 || true
bash check.sh && echo good || echo bad
```

```text
price.sh: line 6: 320
360: arithmetic syntax error in expression (error token is "360")
2.50
bad
```

Find the commit that introduced the bug with `git bisect`, then fix it with a new commit (do not rewrite history).

<details>
<summary>Solution</summary>

<!-- test: contains=Add mocha; output -->
```bash
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh > /dev/null 2>&1
git log -1 --format='first bad commit: %h %s' refs/bisect/bad
git show refs/bisect/bad -- prices.txt | grep '^+'
git bisect reset > /dev/null 2>&1
```

```text
first bad commit: 3ceea03 Add mocha
+++ b/prices.txt
+mocha 3.90
+latte 3.60
```

The mocha commit added a second `latte` line. Remove it in a new commit:

<!-- test: contains=5.70; output -->
```bash
sed -i '/^latte 3.60$/d' prices.txt
git commit -q -am "Remove the duplicate latte price"
bash price.sh espresso latte
```

```text
5.70
```

</details>

Verification:

<!-- test: contains=good; output -->
```bash
cd ~/git-practice/assess-14-bisect
bash check.sh && echo good || echo bad
git branch --show-current
```

```text
good
main
```

## Real-world scenario

A security fix was merged to `main` (future 3.0). Customers run 2.4 and 2.5. Your release manager asks for patched
releases without shipping any 3.0 features.

<details>
<summary>Model answer</summary>

Create (or reuse) `release/2.4` and `release/2.5` from the `v2.4.x` / `v2.5.x` tags, `git cherry-pick -x` the fix onto
each (plus any commit it depends on, in order), resolve conflicts per branch, run the tests, then tag annotated (and
ideally signed) `v2.4.N+1` and `v2.5.N+1` and publish them as releases. The `-x` line lets anyone trace the backport to
the original commit on `main`.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-14-adv ~/git-practice/assess-14-bisect
```
