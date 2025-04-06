# dependencies.py

import sys
import shutil
import os
import subprocess
import platform
import ctypes
import typer
from tool_manager import logger

# We do a quick environment check: Python version, Chocolatey presence, admin rights, etc.

def check_all_dependencies():
    typer.echo("\nChecking your system before we do anything fancy...\n")
    system = platform.system()

    # We're only focusing on Windows or Linux in theory, but Windows is the real deal for now.
    if system not in ["Windows", "Linux"]:
        typer.echo(f"⚠ We mainly tested on Windows (with partial Linux). You have: {system}.")

    python_ok = _check_python_version()

    choco_ok = True
    admin_ok = True

    if system == "Windows":
        choco_ok = _check_chocolatey()
        admin_ok = _check_admin_rights()
    else:
        typer.echo("Skipping Chocolatey/admin checks on non-Windows.")
        logger.log_event("dependencies", "system", "skipped", "Non-Windows OS")

    all_ok = python_ok and choco_ok and admin_ok

    if all_ok:
        typer.echo("✅ Everything looks good to proceed!")
        logger.log_event("dependencies", "system", "ok", "All checks passed")
    else:
        typer.echo("\n⚠ Something's off with your dependencies.")
        typer.echo("   Fix the above issues and run `python main.py diagnose` again.")
        logger.log_event("dependencies", "system", "fail", "Some checks failed")

    return all_ok

def _check_python_version(min_version=(3, 8)):
    # We want Python 3.8 or higher to avoid weird issues with older Python versions.
    current = sys.version_info
    if current >= min_version:
        typer.echo(f"✔ Python {current.major}.{current.minor} is fine.")
        return True
    else:
        typer.echo(f"❌ Your Python ({current.major}.{current.minor}) is too old. Need at least {min_version[0]}.{min_version[1]}.")
        typer.echo("Get a newer Python at: https://www.python.org/downloads/")
        logger.log_event("dependencies", "python", "fail", f"Version {current.major}.{current.minor}")
        return False

def _check_chocolatey():
    # We look for 'choco' in PATH. If not found, user must install it.
    choco_path = shutil.which("choco")
    if not choco_path:
        typer.echo("❌ Can't find Chocolatey. It's required on Windows.")
        typer.echo("Visit https://chocolatey.org/install to get set up.")
        logger.log_event("dependencies", "chocolatey", "fail", "Not in PATH")
        return False

    # We also attempt to run `choco -v` to ensure it doesn’t error out.
    try:
        result = subprocess.run(["choco", "-v"], capture_output=True, text=True, check=True)
        version_str = result.stdout.strip()
        typer.echo(f"✔ Chocolatey is here. (Version: {version_str})")
        return True
    except subprocess.CalledProcessError:
        typer.echo("❌ Found choco but it didn't respond well. Possibly broken install?")
        logger.log_event("dependencies", "chocolatey", "fail", "choco -v call failed")
        return False

def _check_admin_rights():
    # On Windows, we try to see if we have admin privileges. If not, installs might fail.
    if platform.system() != "Windows":
        return True

    try:
        is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        if is_admin:
            typer.echo("✔ Running with admin privileges.")
            return True
        else:
            typer.echo("⚠ Not running as admin. Some actions might fail.")
            typer.echo("   Try re-opening your terminal as Administrator if needed.")
            logger.log_event("dependencies", "admin", "fail", "Not admin user")
            return False
    except Exception:
        # If we can't even check, let's just proceed anyway.
        typer.echo("Couldn't check admin status, but forging ahead.")
        logger.log_event("dependencies", "admin", "unknown", "Check failed")
        return True
