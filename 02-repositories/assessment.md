# Module 02 · Repositories · Assessment

> Lessons 05–08 · ⏱ 30 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
mkdir -p ~/git-practice && rm -rf ~/git-practice/assess-02-shop && echo "lab ready"
bash scripts/new-lab.sh assess-02-broken basic
```

## Quiz

1. Where does Git store a repository's history and configuration?
2. What does `git init` create, and what does it not do?
3. Name the three areas a file moves through before it is in a commit.
4. In `git status --short`, what do `??`, ` M` and `M ` mean?
5. You delete the `.git` folder. What happens to your files and to the history?
6. Which option of `git init` sets the initial branch name?
7. Is an empty folder tracked by Git?

<details>
<summary>Answers</summary>

1. In the `.git` folder at the top of the working directory (lesson 05).
2. It creates an empty `.git` repository; it does not add or commit any file (lesson 06).
3. Working directory → staging area (index) → repository (lesson 07).
4. Untracked; modified but not staged; modified and staged (lesson 08).
5. The files stay; the history and Git configuration of that repository are gone (lesson 05).
6. `git init -b NAME` (or `init.defaultBranch` globally) (lesson 06).
7. No: Git tracks files; an empty folder needs a file such as `.gitkeep` (lesson 07).

</details>

## Practical challenge

Create a repository `~/git-practice/assess-02-shop` on branch `main` with `menu.txt` committed, `notes.txt` present
but untracked, and `prices.txt` modified after its commit (not staged).

<details>
<summary>Reference solution</summary>

<!-- test: contains=?? notes.txt; contains= M prices.txt; output -->
```bash
mkdir -p ~/git-practice/assess-02-shop && cd ~/git-practice/assess-02-shop
git init -q -b main
printf 'espresso\nlatte\n' > menu.txt && printf 'espresso 2.50\n' > prices.txt
git add menu.txt prices.txt && git commit -q -m "Add menu and prices"
echo "call the supplier" > notes.txt
echo "latte 3.20" >> prices.txt
git status --short
```

```text
 M prices.txt
?? notes.txt
```

</details>

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-02-shop
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "a repository on main"           '[ "$(git branch --show-current)" = main ]'
check "menu.txt committed"             'git cat-file -e HEAD:menu.txt'
check "notes.txt untracked"            'git status --short | grep -qx "?? notes.txt"'
check "prices.txt modified, unstaged"  'git status --short | grep -qx " M prices.txt"'
```

```text
ok       a repository on main
ok       menu.txt committed
ok       notes.txt untracked
ok       prices.txt modified, unstaged
```

## Troubleshooting challenge

In `assess-02-broken`, someone ran `git init` inside a subfolder by mistake, then tried to add it:

<!-- test: contains=embedded -->
```bash
cd ~/git-practice/assess-02-broken
mkdir -p docs && cd docs && git init -q && echo "# Docs" > guide.md && git add guide.md && git commit -q -m "Add guide" && cd ..
git add docs 2>&1 | grep -i "embedded" | head -1
```

Symptom: the outer repository records `docs` as a strange entry instead of the file:

<!-- test: contains=docs; output -->
```bash
git status --short
git ls-files --stage docs
```

```text
A  docs
160000 5b84e78a6e22b1055a9b63c05fae267c1034457d 0	docs
```

<details>
<summary>Solution</summary>

`docs/.git` made `docs` a separate repository; the outer repository can only record it as an embedded repository
(mode `160000`, a pointer to the inner commit), not its files. Unstage it, delete the inner `.git` (its single commit
is not needed: check with `git -C docs log` first in real life), and add the file normally (`-f` because the entry
was only staged, never committed):

<!-- test: contains=A  docs/guide.md; output -->
```bash
git rm -q --cached -f docs
rm -rf docs/.git
git add docs
git status --short
```

```text
A  docs/guide.md
```

</details>

## Real-world scenario

A colleague says: "I ran `git init` in my home folder by accident, and now every folder shows hundreds of untracked
files in my prompt." What happened, and what is the safe fix?

<details>
<summary>Model answer</summary>

`git init` created `~/.git`, so every folder below home is inside that repository. Check with
`git rev-parse --show-toplevel` (it prints the home folder) and `git -C ~ log` (no commits). If there are no commits
you need, removing `~/.git` (and only that folder) fixes it; no project files are touched. Repositories inside home
that have their own `.git` were never affected.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-02-shop ~/git-practice/assess-02-broken
```
