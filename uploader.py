"""
EthFS One-Command Uploader
A simple Python script to upload files to EthStorage in one command.
"""

import sys

from checker import check_ethfs_cli
from enums import Colors
from printer import print_banner, print_error, print_info, print_warning
from utils import (
    create_flat_directory,
    display_results,
    generate_access_urls,
    get_user_inputs,
    upload_file,
)


def main():
    print_banner("ETH FILE STORAGE ONE-COMMAND UPLOADER", Colors.PURPLE)

    if not check_ethfs_cli():
        sys.exit(1)

    print_warning("Make sure you have Sepolia ETH for gas fees!")
    print_info("Get free Sepolia ETH from: https://sepoliafaucet.com\n")

    print_banner("UPLOAD DETAILS")

    try:
        private_key, file_path, upload_type = get_user_inputs()
    except KeyboardInterrupt:
        print_warning("\nUpload cancelled by user.")
        sys.exit(1)

    print_banner("UPLOAD PROCESS")

    contract_address = create_flat_directory(private_key)
    if not contract_address:
        sys.exit(1)

    success, output = upload_file(file_path, contract_address, private_key, upload_type)
    if not success:
        print_error("Upload failed. Check the output above for details.")
        sys.exit(1)

    urls = generate_access_urls(contract_address, file_path)

    display_results(contract_address, urls)


if __name__ == "__main__":
    main()
