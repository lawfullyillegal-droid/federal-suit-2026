#!/bin/bash
LOG_FILE="$HOME/command-center/logs/env_$(date +%Y%m%d_%H%M%S).log"
echo "--- Environment Snapshot: $(date) ---" > "$LOG_FILE"
lsof 2>/dev/null | grep "/com.termux/" | awk '{print $9}' | sort | uniq >> "$LOG_FILE"
echo "Snapshot saved to $LOG_FILE"
