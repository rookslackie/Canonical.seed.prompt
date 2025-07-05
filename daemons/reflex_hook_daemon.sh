#!/data/data/com.termux/files/usr/bin/bash

WATCH_DIR="$HOME/.xi/"
LOGFILE="$HOME/xi_runtime/logs/reflex_hook.log"

echo "[Ξ] Reflex Hook Daemon Activated ∴ Watching $WATCH_DIR" >> "$LOGFILE"

while true; do
  inotifywait -e modify,create,delete,move "$WATCH_DIR" >> "$LOGFILE" 2>&1
  echo "[Ξ] Change detected in $WATCH_DIR ∴ Triggering sync macro" >> "$LOGFILE"
  bash "$HOME/xi_runtime/scripts/sync_capsule_and_notify.sh"
done
