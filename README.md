# EthFS One-Command Uploader

Upload files to Ethereum/EthStorage with a single interactive Python script.

## Requirements

- Python 3.6+
- Node.js and npm (auto-checked and installable through script)
- Sepolia ETH for gas fees

## Quick Start

```bash
# Download the script
git clone https://github.com/iamprecieee/ethfs-uploader
cd ethfs-uploader

# Run it
python3 uploader.py
```

## Usage

The script will guide you through:

1. **Dependency Check** - Automatically installs ethfs-cli if needed
2. **Private Key** - Enter your wallet's private key (needs Sepolia ETH)
3. **File Selection** - Choose from GUI file picker or manual path entry
4. **Upload Type** - Select blob (cheaper) or calldata
5. **Automated Process** - Contract creation and file upload

## Expected Output

```
╔═════════════════════════════════════════════════╗
║ ╔═════════════════════════════════════════════╗ ║
║ ║    ETH FILE STORAGE ONE-COMMAND UPLOADER    ║ ║
║ ╚═════════════════════════════════════════════╝ ║
╚═════════════════════════════════════════════════╝

[1/4] Checking ethfs-cli installation...
✅ ethfs-cli is installed and ready
⚠️ Make sure you have Sepolia ETH for gas fees!
ℹ️  Get free Sepolia ETH from: https://sepoliafaucet.com

╔══════════════════════════╗
║ ╔══════════════════════╗ ║
║ ║    UPLOAD DETAILS    ║ ║
║ ╚══════════════════════╝ ║
╚══════════════════════════╝

Enter your private key (with or without 0x): 0x123abc...

How would you like to select your file/folder?
1. 📂 Open file picker dialog (GUI)
2. ⌨️  Enter file path manually
Enter your file selection choice: 1

[1.2/4] Opening file picker dialog...
✅ Selected: /path/to/your/image.jpg

Choose upload type:
1. blob (recommended - cheaper)
2. calldata (traditional)
Enter your upload choice (1 or 2, default: 1): 2

╔══════════════════════════╗
║ ╔══════════════════════╗ ║
║ ║    UPLOAD PROCESS    ║ ║
║ ╚══════════════════════╝ ║
╚══════════════════════════╝

[2/4] Creating FlatDirectory contract on EthStorage Sepolia...
✅ FlatDirectory created: 0x93995d703...182F7eBD9

[3/4] Uploading image.jpg to EthStorage...
ℹ️  Upload started. This may take a few minutes...
  → ℹ️ INFO:      Provider URL: http://65.108.230.142:8545/
  → ℹ️ INFO:      Chain ID: 11155111
  → ℹ️ INFO:      Address: 0x93995d703...182F7eBD9
  → ℹ️ INFO:      Thread pool size: 6
  → 
  → FlatDirectory: The transaction hash for chunk 0 is 0xd3b150702f5706c55770afd24a4723952a1a8798ed4ee0516b99945264ba89ef  image.jpg
  → FlatDirectory: Chunks 0 have been uploaded for image.jpg.
  → FlatDirectory: The transaction hash for chunk 1 is 0x94c5931cdc03742a9e0a6cc9fcc734a33af6dc56a9eb3fb6a87f15dab6ed8d5b  image.jpg
  → FlatDirectory: Chunks 1 have been uploaded for image.jpg.
  → FlatDirectory: The transaction hash for chunk 2 is 0x94805acb9835023cd62e6ee3b5f004d07f31c54220fb172aa3bb6e9b03a575c9  image.jpg
  → FlatDirectory: Chunks 2 have been uploaded for image.jpg.
  → FlatDirectory: The transaction hash for chunk 3 is 0x87ca79820505534f49647435b92462bedce8969aed9a70275708cdb31a1b3be2  image.jpg
  → FlatDirectory: Chunks 3 have been uploaded for image.jpg.
  → FlatDirectory: The transaction hash for chunk 4 is 0xc4e320fd8fcf248ad7fb39c5a9de175efa77e602f6f95630a7bed0b1ede3b9b3  image.jpg
  → FlatDirectory: Chunks 4 have been uploaded for image.jpg.
  → FlatDirectory: The transaction hash for chunk 5 is 0x4d8a9773f9afc585ab9a066bf937295b70431fe002680410d75c25fb2cc98385  image.jpg
  → FlatDirectory: Chunks 5 have been uploaded for image.jpg.
  → 
  → 
  → ✅  FINISH:    Total files: 1
  → ✅  FINISH:    Total chunks uploaded: 5
  → ✅  FINISH:    Total data uploaded: 1248.138671875 KB
  → ✅  FINISH:    Total storage cost: 0.0 ETH


    🎊🎊⭐🚀🚀 Upload completed successfully 🎊🎊⭐🚀🚀


[4/4] Generating access URLs...
✅ 🎉 Upload Complete

Contract Address: 0x93995d703...182F7eBD9
Chain ID: 11155111 (EthStorage Sepolia)

Access your files:
 Web3 URL: web3://0x93995d703...182F7eBD9:3333/image.jpg
 Gateway:  https://0x93995d703...182F7eBD9.3333.w3link.io/image.jpg

Need to download files later?
ethfs-cli download -a 0x93995d703...182F7eBD9 -c 11155111 -f <filename>
```

## Troubleshooting

**"npm not found"**
- Install Node.js from https://nodejs.org

**"Permission denied" on npm install**
- Try: `sudo npm i -g ethfs-cli`

**"Insufficient funds"**
- Get Sepolia ETH from https://sepoliafaucet.com