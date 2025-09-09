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
╔══════════════════════════════════════════════════════════════╗
║             ETH File Storage one-command Uploader            ║
╚══════════════════════════════════════════════════════════════╝

[1/4] Checking ethfs-cli installation...
✅ ethfs-cli is installed and ready!

⚠️  Make sure you have Sepolia ETH for gas fees!
ℹ️  Get free Sepolia ETH from: https://sepoliafaucet.com

Let's get your upload details:

Enter your private key (with or without 0x): 0x123abc...

How would you like to select your file/folder?
1. 📂 Open file picker dialog (GUI)
2. ⌨️  Enter file path manually

Enter your choice: 1
ℹ️  Opening file picker dialog...
✅ Selected: /path/to/your/image.jpg

Choose upload type:
1. blob (recommended - cheaper)
2. calldata (traditional)

Enter choice (1 or 2, default: 1): 1

[2/4] Creating FlatDirectory contract on EthStorage Sepolia...
✅ FlatDirectory created: 0x97f876bD0f27eEBF4b48AE25E300B57db6C27237

[3/4] Uploading image.jpg to EthStorage...
ℹ️  Upload started. This may take a few seconds...
  → FlatDirectory: The transaction hash for chunk 0 is 0x2de16cde...
  → FlatDirectory: Chunks 0,1,2 have been uploaded for image.jpg
✅ Upload completed successfully!

[4/4] Generating access URLs...

🎉 Upload Complete!

Contract Address: 0x97f876bD0f27eEBF4b48AE25E300B57db6C27237
Chain ID: 11155111 (EthStorage Sepolia)

Access your files:
Web3 URL: web3://0x97f876bD0f27eEBF4b48AE25E300B57db6C27237:3333/image.jpg
Gateway:  https://0x97f876bd0f27eebf4b48ae25e300b57db6c27237.3333.w3link.io/image.jpg

Need to download files later?
ethfs-cli download -a 0x97f876bD0f27eEBF4b48AE25E300B57db6C27237 -c 11155111 -f image.jpg

Thanks for using ETH File Storage one-command Uploader! 🚀
```

## Troubleshooting

**"npm not found"**
- Install Node.js from https://nodejs.org

**"Permission denied" on npm install**
- Try: `sudo npm i -g ethfs-cli`

**"Insufficient funds"**
- Get Sepolia ETH from https://sepoliafaucet.com