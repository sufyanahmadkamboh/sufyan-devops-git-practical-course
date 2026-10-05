<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 46 · Connecting local Git to GitHub · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create a branch `docs`, push it with upstream, and list the branches that exist on GitHub.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-46
git switch -q -c docs
git push -q -u origin docs 2>&1
git ls-remote --heads origin
git push -q origin --delete docs 2>&1
```

```text
remote: 
remote: Create a pull request for 'docs' on GitHub by visiting:        
remote:      https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/new/docs        
remote: 
4267004871ae95e12690719f02460f9e3c935cf5	refs/heads/docs
070373402250336f9b54949196ebde41049c58e8	refs/heads/main
```

The last line deletes the branch on GitHub again, to keep the practice repository tidy.

</details>
