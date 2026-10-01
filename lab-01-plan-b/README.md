# Lab 01 — Plan B: your first server in GitHub Codespaces

Use this **only if told to in class**, when Azure isn't working. It's the same lab as on Merlin: same goal, same live check, same cleanup. Only the place your server runs is different. Fix your name and the word of the day exactly as in the main instructions.

## 1. Start your machine (~5 min)

Fork this repo, then in **your fork**: **Code → Codespaces → Create codespace on main**. Open the terminal (**Ctrl + `**) once it's ready.

## 2. Make it a web server (~10 min)

```bash
sudo apt update && sudo apt install -y nginx
echo "<h1>Your Name</h1><p>Word of the day: WORD</p>" | sudo tee /var/www/html/index.html
sudo service nginx start
```

> A codespace is a **container**, so there is no `systemctl`. That's why we use `service`.

Open the **Ports** tab (next to *Terminal*). Port **80** appears as *nginx (Lab 01)*. Right-click it → **Port Visibility → Public**, then copy the **Forwarded Address** and open it on your phone.

## 3. Look around (~5 min)

```bash
nproc
free -h
cat /etc/os-release | head -2
```

Compare with the lecture demo (48 CPUs) and with what the Azure VM in the main instructions would give you. **Is a codespace IaaS or PaaS?** Which layers do *you* manage here? Bring your answer to the live check.

## 4. What does it cost? (~3 min)

Find the **price per hour** of a 2-core codespace in the GitHub Codespaces billing docs, and how many free core-hours per month your account gets. How many hours of this lab could you run for free?

## 5. Live check, then delete (~5 min)

Show me your page on the forwarded address with today's word, and answer one short question.

Then go to <https://github.com/codespaces> → **⋯** next to your codespace → **Delete**, and take a screenshot of the list without it.

## Submission (Merlin, by 19 October)

Same as the main lab, with these changes: instead of region and VM size, give the **machine type** (cores, RAM) and the **forwarded address**. Instead of the Azure price, give the **Codespaces price per hour**. Instead of the Azure screenshot, give the **screenshot of the deleted codespace**. Plus 3–4 sentences: which NIST characteristics did you experience, and is a codespace IaaS or PaaS? Why?
