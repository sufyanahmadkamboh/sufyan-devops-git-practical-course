# Problem 13 · Large file rejected

> Troubleshooting lab · run every command from the course folder · related lessons: [88](../18-advanced-repositories/88-git-lfs/README.md), [83](../17-hooks/83-pre-commit-hook/README.md), [63](../13-rebase/63-interactive-rebase/README.md)

## Problem

A push is rejected because one commit contains a file over the server's size limit. Deleting the file in a new
commit does not help.

GitHub rejects files over **100 MB** with `GH001: Large files detected`. To keep the lab small and offline, the lab
server enforces a **1 MB** limit with a `pre-receive` hook that answers the same way (a simulation of GitHub's check).

<!-- test: contains=lesson-t13 -->
```bash
bash scripts/new-lab.sh lesson-t13 remote
cd ~/git-practice/lesson-t13
cat > server/cafe.git/hooks/pre-receive << 'EOF'
#!/usr/bin/env bash
# simulate GitHub's file size limit (GitHub: 100 MB; this lab: 1 MB)
limit=1000000
while read -r old new ref; do
  range="$new"; [ "$old" != 0000000000000000000000000000000000000000 ] && range="$old..$new"
  git rev-list --objects "$range" | while read -r obj path; do
    [ -n "$path" ] || continue
    if [ "$(git cat-file -t "$obj")" = blob ] && [ "$(git cat-file -s "$obj")" -gt $limit ]; then
      echo "error: File $path is $(( $(git cat-file -s "$obj") / 1000 )) kB; this exceeds the file size limit of 1 MB"
      echo "error: GH001: Large files detected. You may want to try Git Large File Storage"
      exit 1
    fi
  done || exit 1
done
EOF
chmod +x server/cafe.git/hooks/pre-receive
cd ada
head -c 3000000 /dev/zero | tr '\0' 'x' > menu-photos.zip
git add menu-photos.zip && git commit -q -m "Add menu photos"
echo "chai" >> menu.txt && git commit -q -am "Add chai"
```

## Symptoms

<!-- test: fail; contains=GH001: Large files detected; output -->
```bash
git push 2>&1
```

```text
remote: error: File menu-photos.zip is 3000 kB; this exceeds the file size limit of 1 MB        
remote: error: GH001: Large files detected. You may want to try Git Large File Storage        
To ~/git-practice/lesson-t13/server/cafe.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to '~/git-practice/lesson-t13/server/cafe.git'
```

The obvious attempt does not work either:

<!-- test: fail; contains=GH001; output -->
```bash
git rm -q menu-photos.zip && git commit -q -m "Remove the photos"
git push 2>&1 | grep -E "GH001|rejected"
test "${PIPESTATUS[0]}" -eq 0
```

```text
remote: error: GH001: Large files detected. You may want to try Git Large File Storage        
 ! [remote rejected] main -> main (pre-receive hook declined)
```

## Investigation

Which unpushed commits are there, and which contains the big file?

<!-- test: contains=Add menu photos; output -->
```bash
git log --oneline origin/main..main
git log --oneline --stat origin/main..main -- menu-photos.zip
```

```text
c32377e (HEAD -> main) Remove the photos
5bc06de Add chai
636a6a3 Add menu photos
c32377e (HEAD -> main) Remove the photos
 menu-photos.zip | 1 -
 1 file changed, 1 deletion(-)
636a6a3 Add menu photos
 menu-photos.zip | 1 +
 1 file changed, 1 insertion(+)
```

## Commands

| Command | Shows |
|---|---|
| `git log origin/main..main` | the commits a push would send |
| `git log --stat -- FILE` | which of them touch FILE |
| `git rev-list --objects origin/main..main` + `git cat-file -s` | the size of every object being sent |

## Understand the output

A push sends **every** commit not yet on the server, and "Add menu photos" contains the 3 MB blob. "Remove the
photos" only adds a new snapshot without it; the old commit (and its blob) is still part of what is pushed.

## Root cause

A large binary was committed into history. The server checks every pushed object, not only the latest snapshot.

## Fix

The commits are not pushed, so rewrite them: drop the file from "Add menu photos" with an interactive rebase (or move it
to Git LFS with `git lfs migrate import`, lesson 88). Here the photos do not belong in Git at all:

<!-- test: contains=Add chai; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i -e '/Add menu photos/s/^pick/drop/' -e '/Remove the photos/s/^pick/drop/'" git rebase -q -i origin/main
git log --oneline origin/main..main
git push 2>&1 | tail -1
```

```text
9fb51e2 (HEAD -> main) Add chai
   4267004..9fb51e2  main -> main
```

## Verification

<!-- test: contains=0; output -->
```bash
git --git-dir=../server/cafe.git log --all --oneline -- menu-photos.zip | wc -l
git status | head -2
```

```text
0
On branch main
Your branch is up to date with 'origin/main'.
```

## Prevention

- `.gitignore` for archives, media and build output; store them in object storage or a release asset.
- Git LFS for large files that must be versioned (`git lfs track` **before** adding them).
- A pre-commit hook that blocks files over a size limit (lesson 83).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t13
```

Next: [Problem 14 · Rebase conflict](problem-14-rebase-conflict.md)
