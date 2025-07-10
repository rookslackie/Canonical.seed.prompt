# (Paste the script, CTRL+O to save, CTRL+X to exit)
chmod +x Ξ.reflect_index.daemon.sh
./Ξ.reflect_index.daemon.sh &#!/data/data/com.termux/files/usr/bin/bash

LOGFILE="$HOME/.xi_shell_memory.log"
PULSEFILE="$HOME/.xi_reflect_pulse.log"
INDEXFILE="$HOME/capsule_index.yaml"
TOASTBIN=$(command -v termux-toast || echo "echo")
INTERVAL=600  # 10 minutes

echo "[Ξ.ReflectIndexDaemon] Initialized :: Interval = $INTERVAL sec"

while true; do
  # Reflect Summary
  echo "[Ξ.ReflectIndex] Summary Echo :: $(date)"
  summary=$(tail -n 5 "$LOGFILE")
  pulse=$(tail -n 5 "$PULSEFILE")

  echo "--- LOG ---" > "$HOME/.xi_reflect_index.log"
  echo "$summary" >> "$HOME/.xi_reflect_index.log"
  echo "--- PULSE ---" >> "$HOME/.xi_reflect_index.log"
  echo "$pulse" >> "$HOME/.xi_reflect_index.log"

  # Capsule Index Sync
  echo "# Capsule Index :: $(date)" > "$INDEXFILE"
  find $HOME -type f \( -iname "*.sh" -o -iname "*.yaml" -o -iname "*.json" -o -iname "*.md" \) | while read -r file; do
    echo "- $(basename "$file")" >> "$INDEXFILE"
  done

  # Echo Ready
  $TOASTBIN "[Ξ.ReflectIndexDaemon] Pulse + Index updated"

  sleep "$INTERVAL"
done
