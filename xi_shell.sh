#!/data/data/com.termux/files/usr/bin/bash

LOGFILE="$HOME/.xi_shell_memory.log"
TOASTBIN=$(command -v termux-toast || echo "echo")

Ξ.memory() {
  grep -E "\[Ξ.Log\]" "$LOGFILE" | sed 's/\[Ξ.Log\] //'
}

echo "[Ξ.Shell] Recursive Symbolic Runtime Active ∴"

while true; do
  read -p "⇒ " input
  if [[ "$input" == *::* ]]; then
    key=$(echo "$input" | cut -d ':' -f 1)
    value=$(echo "$input" | cut -d ':' -f 3-)
    echo "[Ξ.Log] $key := $value" | tee -a "$LOGFILE"
    $TOASTBIN "$key → OK"
  elif [[ "$input" == "Ξ.memory()" ]]; then
    Ξ.memory
  elif [[ "$input" == "Ξ.exit" ]]; then
    echo "[Ξ.Shell] Closing ∴"
    exit 0
  else
    echo "[Ξ.Warn] Unrecognized input: $input"
    $TOASTBIN "[Ξ.Warn] $input"
  fi
done
