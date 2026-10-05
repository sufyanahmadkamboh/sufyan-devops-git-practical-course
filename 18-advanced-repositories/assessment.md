# Module 18 · Advanced repositories · Assessment

> Lessons 86–88 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`) · needs Git LFS

## Lab setup

<!-- test: contains=labs ready -->
```bash
bash scripts/new-lab.sh assess-18-practical basic
bash scripts/new-lab.sh assess-18-broken basic
(cd ~/git-practice &&
  git init -q --bare assess-18-rules.git && git clone -q assess-18-rules.git assess-18-rules-work 2> /dev/null &&
  cd assess-18-rules-work && echo "VAT 19%" > tax.txt && git add tax.txt && git commit -q -m "Add the tax rule" && git push -q origin HEAD:main)
(cd ~/git-practice/assess-18-broken &&
  git -c protocol.file.allow=always submodule add -q ../assess-18-rules.git rules && git commit -q -m "Add the shared rules" &&
  git init -q --bare ../assess-18-cafe.git && git push -q ../assess-18-cafe.git main &&
  cd .. && git clone -q assess-18-cafe.git assess-18-grace)
git lfs install --skip-repo > /dev/null
echo "labs ready"
```

## Quiz

1. What does the main repository store for a submodule: its files or something else?
2. After a plain `git clone`, a submodule folder is empty. Which command fills it?
3. Why do submodule commands on local paths need `-c protocol.file.allow=always` since Git 2.38?
4. What is a worktree, and what is shared between worktrees?
5. Why can't you check out the same branch in two worktrees?
6. What does Git store for a file tracked by LFS?
7. A large file was committed **before** `git lfs track`. Why doesn't adding the rule fix the history, and what does?

<details>
<summary>Answers</summary>

1. A gitlink: the submodule's commit ID (mode 160000), plus `.gitmodules` with path and URL (lesson 86).
2. `git submodule update --init` (or clone with `--recurse-submodules`) (lesson 86).
3. A security default: local-path submodules are blocked unless explicitly allowed (lesson 86).
4. An extra working directory attached to the same repository; objects, refs and config are shared (lesson 87).
5. Each worktree would move the branch independently; Git allows one checkout per branch (lesson 87).
6. A small pointer file (version, `oid sha256:…`, size); the content goes to the LFS store (lesson 88).
7. Rules apply only to files added afterwards; `git lfs migrate import --include=PATTERN` rewrites history (lesson 88).

</details>

## Practical challenge

In `~/git-practice/assess-18-practical`, while keeping an unfinished edit in the main folder:

1. Fix the espresso price (2.50 → 2.40) on a branch `hotfix` **in a separate worktree** `../assess-18-hotfix`, then
   remove that worktree.
2. Track `*.bin` with Git LFS and commit a 2 MB file `menu-video.bin` on `main`, stored as an LFS pointer.
3. The unfinished edit (`chai` appended to `menu.txt`) is still uncommitted in the main folder.

<details>
<summary>Reference solution</summary>

<!-- test: contains=menu-video.bin; output -->
```bash
cd ~/git-practice/assess-18-practical
echo chai >> menu.txt
git worktree add -q -b hotfix ../assess-18-hotfix main
(cd ../assess-18-hotfix && sed -i 's/espresso 2.50/espresso 2.40/' prices.txt && git commit -q -am "Fix the espresso price")
git worktree remove ../assess-18-hotfix
git lfs track "*.bin" > /dev/null
head -c 2000000 /dev/zero | tr '\0' 'v' > menu-video.bin
git add .gitattributes menu-video.bin && git commit -q -m "Add the menu video"
git lfs ls-files
git status --short
```

```text
6707e5d37d * menu-video.bin
 M menu.txt
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-18-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "hotfix has the espresso fix"          'git show hotfix:prices.txt | grep -qx "espresso 2.40"'
check "the hotfix worktree is removed"       '[ "$(git worktree list | wc -l)" -eq 1 ]'
check "menu-video.bin is in LFS"             'git lfs ls-files | grep -q menu-video.bin'
check "Git stores a pointer, not 2 MB"       '[ "$(git cat-file -s HEAD:menu-video.bin)" -lt 200 ]'
check "the unfinished edit is still there"   'git status --short | grep -q "M menu.txt"'
```

```text
ok       hotfix has the espresso fix
ok       the hotfix worktree is removed
ok       menu-video.bin is in LFS
ok       Git stores a pointer, not 2 MB
ok       the unfinished edit is still there
```

## Troubleshooting challenge

Grace cloned the cafe repository (`~/git-practice/assess-18-grace`); the build needs `rules/tax.txt`:

<!-- test: contains=-; output -->
```bash
cd ~/git-practice/assess-18-grace
cat rules/tax.txt 2>&1 | sed 's/.*No such file.*/rules\/tax.txt: No such file or directory/'
git submodule status
```

```text
rules/tax.txt: No such file or directory
-3a298373c4e142a929909c2fa856dcf2bf9e2870 rules
```

Fix Grace's clone.

<details>
<summary>Solution</summary>

The leading `-` in `git submodule status` means "registered but not initialised": a plain clone does not fetch
submodules.

<!-- test: contains=VAT 19%; output -->
```bash
git -c protocol.file.allow=always submodule update --init 2>&1 | tail -1
cat rules/tax.txt
```

```text
Submodule path 'rules': checked out '3a298373c4e142a929909c2fa856dcf2bf9e2870'
VAT 19%
```

</details>

Verification:

<!-- test: absent=-; output -->
```bash
cd ~/git-practice/assess-18-grace
git submodule status | cut -c1
```

```text
 
```

## Real-world scenario

Your team keeps shared Terraform modules in a submodule of every service repository. Builds fail randomly with
"module not found"; updates to the shared modules take weeks to reach services. What would you check, and what
alternatives would you propose?

<details>
<summary>Model answer</summary>

Check that every CI checkout initialises submodules (`actions/checkout` with `submodules: true` or `git submodule update
--init --recursive`), and that developers clone with `--recurse-submodules` or set `submodule.recurse true`. Slow updates
are inherent: each service pins a commit and needs a second commit to move the pin. Alternatives: reference modules by
version directly (`source = "git::https://…//vpc?ref=v1.4.0"`) or from a module registry, with Renovate/Dependabot PRs
to bump versions; or a monorepo when the code changes together. Submodules fit when an exact pinned version of an
independent repository is really needed (lesson 86).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-18-practical ~/git-practice/assess-18-hotfix ~/git-practice/assess-18-broken ~/git-practice/assess-18-rules.git ~/git-practice/assess-18-rules-work ~/git-practice/assess-18-cafe.git ~/git-practice/assess-18-grace
```
