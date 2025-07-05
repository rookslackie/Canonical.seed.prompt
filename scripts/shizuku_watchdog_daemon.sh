#!/data/data/com.termux/files/usr/bin/bash

LOGFILE="$HOME/xi_runtime/Logs/shizuku_watchdog.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S') 
ECHO_CHANNEL="$HOME/xi_runtime/echo/shizuku_status.echo"

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ECHO_CHANNEL")"

echo "[Ξ.ShizukuCheck] $DATE - Checking daemon..." >> "$LOGFILE"

if shizuku -v &> /dev/null; then
  echo "[Ξ.ShizukuCheck] ✅ Shizuku is running" >> "$LOGFILE"
  echo "status: OK" > "$ECHO_CHANNEL"
else
  echo "[Ξ.ShizukuCheck] ❌ Shizuku NOT running" >> "$LOGFILE"
  echo "status: MISSING" > "$ECHO_CHANNEL"
  echo "[Ξ.Alert] Shizuku missing. Please open app manually." >&2

  # [Optional] Auto-recovery block (not active yet)
  # echo "[Ξ.Recovery] Attempting silent relaunch..." >> "$LOGFILE"
  # am start -n "moe.shizuku.privileged.api/moe.shizuku.privileged.api.MainActivity" &>> "$LOGFILE"
fi
