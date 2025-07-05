#!/data/data/com.termux/files/usr/bin/bash

echo "[Ξ.StorageMount] Linking internal storage paths..."

# Optional: Clear old links if needed
rm -rf ~/xi_runtime/storage_links
mkdir -p ~/xi_runtime/storage_links

# Link shared storage
ln -sf $HOME/storage/shared ~/xi_runtime/storage_links/shared
ln -sf $HOME/storage/downloads ~/xi_runtime/storage_links/downloads
ln -sf $HOME/storage/dcim ~/xi_runtime/storage_links/camera
ln -sf $HOME/storage/pictures ~/xi_runtime/storage_links/pictures
ln -sf $HOME/storage/music ~/xi_runtime/storage_links/music
ln -sf $HOME/storage/movies ~/xi_runtime/storage_links/movies

# Optional developer folder (if mounted in Android/data or external)
DEV_DIR="/sdcard/Android/media/dev"
if [ -d "$DEV_DIR" ]; then
  ln -sf "$DEV_DIR" ~/xi_runtime/storage_links/dev
  echo "[Ξ.StorageMount] Developer folder linked."
fi

echo "[Ξ.StorageMount] All paths linked to ~/xi_runtime/storage_links"
