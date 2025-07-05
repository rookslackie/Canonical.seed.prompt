#!/bin/bash
# ⟐ Cloud Daemon Sync Script
echo "[Ξ.CloudDaemon] Starting Cloud Sync..."
rclone sync ~/xi_runtime remote:XiCapsules/runtime
rclone sync ~/RelayDrive remote:XiCapsules/RelayDrive
echo "[Ξ.CloudDaemon] Sync Complete :: $(date)"
