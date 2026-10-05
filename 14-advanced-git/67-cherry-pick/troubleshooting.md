<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 67 · Cherry-pick · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Production also wants the Tuesday special:

```bash
git cherry-pick "$(git log --format=%h --grep='Tuesday' feature-specials)" 2>&1
```

```text
CONFLICT (modify/delete): specials.txt deleted in HEAD and modified in ea104e4 (Add Tuesday special).  Version ea104e4 (Add Tuesday special) of specials.txt left in tree.
error: could not apply ea104e4... Add Tuesday special
hint: After resolving the conflicts, mark them with
hint: "git add/rm <pathspec>", then run
hint: "git cherry-pick --continue".
hint: You can instead skip this commit with "git cherry-pick --skip".
hint: To abort and get back to the state before "git cherry-pick",
hint: run "git cherry-pick --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
```

## Troubleshoot

`CONFLICT (modify/delete): specials.txt deleted in HEAD and modified in …`: the Tuesday commit **modifies**
`specials.txt`, a file created by an earlier commit ("Start the specials board") that production does not have. A
cherry-picked commit carries only its own change, not the commits it depends on.

## Fix

Abort, and pick the dependency first, in order (a range):

```bash
git cherry-pick --abort
start=$(git log --format=%h --grep='Start the specials' feature-specials)
git cherry-pick "$start"
git cherry-pick "$(git log --format=%h --grep='Tuesday' feature-specials)"
cat specials.txt
```

```text
[production 9ab5895] Start the specials board
 Date: Mon Oct 5 03:49:31 2026 +0200
 1 file changed, 1 insertion(+)
 create mode 100644 specials.txt
[production 876cc7e] Add Tuesday special
 Date: Mon Oct 5 03:49:31 2026 +0200
 1 file changed, 1 insertion(+)
Monday: mocha
Tuesday: chai
```
