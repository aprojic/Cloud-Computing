<p align="center">
  <img src=".github/banner.png" alt="ITSuO Labs — Cloud IT Systems at Aspira University of Applied Sciences" width="100%">
</p>

<p align="center">
  <a href="https://codespaces.new/aprojic/ITSuO-labs?quickstart=1"><img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces" height="32"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Ubuntu-24.04-0E1116?style=flat-square&logo=ubuntu&logoColor=white" alt="Ubuntu 24.04">
  <img src="https://img.shields.io/badge/Docker-in--Docker-0E1116?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Azure-for%20Students-0E1116?style=flat-square&logo=microsoftazure&logoColor=white" alt="Azure for Students">
  <img src="https://img.shields.io/badge/semester-2026%2F27-E82028?style=flat-square" alt="Semester 2026/27">
</p>

Lab environment for **IT sustavi u oblaku / Cloud IT Systems** at Aspira University of Applied Sciences, Split.
Lab instructions (EN + HR) are on **Merlin**. This repository holds the environment and the code the labs use.

## 🚀 Quick start

| # | Do this | What you get |
|:-:|---|---|
| **1** | Click **Open in GitHub Codespaces** above | or *Code → Codespaces → Create codespace on main* |
| **2** | Wait a minute or two for the environment to build | Ubuntu 24.04 + Docker, the same OS as the Azure VM in Lab 01 |
| **3** | Open the terminal with <kbd>Ctrl</kbd> + <kbd>`</kbd> and follow the lab | instructions on Merlin, code in this repo |

> [!TIP]
> When a lab asks you to **save your work**, fork the repo first (top right → **Fork**) and open the codespace from *your* fork. When new labs appear here, update your fork with **Sync fork → Update branch**.

## 🧪 Labs

| # | Lab | Runs on | In this repo |
|:-:|---|---|---|
| 00 | Set up your cloud | Azure for Students | — |
| 01 | Your first server in the cloud (IaaS) | Azure Cloud Shell | [`lab-01-plan-b/`](lab-01-plan-b/), the same lab in Codespaces, **only when told to use Plan B** |
| 02 | Same app, different model (PaaS) | Azure App Service | *coming soon* |
| 03–05 | Containers with Docker | Codespaces | *coming soon* |
| 06 | Containers in the cloud | Azure Container Apps | *coming soon* |
| 07 | AI in the cloud | Codespaces + model APIs | *coming soon* |

## 🧰 What's inside

- **Ubuntu 24.04** dev container ([`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json))
- **Docker** inside the codespace (Docker-in-Docker), for the container labs
- Port **80** forwarded automatically and labelled *nginx (Lab 01)*
- 2 CPU cores, which fits the free monthly Codespaces quota

> [!WARNING]
> **Stop or delete your codespace when you're done.** A running codespace uses your free monthly quota even when you're not looking at it.
> Manage them at <https://github.com/codespaces>.

<details>
<summary><b>🛟 Troubleshooting</b></summary>

<br>

| Problem | Fix |
|---|---|
| `systemctl` says *systemd is not running* | A codespace is a container. Use `sudo service <name> start` instead. |
| Page opens only for you, not on your phone | **Ports** tab → right-click the port → **Port Visibility → Public** |
| Codespace stopped by itself | It stops after 30 minutes of inactivity. Restart it from <https://github.com/codespaces>, and your files are still there. |
| Out of free hours | Delete codespaces you don't use. Verified students get more hours with the [GitHub Student Developer Pack](https://education.github.com/pack). |

</details>

---

<p align="center">
  <sub>Cloud IT Systems · Aspira University of Applied Sciences · <a href="https://www.aspira.hr">aspira.hr</a></sub>
</p>
