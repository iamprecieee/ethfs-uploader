import subprocess

from printer import print_error, print_info, print_input, print_step, print_success


def check_npm():
    try:
        result = subprocess.run(
            ["npm", "--version"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_ethfs_cli():
    print_step(1, 4, "Checking ethfs-cli installation...")

    try:
        result = subprocess.run(
            ["ethfs-cli", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print_success("ethfs-cli is installed and ready")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print_error("ethfs-cli not found!")

    if not check_npm():
        print_error("npm is also not installed!")
        print_info("\nTo use this script, you need to install Node.js and npm first")
        print_info("Visit: https://nodejs.org/en/download/")
        print_info("Download and install Node.js (includes npm)")
        print_info("Then run this script again")
        return False

    install_now = (
        print_input("Would you like to try installing it now? (y/n): ").lower().strip()
    )

    if install_now == "y":
        print_step(1.1, 4, "Installing ethfs-cli...")
        try:
            subprocess.run(["npm", "i", "-g", "ethfs-cli"], check=True)
            print_success("ethfs-cli installed successfully")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install ethfs-cli. Please install manually.")
            return False

    return False
