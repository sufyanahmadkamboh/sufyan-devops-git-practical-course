<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 88 · Git LFS · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Clone without downloading LFS content (as a fast CI job that only needs the code would), and show that the file is a
pointer.

<details>
<summary>Solution</summary>

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
