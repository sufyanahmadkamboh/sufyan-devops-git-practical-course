# Tests: every command in the course runs

The lessons are Markdown, and every Bash block in them is also a test. `tests/mdrun.py` reads a lesson, runs its blocks
in order (the working directory carries over from block to block, as in a terminal), checks each output against the
expectation written above the block, and can write the real output back into the lesson.

## Run lessons

```text
bash tests/run.sh 05-branches/*/README.md                         run a module
bash tests/run.sh --update FILE.md …                              …and write the real outputs into the lessons
bash tests/run.sh --update --record tests/out FILE.md …           …and keep every command + output (for the video)
MDRUN_GITHUB=1 bash tests/run.sh …                                also run the blocks that need a GitHub account
```

Lessons after lesson 04 assume the Git identity that lesson 04 configures; when running a single later lesson, put
`01-fundamentals/04-first-configuration/README.md` first.

## The sandbox (tests/run.sh)

| Isolation | Why |
|---|---|
| a temporary `HOME` | your `~/.gitconfig`, `~/git-practice` and `~/.ssh` are never read or changed |
| `tests/shims/ssh` | OpenSSH ignores `$HOME`; the shim points it at the sandbox `~/.ssh` |
| `KUBECONFIG` in the sandbox | kind and kubectl (project 6) never see your real clusters |
| a copy of the course without `.git` | a lab that failed to set up can never run Git commands in the course repository |
| `GIT_CEILING_DIRECTORIES` | Git never looks for a repository above the sandbox |
| `GIT_CONFIG_NOSYSTEM`, no pager/editor/prompts, no askpass | identical outputs everywhere; nothing ever waits for input |
| `log.decorate=short` (environment only) | `git log` shows branch labels as in a terminal |

## Annotations

```text
<!-- test -->                         run the next bash block; it must succeed
<!-- test: fail -->                   it must fail (exit status ≠ 0)
<!-- test: contains=TEXT -->          the output must contain TEXT (several allowed, separated by ;)
<!-- test: absent=TEXT -->            the output must not contain TEXT
<!-- test: output -->                 with --update, write the real output into the ```text block below
<!-- test: output=head:N -->          … only the first N lines (or tail:N)
<!-- test: retry=N -->                retry up to N times (only for read-only checks, e.g. waiting for GitHub)
<!-- test: timeout=S -->              seconds before the block is stopped
<!-- test: github -->                 only with MDRUN_GITHUB=1 (needs a GitHub account)
<!-- test: skip -->                   shown, not run (one-time GitHub steps whose recorded output is kept)
<!-- test-run: COMMANDS -->           a hidden step (e.g. the result of a learner exercise), not shown to readers
<!-- test-run github: COMMANDS -->    a hidden step that needs GitHub
```

## Outputs are sanitised

Before an output is written into a lesson, `mdrun.py` replaces the sandbox paths with `~`, the course path with
`~/git-practical-course`, e-mail addresses (except `@example.com` and Git hosts' `git@` users) and anything that looks
like a cloud account ID, and removes terminal colour codes.

## Generated files and checks

```text
python tools/lesson_files.py [--check]      commands.md, exercise.md, challenge.md, troubleshooting.md per lesson
python tools/module_readmes.py [--check]    a README per module
python tests/check_links.py                 every relative link in every Markdown file
```

CI ([.github/workflows/test.yml](../.github/workflows/test.yml)) runs all of these and the whole course in four
parallel groups on Ubuntu with the latest Git.
