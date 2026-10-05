<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 12 · What actually happens during a commit? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Try to change an old commit's message "in place" by editing the history directly. You can't: the closest thing,
`--amend`, works only on the **latest** commit, and changes its ID:

```bash
before=$(git rev-parse --short HEAD)
git commit -q --amend -m "Add pricing (green tea)"
echo "before: $before  after: $(git rev-parse --short HEAD)"
git log --oneline -2
```

## Troubleshoot

Why can't an old commit simply be edited? Its ID is a hash of its content **including its parent's ID**. Changing a
commit changes its ID, which changes the parent recorded in every later commit, which changes all their IDs. History
is a chain of hashes: tamper with one link and every following link is different. That is what makes Git history
trustworthy, and why rewriting shared history causes trouble.

## Fix

Rewriting older commits is possible, as a deliberate new history, with interactive rebase (lesson 63). For a mistake
in the latest, unpushed commit, `--amend` (above) is the right tool. Put the message back:

```bash
git commit -q --amend -m "Add green tea"
git log --oneline -1
```
