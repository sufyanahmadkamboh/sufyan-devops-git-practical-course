<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 88 · Git LFS · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Someone commits a large file of a type that is **not** tracked yet, then adds the LFS rule afterwards:

```bash
cd ~/git-practice/lesson-88
head -c 3000000 /dev/zero | tr '\0' 'y' > dataset.csv
git add dataset.csv && git commit -q -m "Add the dataset"
git lfs track "*.csv" > /dev/null && git add .gitattributes && git commit -q -m "Track CSV files with LFS"
git cat-file -s HEAD:dataset.csv
```

```text
3000000
```

## Troubleshoot

The blob is 3,000,000 bytes: a full file inside Git, not a pointer. A tracking rule only applies to files added
**after** it; the existing commit already contains the big blob, and pushing it would put it in Git history forever
(on GitHub: rejected above 100 MB).

```bash
git lfs ls-files
```

```text
be8889d3b8 * menu-video.bin
```

## Fix

The commits are not pushed yet, so history can be rewritten: move every CSV in the unpushed commits into LFS.

```bash
git lfs migrate import --yes --include="*.csv" --include-ref=main --exclude-ref=refs/remotes/origin/main > /dev/null 2>&1
git cat-file -s HEAD:dataset.csv
git lfs ls-files
```

```text
132
a15eccdf74 - dataset.csv
be8889d3b8 * menu-video.bin
```

`--yes` answers its prompt about rewriting the working copy. (For commits already pushed and shared, the same rewrite needs a force push and every clone to be re-cloned: lesson 90
describes the procedure.)
