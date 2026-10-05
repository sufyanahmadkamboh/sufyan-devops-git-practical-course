<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 66 · Continuing a rebase · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

At an `edit` stop meant to **change** "Add mocha", commit without `--amend` (a very common slip), and continue:

```bash
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~2
sed -i 's/^mocha$/mocha (seasonal)/' menu.txt
git commit -q -am "Mark mocha as seasonal"
git rebase --continue
git log --oneline -3
```

```text
Stopped at 705a714...  # Add mocha
You can amend the commit now, with

  git commit --amend 

Once you are satisfied with your changes, run

  git rebase --continue
a83ed5c (HEAD -> main) Price mocha
585d1aa Mark mocha as seasonal
705a714 Add mocha
```

## Troubleshoot

No error: Git simply kept your extra commit. The history now has "Add mocha" **and** "Mark mocha as seasonal", instead
of one corrected "Add mocha". At an `edit` stop, `git commit` adds a commit; `git commit --amend` changes the stopped
one. Both are valid, so Git cannot warn you.

## Fix

Fold the extra commit into "Add mocha" with a second interactive rebase (`fixup` keeps the first message):

```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/fixup/'" git rebase -q -i HEAD~3
git log --oneline -3
git show HEAD~1 | grep "^+mocha"
```

```text
881b387 (HEAD -> main) Price mocha
e49b0d2 Add mocha
33f0085 Price green tea
+mocha (seasonal)
```
