<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 68 · Git tags · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Push the branch and expect the tags on the server:

```bash
git push -q
git ls-remote --tags origin | grep . || echo "no tags on the server"
```

```text
no tags on the server
```

## Troubleshoot

`git push` sends branches, not tags. Grace, cloning or fetching from the server, would not see `v1.0.0`, and a CI job
triggered "on tag push" would never run.

## Fix

```bash
git push origin v1.0.0 2>&1
git ls-remote --tags origin
```

```text
To ~/git-practice/lesson-68/server/cafe.git
 * [new tag]         v1.0.0 -> v1.0.0
4267004871ae95e12690719f02460f9e3c935cf5	refs/tags/v1.0.0
```

(`git push --tags` would also push `v0.9.0`; push the tags you mean to publish.)
