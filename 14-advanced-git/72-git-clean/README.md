# Lesson 72 · Git clean

> Level 14 · Advanced Git · ⏱ 15 minutes

## What are we learning?

`git clean` deletes **untracked** files: build output, temporary files, experiments. They are not in Git, so nothing
can bring them back. That is why we always preview with `-n` first.

## Visual

```text
 working directory
 ├── menu.txt          tracked          git clean never touches it
 ├── notes-draft.txt   untracked        git clean -f  deletes it
 ├── build/            untracked dir    git clean -fd deletes it
 └── .env              ignored          only git clean -x deletes it (careful: local secrets, config)

 ALWAYS:  git clean -n …   (dry run: "Would remove …")   then the same with -f
```

## Lab setup

<!-- test: contains=lesson-72 -->
```bash
bash scripts/new-lab.sh lesson-72 basic
cd ~/git-practice/lesson-72
echo ".env" > .gitignore && git add .gitignore && git commit -q -m "Ignore .env"
echo "draft" > notes-draft.txt
mkdir build && echo "binary" > build/app
echo "DB_PASSWORD=local-only" > .env
git status --short --ignored
```

## Demonstration

Without `-f`, Git refuses:

<!-- test: fail; contains=refusing to clean; output -->
```bash
git clean 2>&1
```

```text
fatal: clean.requireForce is true and -f not given: refusing to clean
```

Preview, then clean files and directories:

<!-- test: contains=Would remove build/; output -->
```bash
git clean -n -d
```

```text
Would remove build/
Would remove notes-draft.txt
```

<!-- test: contains=Removing build/; output -->
```bash
git clean -f -d
git status --short --ignored
```

```text
Removing build/
Removing notes-draft.txt
!! .env
```

`.env` survived: ignored files are only removed with `-x`.

## Command breakdown

| Command | Deletes |
|---|---|
| `git clean -n` | nothing: lists what `-f` would delete |
| `git clean -f` | untracked files |
| `git clean -fd` | untracked files and directories |
| `git clean -fX` | only ignored files (rebuild from scratch, keep your new files) |
| `git clean -fdx` | everything untracked, ignored included |
| `git clean -fd -e PATTERN` | … except PATTERN |
| `git clean -i` | interactive menu |

## Hands-on exercise

**Instructions.** Create two untracked files, `a.tmp` and `keep.txt`. Remove `a.tmp` only, using an exclude pattern.

**Expected result.** `keep.txt` remains.

<!-- test-run: cd ~/git-practice/lesson-72 && touch a.tmp keep.txt && git clean -q -f -e keep.txt -->

**Verification.**

<!-- test: contains=keep.txt; absent=a.tmp -->
```bash
cd ~/git-practice/lesson-72
ls
```

## Break it

"Make it like a fresh clone", with `-x` and without a preview:

<!-- test: contains=Removing .env; output -->
```bash
git clean -f -d -x
```

```text
Removing .env
Removing keep.txt
```

## Troubleshoot

`.env` held local settings and a password that are not in Git (on purpose: lesson 73). `git clean` does not use a
trash bin, the reflog or the stash: the file is gone. Git has no record of it:

<!-- test: contains=no such file -->
```bash
cat .env 2>&1 | sed 's/.*No such file.*/no such file/'
git log --all --oneline -- .env | wc -l
```

## Fix

Recreate it from the documented template (projects keep a `.env.example` for exactly this), and never use `-x` without
`-n` first:

<!-- test: contains=Would remove .env; output -->
```bash
printf 'DB_PASSWORD=change-me\n' > .env.example && git add .env.example && git commit -q -m "Add .env.example"
cp .env.example .env
git clean -n -d -x
```

```text
Would remove .env
```

The preview now shows `.env` would be removed: you see it **before** it happens.

## Real-world example

CI jobs and Dockerfiles often run `git clean -fdx` to guarantee a pristine build, which is fine on a disposable
runner. On your laptop, prefer `git clean -fdX` (capital X: only ignored build output) or `-n` first, and keep
`.env.example` / a secrets manager so local configuration can be restored.

## Practice challenge

Delete only ignored files (build caches), keeping your untracked work.

<details>
<summary>Solution</summary>

<!-- test: contains=Removing .env; contains=work.txt; output -->
```bash
cd ~/git-practice/lesson-72
echo "my work" > work.txt
git clean -f -X
ls
```

```text
Removing .env
README.md
menu.txt
prices.txt
work.txt
```

</details>

## Recap

- `git clean` permanently deletes untracked files; it requires `-f`.
- Always run `-n` first; `-d` for directories; `-x`/`-X` for ignored files.
- Keep templates (`.env.example`) for anything local you might wipe.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-72
```

Next: [Lesson 73 · .gitignore](../73-gitignore/README.md).
