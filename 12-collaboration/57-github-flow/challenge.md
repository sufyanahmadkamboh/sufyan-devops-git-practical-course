<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 57 · GitHub Flow · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Turn the smoke test into a guard: make `deploy.sh` refuse to replace production when the new version fails, keeping the
previous one running.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-57
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh: test the server's main in a staging folder, and only then replace production/
set -e
rm -rf staging && git clone -q server/cafe.git staging
if grep -q "^espresso [0-9]" staging/prices.txt; then
  rm -rf production && mv staging production && echo "deployed $(git -C production log --oneline -1)"
else
  echo "smoke test failed: kept $(git -C production log --oneline -1)"; exit 1
fi
EOF
(cd ada && sed -i 's/^espresso 2.50/espresso broken/' prices.txt && git commit -q -am "Another quick fix" && git push -q)
bash deploy.sh || true
```

```text
smoke test failed: kept 333283f (HEAD -> main, origin/main, origin/HEAD) Merge branch 'revert-quick-fix'
```

</details>
