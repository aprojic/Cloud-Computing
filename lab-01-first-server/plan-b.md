# Lab 01 — Plan B: your first server in GitHub Codespaces

Use this if you **can't use Azure for Students** (e.g. you're a part-time student), or when I announce Plan B for the whole class. It's the same lab as the [main instructions](README.md): same goal, same live check, same cleanup. Only the place your server runs is different. Put your name and the word of the day on the page exactly as in the main instructions.

## 1. Start your machine (~5 min)

Click **Open in GitHub Codespaces** on the [repository's main page](../README.md), or use **Code → Codespaces → Create codespace on main**. You don't need a fork for this lab. Once it's ready, open a terminal: menu **☰ → Terminal → New Terminal**.

## 2. Make it a web server (~10 min)

```bash
sudo apt update && sudo apt install -y nginx
echo '<meta charset="utf-8"><h1>Your Name</h1><p>Word of the day: WORD</p>' | sudo tee /var/www/html/index.html
sudo service nginx start
```

> A codespace is a **container**, so there is no `systemctl`. That's why we use `service`.

Open the **Ports** tab (next to *Terminal*). Port **80** appears as *nginx (Lab 01)*. Right-click it → **Port Visibility → Public**, then copy the **Forwarded Address** and open it on your phone.

> Notice the address starts with `https://`, while on the Azure VM it was `http://`. GitHub puts its own HTTPS proxy in front of your server. Who manages that layer here: you or GitHub?

## 3. Look around (~5 min)

```bash
nproc
free -h
cat /etc/os-release | head -2
```

Remember these numbers and compare them with what the Azure VM in the main instructions would give you. Think about it: **is a codespace IaaS or PaaS?** Which layers do *you* manage here? (We cover the models in the lecture on 12 October, so this goes in your report, not the live check.)

## 4. What does it cost? (~3 min)

Find the **price per hour** of a 2-core codespace in the GitHub Codespaces billing docs, and how many free core-hours per month your account gets. How many hours of this lab could you run for free?

## 5. Live check, then delete (~5 min)

Show me your page on the forwarded address with today's word, and answer one short question.

Then go to <https://github.com/codespaces> → **⋯** next to your codespace → **Delete**, and take a screenshot of the list without it.

## Submission (Merlin, by 19 October)

Same as the main lab, with these changes: instead of region and VM size, give the **machine type** (cores, RAM) and the **forwarded address**. Instead of the Azure price, give the **Codespaces price per hour**. Instead of the Azure screenshot, give the **screenshot of the deleted codespace**. Plus 3–4 sentences: which NIST characteristics did you experience, and is a codespace IaaS or PaaS? Why?
