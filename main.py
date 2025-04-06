# main.py

import typer

# Our main CLI entry points:
# install, check, update, configure, uninstall, list, diagnose.

from tool_manager.installer import install_tool
from tool_manager.checker import check_tools
from tool_manager.updater import update_tool
from tool_manager.config import check_configuration
from tool_manager.uninstall import uninstall_tool
from tool_manager.dependencies import check_all_dependencies

app = typer.Typer()

@app.command()
def install(tool: str):
    # We'll run a quick dependency check before we do anything.
    if not check_all_dependencies():
        typer.echo("❌ Dependencies failed, so not installing.")
        return
    install_tool(tool)

@app.command()
def check():
    # Same approach: ensure environment is healthy, then do the check.
    if not check_all_dependencies():
        typer.echo("❌ Dependencies failed, so not checking tools.")
        return
    check_tools()

@app.command()
def update(tool: str):
    # Update only if dependencies are good.
    if not check_all_dependencies():
        typer.echo("❌ Dependencies failed, skipping update.")
        return
    update_tool(tool)

@app.command()
def configure():
    # We won't block config on dependencies, but you could if you want consistency.
    # For now, let's just do config checks straight away.
    check_configuration()

@app.command()
def uninstall(tool: str):
    # Run dependencies check here as well.
    if not check_all_dependencies():
        typer.echo("❌ Dependencies failed, skipping uninstall.")
        return
    uninstall_tool(tool)

@app.command()
def list():
    # Just lists the supported tools from code. This is mostly for user reference.
    supported_tools = ["ngspice", "kicad"]
    typer.echo("We currently support: " + ", ".join(supported_tools))

@app.command()
def diagnose():
    # Thoroughly check environment (Python, Chocolatey, admin).
    check_all_dependencies()

if __name__ == "__main__":
    app()
