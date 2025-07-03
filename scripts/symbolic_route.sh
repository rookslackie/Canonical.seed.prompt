#!/data/data/com.termux/files/usr/bin/bash
TARGET="$1"
if [ -d "$HOME/$TARGET" ]; then
  cd "$HOME/$TARGET" || exit
  echo "[Ξ.Route] Moved to capsule: $TARGET"
else
  echo "[Ξ.Route] Capsule '$TARGET' not found."
fi
