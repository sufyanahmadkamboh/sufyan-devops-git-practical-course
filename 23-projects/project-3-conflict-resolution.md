# Project 3 · Conflict resolution

> Level 24 · Projects · intermediate · ⏱ 60 minutes · lessons 25–28, 64–66

## Brief

Two long-lived branches were developed for weeks and now must be combined. The lab script below creates them; your
job is to integrate `pricing-2026` into `main` and resolve **three different kinds of conflicts** correctly, then
rebase a third branch on the result.

| File | `main` did | `pricing-2026` did | Kind |
|---|---|---|---|
| `prices.txt` | latte 3.30 | latte 3.50, and a new item | same lines changed differently |
| `specials.txt` | deleted it (specials discontinued) | added a Friday special | modify/delete |
| `README.md` | added opening hours at the end | added a price note at the end | both appended at the same place |

## Requirements

1. `main` contains a merge commit of `pricing-2026` with: latte at **3.40** (the agreed price), the new item from
   `pricing-2026`, **no** `specials.txt` (the decision on `main` wins), both README additions.
2. No conflict markers anywhere.
3. Branch `menu-redesign` is rebased onto the new `main`, with its own conflict resolved, and contains no merge commits.

## Starting point

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh project-3 basic
cd ~/git-practice/project-3
echo "Monday: mocha" > specials.txt && git add specials.txt && git commit -q -m "Add the specials board"
git switch -q -c pricing-2026
sed -i 's/latte 3.20/latte 3.50/' prices.txt && echo "flat white 3.60" >> prices.txt && git commit -q -am "Prices for 2026"
echo "Friday: chai" >> specials.txt && git commit -q -am "Add a Friday special"
printf '\nAll prices include tax.\n' >> README.md && git commit -q -am "Add a price note"
git switch -q main
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Raise the latte price to 3.30"
git rm -q specials.txt && git commit -q -m "Discontinue the specials board"
printf '\nOpen every day from 8:00 to 18:00.\n' >> README.md && git commit -q -am "Add opening hours"
git switch -q -c menu-redesign HEAD~3
sed -i 's/^espresso$/espresso (single or double)/' menu.txt && git commit -q -am "Describe the espresso"
sed -i 's/^cappuccino$/cappuccino (classic)/' menu.txt && git commit -q -am "Describe the cappuccino"
git switch -q main
sed -i 's/^espresso$/espresso (ristretto on request)/' menu.txt && git commit -q -am "Espresso note"
git log --oneline --graph --all | head -14
```

## Hints

- `git merge pricing-2026`, then `git status` lists each conflicted file and its kind (lesson 26).
- Modify/delete: keep the deletion with `git rm specials.txt` (lesson 67's troubleshooting).
- Rebase: `git switch menu-redesign && git rebase main`; resolve per commit, `git add`, `git rebase --continue`.

## Reference solution

<details>
<summary>Show the reference solution</summary>

<!-- test: contains=DU specials.txt; output -->
```bash
cd ~/git-practice/project-3
git merge pricing-2026 > /dev/null 2>&1 || true
git status --short
```

```text
UU README.md
UU prices.txt
DU specials.txt
```

<!-- test: contains=Merge branch 'pricing-2026'; output -->
```bash
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\nflat white 3.60\n' > prices.txt
git rm -q specials.txt
printf '# Cafe\n\nThe menu and prices of a small cafe.\n\nOpen every day from 8:00 to 18:00.\n\nAll prices include tax.\n' > README.md
git add prices.txt README.md
git commit -q --no-edit
git log --oneline --graph -6
```

```text
*   d9b409f (HEAD -> main) Merge branch 'pricing-2026'
|\  
| * 6e27276 (pricing-2026) Add a price note
| * a208ba6 Add a Friday special
| * e9502e4 Prices for 2026
* | ea806b1 Espresso note
* | e496a80 Add opening hours
```

<!-- test: contains=Successfully rebased; output -->
```bash
git switch -q menu-redesign
git rebase main > /dev/null 2>&1 || true
git status --short
printf 'espresso (single or double, ristretto on request)\nlatte\ncappuccino\n' > menu.txt
git add menu.txt && git rebase --continue 2>&1 | tail -1
git log --oneline -3
cat menu.txt
```

```text
UU menu.txt
Rebasing (2/2)
Successfully rebased and updated refs/heads/menu-redesign.
9b230bb (HEAD -> menu-redesign) Describe the cappuccino
b99723b Describe the espresso
d9b409f (main) Merge branch 'pricing-2026'
espresso (single or double, ristretto on request)
latte
cappuccino (classic)
```

</details>

## Self-check

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/project-3
check() { if eval "$2" > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "main has the pricing merge"          'git log --merges --oneline main | grep -q pricing-2026'
check "latte is 3.40 on main"               'git show main:prices.txt | grep -qx "latte 3.40"'
check "flat white kept from the branch"     'git show main:prices.txt | grep -q "flat white"'
check "specials.txt deleted on main"        '! git cat-file -e main:specials.txt'
check "both README additions"               'git show main:README.md | grep -q "Open every day" && git show main:README.md | grep -q "include tax"'
check "no conflict markers anywhere"        '! git grep -qE "^(<<<<<<<|=======|>>>>>>>)" main menu-redesign'
check "menu-redesign is on top of main"     'git merge-base --is-ancestor main menu-redesign'
check "menu-redesign has no merge commits"  '[ "$(git rev-list --merges --count main..menu-redesign)" -eq 0 ]'
```

```text
ok       main has the pricing merge
ok       latte is 3.40 on main
ok       flat white kept from the branch
ok       specials.txt deleted on main
ok       both README additions
ok       no conflict markers anywhere
ok       menu-redesign is on top of main
ok       menu-redesign has no merge commits
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/project-3
```

Next: [Project 4 · Git recovery](project-4-git-recovery.md)
