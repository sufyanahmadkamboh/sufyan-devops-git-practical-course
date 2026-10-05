<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 65 · Aborting a rebase · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Forget that a rebase is still in progress (a terminal closed, a day later), and start another one:

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

```bash
git rebase --abort
git status
```
