<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 06 · git init · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

The most common mistake: `git init` in the wrong place, typically your home folder. Simulate it:

```bash
cd ~/git-practice/lesson-06
mkdir -p home-sim/projects/website && cd home-sim
git init -q
cd projects/website
echo "<h1>Hi</h1>" > index.html
git status --short
git rev-parse --show-toplevel
```

```text
?? ../
~/git-practice/lesson-06/home-sim
```

## Troubleshoot

`git status` inside `website` shows files from the wrong level, and `--show-toplevel` reveals the repository root is
`home-sim`, two levels up: every folder below it is now "inside" that accidental repository. Symptoms in real life:
`git status` listing your whole home folder, or a project that suddenly "has" thousands of untracked files.

## Fix

Remove the accidental `.git` (only the one you created by mistake: check the path first!), then initialise in the
right folder:

```bash
cd ~/git-practice/lesson-06/home-sim
ls -A
rm -rf .git
cd projects/website && git init -q
git rev-parse --show-toplevel
```
