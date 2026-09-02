# Changelog

## 2026-05-06

### Experiência Sendit — Reordenação de bullets

Bullets reordenados para refletir o foco principal (Linux/Windows Server/M365/monitorização/automação), com Kubernetes e Ceph movidos para baixo:

| Posição | Bullet |
|---|---|
| 1 | Windows Server, Hybrid Azure AD, Active Directory, Group Policies |
| 2 | Linux **Ubuntu** 80+ hosts via Ansible *(adicionado "Ubuntu")* |
| 3 | Observabilidade: Zabbix, Prometheus, Grafana |
| 4 | Exchange Online / M365 automação PowerShell |
| 5 | Firewalls Fortinet/WatchGuard/HAProxy |
| 6 | Portal IT self-service (UserPortal) |
| 7 | **Kubernetes + Ceph** ← era o 1.º |
| 8 | Serviço de compressão de vídeo |
| 9 | OpenVAS vulnerability assessments |
| 10 | ITIL change management |

### Certificações

| Certificação | Antes | Depois |
|---|---|---|
| NSE 4 / NSE 7 | Planned | **Considering** |
| RHCSA | Considering | **Removida** |
| LFCS (Linux Foundation Certified SysAdmin) | — | **Adicionada** (Considering, Ubuntu-based) |

### Projetos — Divisão em duas categorias

`Projects.jsx` e `content.json` atualizados para mostrar dois grupos:

**Built at Work** (5 projetos):
- IT Infra Planning Toolkit
- Ansible Infrastructure Automation
- SharePoint Video Compression Pipeline
- Exchange Online Automation Suite
- UserPortal — Internal IT Self-Service Portal

**Personal & Homelab** (3 projetos):
- Proxmox VE Homelab
- Observability Stack
- Budget App — Personal Finance Tracker

### Email removido do website

`About.jsx` — removido o link `mailto:filipe.fernandes.work@gmail.com`. O bloco de contacto da página About agora só mostra LinkedIn.

### Ficheiros alterados
- `content.json`
- `website/src/content.json`
- `website/src/pages/About.jsx`
- `website/src/pages/Projects.jsx`
- `website/src/pages/Projects.css`
