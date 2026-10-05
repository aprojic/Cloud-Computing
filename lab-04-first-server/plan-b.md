# Lab 04 — Plan B: your first server in GitHub Codespaces

Use this if you **can't use Azure for Students** (e.g. you're a part-time student), or when I announce Plan B for the whole class. It's the same lab as the [main instructions](README.md): same goal, same kind of report, same cleanup. Only the place your server runs is different.

## 1. Start your machine (~5 min)

Click **Open in GitHub Codespaces** on the [repository's main page](../README.md), or use **Code → Codespaces → Create codespace on main**. You don't need a fork for this lab. Once it's ready, open a terminal: menu **☰ → Terminal → New Terminal**.

## 2. Make it a web server (~10 min)

```bash
sudo apt update && sudo apt install -y nginx
echo "<meta charset=utf-8><h1>Your Name</h1><p>$GITHUB_USER · $CODESPACE_NAME · $(date -u '+%Y-%m-%d %H:%M UTC')</p>" | sudo tee /var/www/html/index.html
sudo service nginx start
```

> A codespace is itself a **container**, running on a VM that GitHub rents for you. That's why there is no `systemctl`, and we use `service` instead.

Open the **Ports** tab (next to *Terminal*). Port **80** appears in the list. Right-click it → **Port Visibility → Public**, then copy the **Forwarded Address** and open it in a browser (your phone works too). The page shows your GitHub username, your codespace name (it's also part of the address) and the time.

**Take Screenshot A now:** the browser with the **forwarded address in the address bar** and your page.

> Notice the address starts with `https://`, while the Azure VM in the main lab serves plain `http://`. GitHub puts its own HTTPS proxy in front of your server. Who manages that layer here: you or GitHub?

## 3. Look around (~5 min)

```bash
nproc
free -h
head -2 /etc/os-release
```

In Lab 01 you ran nginx **inside a container** on a codespace. Today you installed it **on the codespace itself**, the way you would on a VM. Think about it: **is a codespace IaaS or PaaS?** Which layers do *you* manage here, and which ones does GitHub manage? (The service models are covered in Lecture 1.)

## 4. What would the VM cost? (~8 min)

You didn't rent an Azure VM, but you can still price one. The pricing pages are public, so you don't need a subscription. Use the same VM as the main lab: **Standard_B2ats_v2**, Linux, in **West Europe**.

1. **List price.** On <https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/> find the hourly price of that VM. A VM is not just the VM: it also needs an OS disk (assume a 30 GB Standard SSD) and a public IP, and both cost money too. Estimate all three for one forgotten month (730 hours).
2. **What a student would really pay.** Read the free services on <https://azure.microsoft.com/en-us/free/students>. With Azure for Students, how much of that month would come out of the $100 credit, and why?
3. **Compare.** In Lab 01 you found the price per hour of a 2-core codespace. Which is cheaper per hour, and what do you get for the money in each case?

## 5. Delete it (~3 min)

Go to <https://github.com/codespaces> → **⋯** next to your codespace → **Delete**. Take **Screenshot C**: the list without it.

## Submission (Merlin, any time before the first exam period)

`lab04_<surname>.pdf` with:

1. **Your data:** machine type (cores, RAM) and the forwarded address.
2. **Screenshot A:** your page in a browser, with the forwarded address in the address bar (2).
3. **Screenshot C:** your codespace list without the deleted codespace (5). There's no Screenshot B.
4. **Your cost answers** from 4: list price per month of VM + disk + IP (show the calculation), what a student would really pay and why, and the comparison with a codespace.
5. **Short answers**, in your own words:
   - Is a codespace IaaS or PaaS? Which layers did you manage, and which did GitHub?
   - What changed between running nginx in a container (Lab 01) and installing it on the machine (today)?
   - What did `nproc` print, and what does that number mean here?
   - Why does the address start with `https://`, and who manages that layer?
   - Which NIST characteristics did you experience in this lab, and where exactly? Name at least three and use **your own numbers**.

*Your report is about **your** run: your username, your codespace, your times. Reports that don't match each other or look copied will be checked again, and I may ask you to walk me through your report.*
