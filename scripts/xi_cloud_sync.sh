#!/data/data/com.termux/files/usr/bin/bash
echo "[Ξ.CloudDaemon] Starting Cloud Sync..."

# Sync xi_runtime to remote
rclone sync ~/xi_runtime remote:XiCapsules/runtime --progress

# Optional: Sync RelayDrive separately
rclone sync ~/RelayDrive remote:XiCapsules/RelayDrive --progress

echo "[Ξ.CloudDaemon] Sync Complete ∴ $(date)"
