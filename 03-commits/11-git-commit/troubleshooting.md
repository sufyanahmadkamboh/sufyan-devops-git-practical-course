<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 11 · git commit · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A typo in the message, and a forgotten file:

```bash
echo "Open 8-18" > hours.txt
echo "Closed on public holidays" > holidays.txt
git add hours.txt
git commit -q -m "Add hte opening hours"
git log --oneline -1
```

## Troubleshoot

The summary has a typo and `holidays.txt` belongs to the same change but is still untracked. The commit has **not**
been pushed (no remote here at all), so it is safe to rewrite it.

## Fix

```bash
git add holidays.txt
git commit -q --amend -m "Add the opening hours"
git log --oneline -1
git show --stat --format= HEAD
```

```text
026b507 Add the opening hours
 holidays.txt | 1 +
 hours.txt    | 1 +
 2 files changed, 2 insertions(+)
```

`--amend` replaced the commit: same parent, new snapshot, new message, **new ID**. Never amend a commit that others
already pulled: their copy still has the old one (lesson 32 shows the safe alternative, `git revert`).
