<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 97 · Releases · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Publish v1.1.0 again with corrected notes:

```bash
gh release create v1.1.0 --notes "New drinks: green tea and chai." 2>&1
```

```text
HTTP 422: Validation Failed (https://api.github.com/repos/sufyanahmadkamboh/git-practice-cafe/releases)
Release.tag_name already exists
```

## Troubleshoot

A tag can have one release, and a published version number must never be reused for different content (users,
caches and lock files already refer to it). Changing the **text** of a release is fine; changing its **code** means a
new version.

## Fix

```bash
gh release edit v1.1.0 --notes "New drinks: green tea and chai." > /dev/null
gh release view v1.1.0 --json tagName,body --jq '"\(.tagName): \(.body)"'
```

```text
v1.1.0: New drinks: green tea and chai.
```
