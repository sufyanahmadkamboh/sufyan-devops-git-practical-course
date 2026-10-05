# Project 1 · Personal Git repository

> Level 24 · Projects · beginner · ⏱ 60 minutes · lessons 01–22, 37–43, 68, 73

## Brief

You keep your own notes and scripts (dotfiles, small tools, a reading list) scattered across folders. Turn them into a
clean personal repository: tracked from the first file, with meaningful commits, an ignore file, a feature branch, a
first release tag, and a copy on a remote.

## Requirements

1. A repository `my-notes` with `main` as the default branch and your identity configured.
2. At least five commits, each with one purpose and a clear message (`docs: …`, `feat: …`).
3. A `.gitignore` that keeps editor files, logs and `.env` out; an `.env` file exists locally but is not tracked.
4. One feature developed on a branch and merged into `main`.
5. An annotated tag `v0.1.0`.
6. A remote `origin` with `main` and the tag pushed (a local bare repository here; your GitHub account in real life).

## Starting point

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh project-1 empty
cd ~/git-practice/project-1
git status | head -2
```

## Hints

- `git switch -c NAME`, `git merge --no-ff`, `git tag -a`, `git push --follow-tags` (lessons 20, 24, 69, 43).
- Check before each commit: `git status` and `git diff --cached` (lessons 08, 15).

## Reference solution

Try it yourself first.

<details>
<summary>Show the reference solution</summary>

<!-- test: contains=v0.1.0; output -->
```bash
cd ~/git-practice/project-1
printf '# My notes\n\nPersonal notes and small scripts.\n' > README.md
git add README.md && git commit -q -m "docs: add README"
printf '.vscode/\n.idea/\n*.log\n.env\n' > .gitignore
git add .gitignore && git commit -q -m "chore: ignore editor files, logs and .env"
mkdir -p notes scripts
printf '# Git\n\n- git switch -c NAME\n' > notes/git.md
git add notes && git commit -q -m "docs: add Git notes"
printf '#!/usr/bin/env bash\n# backup.sh: copy notes to a backup folder\ncp -r notes "${1:-$HOME/notes-backup}"\n' > scripts/backup.sh
git add scripts && git commit -q -m "feat: add the backup script"
echo "API_KEY=local-only" > .env && echo "debug" > run.log
git switch -q -c feature/reading-list
printf '# Reading list\n\n- Pro Git, chapter 3\n' > notes/reading.md
git add notes/reading.md && git commit -q -m "docs: add a reading list"
git switch -q main && git merge -q --no-ff -m "Merge branch 'feature/reading-list'" feature/reading-list
git branch -d -q feature/reading-list
git tag -a v0.1.0 -m "First version of my notes"
git init -q --bare ../project-1-remote.git
git remote add origin ../project-1-remote.git
git push -q -u origin main --follow-tags
git log --oneline --graph --decorate
```

```text
*   06833af (HEAD -> main, tag: v0.1.0, origin/main) Merge branch 'feature/reading-list'
|\  
| * 775f408 docs: add a reading list
|/  
* ce9acba feat: add the backup script
* 1dfa938 docs: add Git notes
* 728d73f chore: ignore editor files, logs and .env
* 2b7e13e docs: add README
```

</details>

## Self-check

Run this in your repository; every line should say `ok`:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/project-1
check() { if eval "$2" > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "on main"                          '[ "$(git branch --show-current)" = main ]'
check "at least 5 commits"               '[ "$(git rev-list --count HEAD)" -ge 5 ]'
check ".gitignore ignores .env and logs" 'git check-ignore -q .env && git check-ignore -q run.log'
check ".env exists but is not tracked"   '[ -f .env ] && ! git ls-files --error-unmatch .env'
check "a merged feature branch"          '[ "$(git rev-list --merges --count HEAD)" -ge 1 ]'
check "annotated tag v0.1.0"             '[ "$(git cat-file -t v0.1.0)" = tag ]'
check "main and the tag on the remote"   'git ls-remote --exit-code origin refs/heads/main refs/tags/v0.1.0'
```

```text
ok       on main
ok       at least 5 commits
ok       .gitignore ignores .env and logs
ok       .env exists but is not tracked
ok       a merged feature branch
ok       annotated tag v0.1.0
ok       main and the tag on the remote
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/project-1 ~/git-practice/project-1-remote.git
```

Next: [Project 2 · Team collaboration](project-2-team-collaboration.md)
