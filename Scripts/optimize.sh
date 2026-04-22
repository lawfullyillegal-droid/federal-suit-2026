#!/data/data/com.termux/files/usr/bin/bash
# Simple Termux optimization script (non‑root)

echo "=== Step 1: Updating package lists and installed packages ==="
pkg update -y && pkg upgrade -y

echo "=== Step 2: Cleaning package cache ==="
apt clean
apt autoremove -y

echo "=== Step 3: Finding largest files in home directory (top 10) ==="
cd ~
du -ha | sort -k1hr | head -n 10

echo
echo "Review the list above and manually delete files you don't need."
echo "Example to delete a file or folder:"
echo "  rm -rf path/to/file_or_folder"
echo

echo "=== Step 4: Clearing Termux history and temp files ==="
rm -f ~/.bash_history 2>/dev/null
rm -rf /data/data/com.termux/files/usr/tmp/* 2>/dev/null

echo
echo "Done. For best effect, close all other apps and reboot your phone."


xy

