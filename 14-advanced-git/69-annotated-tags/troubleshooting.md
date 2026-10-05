<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 69 · Annotated tags · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

In a repository with **only lightweight** tags, the build script calls `git describe`:

```bash
git tag -d v1.0.0 > /dev/null
git describe 2>&1
```

```text
fatal: No annotated tags can describe 'ecff18af63d0d85da66114f18c12b06e2ae9888b'.
However, there were unannotated tags: try --tags.
```

## Troubleshoot

`No annotated tags can describe '…'. However, there were unannotated tags: try --tags.`: `git describe` uses only
annotated tags by default, because lightweight tags are often temporary, personal markers. The version a build
reports must come from a real release tag.

## Fix

Create the release as an annotated tag (or, if lightweight tags are intentional, `git describe --tags`):

```bash
git tag -a v1.0.0 4267004 -m "Release 1.0.0"
git describe
git describe --tags --abbrev=0 HEAD~4
```

```text
v1.0.0-4-gecff18a
v1.0.0
```
