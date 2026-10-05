<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 12 · What actually happens during a commit? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-12 basic
cd ~/git-practice/lesson-12
git log --oneline
```

## Demonstration

```bash
git cat-file -p HEAD
```

```bash
git cat-file -p 'HEAD^{tree}'
```

```bash
echo "green tea" >> menu.txt && git add menu.txt
export GIT_AUTHOR_DATE="2026-01-05T10:00:00+00:00" GIT_COMMITTER_DATE="2026-01-05T10:00:00+00:00"
git commit -q -m "Add green tea";           echo "commit:               $(git rev-parse --short HEAD)"
git commit -q --amend -m "Add green tea";   echo "same everything:      $(git rev-parse --short HEAD)"
git commit -q --amend -m "Add green tea!";  echo "one character more:   $(git rev-parse --short HEAD)"
export GIT_COMMITTER_DATE="2026-01-05T10:01:00+00:00"
git commit -q --amend -m "Add green tea!";  echo "one minute later:     $(git rev-parse --short HEAD)"
unset GIT_AUTHOR_DATE GIT_COMMITTER_DATE
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-12
git log --format='%h  parents: %p  %s'
```

## Break it

```bash
before=$(git rev-parse --short HEAD)
git commit -q --amend -m "Add pricing (green tea)"
echo "before: $before  after: $(git rev-parse --short HEAD)"
git log --oneline -2
```

## Fix

```bash
git commit -q --amend -m "Add green tea"
git log --oneline -1
```

## Practice challenge

```bash
cd ~/git-practice/lesson-12
git rev-parse "$(git rev-list --max-parents=0 HEAD):README.md"
git rev-parse HEAD:README.md
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-12
```
