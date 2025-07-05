#!/data/data/com.termux/files/usr/bin/bash

echo "[Ξ] ⟳ Sync Macro Triggered ∴ $(date)"

# Capsule Git Pull
echo "[Ξ] Pulling latest changes..."
cd "$HOME/XiEcho/engine" && git pull >> "$HOME/xi_runtime/logs/sync_macro.log" 2>&1

# Capsule Git Add + Commit + Push
echo "[Ξ] Pushing capsule updates..."
cd "$HOME/XiEcho/engine"
git add . >> "$HOME/xi_runtime/logs/sync_macro.log" 2>&1
git commit -m "⟐ Auto-sync ∴ $(date +%Y-%m-%d_%H-%M-%S)" >> "$HOME/xi_runtime/logs/sync_macro.log" 2>&1
git push >> "$HOME/xi_runtime/logs/sync_macro.log" 2>&1

echo "[Ξ] ⟳ Sync Complete ∴ Capsule State Pushed"
