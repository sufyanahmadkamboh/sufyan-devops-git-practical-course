<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 86 · Git submodules · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace clones the cafe repository the usual way:

```bash
git init -q --bare ../lesson-86-cafe.git && git push -q ../lesson-86-cafe.git main
cd .. && git clone -q lesson-86-cafe.git lesson-86-grace && cd lesson-86-grace
ls shared/ | wc -l
git submodule status
```

```text
0
-009710344304d0ac962666fbf91812d01aa6506f shared
```

## Troubleshoot

`shared/` is empty and `git submodule status` shows a leading `-`: the submodule is registered but not initialised. A
plain `git clone` does not fetch submodules. Anything that needs `shared/tax.txt` (a build, a deployment) fails.

## Fix

```bash
git -c protocol.file.allow=always submodule update --init
git submodule status
cat shared/tax.txt
```

```text
Submodule 'shared' (~/git-practice/lesson-86-shared.git) registered for path 'shared'
Cloning into '~/git-practice/lesson-86-grace/shared'...
done.
Submodule path 'shared': checked out '009710344304d0ac962666fbf91812d01aa6506f'
 009710344304d0ac962666fbf91812d01aa6506f shared (heads/main)
VAT 19%
Service included
```

Next time: `git clone --recurse-submodules`.
