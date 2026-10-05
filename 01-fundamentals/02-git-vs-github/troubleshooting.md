<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 02 · Git vs GitHub · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Push to a remote that does not exist (a typo in the path, a repository that was never created):

```bash
cd ~/git-practice/lesson-02
git remote add backup ~/git-practice/no-such-server/cafe.git
git push backup main 2>&1
```

```text
fatal: '/tmp/tmp.4t0bo0lUV9/git-practice/no-such-server/cafe.git' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

## Troubleshoot

The error names the remote it tried and says it is not a repository. Check what the remote points to:

```bash
git remote -v
```

## Fix

Point the remote at a real repository (here: create it), or remove the wrong remote:

```bash
git remote remove backup
git remote -v
git push origin main 2>&1 | tail -1 || true
git init -q --bare -b main ~/git-practice/lesson-02-backup.git
git remote add backup ~/git-practice/lesson-02-backup.git
git push backup main 2>&1
```
