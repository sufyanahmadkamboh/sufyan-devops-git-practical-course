# Git Practical Course · project summary

**What:** a free, hands-on Git and GitHub course for DevOps work: 98 lessons from the first commit to interactive
rebase, recovery, hooks, security, pull requests, branch protection, releases and GitHub Actions, then a DevOps
workflow, 18 troubleshooting labs, 6 projects, a capstone that ends with a release deployed to Kubernetes, and a final
exam.

**Problem:** Git is usually learned as a list of commands; the hard parts at work are conflicts, rejected pushes,
lost commits, rewritten history, authentication, secrets in the history and team rules. Those are rarely practised.

**Contents**
- 98 lessons, each: concept, diagram, lab with a known history (identical commit IDs for every learner), real
  commands and outputs, command table, exercise, a mistake made on purpose, troubleshooting, fix, real-world example,
  challenge and recap; generated `commands.md`, `exercise.md`, `challenge.md`, `troubleshooting.md` per lesson
- an assessment per module (quiz, practical challenge, troubleshooting challenge on a broken repository, real-world
  scenario), a command reference lab linked to the lessons
- 18 troubleshooting labs in the format problem → symptoms → investigation → root cause → fix → verification → prevention
- a DevOps workflow lab on a realistic repository (application, Dockerfile, Helm chart, Kubernetes, scripts, CI)
- 6 projects with self-check graders, including tag-driven deployments to a kind cluster with Helm and a rollback
- a capstone (a deliberately broken repository → a protected GitHub repository, PRs through required checks, a
  release workflow that pushes an image to GHCR and deploys it with Helm to a kind cluster) and a final exam with a
  grader and a separate solution
- a 23-video series (full and silent versions), a 125-page study guide PDF, a glossary and 35 interview questions

**Engineering details**
- `tests/mdrun.py` runs every Bash block of the course and writes the real outputs back into the lessons; a sandbox
  (temporary HOME, an ssh shim for the sandbox `~/.ssh`, a sandbox kubeconfig, a copy of the course without `.git`,
  ceiling directories, no pager/editor/prompts/askpass) keeps runs reproducible and the author's environment untouched
- GitHub Actions runs all 1,308 blocks in four parallel groups on Ubuntu with the latest Git (git-core PPA), Git LFS,
  git-filter-repo, kind and Helm; static checks for links, generated files and ShellCheck
- 153 blocks run against GitHub with the author's account: a practice repository, real PRs and reviews, branch
  protection, issues, labels, milestones, releases and Actions runs; the capstone's reference run is a public repository
- the videos are generated from the lessons: scenes per lesson, two narrator voices, real recorded outputs,
  original synthesised music and effects, captions, chapters and an audio-license register with timestamps

**Repository:** https://github.com/sufyanahmadkamboh/sufyan-devops-git-practical-course
