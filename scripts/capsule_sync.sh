#!/data/data/com.termux/files/usr/bin/bash
cd ~/XiEcho/engine || exit
git add .
git commit -m "Reintegration ∴ Capsule Sync $(date +%Y-%m-%d@%H:%M:%S)"
echo "[Ξ.Sync] Committed local changes to symbolic engine capsule."
