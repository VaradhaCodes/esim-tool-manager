# config.py

import platform
import subprocess
import os
import typer
from pathlib import Path
from tool_manager import logger

# This module checks if common tool folders are in the PATH and optionally fixes it.
# Works only for Windows (for now).

def check_configuration():
    system = platform.system()
    if system != "Windows":
        typer.echo("⚠ PATH auto-configuration is only implemented for Windows right now.")
        logger.log_event("configure", "all", "skipped", "Non-Windows system")
        return

    typer.echo(f"(Detected OS: {system})")
    typer.echo("Checking if important folders are in your PATH...\n")

    possible_paths = _find_dynamic_paths()
    anything_checked = False

    for label, folder in possible_paths.items():
        typer.echo(f"→ Checking: {label} ({folder})")

        if not os.path.isdir(folder):
            typer.echo(f"   ⚠ Folder not found — maybe {label} isn't installed yet.")
            logger.log_event("configure", label, "not_found", f"Folder {folder} doesn't exist")
            continue

        anything_checked = True
        if _is_in_path(folder):
            typer.echo(f"   ✔ Already in PATH.")
            logger.log_event("configure", folder, "ok", "Already in PATH")
        else:
            typer.echo(f"   ⚠ Not in PATH.")
            logger.log_event("configure", folder, "missing", "")
            _maybe_add_to_path_windows(folder)

    if not anything_checked:
        typer.echo("\n⚠ None of the tool folders were found. Maybe nothing is installed yet.")
        logger.log_event("configure", "all", "skipped", "No folders existed")

    typer.echo("\n✅ PATH check complete.")


def _find_dynamic_paths() -> dict:
    paths = {}

    # Chocolatey is always fixed
    paths["Chocolatey bin"] = "C:\\ProgramData\\chocolatey\\bin"

    # Detect KiCad bin dynamically
    kicad_base = Path("C:/Program Files/KiCad")
    if kicad_base.exists():
        for folder in kicad_base.iterdir():
            bin_path = folder / "bin"
            if bin_path.is_dir():
                paths["KiCad bin"] = str(bin_path)
                break

    # Detect ngspice version folder dynamically
    ng_base = Path("C:/ProgramData/chocolatey/lib/ngspice/tools")
    if ng_base.exists():
        for folder in ng_base.iterdir():
            if folder.name.lower().startswith("ngspice-") and folder.is_dir():
                paths["ngspice install"] = str(folder)
                break

    return paths


def _maybe_add_to_path_windows(folder: str):
    confirm = input(f"Add {folder} to PATH now? (y/n): ").strip().lower()
    if confirm != "y":
        typer.echo("↪ Skipping update.")
        logger.log_event("configure", folder, "skipped", "User declined")
        return

    try:
        current_path = os.environ.get("PATH", "")
        if folder.lower() in current_path.lower():
            typer.echo(f"✔ {folder} already in PATH.")
            return

        new_path = f"{current_path};{folder}"
        if len(new_path) > 1023:
            typer.echo("❌ PATH too long — can't add this folder automatically.")
            typer.echo("🔧 Tip: You can add it manually via:")
            typer.echo("   Control Panel → System → Environment Variables → User PATH")
            logger.log_event("configure", folder, "fail", "PATH too long")
            return

        subprocess.run(["setx", "Path", new_path], shell=True)
        typer.echo("✅ Added to PATH. You may need to restart your terminal.")
        logger.log_event("configure", folder, "success", "Added to PATH")
        typer.echo("⚠ PATH changes only take effect in new terminals.")

    except Exception as e:
        typer.echo(f"❌ Failed to update PATH: {e}")
        logger.log_event("configure", folder, "fail", f"Exception: {e}")


def _is_in_path(folder: str) -> bool:
    path_env = os.environ.get("PATH", "")
    return any(folder.lower() in part.lower() for part in path_env.split(";"))
