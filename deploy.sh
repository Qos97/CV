#!/bin/bash
set -e

VM_USER="ffernandes"
VM_HOST="192.168.1.225"
VM_PASS="Pipoqos0411!"

LOCAL="/mnt/c/Users/filip/OneDrive/Documentos/CV/website/"
REMOTE="~/cv-filipe/"

export SSHPASS="$VM_PASS"

echo "→ Converting CVs to PDF..."
powershell.exe -NoProfile -ExecutionPolicy Bypass \
  -File "C:\\Users\\filip\\OneDrive\\Documentos\\CV\\scripts\\convert-cv.ps1" \
  || { echo "ERROR: CV conversion failed"; exit 1; }

echo "→ Generating site content..."
python3 generate.py || { echo "ERROR: generate.py failed"; exit 1; }

echo "→ Syncing files..."
sshpass -e rsync -avz -e "ssh -o StrictHostKeyChecking=no" "$LOCAL" "$VM_USER@$VM_HOST:$REMOTE"

echo "→ Building and starting container..."
sshpass -e ssh -o StrictHostKeyChecking=no "$VM_USER@$VM_HOST" "cd ~/cv-filipe && docker compose up -d --build"
# Note: remote folder remains ~/cv-filipe (VM side unchanged)

echo "✓ Done — http://$VM_HOST:8080"
