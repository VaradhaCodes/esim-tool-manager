import platform
import subprocess
import typer
from tool_manager.logger import log_event
from tool_manager.constants import SUPPORTED_TOOLS
from tool_manager.tool_detection import is_tool_installed

def uninstall_tool(tool: str):
    tool = tool.lower().strip()

    if tool not in SUPPORTED_TOOLS:
        typer.echo(f"❌ '{tool}' isn't a tool we manage.")
        log_event("uninstall", tool, "fail", "Unsupported tool")
        return

    system = platform.system()
    typer.echo(f"(Detected OS: {system})")
    typer.echo(f"Let's try to uninstall {tool}...")

    if system != "Windows":
        typer.echo("❌ We only handle uninstalls on Windows, sorry.")
        log_event("uninstall", tool, "fail", "Unsupported OS")
        return

    if not is_tool_installed(tool):
        typer.echo(f"ℹ {tool} doesn't seem installed, so nothing to remove.")
        log_event("uninstall", tool, "skipped", "Not installed")
        return

    try:
        # For KiCad, always use the safer uninstall command
        if tool == "kicad":
            typer.echo("→ Running: choco uninstall kicad -y -n --skip-autouninstaller")
            subprocess.run(["choco", "uninstall", tool, "-y", "-n", "--skip-autouninstaller"], check=True)
            typer.echo(f"✅ {tool} forcibly uninstalled using fallback.")
            log_event("uninstall", tool, "force_success", "Fallback uninstall succeeded")
        else:
            # Normal uninstall for other tools like ngspice
            typer.echo(f"→ Running: choco uninstall {tool} -y")
            subprocess.run(["choco", "uninstall", tool, "-y"], check=True)
            typer.echo(f"✅ {tool} uninstalled successfully.")
            log_event("uninstall", tool, "success", "Uninstalled via Chocolatey")

    except subprocess.CalledProcessError:
        typer.echo(f"❌ Choco couldn't remove {tool}. Could be permissions or PATH issues.")
        log_event("uninstall", tool, "fail", "Uninstall command failed")
