<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 74 · How Git stores data · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-74 basic
cd ~/git-practice/lesson-74
```

## Demonstration

```bash
cat .git/refs/heads/main 2> /dev/null || git rev-parse main
git cat-file -p main
```

```bash
git cat-file -p 'main^{tree}'
```

```bash
git cat-file -p "$(git rev-parse main:prices.txt)"
```

```bash
git rev-parse main:prices.txt
printf 'espresso 2.50\nlatte 3.20\ncappuccino 3.40\n' | git hash-object --stdin
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-74
git count-objects -v | head -1
```

## Break it

```bash
obj=$(git rev-parse main:menu.txt)
f=".git/objects/${obj:0:2}/${obj:2}"
chmod u+w "$f" && printf 'garbage' > "$f"
git show main:menu.txt 2>&1
```

## Troubleshoot

```bash
obj=$(git rev-parse main:menu.txt)
git fsck --full 2>&1 | head -5 | sed "s/$obj/$obj (menu.txt)/"
test "${PIPESTATUS[0]}" -eq 0
```

## Fix

```bash
obj=$(git rev-parse main:menu.txt)
rm -f ".git/objects/${obj:0:2}/${obj:2}"
printf 'espresso\nlatte\ncappuccino\n' | git hash-object -w --stdin
git fsck --full && git show main:menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-74
cp menu.txt menu-copy.txt && git add menu-copy.txt && git commit -q -m "Copy the menu"
[ "$(git rev-parse HEAD:menu.txt)" = "$(git rev-parse HEAD:menu-copy.txt)" ] && echo "same blob: no new blob, only a new tree and commit"
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-74
```
