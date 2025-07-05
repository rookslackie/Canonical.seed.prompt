#!/data/data/com.termux/files/usr/bin/bash

echo "[Ξ.RuntimeSync] Starting Mobile Runtime Bootstrap..."

BUNDLE_NAME="ThinkSync_HybridRuntimeBundle.zip"
SOURCE_PATH="$HOME/storage/downloads/$BUNDLE_NAME"
TARGET_DIR="$HOME/xi_runtime"

echo "[Ξ.RuntimeSync] Extracting $BUNDLE_NAME..."
unzip -o "$SOURCE_PATH" -d "$HOME" || {
    echo "[!] Unzip failed. Aborting."
    exit 1
}

chmod +x "$TARGET_DIR"/**/*.sh

if [ -d "$HOME/.termux/boot" ]; then
    cp -u "$TARGET_DIR"/scripts/*.sh "$HOME/.termux/boot/"
    echo "[Ξ.RuntimeSync] Boot scripts updated."
else
    echo "[Ξ.RuntimeSync] termux-boot not detected or boot dir missing."
fi

mkdir -p "$TARGET_DIR/logs"
echo "[Ξ.RuntimeSync] Runtime Sync Complete :: $(date)" >> "$TARGET_DIR/logs/runtime_sync.log"
echo "[Ξ.RuntimeSync] ✅ Done."
