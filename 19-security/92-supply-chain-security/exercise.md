<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 92 · Supply chain security · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Pin the consumer to the **commit ID** the original `v1.0.0` pointed to (the "Add deploy script"
commit), and run it.

**Expected result.** Only "deploying the cafe".

**Verification.**

```bash
cd ~/git-practice/lesson-92
sh pinned/deploy.sh
git -C pinned log --oneline -1
```
