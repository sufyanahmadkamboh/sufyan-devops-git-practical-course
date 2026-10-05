<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 71 · Git blame · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A teammate aligns the price column for readability, touching every line:

```bash
awk '{printf "%-12s %s\n", $1, $2}' prices.txt > p.tmp && mv p.tmp prices.txt
git commit -q -am "Align the prices"
git log --oneline -1
git blame prices.txt
```

```text
4a8b468 (HEAD -> main) Align the prices
4a8b4686 (Ada Lovelace 2026-10-05 03:49:42 +0200 1) espresso     2.50
4a8b4686 (Ada Lovelace 2026-10-05 03:49:42 +0200 2) latte        3.30
4a8b4686 (Ada Lovelace 2026-10-05 03:49:42 +0200 3) cappuccino   3.40
```

## Troubleshoot

Every line now points to "Align the prices": blame shows who touched the line last, even if the change was only
formatting. The real history of the latte price is hidden behind the reformatting commit.

## Fix

Tell blame to ignore that commit (and record it for everyone in `.git-blame-ignore-revs`):

```bash
git rev-parse HEAD > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
git blame prices.txt
git log --oneline -1 "$(git blame -L 2,2 --porcelain prices.txt | head -1 | cut -c1-40)"
```

```text
42670048 (Ada Lovelace 2026-01-05 09:03:00 +0000 1) espresso     2.50
594657b3 (Grace Hopper 2026-01-05 09:05:00 +0000 2) latte        3.30
42670048 (Ada Lovelace 2026-01-05 09:03:00 +0000 3) cappuccino   3.40
594657b Raise the latte price to 3.30
```

GitHub's blame view honours `.git-blame-ignore-revs` in the repository root too.
