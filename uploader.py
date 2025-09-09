"""
EthFS One-Command Uploader
A simple Python script to upload files to EthStorage in one command.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_GUI = True
except ImportError:
    HAS_GUI = False


class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_banner():
    banner = f"""
    {Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║             ETH File Storage one-command Uploader            ║
    ╚══════════════════════════════════════════════════════════════╝
    {Colors.END}
    """
    print(banner)


def print_step(step_num, total_steps, message):
    print(
        f"\n{Colors.BLUE}{Colors.BOLD}[{step_num}/{total_steps}]{Colors.END} {Colors.BOLD}{message}{Colors.END}"
    )

def print_info(message):
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}{Colors.BOLD}✅ {message}{Colors.END}")


def print_error(message):
    print(f"{Colors.RED}{Colors.BOLD}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {message}{Colors.END}")


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
            print_success("ethfs-cli is installed and ready!")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print_error("ethfs-cli not found!")
    
    if not check_npm():
        print_error("npm is also not installed!")
        print(f"\n{Colors.YELLOW}To use this script, you need to install Node.js and npm first:{Colors.END}")
        print("• Visit: https://nodejs.org/en/download/")
        print("• Download and install Node.js (includes npm)")
        print("• Then run this script again")
        return False

    install_now = (
        input(
            f"\n{Colors.YELLOW}{Colors.BOLD}Would you like to try installing it now? (y/n): {Colors.END}"
        )
        .lower()
        .strip()
    )

    if install_now == "y":
        print_info("Installing ethfs-cli...")
        try:
            subprocess.run(["npm", "i", "-g", "ethfs-cli"], check=True)
            print_success("ethfs-cli installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install ethfs-cli. Please install manually.")
            return False

    return False


def validate_private_key(private_key):
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key

    if len(private_key) != 66:
        return False, "Private key must be 64 characters (66 with 0x prefix)"

    if not re.match(r"^0x[a-fA-F0-9]{64}$", private_key):
        return False, "Private key contains invalid characters"

    return True, private_key


def validate_file_path(file_path):
    path = Path(file_path)
    if not path.exists():
        return False, f"Path does not exist: {file_path}"

    if path.is_file():
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > 100:
            print_warning(
                f"Large file detected: {size_mb:.1f}MB. Upload may take longer and cost more gas."
            )

    return True, str(path)


def gui_file_picker():
    if not HAS_GUI:
        return None
    
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print_info("Opening file picker dialog...")
       
        selected_path = filedialog.askopenfilename(
            title="Select file to upload",
            filetypes=[
                ("All files", "*.*"),
                ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("Documents", "*.pdf *.doc *.docx *.txt *.md"),
                ("Videos", "*.mp4 *.avi *.mov *.mkv"),
                ("Audio", "*.mp3 *.wav *.flac *.ogg")
            ]
        )
        
        root.destroy()
        return selected_path if selected_path else None
        
    except Exception as e:
        print_warning(f"GUI picker failed: {str(e)}")
        return None

def get_user_inputs():
    print(f"\n{Colors.BOLD}Let's get your upload details:{Colors.END}\n")

    while True:
        private_key = input(
            f"\n{Colors.CYAN}{Colors.BOLD}Enter your private key (with or without 0x): {Colors.END}"
        ).strip()
        if not private_key:
            print_error("Private key cannot be empty")
            continue

        valid, result = validate_private_key(private_key)
        if valid:
            private_key = result
            break
        else:
            print_error(result)

    file_path = None
    
    print(f"\n{Colors.BOLD}How would you like to select your file/folder?{Colors.END}")
    selection_options = []
    
    if HAS_GUI:
        selection_options.append("1. 📂 Open file picker dialog (GUI)")
    
    selection_options.extend([
        f"{len(selection_options) + 1}. ⌨️  Enter file path manually"
    ])
    
    for option in selection_options:
        print(option)
    
    while not file_path:
        choice = input(f"\n{Colors.YELLOW}Enter your choice: {Colors.END}").strip()
        
        try:
            choice_num = int(choice)
            
            if HAS_GUI and choice_num == 1:
                file_path = gui_file_picker()
                if not file_path:
                    print_warning("No file selected")
                    continue
                
            if not file_path:
                print(f"\n{Colors.CYAN}{Colors.BOLD}Enter the path to your file or folder:{Colors.END}")
                file_path = input("Path: ").strip().strip('"').strip("'")
                
                if not file_path:
                    print_error("File path cannot be empty")
                    file_path = None
                    continue
        
        except ValueError:
            print_error("Please enter a valid option number")
            continue
        
        if file_path:
            valid, result = validate_file_path(file_path)
            if valid:
                file_path = result
                print_success(f"Selected: {file_path}")
                break
            else:
                print_error(result)
                file_path = None
                

    print(f"\n{Colors.CYAN}{Colors.BOLD}Choose upload type:\n1. blob (recommended - cheaper)\n2. calldata (traditional){Colors.END}")

    while True:
        choice = input(f"\n{Colors.CYAN}{Colors.BOLD}Enter choice (1 or 2, default: 1): {Colors.END}").strip()
        if choice == "" or choice == "1":
            upload_type = "blob"
            break
        elif choice == "2":
            upload_type = "calldata"
            break
        else:
            print_error("Please enter 1 or 2")

    return private_key, file_path, upload_type


def create_flat_directory(private_key):
    print_step(2, 4, "Creating FlatDirectory contract on EthStorage Sepolia...")

    try:
        cmd = ["ethfs-cli", "create", "-p", private_key, "-c", "11155111"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print_error(f"Failed to create contract: {result.stderr}")
            return None

        output = result.stdout
        address_match = re.search(r"Address is (0x[a-fA-F0-9]{40})", output)

        if address_match:
            contract_address = address_match.group(1)
            print_success(f"FlatDirectory created: {contract_address}")
            return contract_address
        else:
            print_error("Could not extract contract address from output")
            print(f"{output}")
            return None

    except subprocess.TimeoutExpired:
        print_error("Contract creation timed out. Please try again.")
        return None
    except Exception as e:
        print_error(f"Error creating contract: {str(e)}")
        return None


def upload_file(file_path, contract_address, private_key, upload_type):
    print_step(3, 4, f"Uploading {os.path.basename(file_path)} to EthStorage...")

    try:
        cmd = [
            "ethfs-cli",
            "upload",
            "-f",
            file_path,
            "-a",
            contract_address,
            "-c",
            "11155111",
            "-p",
            private_key,
            "-t",
            upload_type,
        ]

        print_info("Upload started. This may take a few seconds...")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        output_lines = []
        for line in process.stdout:
            output_lines.append(line.strip())
            if "transaction hash" in line.lower():
                print(f"{Colors.GREEN}  → {line.strip()}{Colors.END}")
            elif "chunks" in line.lower() and "uploaded" in line.lower():
                print(f"{Colors.GREEN}  → {line.strip()}{Colors.END}")
            elif "total" in line.lower():
                print(f"{Colors.CYAN}  → {line.strip()}{Colors.END}")

        process.wait()

        if process.returncode == 0:
            print_success("Upload completed successfully!")
            return True, output_lines
        else:
            print_error("Upload failed!")
            return False, output_lines

    except Exception as e:
        print_error(f"Error during upload: {str(e)}")
        return False, []


def generate_access_urls(contract_address, file_path):
    print_step(4, 4, "Generating access URLs...")

    urls = []
    path_obj = Path(file_path)

    if path_obj.is_file():
        filename = path_obj.name
        web3_url = f"web3://{contract_address}:3333/{filename}"
        gateway_url = f"https://{contract_address.lower()}.3333.w3link.io/{filename}"
        urls.append((filename, web3_url, gateway_url))
    else:
        print_info("For directories, you can access files using:")
        print(f"  web3://{contract_address}:3333/path/to/your/file.ext")
        print(
            f"  https://{contract_address.lower()}.3333.w3link.io/path/to/your/file.ext"
        )

        try:
            for file in path_obj.rglob("*"):
                if file.is_file() and len(urls) < 5:
                    rel_path = file.relative_to(path_obj)
                    web3_url = f"web3://{contract_address}:3333/{rel_path}"
                    gateway_url = (
                        f"https://{contract_address.lower()}.3333.w3link.io/{rel_path}"
                    )
                    urls.append((str(rel_path), web3_url, gateway_url))
        except:
            pass

    return urls


def display_results(contract_address, urls, file_path):
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Upload Complete!{Colors.END}\n")

    print(
        f"{Colors.BOLD}Contract Address:{Colors.END} {Colors.CYAN}{contract_address}{Colors.END}"
    )
    print(f"{Colors.BOLD}Chain ID:{Colors.END} 11155111 (EthStorage Sepolia)")

    if urls:
        print(f"\n{Colors.BOLD}Access your files:{Colors.END}")
        for filename, web3_url, gateway_url in urls:
            print(
                f" {Colors.BOLD}Web3 URL:{Colors.END} {Colors.CYAN}{web3_url}{Colors.END}"
            )
            print(
                f"  {Colors.BOLD}Gateway:{Colors.END}  {Colors.CYAN}{gateway_url}{Colors.END}"
            )

    print(f"\n{Colors.PURPLE}{Colors.BOLD}Need to download files later?{Colors.END}")
    print(f"ethfs-cli download -a {contract_address} -c 11155111 -f <filename>")


def main():
    print_banner()

    if not check_ethfs_cli():
        sys.exit(1)

    print_warning("Make sure you have Sepolia ETH for gas fees!")
    print_info("Get free Sepolia ETH from: https://sepoliafaucet.com\n")

    try:
        private_key, file_path, upload_type = get_user_inputs()
    except KeyboardInterrupt:
        print_warning(f"\nUpload cancelled by user.")
        sys.exit(1)

    print_info(f"Starting upload process...")

    contract_address = create_flat_directory(private_key)
    if not contract_address:
        sys.exit(1)

    success, output = upload_file(file_path, contract_address, private_key, upload_type)
    if not success:
        print_error("Upload failed. Check the output above for details.")
        sys.exit(1)

    urls = generate_access_urls(contract_address, file_path)

    display_results(contract_address, urls, file_path)

    print(
        f"\n{Colors.GREEN}{Colors.BOLD}Thanks for using ETH File Storage one-command Uploader! 🚀{Colors.END}"
    )


if __name__ == "__main__":
    main()