<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 04 · First Git configuration · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Make every repository under `~/git-practice/work/` use the e-mail `ada@work.example.com` automatically, without setting
it in each repository. (Hint: `includeIf "gitdir:..."` in `~/.gitconfig`.)

<details>
<summary>Solution</summary>

```bash
printf '[user]\n\temail = ada@work.example.com\n' > ~/.gitconfig-work
git config --global includeIf."gitdir:~/git-practice/work/".path '~/.gitconfig-work'
mkdir -p ~/git-practice/work/project && cd ~/git-practice/work/project && git init -q
git config --show-origin --get user.email
```

```text
file:~/.gitconfig-work	ada@work.example.com
```

The conditional include applies the extra file only to repositories inside that folder. Quote `'~/...'` so that
Git, not your shell, expands the `~`: that works the same on every system.

</details>
