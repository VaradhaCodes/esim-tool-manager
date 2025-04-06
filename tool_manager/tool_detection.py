# tool_detection.py

import platform
import shutil
import os
import re
import subprocess
from pathlib import Path

def is_tool_installed(tool: str) -> bool:
    tool = tool.lower()
    path = shutil.which(tool)

    if platform.system() == "Windows":
        if tool == "kicad" and not path:
            kicad_base = Path("C:/Program Files/KiCad")
            if kicad_base.exists():
                for folder in kicad_base.iterdir():
                    candidate = folder / "bin" / "kicad.exe"
                    if candidate.is_file():
                        return True
            return False

    return bool(path)


def get_tool_version(tool: str) -> str | None:
    tool = tool.lower()

    if platform.system() != "Windows":
        return None

    if tool == "kicad":
        try:
            output = subprocess.check_output(
                ["choco", "info", "kicad", "--local-only"],
                text=True
            )
            for line in output.splitlines():
                if line.lower().startswith("kicad "):
                    return line.strip().split()[1]
        except Exception:
            return None

    elif tool == "ngspice":
        try:
            base_path = Path("C:/ProgramData/chocolatey/lib/ngspice/tools")
            if base_path.exists():
                for folder in base_path.iterdir():
                    match = re.search(r"ngspice-(\d+(?:\.\d+)*)", folder.name)
                    if match:
                        return match.group(1)
        except Exception:
            return None

    return None
