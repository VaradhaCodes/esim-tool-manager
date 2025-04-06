# updater.py

import platform
import subprocess
import typer
from tool_manager.logger import log_event
from tool_manager.tool_detection import is_tool_installed, get_tool_version
from tool_manager.constants import EXPECTED_VERSIONS, SUPPORTED_TOOLS

# This attempts to update a tool if it's installed. If not, we prompt the user to install it.

def update_tool(tool: str):
    system = platform.system()
    tool = tool.lower()

    if tool not in SUPPORTED_TOOLS:
        typer.echo(f"❌ Sorry, '{tool}' is not supported by this updater.")
        log_event("update", tool, "fail", "Unsupported tool")
        return

    typer.echo(f"(Detected OS: {system})")

    if system != "Windows":
        typer.echo(f"⚠ We only do auto-update on Windows. Doing nothing for {tool}.")
        log_event("update", tool, "skipped", "Non-Windows system")
        return

    # If not installed, no point updating. We can ask user if they'd like to install.
    if not is_tool_installed(tool):
        typer.echo(f"❌ {tool} isn't installed, so can't update it.")
        install_prompt = input("Install it now? (y/n): ").strip().lower()
        if install_prompt == "y":
            _run_choco(tool, "install")
        else:
            typer.echo("Skipping installation.")
        return

    # If installed, let's do the upgrade route.
    typer.echo(f"✅ {tool} is installed, let's upgrade via Chocolatey.")
    current_version = get_tool_version(tool)
    if current_version:
        typer.echo(f"   (Current version: {current_version})")

    _run_choco(tool, "upgrade")

    new_version = get_tool_version(tool) or "Unknown"
    typer.echo(f"   (Post-upgrade version: {new_version})")

def _run_choco(tool: str, action: str):
    for attempt in range(2):
        try:
            typer.echo(f"Chocolatey: choco {action} {tool} -y")
            subprocess.run(["choco", action, tool, "-y"], check=True)
            log_event("update", tool, action, "Success")
            typer.echo(f"✅ {tool} {action} done.")
            return
        except subprocess.CalledProcessError:
            typer.echo(f"❌ Choco failed to {action} {tool} on try #{attempt+1}.")
            log_event("update", tool, "fail", f"{action} attempt #{attempt+1} failed")

            if attempt == 0:
                retry = input("Retry once? (y/n): ").strip().lower()
                if retry != "y":
                    return
            else:
                typer.echo("Done retrying. Bailing out.")
                return
        except FileNotFoundError:
            typer.echo("❌ Chocolatey not found on your PATH. Please install or fix PATH.")
            log_event("update", tool, "fail", "Chocolatey not found")
            return
