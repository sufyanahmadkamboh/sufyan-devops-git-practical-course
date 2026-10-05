<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 42 · git push · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-42 remote
cd ~/git-practice/lesson-42/ada
```

## Demonstration

```bash
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git push
```

```bash
git switch -q -c feature-chai && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push origin feature-chai
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-42/ada
git ls-remote --heads origin
```

## Break it

```bash
cd ../grace && git pull -q && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" && git push -q
cd ../ada && git switch -q main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git push 2>&1
```

## Fix

```bash
git pull -q --rebase
git push
git log --oneline -3
```

## Practice challenge

```bash
cd ~/git-practice/lesson-42/grace && git pull -q && echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q
cd ../ada && git commit -q --amend -m "Raise the espresso price to 2.60"
git push --force-with-lease 2>&1 || true
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-42
```
