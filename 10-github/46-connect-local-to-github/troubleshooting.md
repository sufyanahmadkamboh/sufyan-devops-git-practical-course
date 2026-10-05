<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 46 · Connecting local Git to GitHub · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A typo in the repository name when adding the remote:

```bash
me=$(gh api user --jq .login)
git remote set-url origin "https://github.com/$me/git-practise-cafe.git"
git ls-remote origin 2>&1
```

```text
remote: Repository not found.
fatal: repository 'https://github.com/sufyanahmadkamboh/git-practise-cafe.git/' not found
```

## Troubleshoot

`remote: Repository not found.` Now that Git is authenticated (unlike lesson 44), GitHub says it clearly: under this
owner there is no repository with that name, or you have no access to it. Compare the remote URL with the page URL:

```bash
git remote get-url origin
```

## Fix

```bash
me=$(gh api user --jq .login)
git remote set-url origin "https://github.com/$me/git-practice-cafe.git"
git ls-remote --heads origin
```

```text
070373402250336f9b54949196ebde41049c58e8	refs/heads/main
```
