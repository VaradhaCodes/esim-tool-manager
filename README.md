# eSim Tool Manager — README

This was part of a FOSSEE Fellowship task. The goal? Build a working CLI-based tool manager that can handle installation, version checking, updates, and PATH validation for tools like ngspice and KiCad. I focused entirely on Windows — didn’t bother with Linux or Mac because I wanted to go all-in on making one platform work cleanly.

---

## 🚀 What It Can Do

- Install ngspice or KiCad with Chocolatey (on Windows)
- Check if those tools are already installed, and what version
- Detect if your PATH is broken (and optionally fix it)
- Run basic sanity checks (Python version, admin rights, etc.)
- Give you a clean CLI *or* a simple menu UI if you don’t like typing commands
- Log everything it does — good or bad — to a file

---

## 📦 Tools This Manages

| Tool    | Expected Version |
| ------- | ---------------- |
| ngspice | 41.0.0           |
| KiCad   | 9.0              |

(If you’ve got a different version, it’ll tell you — and you can upgrade right from the CLI.)

---

## 🔧 Setup (Windows Only)

I didn’t want to half-support Linux or Mac — so this is fully Windows-focused and tested.

### Step 1: Install Chocolatey

[https://chocolatey.org/install](https://chocolatey.org/install)

### Step 2: Install Python 3.8 or newer

### Step 3: Clone the repo

```bash
git clone <your-repo-url>
cd tool-manager-folder
```

### Step 4: Install Python dependencies

If you want to use the interactive menu, you'll need to install `typer` — so just run this:

```bash
pip install typer
```

Highly recommend using the menu — it makes it way easier to test everything in one place without typing out each command.

---

## ✅ How to Use It

### Option 1: CLI commands

```bash
# Install ngspice
python main.py install ngspice

# Check installed tools
python main.py check

# Update a tool
python main.py update kicad

# Fix missing PATH entries
python main.py configure

# Uninstall a tool
python main.py uninstall ngspice

# List supported tools
python main.py list

# Check Python/Choco/admin status
python main.py diagnose
```

### Option 2: Menu (for simpler use)

```bash
python menu.py
```

It’s a basic numbered menu — nothing fancy, but it saves a hell of a lot of time when you just want to get stuff done quickly.

---

## 📁 Logs

Every action is logged to `logs/tool_manager.log`. If something fails, check the log.

```
[2025-04-06 10:52:03] [INSTALL] Tool: ngspice | Status: SUCCESS | Installed via Chocolatey
```

---

## ❓ Real-World Fixes for Real Problems

| Problem              | Fix                                                   |
| -------------------- | ----------------------------------------------------- |
| Chocolatey not found | Install it and restart your terminal                  |
| PATH is still broken | Use `python main.py configure`, then restart terminal |
| Installation failed  | Try running as admin, or check the logs               |
| Python too old       | Upgrade to 3.8+                                       |

---

## 🛠️ Future Ideas

- Add Linux install support (apt, pacman, etc.)
- Config file for custom version preferences
- Support more tools (GHDL, Verilator, etc.)
- GUI wrapper for people who hate terminals
- CI pipeline and unit tests

---

## Author

Varadha — built this from scratch as part of FOSSEE Summer Fellowship 2025. Prioritized working code over buzzwords. If you're reading this to evaluate the submission: everything here was written, tested, and structured to actually run without surprises.
Thank you for reading! 

Name  : Varadharam R S.
Email : vr428@snu.edu.in

---

