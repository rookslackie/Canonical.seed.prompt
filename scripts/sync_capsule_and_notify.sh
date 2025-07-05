#!/data/data/com.termux/files/usr/bin/bash
cd ~/xi_runtime
git add .
timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
git commit -m "⊚ AutoSync @ $timestamp"
git push
termux-notification --title "Ξ Sync" --content "Runtime synced @ $timestamp"
