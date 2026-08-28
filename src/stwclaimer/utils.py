import sys
import os
import shutil
from pathlib import Path


def base_path(exe_path: bool = True) -> Path:
    is_compiled = hasattr(sys, "frozen") or "__compiled__" in globals()

    if not is_compiled or not exe_path:
        return Path(__file__).resolve().parent

    appimage_path = os.environ.get("APPIMAGE")

    if appimage_path:
        return Path(appimage_path).parent

    exe_path = Path(sys.executable if hasattr(sys, "frozen") else sys.argv[0])

    if not exe_path.is_absolute():
        resolved_which = shutil.which(exe_path.name)
        exe_path = Path(resolved_which) if resolved_which else exe_path.resolve()

    base_dir = exe_path.parent

    if sys.platform == "darwin" and "Contents/MacOS" in base_dir.parts:
        base_dir = base_dir.parents[2]

    return base_dir
