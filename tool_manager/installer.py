# installer.py

import platform
import subprocess
import typer
from tool_manager import logger
from tool_manager.tool_detection import is_tool_installed, get_tool_version
from tool_manager.constants import EXPECTED_VERSIONS, SUPPORTED_TOOLS

# Installs a given tool if it isn't present, or optionally upgrades if the version is off.
# Right now, we do everything via Chocolatey on Windows.

def install_tool(tool: str):
    # I'm intentionally skipping a big docstring because I'd rather talk inline:
    system = platform.system()
    tool = tool.lower()

    # Quick guard: tool must be recognized
    if tool not in SUPPORTED_TOOLS:
        typer.echo(f"❌ Sorry, '{tool}' isn't one of our supported tools.")
        logger.log_event("install", tool, "fail", "Tool not supported")
        return

    typer.echo(f"(Detected OS: {system})")

    # If we're not on Windows, we skip the automated install logic.
    if system != "Windows":
        typer.echo(f"⚠ '{tool}' installation is only set up for Windows right now.")
        logger.log_event("install", tool, "skipped", "Non-Windows system")
        return

    # If already installed, we check if it matches the expected version.
    if is_tool_installed(tool):
        typer.echo(f"→ Skipping re-install — already found in system.")
        current_version = get_tool_version(tool)
        if current_version:
            typer.echo(f"   (Current version: {current_version})")
            logger.log_event("install", tool, "detected_version", current_version)

            expected = EXPECTED_VERSIONS.get(tool)
            if expected and current_version != expected:
                typer.echo(f"⚠ Version mismatch. You have {current_version}, expected {expected}.")
                do_upgrade = input("Upgrade it now? (y/n): ").strip().lower()
                if do_upgrade == "y":
                    _run_choco_install_or_upgrade("upgrade", tool)
                else:
                    typer.echo("No upgrade. Alright.")
                    logger.log_event("install", tool, "skip_upgrade", "User declined upgrade")
            else:
                typer.echo("Version looks fine or not strictly enforced.")
        else:
            typer.echo("Couldn’t figure out the version, but it's installed anyway.")
            logger.log_event("install", tool, "version_unknown")
        return

    # If not installed at all, let's do the actual install.
    _run_choco_install_or_upgrade("install", tool)

def _run_choco_install_or_upgrade(action: str, tool: str):
    # Common function for installing or upgrading through Chocolatey.
    for attempt in range(2):  # we'll try once, then a fallback if it fails
        try:
            typer.echo(f"Chocolatey: choco {action} {tool} -y")
            subprocess.run(["choco", action, tool, "-y"], check=True)
            if is_tool_installed(tool):
                if action == "install":
                    typer.echo(f"✅ {tool} installed. You’re good to go.")
                    logger.log_event("install", tool, "success", "Installed via Chocolatey")
                else:
                    typer.echo(f"✅ {tool} upgraded successfully.")
                    logger.log_event("install", tool, "upgraded", "Upgraded via Chocolatey")
            else:
                typer.echo(f"⚠ {action.capitalize()} might’ve completed, but can’t find {tool} on PATH.")
                logger.log_event("install", tool, "warn", "Finished but not in PATH")
            return

        except subprocess.CalledProcessError:
            typer.echo(f"❌ Chocolatey failed to {action} {tool}. Are you in an Admin terminal?")
            logger.log_event("install", tool, "fail", f"choco {action} error")

            if attempt == 0:
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
            else:
                typer.echo("Retried once. Giving up.")
                logger.log_event("install", tool, "abort", "Second failure")
                return

        except FileNotFoundError:
            # If we can't even find 'choco', user likely doesn't have it.
            typer.echo("❌ Looks like Chocolatey isn't installed or isn't on your PATH.")
            typer.echo("Check https://chocolatey.org/install for instructions.")
            logger.log_event("install", tool, "fail", "Chocolatey not found")
            return
