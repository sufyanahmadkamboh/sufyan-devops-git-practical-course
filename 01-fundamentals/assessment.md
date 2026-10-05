# Module 01 · Git fundamentals · Assessment

> Lessons 01–04 · ⏱ 30 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-01-identity empty
bash scripts/new-lab.sh assess-01-broken basic
```

## Quiz

1. Git is: (a) a website for hosting code, (b) a distributed version control system, (c) a backup service.
2. Name two things GitHub adds on top of Git.
3. Does every clone of a Git repository contain the full history?
4. Which command shows the installed Git version?
5. Which two settings must be configured before your first commit, and why?
6. What is the difference between `git config --global` and `git config --local`?
7. Which scope wins when the same setting is defined globally and locally?
8. Which command shows every setting together with the file it comes from?

<details>
<summary>Answers</summary>

1. (b): Git records snapshots of a project's history locally (lesson 01).
2. Any two of: pull requests, reviews, issues, Actions, releases, access control (lesson 02).
3. Yes: every clone is a full copy, which is what "distributed" means (lesson 01).
4. `git --version` (lesson 03).
5. `user.name` and `user.email`: they are written into every commit as author and committer (lesson 04).
6. `--global` writes `~/.gitconfig` (all repositories of your user); `--local` writes `.git/config` (one repository) (lesson 04).
7. The local one: the most specific scope wins (lesson 04).
8. `git config --list --show-origin` (add `--show-scope` for the scope) (lesson 04).

</details>

## Practical challenge

In `~/git-practice/assess-01-identity`, use a separate identity for this repository only: name "Ada Lovelace", email
`ada@work.example.com`, and default branch `main` for new repositories (already global from lesson 04). Make one commit
and prove it carries the work email, while your global email is unchanged.

<details>
<summary>Reference solution</summary>

<!-- test: contains=ada@work.example.com; output -->
```bash
cd ~/git-practice/assess-01-identity
git config --local user.name "Ada Lovelace"
git config --local user.email "ada@work.example.com"
echo "# Work notes" > README.md && git add README.md && git commit -q -m "Add README"
git log -1 --format='%an <%ae>'
```

```text
Ada Lovelace <ada@work.example.com>
```

</details>

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-01-identity
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "local email is the work email"     '[ "$(git config --local user.email)" = ada@work.example.com ]'
check "the commit carries the work email" '[ "$(git log -1 --format=%ae)" = ada@work.example.com ]'
check "global email unchanged"            '[ "$(git config --global user.email)" = ada@example.com ]'
check "branch is main"                    '[ "$(git branch --show-current)" = main ]'
```

```text
ok       local email is the work email
ok       the commit carries the work email
ok       global email unchanged
ok       branch is main
```

## Troubleshooting challenge

Someone set a wrong local email in `assess-01-broken` and committed with it:

<!-- test: contains=wrong.example.com -->
```bash
cd ~/git-practice/assess-01-broken
git config --local user.email "ada@wrong.example.com"
echo "chai" >> menu.txt && git commit -q -am "Add chai"
git config --local user.email
```

Symptom:

<!-- test: contains=ada@wrong.example.com; output -->
```bash
git log -2 --format='%h %an <%ae> %s'
git config --show-origin user.email
```

```text
da9e16f Ada Lovelace <ada@wrong.example.com> Add chai
4267004 Ada Lovelace <ada@example.com> Add prices
file:.git/config	ada@wrong.example.com
```

<details>
<summary>Solution</summary>

The local setting (`.git/config`) overrides the global one. Remove it, then re-author the unpushed commit:

<!-- test: contains=ada@example.com; output -->
```bash
git config --local --unset user.email
git commit -q --amend --no-edit --reset-author
git log -1 --format='%h %an <%ae> %s'
git config --show-origin user.email
```

```text
e89e51b Ada Lovelace <ada@example.com> Add chai
file:~/.gitconfig	ada@example.com
```

</details>

## Real-world scenario

You use the same laptop for personal open-source work and for your employer. Last week several commits to the
company repository went out with your personal email, and the company's audit tooling flagged them. How do you make
the right email automatic per folder?

<details>
<summary>Model answer</summary>

Keep the personal identity global, and add a conditional include for the work folder, as in lesson 04:
`git config --global includeIf.gitdir:~/work/.path ~/.gitconfig-work`, with `~/.gitconfig-work` setting the work
`user.email`. Every repository under `~/work/` then uses the work email automatically; check with
`git config --show-origin user.email` inside a work repository. Already pushed commits keep their author; fixing them
would rewrite shared history, so only do it if the company requires it and the team agrees.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-01-identity ~/git-practice/assess-01-broken
```
