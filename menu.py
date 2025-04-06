import subprocess
import sys

python_executable = sys.executable

# Define the tools in a simple map so we don't repeat "if choice == '1' -> 'ngspice', etc." in multiple places.
TOOLS = {
    "1": "ngspice",
    "2": "kicad"
}

def print_menu():
    """Prints the main menu options."""
    print("\n=== eSim Tool Manager ===")
    print("1. Install a tool")
    print("2. Check installed tools")
    print("3. Update a tool")
    print("4. Configure environment")
    print("5. Uninstall a tool")
    print("6. Exit")

def install_menu():
    """Presents a sub-menu for installing a specific tool."""
    print("\nSelect a tool to install:")
    print("1. ngspice")
    print("2. kicad")
    choice = input("Enter your choice (1-2): ").strip()

    if choice in TOOLS:
        subprocess.run([python_executable, "main.py", "install", TOOLS[choice]])
    else:
        print("Invalid option. Please try again.")

def update_menu():
    """Sub-menu for updating a tool."""
    print("\nSelect a tool to update:")
    print("1. ngspice")
    print("2. kicad")
    choice = input("Enter your choice (1-2): ").strip()

    if choice in TOOLS:
        subprocess.run([python_executable, "main.py", "update", TOOLS[choice]])
    else:
        print("Invalid option. Please try again.")

def uninstall_menu():
    """Sub-menu for uninstalling a tool."""
    print("\nSelect a tool to uninstall:")
    print("1. ngspice")
    print("2. kicad")
    choice = input("Enter your choice (1-2): ").strip()

    if choice in TOOLS:
        subprocess.run([python_executable, "main.py", "uninstall", TOOLS[choice]])
    else:
        print("Invalid option. Please try again.")

def main():
    """Main loop that shows the menu and handles user selections."""
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            install_menu()
        elif choice == "2":
            subprocess.run([python_executable, "main.py", "check"])
        elif choice == "3":
            update_menu()
        elif choice == "4":
            subprocess.run([python_executable, "main.py", "configure"])
        elif choice == "5":
            uninstall_menu()
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
