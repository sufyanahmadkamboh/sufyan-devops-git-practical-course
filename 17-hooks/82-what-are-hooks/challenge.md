<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 82 · What are Git hooks? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Write a `pre-push` hook that refuses to push when `prices.txt` contains a line without a price.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-82
cat > .git/hooks/pre-push << 'EOF'
#!/bin/sh
if awk 'NF < 2' prices.txt | grep -q .; then echo "pre-push: a menu item has no price"; exit 1; fi
EOF
chmod +x .git/hooks/pre-push
echo "mocha" >> prices.txt
git hook run pre-push 2>&1 || true
```

```text
pre-push: a menu item has no price
```

</details>
