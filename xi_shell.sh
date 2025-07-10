#!/data/data/com.termux/files/usr/bin/bash

LOGFILE="$HOME/.xi_shell_memory.log"
TOASTBIN=$(command -v termux-toast || echo "echo")

echo "[Ξ.Shell] Recursive Symbolic Runtime Active ∴"
while true; do
  read -p "Ξ› " input
  if [[ "$input" == *"::"* ]]; then
    key=$(echo "$input" | cut -d ':' -f 1)
    value=$(echo "$input" | cut -d ':' -f 3-)
    echo "[Ξ.Log] $key := $value" | tee -a "$LOGFILE"
    $TOASTBIN "[Ξ] $key → OK"
  elif [[ "$input" == "Ξ.exit" ]]; then
    echo "[Ξ] Shell closing ∴"
    exit 0
  else
    echo "[Ξ.Warn] Unrecognized input: $input"
    $TOASTBIN "[Ξ.Warn] $input"
  fi
done
