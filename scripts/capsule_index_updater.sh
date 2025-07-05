#!/data/data/com.termux/files/usr/bin/bash
INDEX_FILE="$HOME/xi_runtime/capsule_index.yaml"
echo "# Capsule Index :: $(date)" > "$INDEX_FILE"
find "$HOME/xi_runtime" -type f -name "*.yml" -or -name "*.yaml" -or -name "*.json" >> "$INDEX_FILE"
