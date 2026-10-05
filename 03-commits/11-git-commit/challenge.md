<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 11 · git commit · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Make a commit whose message has a summary line and a two-line body, using only `git commit` with an editor command
that writes the message for you (as Git would with your editor). Hint: `GIT_EDITOR` can be any command that edits the
file passed to it.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-11
echo "mocha" >> menu.txt && git add menu.txt
GIT_EDITOR='printf "Add a mocha\n\nCustomers asked for it.\nPrice follows tomorrow.\n" >' git commit -q
git log -1 --format='%s%n---%n%b'
```

```text
Add a mocha
---
Customers asked for it.
Price follows tomorrow.
```

Git writes a template into `.git/COMMIT_EDITMSG` and runs the editor on it; whatever the file contains afterwards
(minus `#` comment lines) becomes the message.

</details>
