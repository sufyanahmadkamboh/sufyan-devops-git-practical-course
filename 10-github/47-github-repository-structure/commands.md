<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 47 · GitHub repository structure · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-47 empty
cd ~/git-practice/lesson-47
```

```bash
me=$(gh api user --jq .login)
gh repo clone "$me/git-practice-cafe" 2>&1
cd git-practice-cafe
```

## Demonstration

```bash
ls
git branch -r
git tag
```

```bash
echo "issues:   $(gh issue list --state all --json number --jq length)"
echo "PRs:      $(gh pr list --state all --json number --jq length)"
echo "runs:     $(gh run list --json databaseId --jq length)"
echo "releases: $(gh release list --json tagName --jq length)"
```

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe" --jq '{default_branch, visibility, has_issues, allow_squash_merge, delete_branch_on_merge}'
```

## Hands-on exercise

```bash
url=$(gh repo view --json url --jq .url)
for tab in "" /issues /pulls /actions /releases /branches /tags; do echo "$url$tab"; done
```

## Break it

```bash
cd ~/git-practice/lesson-47
gh issue list 2>&1
```

## Fix

```bash
me=$(gh api user --jq .login)
gh issue list -R "$me/git-practice-cafe" > /dev/null && echo OK
```

## Practice challenge

```bash
cd ~/git-practice/lesson-47/git-practice-cafe
gh repo view | head -8
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-47
```
