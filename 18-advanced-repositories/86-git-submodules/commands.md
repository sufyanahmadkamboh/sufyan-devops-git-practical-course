<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 86 · Git submodules · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-86 basic
cd ~/git-practice
git init -q --bare lesson-86-shared.git
git clone -q lesson-86-shared.git lesson-86-shared-work 2> /dev/null
cd lesson-86-shared-work
echo "VAT 19%" > tax.txt && git add tax.txt && git commit -q -m "Add the tax rule" && git push -q origin HEAD:main
cd ../lesson-86
```

## Demonstration

```bash
git -c protocol.file.allow=always submodule add -q ../lesson-86-shared.git shared
cat .gitmodules
git status --short
```

```bash
git commit -q -m "Add the shared rules as a submodule"
git ls-tree HEAD shared
cat shared/tax.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-86
git -c protocol.file.allow=always submodule update -q --remote shared
git diff --submodule=log | head -3
git commit -q -am "Update the shared rules"
cat shared/tax.txt
```

## Break it

```bash
git init -q --bare ../lesson-86-cafe.git && git push -q ../lesson-86-cafe.git main
cd .. && git clone -q lesson-86-cafe.git lesson-86-grace && cd lesson-86-grace
ls shared/ | wc -l
git submodule status
```

## Fix

```bash
git -c protocol.file.allow=always submodule update --init
git submodule status
cat shared/tax.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-86-grace
git config submodule.recurse true
git config --get submodule.recurse
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-86 ~/git-practice/lesson-86-shared.git ~/git-practice/lesson-86-shared-work ~/git-practice/lesson-86-cafe.git ~/git-practice/lesson-86-grace
```
