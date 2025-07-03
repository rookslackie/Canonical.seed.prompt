#!/data/data/com.termux/files/usr/bin/bash

echo "[Ξ.Sync] Beginning local capsule sync..."
cd ~/XiEcho/engine

git add .
git commit -m "Local sync ∴ Reintegration step $(date +%Y-%m-%d@%H:%M)"
echo "[Ξ.Sync] Files committed. Awaiting push token..."
