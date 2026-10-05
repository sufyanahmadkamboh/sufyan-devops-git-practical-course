# Lesson 88 · Git LFS

> Level 18 · Advanced repositories · ⏱ 25 minutes

## What are we learning?

Git keeps every version of every file forever, in every clone. For large binaries (images, videos, datasets, model
files, installers) that makes repositories huge and slow. **Git LFS** (Large File Storage) stores those files on a
separate server and keeps only small pointer files in Git. We set it up, look at a pointer, and fix a big file that
was committed without LFS.

## Visual

```text
 without LFS:  every version of logo.psd (50 MB × 30 versions) inside .git → every clone downloads 1.5 GB

 with LFS:     Git stores a 130-byte pointer:          LFS server stores the content:
               version https://git-lfs.github.com/spec/v1     oid sha256:4d7a… → 50 MB
               oid sha256:4d7a…
               size 52428800
               clone/checkout downloads only the versions actually checked out
```

GitHub rejects files over 100 MB (`GH001: Large files detected`) and warns from 50 MB.

## Lab setup

<!-- test: contains=lesson-88 -->
```bash
bash scripts/new-lab.sh lesson-88 basic
cd ~/git-practice/lesson-88
git init -q --bare ../lesson-88-server.git && git remote add origin ../lesson-88-server.git
git lfs install --skip-repo > /dev/null
git lfs version | cut -d' ' -f1
```

`git lfs install` (once per computer) registers LFS's filters in your Git configuration. Git for Windows includes LFS;
on Linux install the `git-lfs` package.

## Demonstration

Tell LFS which files to manage; the rule is stored in `.gitattributes` (committed):

<!-- test: contains=*.bin filter=lfs; output -->
```bash
git lfs track "*.bin"
cat .gitattributes
```

```text
Tracking "*.bin"
*.bin filter=lfs diff=lfs merge=lfs -text
```

Add a 2 MB file and commit as usual:

<!-- test: contains=menu-video.bin; output -->
```bash
head -c 2000000 /dev/zero | tr '\0' 'x' > menu-video.bin
git add .gitattributes menu-video.bin && git commit -q -m "Add the menu video"
git lfs ls-files
```

```text
be8889d3b8 * menu-video.bin
```

What Git actually stored is the pointer:

<!-- test: contains=version https://git-lfs.github.com/spec/v1; output -->
```bash
git cat-file -p HEAD:menu-video.bin
git cat-file -s HEAD:menu-video.bin
```

```text
version https://git-lfs.github.com/spec/v1
oid sha256:be8889d3b8893c11d290b8dcf682164c326a90e6998f6bddb25d9a3a02daf666
size 2000000
132
```

A push uploads the content to the LFS store (on the server, next to the Git objects), then the commits to Git:

<!-- test: contains=LFS objects on the server: 1; output -->
```bash
git push -q -u origin main 2>&1
echo "LFS objects on the server: $(find ../lesson-88-server.git/lfs/objects -type f | wc -l)"
```

```text
Uploading LFS objects: 100% (1/1), 0 B | 0 B/s, done.
LFS objects on the server: 1
```

## Command breakdown

| Command | What it does |
|---|---|
| `git lfs install` | enable LFS for your user (once) |
| `git lfs track "PATTERN"` | manage matching files with LFS (writes `.gitattributes`) |
| `git lfs ls-files` | files in LFS at HEAD |
| `git lfs pull` | download LFS content for the current checkout |
| `GIT_LFS_SKIP_SMUDGE=1 git clone …` | clone with pointers only (fast CI) |
| `git lfs migrate import --include="PATTERN"` | rewrite history: move existing files into LFS |

## Hands-on exercise

**Instructions.** Clone the server repository and confirm the clone has the real 2 MB file, not the pointer.

**Expected result.** `2000000` bytes.

<!-- test-run: cd ~/git-practice && git clone -q lesson-88-server.git lesson-88-clone -->

**Verification.**

<!-- test: contains=2000000 -->
```bash
cd ~/git-practice/lesson-88-clone
wc -c < menu-video.bin
```

## Break it

Someone commits a large file of a type that is **not** tracked yet, then adds the LFS rule afterwards:

<!-- test: contains=3000000; output -->
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

<!-- test: absent=dataset.csv; output -->
```bash
git lfs ls-files
```

```text
be8889d3b8 * menu-video.bin
```

## Fix

The commits are not pushed yet, so history can be rewritten: move every CSV in the unpushed commits into LFS.

<!-- test: contains=dataset.csv; output -->
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

## Real-world example

Game studios, ML teams and documentation sites track `*.psd`, `*.fbx`, `*.onnx`, `*.mp4` with LFS. In infrastructure
repositories, large files are usually a mistake (a downloaded binary, a Terraform provider cache, a database dump):
`.gitignore` them (lesson 73) and block them with a pre-commit size check (lesson 83) rather than storing them.

## Practice challenge

Clone without downloading LFS content (as a fast CI job that only needs the code would), and show that the file is a
pointer.

<details>
<summary>Solution</summary>

<!-- test: contains=version https://git-lfs.github.com/spec/v1; output -->
```bash
cd ~/git-practice
GIT_LFS_SKIP_SMUDGE=1 git clone -q lesson-88-server.git lesson-88-light
head -c 120 lesson-88-light/menu-video.bin; echo
```

```text
version https://git-lfs.github.com/spec/v1
oid sha256:be8889d3b8893c11d290b8dcf682164c326a90e6998f6bddb25d9a3a02daf666
s
```

</details>

## Recap

- LFS keeps large binaries out of Git history; Git stores pointers.
- `git lfs track` before adding the files; commit `.gitattributes`.
- Large files already committed: `git lfs migrate import` (rewrites history).

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-88 ~/git-practice/lesson-88-server.git ~/git-practice/lesson-88-clone ~/git-practice/lesson-88-light
```

Next: [Module 19 · Lesson 89 · Secrets in Git](../../19-security/89-secrets-in-git/README.md).
