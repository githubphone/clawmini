#!/bin/bash
# Keep Codespace alive by logging heartbeat every 20 minutes

echo "$(date): Heartbeat - Preventing Codespace sleep" >> /workspaces/clawmini/logs/heartbeat.log
# Create or touch a file to show activity
touch /workspaces/clawmini/.keepalive

# Optionally, we can do a light git operation to ensure git connection stays alive
cd /workspaces/clawmini && git status > /dev/null 2>&1 || true