# Lesson 65 · Aborting a rebase

> Level 13 · Rebase · ⏱ 15 minutes

## What are we learning?

`git rebase --abort` cancels a rebase in progress and puts the branch back exactly where it was before, however many
commits were already replayed. It is the emergency exit that makes rebasing safe to try.

## Visual

```text
 git rebase main
   replay C1 ✓   replay C2 ✓   replay C3 ✗ CONFLICT … "this is getting complicated"
                                     │
                                     └── git rebase --abort ──► branch back at C3 (old IDs), as if nothing happened
```

## Lab setup

<!-- test: contains=lesson-65 -->
```bash
bash scripts/new-lab.sh lesson-65 conflict
cd ~/git-practice/lesson-65
git switch -q feature-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git rev-parse --short HEAD
```

## Demonstration

<!-- test: fail; contains=CONFLICT; output -->
```bash
git rebase main 2>&1 | grep -E "CONFLICT|error"
test "${PIPESTATUS[0]}" -eq 0
```

```text
CONFLICT (content): Merge conflict in prices.txt
error: could not apply 00931cc... Raise the latte price to 3.50
```

You are mid-rebase (`git status` says so, and your prompt may show `feature-tea|REBASE 1/2`). Abort:

<!-- test: contains=On branch feature-tea; contains=nothing to commit; output -->
```bash
git rebase --abort
git status
git log --oneline -3
```

```text
On branch feature-tea
nothing to commit, working tree clean
b158326 (HEAD -> feature-tea) Add green tea
00931cc Raise the latte price to 3.50
4267004 Add prices
```

Same commits, same IDs as before the rebase; no conflict markers.

## Command breakdown

| Command | What it does |
|---|---|
| `git rebase --abort` | stop and restore the branch and working directory as before the rebase |
| `git rebase --quit` | stop but leave HEAD where it is now (rarely what you want) |
| `ORIG_HEAD` | the branch tip before the rebase started |
| `git reflog` | if you already finished a bad rebase: find the pre-rebase position (lesson 33) |

## Hands-on exercise

**Instructions.** Start the rebase again, resolve the conflict halfway (edit the file but do not add), then abort.
Check the file afterwards.

**Expected result.** `latte 3.50`, your branch's original version.

<!-- test-run: cd ~/git-practice/lesson-65 && (git rebase main > /dev/null 2>&1 || true) && echo "half-resolved" > prices.txt && git rebase --abort -->

**Verification.**

<!-- test: contains=latte 3.50 -->
```bash
cd ~/git-practice/lesson-65
grep latte prices.txt
```

## Break it

Forget that a rebase is still in progress (a terminal closed, a day later), and start another one:

<!-- test: fail; contains=already a rebase-merge directory; output -->
```bash
git rebase main > /dev/null 2>&1 || true
git rebase main 2>&1
```

```text
fatal: It seems that there is already a rebase-merge directory, and
I wonder if you are in the middle of another rebase.  If that is the
case, please try
	git rebase (--continue | --abort | --skip)
If that is not the case, please
	rm -fr ".git/rebase-merge"
and run me again.  I am stopping in case you still have something
valuable there.
```

## Troubleshoot

`It seems that there is already a rebase-merge directory`: Git keeps the rebase's state in `.git/rebase-merge/` until
it is finished or aborted. Only one can be in progress. Check what it was:

<!-- test: contains=rebase in progress; output -->
```bash
git status | head -3
```

```text
interactive rebase in progress; onto 594657b
Last command done (1 command done):
   pick 00931cc # Raise the latte price to 3.50
```

## Fix

Decide: finish it (resolve, `git add`, `--continue`) or abort it. Here, abort:

<!-- test: contains=nothing to commit -->
```bash
git rebase --abort
git status
```

## Real-world example

You run `git pull --rebase` on a branch that turns out to be far behind, and 12 conflicts appear one after another.
`git rebase --abort`, then choose a better plan: `git pull --no-rebase` (one merge, one conflict resolution), or squash
your commits first and rebase one commit. Abort early instead of resolving the same conflict five times.

## Practice challenge

Finish a rebase, then decide you want the old branch back anyway. Undo it **after** it completed.

<details>
<summary>Solution</summary>

<!-- test: contains=latte 3.50; output -->
```bash
cd ~/git-practice/lesson-65
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git add prices.txt && git rebase --continue > /dev/null
git reset -q --hard ORIG_HEAD
grep latte prices.txt
```

```text
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
latte 3.50
```

After a completed rebase, `ORIG_HEAD` (or `git reflog`, the line before `rebase (start)`) is the old tip.

</details>

## Recap

- `git rebase --abort` restores everything as before the rebase.
- Only one rebase at a time; `git status` tells you if one is in progress.
- After a completed rebase, `ORIG_HEAD` / reflog bring the old branch back.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-65
```

Next: [Lesson 66 · Continuing a rebase](../66-continue-rebase/README.md).
