<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 67 · Cherry-pick · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-67 basic
cd ~/git-practice/lesson-67
git branch production
git switch -q -c feature-specials
echo "Monday: mocha" > specials.txt && git add specials.txt && git commit -q -m "Start the specials board"
sed -i 's/cappuccino 3.40/cappuccino 3.50/' prices.txt && git commit -q -am "Fix the cappuccino price (charged too little)"
echo "Tuesday: chai" >> specials.txt && git commit -q -am "Add Tuesday special"
git log --oneline --graph --all
```

## Demonstration

```bash
fix=$(git log --format=%h --grep="Fix the cappuccino price" feature-specials)
git switch -q production
git cherry-pick "$fix"
git log --oneline -2
ls
```

```bash
git show "$fix" | git patch-id | cut -c1-12
git show HEAD | git patch-id | cut -c1-12
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-67
git cherry -v production feature-specials
```

## Break it

```bash
git cherry-pick "$(git log --format=%h --grep='Tuesday' feature-specials)" 2>&1
```

## Fix

```bash
git cherry-pick --abort
start=$(git log --format=%h --grep='Start the specials' feature-specials)
git cherry-pick "$start"
git cherry-pick "$(git log --format=%h --grep='Tuesday' feature-specials)"
cat specials.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-67
git switch -q -c release-1.0 4267004
git cherry-pick -x "$(git log --format=%h --grep='Fix the cappuccino' feature-specials)" > /dev/null
git log -1 --format=%B
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-67
```
