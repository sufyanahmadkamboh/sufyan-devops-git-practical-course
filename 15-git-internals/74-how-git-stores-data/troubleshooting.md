<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 74 · How Git stores data · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Corrupt an object file (simulating a disk error), then use the repository:

```bash
obj=$(git rev-parse main:menu.txt)
f=".git/objects/${obj:0:2}/${obj:2}"
chmod u+w "$f" && printf 'garbage' > "$f"
git show main:menu.txt 2>&1
```

```text
error: inflate: data stream error (incorrect header check)
error: unable to unpack 6c76265ddb2eef943f09b0eac893294d1827affa header
error: inflate: data stream error (incorrect header check)
error: unable to unpack 6c76265ddb2eef943f09b0eac893294d1827affa header
error: inflate: data stream error (incorrect header check)
error: unable to unpack 6c76265ddb2eef943f09b0eac893294d1827affa header
fatal: loose object 6c76265ddb2eef943f09b0eac893294d1827affa (stored in .git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa) is corrupt
```

## Troubleshoot

The object file no longer decompresses to content whose hash matches its name; Git detects it (every object is
verified by its hash) and refuses to use it. `git fsck` checks the whole repository:

```bash
obj=$(git rev-parse main:menu.txt)
git fsck --full 2>&1 | head -5 | sed "s/$obj/$obj (menu.txt)/"
test "${PIPESTATUS[0]}" -eq 0
```

```text
error: inflate: data stream error (incorrect header check)
error: unable to unpack header of .git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa
error: 6c76265ddb2eef943f09b0eac893294d1827affa (menu.txt): object corrupt or missing: .git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa
missing blob 6c76265ddb2eef943f09b0eac893294d1827affa (menu.txt)
```

## Fix

A blob is defined by its content: write the same content again and Git recreates exactly the same object. In real
life you get the content back from another clone (`git fetch` from the remote restores missing objects).

```bash
obj=$(git rev-parse main:menu.txt)
rm -f ".git/objects/${obj:0:2}/${obj:2}"
printf 'espresso\nlatte\ncappuccino\n' | git hash-object -w --stdin
git fsck --full && git show main:menu.txt
```

```text
6c76265ddb2eef943f09b0eac893294d1827affa
espresso
latte
cappuccino
```
