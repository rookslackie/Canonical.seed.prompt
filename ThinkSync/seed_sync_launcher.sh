#!/bin/bash
# ⟐ Seed Sync Launcher
while true; do
  echo "[Ξ.SeedSync] Active at $(date)"
  bash ~/xi_runtime/scripts/xi_cloud_sync.sh
  sleep 120
done
