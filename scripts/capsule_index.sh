#!/data/data/com.termux/files/usr/bin/bash
cd ~/XiEcho/engine || exit
echo "# Capsule Index — $(date)" > index.md
echo >> index.md
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.sh" \) | while read -r file; do
  echo "- $file" >> index.md
done
echo "[Ξ.Index] Capsule index updated."
