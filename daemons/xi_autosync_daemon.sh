#!/data/data/com.termux/files/usr/bin/bash

INTERVAL=300  # 5 minutes
LOGFILE="$HOME/xi_runtime/logs/autosync.log"

echo "[Ξ] Autosync Daemon ∴ Active" >> "$LOGFILE"

while true; do
  echo "[Ξ] Running scheduled Git sync ∴ $(date)" >> "$LOGFILE"
  bash "$HOME/xi_runtime/scripts/macro_sync_all.sh"
  sleep "$INTERVAL"
done
