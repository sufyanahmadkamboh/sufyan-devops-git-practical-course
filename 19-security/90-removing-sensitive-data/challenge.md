<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 90 · Removing sensitive data · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Instead of deleting a whole file, replace one leaked string everywhere in history with `***REMOVED***`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-90
git init -q text-demo && cd text-demo
printf 'host=db\npassword=Cafe-2026-not-a-real-password\n' > app.conf && git add app.conf && git commit -q -m "Add app.conf"
echo 'Cafe-2026-not-a-real-password==>***REMOVED***' > ../replacements.txt
git filter-repo --force --replace-text ../replacements.txt > /dev/null 2>&1
git show HEAD:app.conf
```

```text
host=db
password=***REMOVED***
```

</details>
