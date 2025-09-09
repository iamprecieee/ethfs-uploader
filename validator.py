import re
from pathlib import Path

from printer import print_warning


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
