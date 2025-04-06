# eSim Tool Manager — Design Document

This doc explains the entire layout of the tool manager, why these pieces exist, and how they interact. The main focus is to automate tasks like installing, updating, and configuring KiCad/ngspice on Windows.

---

## 1. High-Level Overview
- **Goal:** Minimize hassle when setting up external tools (ngspice, KiCad) on Windows.
- **Core Features:** Installs tools via Chocolatey, checks if they exist, updates them if needed, configures your PATH, can uninstall them, and logs everything so you know exactly what happened.

---

## 2. High-Level Architecture

```
                   +-----------------------------+
                   |        User Interface       |
                   | (main.py CLI / menu.py UI)  |
                   +--------------+--------------+
                                  |
                     CLI command or menu choice
                                  v
              +------------------+------------------+
              |  Core Operations Dispatcher         |
              | (main.py Typer commands)            |
              +------------------+------------------+
                                  |
              +------------------+------------------+
              |    tool_manager (Modular Logic)     |
              +------------------+------------------+
  +------------------+    +------------------+    +------------------+
  | checker.py       |    | installer.py     |    | updater.py       |
  | - sees if tool   |    | - uses Choco to  |    | - upgrades tool  |
  |   is installed   |    |   install        |    | - verifies post  |
  +------------------+    +------------------+    +------------------+
  +------------------+    +------------------+    +------------------+
  | uninstall.py     |    | config.py        |    | dependencies.py  |
  | - removes tool   |    | - checks & fixes |    | - system checks  |
  |   (KiCad tricky) |    |   PATH           |    |   (Python, admin)|
  +------------------+    +------------------+    +------------------+
  +------------------+    +------------------+
  | logger.py        |    | tool_detection.py|
  | - writes logs    |    | - sees if tool   |
  | - timestamped    |    |   is installed   |
  +------------------+    +------------------+
```

At the top, you have two main entry points: `main.py` for a Typer-based CLI, and `menu.py` for a more user-friendly, numbered menu system. Both call into the same underlying logic.

---

## 3. Modules (Detailed)

### `main.py`
- **What It Does:** This is the central CLI interface. Defines commands (install, check, update, configure, etc.) using Typer.
- **Flow:** Before running any command, it checks dependencies (via `dependencies.py`). If everything is okay, it delegates to the correct module.
- **Why We Need It:** Clearly separates user interaction from the internal logic.

### `menu.py`
- **What It Does:** A simple text-based menu that calls `main.py` commands using `subprocess`. For example, if you choose "Install a tool" from the menu, it’ll effectively run `python main.py install <tool>`.
- **Why It Exists:** Great for quick demos, or if you don’t feel like typing individual commands. Also helpful for testing all features in one place.

### `tool_manager/checker.py`
- **What It Does:** Iterates through `SUPPORTED_TOOLS` (from `constants.py`), checks if they’re installed, and logs their version.
- **Key Func:** `check_tools()` — prints OS, loops tools, logs each status.

### `tool_manager/installer.py`
- **What It Does:** Installs or upgrades a tool through Chocolatey. Handles version mismatches if the tool is already present.
- **Key Func:** `install_tool(tool)` — decides if it needs a fresh install or an upgrade, logs the outcome.

### `tool_manager/updater.py`
- **What It Does:** Upgrades a tool if it’s installed, otherwise offers to install it.
- **Key Func:** `update_tool(tool)` — triggers `choco upgrade`, checks success.

### `tool_manager/uninstall.py`
- **What It Does:** Removes a tool via Chocolatey. If KiCad’s uninstaller needs special handling, it does that.
- **Key Func:** `uninstall_tool(tool)` — logs the process, tries to remove the tool cleanly.

### `tool_manager/config.py`
- **What It Does:** Checks if key folders (like KiCad’s bin) are in your PATH. If not, it prompts you to add them.
- **Key Funcs:**
  - `check_configuration()` — finds typical KiCad or ngspice install directories, sees if they’re in PATH.
  - `_maybe_add_to_path_windows(folder)` — uses `setx` to append to PATH if you say yes.

