#!/data/data/com.termux/files/usr/bin/bash

PS3="Ξ.Select Task > "
options=("Sync Capsule" "Index Files" "Route Project" "Mirror Capsule" "Reset Git" "Load Env" "Quit")

select opt in "${options[@]}"
do
  case $opt in
    "Sync Capsule") ~/xi_runtime/scripts/capsule_sync.sh ;;
    "Index Files") ~/xi_runtime/scripts/capsule_index.sh ;;
    "Route Project") read -p "Enter capsule name: " cap; ~/xi_runtime/scripts/symbolic_route.sh "$cap" ;;
    "Mirror Capsule") python ~/xi_runtime/scripts/capsule_mirror.py ;;
    "Reset Git") ~/xi_runtime/scripts/capsule_git_reset.sh ;;
    "Load Env") ~/xi_runtime/scripts/capsule_env_loader.sh ;;
    "Quit") break ;;
    *) echo "Invalid";;
  esac
done
