<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 44 · What is GitHub? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Clone a repository whose name is misspelled:

```bash
cd ~/git-practice/lesson-44
git clone https://github.com/octocat/Hello-Wrld 2>&1
```

```text
Cloning into 'Hello-Wrld'...
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

## Troubleshoot

GitHub does not say "this repository does not exist". For a repository you cannot see, it answers "authentication
required", because a private repository with that name **might** exist and GitHub will not reveal it to strangers. So
Git asks for a username (in this course's test setup prompts are disabled, so it stops with `could not read
Username`; on your computer a login window or a `Username for 'https://github.com':` prompt appears).

A username prompt for a public repository therefore usually means: **wrong owner or name**, or a private repository you
have no access to. Check the name before typing any credentials.

## Fix

```bash
rm -rf Hello-World
git clone https://github.com/octocat/Hello-World 2>&1
```
