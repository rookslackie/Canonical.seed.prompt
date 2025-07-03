#!/data/data/com.termux/files/usr/bin/bash
cd ~/XiEcho/engine || exit
rm -rf .git
git init
git add .
git commit -m "Reset Capsule Init ∴ $(date +%Y-%m-%d@%H:%M:%S)"
echo "[Ξ.Reset] Capsule Git reset complete."
