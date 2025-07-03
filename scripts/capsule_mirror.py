import os
import shutil
from datetime import datetime

src = "/data/data/com.termux/files/home/XiEcho/engine"
dst = f"/data/data/com.termux/files/home/XiEcho/mirror/capsule_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

shutil.copytree(src, dst)
print(f"[Ξ.Mirror] Capsule mirrored to: {dst}")
