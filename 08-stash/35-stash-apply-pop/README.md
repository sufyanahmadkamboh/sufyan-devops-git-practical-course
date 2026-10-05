# Lesson 35 · Stash, apply and pop

> Level 7 · Stash · ⏱ 15 minutes

## What are we learning?

The difference between `apply` (re-apply, keep the stash) and `pop` (re-apply and delete it), how to give stashes
names, and what happens when a stash conflicts with newer commits.

## Visual

```text
 stash@{0}  ──── git stash apply ───►  changes back in the working directory; stash@{0} STAYS on the shelf
 stash@{0}  ──── git stash pop   ───►  changes back in the working directory; stash@{0} REMOVED
                                       (if the apply conflicts, pop keeps the stash, just in case)
```

## Lab setup

<!-- test: contains=lesson-35 -->
```bash
bash scripts/new-lab.sh lesson-35 feature
cd ~/git-practice/lesson-35
```

## Demonstration

Stash with a message, so you recognise it later:

<!-- test: contains=On main: autumn prices; output -->
```bash
sed -i 's/latte 3.20/latte 3.40/' prices.txt
git stash push -m "autumn prices"
git stash list
```

```text
Saved working directory and index state On main: autumn prices
stash@{0}: On main: autumn prices
```

`apply` the same stash onto two branches, because it is useful on both:

<!-- test: contains=stash@{0}: On main: autumn prices; output -->
```bash
git stash apply -q
git commit -q -am "Autumn latte price on main"
git switch -q feature-tea
git stash apply -q
git diff --stat
git stash list
```

```text
 prices.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
stash@{0}: On main: autumn prices
```

After two `apply`s the stash is still there. Remove it when you are done:

<!-- test: contains=Dropped -->
```bash
git commit -q -am "Autumn latte price on feature-tea"
git stash drop
git stash list | wc -l
```

## Command breakdown

| Command | What it does |
|---|---|
| `git stash push -m "msg"` | stash with a description |
| `git stash push FILE` | stash only FILE |
| `git stash apply [stash@{N}]` | re-apply, keep the stash |
| `git stash pop [stash@{N}]` | re-apply and remove (kept if it conflicts) |
| `git stash apply --index` | also restore which changes were staged |
| `git stash drop [stash@{N}]` | delete one stash |

## Hands-on exercise

**Instructions.** Change `menu.txt` and `prices.txt`, but stash only `menu.txt`.

**Expected result.** `prices.txt` stays modified in your folder; the stash contains only `menu.txt`.

<!-- test-run: cd ~/git-practice/lesson-35 && echo "chai" >> menu.txt && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git stash push -q -m "chai" menu.txt -->

**Verification.**

<!-- test: contains=M prices.txt; contains=menu.txt -->
```bash
cd ~/git-practice/lesson-35
git status --short
git stash show --name-only
```

## Break it

Pop a stash onto a version of the file that changed since you stashed it, on the same lines:

<!-- test: fail; contains=CONFLICT; output -->
```bash
git commit -q -am "Espresso 2.60"
sed -i 's/^green tea$/green tea (sencha)/' menu.txt && git commit -q -am "Sencha"
git stash pop 2>&1
```

```text
Auto-merging menu.txt
CONFLICT (content): Merge conflict in menu.txt
On branch feature-tea
Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   menu.txt

no changes added to commit (use "git add" and/or "git commit -a")
The stash entry is kept in case you need it again.
```

## Troubleshoot

The stash's `chai` line was added right after `green tea`, which was changed since: a conflict, resolved like a merge.
Note the last line: `The stash entry is kept in case you need it again.`

<!-- test: contains=stash@{0}: On feature-tea: chai; output -->
```bash
git status --short
git stash list
```

```text
UU menu.txt
stash@{0}: On feature-tea: chai
```

## Fix

Resolve (keep both lines), mark resolved, and drop the stash yourself since `pop` did not:

<!-- test: contains=chai; absent=<<<; output -->
```bash
printf 'espresso\nlatte\ncappuccino\ngreen tea (sencha)\nchai\n' > menu.txt
git restore --staged menu.txt
git stash drop
cat menu.txt
```

```text
Dropped refs/stash@{0} (dacb5f09d406bf5e567fd44f401d6738c23f36ed)
espresso
latte
cappuccino
green tea (sencha)
chai
```

`git restore --staged` here only clears the "unmerged" state; the resolved file stays as uncommitted work, like after a
normal pop.

## Real-world example

A teammate asks you to try their quick fix locally: you `git stash` your work, check out their branch, test, switch
back, `git stash pop`. Naming stashes (`-m "WIP: login form"`) matters as soon as you have more than one: after a week,
`stash@{3}: WIP on main: 4267004 Add prices` tells you nothing.

## Practice challenge

Stash a change that is partly staged and partly unstaged, then restore it with exactly the same staged/unstaged split.

<details>
<summary>Solution</summary>

<!-- test: contains=M  menu.txt; contains= M prices.txt; output -->
```bash
cd ~/git-practice/lesson-35
git stash -q
echo "mocha" >> menu.txt && git add menu.txt
sed -i 's/latte 3.40/latte 3.50/' prices.txt
git stash -q
git stash pop -q --index
git status --short
```

```text
M  menu.txt
 M prices.txt
```

Without `--index`, everything comes back unstaged.

</details>

## Recap

- `apply` keeps the stash, `pop` removes it (unless it conflicts).
- Name stashes with `-m`; stash single files with `git stash push FILE`.
- Stash conflicts are resolved like merge conflicts; then `git stash drop`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-35
```

Next: [Lesson 36 · Managing stashes](../36-managing-stashes/README.md).
