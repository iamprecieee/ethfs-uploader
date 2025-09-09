import os
import re
import subprocess
from pathlib import Path

from enums import Colors
from printer import (
    celebration,
    print_error,
    print_info,
    print_input,
    print_process,
    print_step,
    print_success,
    print_warning,
)
from validator import validate_file_path, validate_private_key

try:
    import tkinter as tk
    from tkinter import filedialog

    HAS_GUI = True
except ImportError:
    HAS_GUI = False


def gui_file_picker():
    if not HAS_GUI:
        return None

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        print_step(1.2, 4, "Opening file picker dialog...")

        selected_path = filedialog.askopenfilename(
            title="Select file to upload",
            filetypes=[
                ("All files", "*.*"),
                ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("Documents", "*.pdf *.doc *.docx *.txt *.md"),
                ("Videos", "*.mp4 *.avi *.mov *.mkv"),
                ("Audio", "*.mp3 *.wav *.flac *.ogg"),
            ],
        )

        root.destroy()
        return selected_path if selected_path else None

    except Exception as e:
        print_warning(f"GUI picker failed: {str(e)}!")
        return None


def get_user_inputs():
    while True:
        private_key = print_input(
            "Enter your private key (with or without 0x): "
        ).strip()
        if not private_key:
            print_error("Private key cannot be empty!")
            continue

        valid, result = validate_private_key(private_key)
        if valid:
            private_key = result
            break
        else:
            print_error(result)

    file_path = None

    print("\nHow would you like to select your file/folder?")
    selection_options = []

    if HAS_GUI:
        selection_options.append("1. 📂 Open file picker dialog (GUI)")

    selection_options.extend(
        [f"{len(selection_options) + 1}. ⌨️  Enter file path manually"]
    )

    for option in selection_options:
        print(option)

    while not file_path:
        choice = print_input("Enter your file selection choice: ").strip()

        try:
            choice_num = int(choice)

            if HAS_GUI and choice_num == 1:
                file_path = gui_file_picker()
                if not file_path:
                    print_warning("No file selected!")
                    continue

            if not file_path:
                file_path = (
                    print_input("\nEnter the path to your file or folder: ")
                    .strip()
                    .strip('"')
                    .strip("'")
                )

                if not file_path:
                    print_error("File path cannot be empty!")
                    file_path = None
                    continue

        except ValueError:
            print_error("Please enter a valid option number!")
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

    print(
        "\nChoose upload type:\n1. blob (recommended - cheaper)\n2. calldata (traditional)"
    )

    while True:
        choice = print_input("Enter your upload choice (1 or 2, default: 1): ").strip()
        if choice == "" or choice == "1":
            upload_type = "blob"
            break
        elif choice == "2":
            upload_type = "calldata"
            break
        else:
            print_error("Please enter 1 or 2!")

    return private_key, file_path, upload_type


def create_flat_directory(private_key):
    print_step(2, 4, "Creating FlatDirectory contract on EthStorage Sepolia...")

    try:
        cmd = ["ethfs-cli", "create", "-p", private_key, "-c", "11155111"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print_error(f"Failed to create contract: {result.stderr}!")
            return None

        output = result.stdout
        address_match = re.search(r"Address is (0x[a-fA-F0-9]{40})", output)

        if address_match:
            contract_address = address_match.group(1)
            print_success(f"FlatDirectory created: {contract_address}")
            return contract_address
        else:
            print_error("Could not extract contract address from output")
            print(f"\n{output}")
            return None

    except subprocess.TimeoutExpired:
        print_error("Contract creation timed out!")
        return None
    except Exception as e:
        print_error(f"Error creating contract: {str(e)}!")
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

        print_info("Upload started. This may take a few minutes...")

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
            if "chunks" in line.lower() and "uploaded" in line.lower():
                print_process(line.strip(), Colors.CYAN)
            else:
                print_process(line.strip(), Colors.GREEN)

        process.wait()

        output_text = "\n".join(output_lines).lower()
        has_error = any(
            error_phrase in output_text
            for error_phrase in [
                "insufficient funds",
                "execution failed",
                "error:",
                "failed",
                "reverted",
            ]
        )

        if process.returncode == 0 and not has_error:
            celebration("Upload completed successfully")
            return True, output_lines
        else:
            print_error("Upload failed!")
            return False, output_lines

    except Exception as e:
        print_error(f"Error during upload: {str(e)}!")
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


def display_results(contract_address, urls):
    print_success("🎉 Upload Complete\n")

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
