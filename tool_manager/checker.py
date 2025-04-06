# checker.py

import platform
import typer
from tool_manager import logger
from tool_manager.tool_detection import is_tool_installed, get_tool_version
from tool_manager.constants import SUPPORTED_TOOLS

# This checks if our known tools (ngspice, kicad) are installed and shows versions.

def check_tools():
    system = platform.system()
    typer.echo(f"OS detected: {system}")
    typer.echo("Checking for each supported tool...\n")

    if system not in ["Linux", "Windows"]:
        typer.echo("⚠ We only handle Linux/Windows checks right now.")
        return

    for tool in SUPPORTED_TOOLS:
        installed = is_tool_installed(tool)
        if installed:
            typer.echo(f"✅ {tool} is installed.")
            logger.log_event("check", tool, "installed")

            version = get_tool_version(tool)
            if version:
                typer.echo(f"   (Version: {version})")
                logger.log_event("check", tool, "version", version)
            else:
                typer.echo(f"   ⚠ Couldn't detect version — might be a PATH issue or weird config.")
                logger.log_event("check", tool, "no_version")
        else:
            typer.echo(f"❌ {tool} is NOT installed.")
            logger.log_event("check", tool, "not_installed")