### `tool_manager/dependencies.py`
- **What It Does:** Makes sure the system meets basic requirements (Python ≥ 3.8, admin privileges on Windows, and Chocolatey installed).
- **Key Func:** `check_all_dependencies()` — logs if anything’s missing.

### `tool_manager/tool_detection.py`
- **What It Does:** Figures out if a tool is installed at all, and if so, which version.
- **Key Funcs:**
  - `is_tool_installed(tool)` — uses `shutil.which` or special checks for KiCad’s folder.
  - `get_tool_version(tool)` — tries to parse from folder names or `choco info`.

### `tool_manager/constants.py`
- **What It Does:** Lists `SUPPORTED_TOOLS` (`ngspice`, `kicad`) and `EXPECTED_VERSIONS`. Single source of truth.

### `tool_manager/logger.py`
- **What It Does:** Logs each action to `logs/tool_manager.log` with timestamps.
- **Sample Log:** `[2025-04-06 10:52:03] [INSTALL] Tool: ngspice | Status: SUCCESS | Installed via Chocolatey`

---

## 4. Core Interactions
1. **CLI Command**: User runs `python main.py install kicad`.
2. **Dependency Check**: `dependencies.check_all_dependencies()` ensures you have Python ≥ 3.8, admin on Windows, and Chocolatey.
3. **Module Call**: If the environment’s good, calls `installer.install_tool('kicad')`.
4. **Logging**: Everything is recorded by `logger.py`.
5. **Menu Alternative**: `menu.py` does the same routine, but offers a numbered selection.

---

## 5. Example Flow: Installing ngspice
1. **Command**: `python main.py install ngspice`
2. **Dependencies**: `dependencies.check_all_dependencies()` → if something’s off, it logs and stops.
3. **Install**: `installer.install_tool('ngspice')` — checks if it’s already there, else triggers Chocolatey.
4. **Log**: The outcome (success/fail) gets logged.
5. Done.

---

## 6. Why This Structure?
- **Modularity**: Each file focuses on a single concern (check, install, update, etc.).
- **Clarity**: `main.py` is easy to read, while the heavy logic is in `tool_manager`.
- **Extensibility**: Add new tools by updating `constants.py` and adjusting detection logic in `tool_detection.py`.
- **Reliability**: Everything logs to a single file for easy debugging.

---

## 7. Features Present vs. Task Requirements

Below is a table matching the official requirements to the relevant features we’ve implemented:

| **Requirement**                 | **Implementation**                                                                                 |
|---------------------------------|----------------------------------------------------------------------------------------------------|
| Tool Installation Management    | Installs ngspice & KiCad via Chocolatey (Windows). Handles version checks, logs each install.     |
| Update and Upgrade System       | `update` command in `main.py` calls `choco upgrade` behind the scenes.                             |
| Configuration Handling          | `config.py` checks/fixes PATH. Specifically deals with KiCad’s bin directory.                      |
| Dependency Checker              | `dependencies.py` ensures Python ≥ 3.8, admin rights, and Chocolatey presence.                    |
| User Interface                  | CLI (Typer-based) plus optional menu (`menu.py`) for a guided approach.                           |
| Additional Features (Partial)   | Windows-only, partial Linux detection (no auto-install). Logging system for easy debugging.        |

> We primarily meet the installation, update, config, dependency checker, and user interface aspects. Full cross-platform support is not yet done.

---

## 8. Logging
We log all activity in `logs/tool_manager.log`. Each operation has a timestamp, so it’s simple to trace issues.

---

## 9. OS Support
- **Windows**: Fully tested. Chocolatey-based installs.
- **Linux**: Limited detection logic, no auto-install.
- **macOS**: Not yet implemented.

---

## 10. Future Enhancements
- Real Linux installation via apt or pacman.
- More EDA tools like GHDL or Verilator.
- Config file (`.toolmanagerrc`) for user prefs.
- GUI front-end for absolute novices.
- Automated testing + CI.

---

## 11. Conclusion
This system aims to centralize tool management for eSim, focusing on Windows. `main.py` and `menu.py` handle user interaction, while `tool_manager` does the heavy lifting. It’s not fancy, but it’s reliable, easy to extend, and logs everything that happens.

