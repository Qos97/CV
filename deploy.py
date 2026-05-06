#!/usr/bin/env python3
"""
deploy.py — Pipeline completo de deploy

  1. python3 generate.py  (valida, gera DOCX + PDF, sincroniza website/src/ e website/public/)
  2. rsync website/ → VM
  3. docker compose up -d --build na VM

Uso: python3 deploy.py
Requisito: sshpass instalado  (sudo apt install sshpass)
Configuração: cria um ficheiro .env na raiz com VM_USER, VM_HOST e VM_PASS (ver .env.example)
"""

import subprocess, sys, os
from pathlib import Path

BASE = Path(__file__).parent

# Carrega .env se existir
env_file = BASE / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

VM_USER = os.environ.get("VM_USER", "ffernandes")
VM_HOST = os.environ.get("VM_HOST", "192.168.1.225")
VM_PASS = os.environ.get("VM_PASS", "")
LOCAL   = str(BASE / "website") + "/"
REMOTE  = "~/cv-filipe/"

if not VM_PASS:
    print("ERROR: VM_PASS não definido. Cria um ficheiro .env (ver .env.example)")
    sys.exit(1)


def step(msg):
    print(f"\n→ {msg}...")


def run(cmd, env_extra=None, check=True):
    import os
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(cmd, env=env, check=check)


# ── 1. Gerar tudo ─────────────────────────────────────────────────────────────
step("Gerando conteúdo (content.json → DOCX + PDF + website/src/)")
try:
    run(["python3", str(BASE / "generate.py")])
except subprocess.CalledProcessError:
    print("ERROR: generate.py falhou — corrige os erros acima antes de fazer deploy")
    sys.exit(1)


# ── 2. Rsync → VM ─────────────────────────────────────────────────────────────
step(f"Sincronizando ficheiros → {VM_HOST}:{REMOTE}")
try:
    run(
        ["sshpass", "-e", "rsync", "-avz", "--delete",
         "-e", "ssh -o StrictHostKeyChecking=no",
         LOCAL, f"{VM_USER}@{VM_HOST}:{REMOTE}"],
        env_extra={"SSHPASS": VM_PASS},
    )
except subprocess.CalledProcessError:
    print("ERROR: rsync falhou")
    sys.exit(1)


# ── 3. Rebuild container ───────────────────────────────────────────────────────
step("Rebuild Docker na VM")
try:
    run(
        ["sshpass", "-e", "ssh", "-o", "StrictHostKeyChecking=no",
         f"{VM_USER}@{VM_HOST}",
         "cd ~/cv-filipe && docker compose up -d --build 2>&1"],
        env_extra={"SSHPASS": VM_PASS},
    )
except subprocess.CalledProcessError:
    print("ERROR: docker compose falhou na VM")
    sys.exit(1)


print(f"\n✓ Deploy completo → http://{VM_HOST}:8080\n")
