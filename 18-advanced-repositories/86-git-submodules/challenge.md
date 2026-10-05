<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 86 · Git submodules · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Make `git pull` in Grace's clone update the submodule automatically.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-86-grace
git config submodule.recurse true
git config --get submodule.recurse
```

```text
true
```

</details>
