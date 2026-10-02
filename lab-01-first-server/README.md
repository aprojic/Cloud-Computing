<!-- kicker: Lab 01 · IaaS · 5 October 2026 -->
# Lab 01 — Your first server in the cloud

*Rent a Linux machine in a Microsoft data centre, make it serve your web page, find out what it costs, and delete it, all in 45 minutes.*

`45 min` · `Azure · Cloud Shell · nginx` · `level: intro` · `submit: Merlin`

## Scenario

A small Split agency wants a web page online **tonight**. They have no servers and no budget to buy one. You are going to rent one by the hour, put the page on it, show the client that it works from a phone, tell them what it would cost per month, and then switch everything off so it costs nothing.

## Learning outcomes

- Provision a virtual machine yourself, without a ticket or a phone call (*on-demand self-service*).
- Explain which layers you manage in **IaaS** and which ones the provider manages.
- Connect to a cloud server over SSH and run a web server on it.
- Find the real price of a cloud resource, and remove resources so they stop costing money.

## Prerequisites

- [ ] **[Lab 00](../lab-00-setup/README.md) done:** Azure for Students is active, Cloud Shell works, and you have **your list of allowed regions**.
- [ ] A phone (or a second browser tab) to open your page.

> [!TIP]
> **No Azure subscription? Plan B**
>
> If you can't use Azure for Students (e.g. you're a part-time student), do the same lab **on your own** in GitHub Codespaces: [plan-b.md](plan-b.md). You only need a GitHub account. If Azure fails for most of the class, I'll announce Plan B for everyone.

> [!TIP]
> **Copy commands from this GitHub page** (copy button on each code block), not from the PDF. PDF viewers often break multi-line commands.

## Part 1 — Rent a server · ~12 min

### 1.1 Set your variables

In Cloud Shell, set three variables. Change `swedencentral` to **your Lab 01 region** from Lab 00:

```bash
RG=lab1-rg
LOC=swedencentral   # ← change to YOUR region from Lab 00
VM=web1
```

> [!TIP]
> **Cloud Shell forgets**
>
> The session ends after 20 minutes without activity, **and also when you close or reload its browser tab**. Then the variables are gone. Open anything else (portal pages, pricing) in a **new browser tab**. If a command later complains about an empty value, run these three lines again.

### 1.2 Create a resource group

A *resource group* is a folder for everything you create today. Deleting it at the end deletes everything inside.

```bash
az group create --name $RG --location $LOC -o table
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> Location     Name
> -----------  -------
> westeurope   lab1-rg
> ```

### 1.3 Create the virtual machine

```bash
time az vm create \
  --resource-group $RG --name $VM \
  --image Ubuntu2404 --size Standard_B2ats_v2 \
  --admin-username student --generate-ssh-keys \
  --public-ip-sku Standard
```

`time` measures how long it took. **Write down the `real` time**, because it goes in your report. While you wait, think about how long it took a company in 2005 to get a new server.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> {
>   "location": "westeurope",
>   "powerState": "VM running",
>   "privateIpAddress": "10.0.0.4",
>   "publicIpAddress": "20.123.45.67",
>   "resourceGroup": "lab1-rg",
>   ...
> }
> real    1m12.345s
> user    0m1.234s
> sys     0m0.123s
> ```

> [!TIP]
> **Common errors**
>
> - `RequestDisallowedByAzure` or `RequestDisallowedByPolicy`: the region isn't on your allowed list. Pick another one, run `az group delete -n $RG --yes`, and start again from 1.1.
> - `SkuNotAvailable`: that VM size isn't available there. Try `--size Standard_B1s` or another allowed region.

> [!IMPORTANT]
> **In the report**
>
> Region, VM size and the `real` time.

## Part 2 — Make it a web server · ~12 min

### 2.1 Open port 80

By default the VM only lets in SSH (port 22). A web server needs port 80.

```bash
az vm open-port --resource-group $RG --name $VM --port 80 -o none
```

### 2.2 Log in

```bash
IP=$(az vm show -d -g $RG -n $VM --query publicIps -o tsv)
echo $IP
ssh student@$IP
```

Type `yes` when asked about the host fingerprint. Your prompt changes to `student@web1:~$`. You are now on a computer in a data centre.

> [!TIP]
> **Permission denied (publickey)?**
>
> Your Cloud Shell session probably restarted and lost the SSH key **and** your variables. First run the three lines from 1.1 and the `IP=` line from 2.2 again. Then run `ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa`, then `az vm user update -g $RG -n $VM -u student --ssh-key-value ~/.ssh/id_rsa.pub`, and try `ssh` again.

### 2.3 Install nginx and publish your page

On the VM:

```bash
sudo apt update && sudo apt install -y nginx
echo '<meta charset="utf-8"><h1>Your Name</h1><p>Word of the day: WORD</p>' | sudo tee /var/www/html/index.html
```

Replace **Your Name** with your name (č, ć, š, ž, đ are fine) and **WORD** with the word written on the board at the start of the lab. Then open `http://` followed by your IP on your phone. Note that it is `http`, not `https`.

> [!TIP]
> **Page doesn't load?**
>
> - Check that the address starts with `http://`, because the browser may add `https`.
> - Chrome may warn **"Connection is not secure"**. Tap **Continue to site**. That's expected: your server has no certificate. (Who would manage that layer in IaaS?)
> - Check that 2.1 ran.
> - Check that nginx is running: `systemctl is-active nginx` should print `active`.

## Part 3 — Look around and count the cost · ~8 min

### 3.1 What did you get?

Still on the VM:

```bash
nproc
free -h
curl -s -H Metadata:true \
  "http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01" \
  | python3 -m json.tool | grep -E '"(location|vmSize|zone)"'
```

The last command asks the **Azure Instance Metadata Service** about the machine itself. It only answers from inside an Azure VM.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> 2
>               total        used        free      shared  buff/cache   available
> Mem:          960Mi        ...
>     "location": "westeurope",
>     "vmSize": "Standard_B2ats_v2",
>     "zone": "",
> ```

Remember this number: **2** (or 1 on `B1s`). In an upcoming lecture you'll see a machine answer the same command with **48**, and we'll work out why.

Type `exit` to leave the VM.

### 3.2 What does it cost?

Open these in a **new browser tab** (keep Cloud Shell open):

1. **List price.** On <https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/> find the hourly price of your VM size in your region. A VM is not just the VM: it also has an OS disk and a public IP, and both cost money too. Estimate the list price of all three for one forgotten month (730 hours). Use the portal (your VM → *Disks* and *Overview*) to see which disk type you got.
2. **What you'd really pay.** Read the free services on <https://azure.microsoft.com/en-us/free/students>. With Azure for Students, how much of that month would actually come out of your $100 credit, and why?

> [!IMPORTANT]
> **In the report**
>
> The list price per month of VM + disk + IP (show the calculation), what you'd actually pay with Azure for Students, and why the two differ.

## Part 4 — Show it, then delete it · ~8 min

### 4.1 Live check

**Raise your hand as soon as your page works** (usually from about minute 20). I check people in the order they're ready, and you carry on with Part 3 or delete (4.2) right after. Show me your page on **your** public IP with today's word. I write down your IP, so put the same IP in your report. Then I ask one short question about what you just did, for example:

- Why did we have to open port 80?
- What did `nproc` print, and what does that number mean?
- What gets deleted when you delete the resource group?
- What would keep costing money if you didn't delete anything?

If I haven't reached you by the end of class, **don't delete yet**: stay a few minutes after class, show me, then delete.

### 4.2 Delete everything. Don't skip this!

Back in Cloud Shell (not on the VM):

```bash
az group delete --name $RG --yes
az group list -o table
```

The delete takes a minute or two. Afterwards `lab1-rg` must **not** appear in the list.

> [!NOTE]
> **Expected output**
>
> `lab1-rg` is gone. You may see other groups that Azure created automatically (e.g. `NetworkWatcherRG`), and that's fine.

> [!WARNING]
> **Why this matters**
>
> A running VM keeps using your credit even when you're not looking at it, and so do its disk and public IP. Deleting the resource group removes all of it at once.

## Submission · by 19 October, before Lab 02

> [!IMPORTANT]
> **To Merlin**
>
> - `lab01_<surname>.pdf` with:
>   1. Region, VM size, the `real` time from 1.3, and the **public IP** you showed at the live check.
>   2. A screenshot of the `az vm create` output showing that same IP.
>   3. The cost answers from 3.2: list price per month (VM + disk + IP) and what you'd actually pay.
>   4. A screenshot of `az group list` showing that `lab1-rg` is gone.
>   5. **3–4 sentences:** which NIST characteristics did you experience in this lab, and where exactly? Name at least three and use **your own numbers** (time, price, IP). We cover NIST in the lecture on 12 October, before the deadline.
> - **Live check (4.1)** done in class. Without it the lab is not accepted.

| Item | Required |
|---|:-:|
| Live check: page on your own IP with today's word + one answer | gate (pass/fail) |
| Report: region, size, time, IP (matches the live check), cost answers | ✓ |
| Proof of cleanup (screenshot) | ✓ |
| NIST reflection (3+ characteristics, tied to your own numbers) | ✓ |

*Your answers are about **your** run: your region, your time, your price. Two identical reports will both be checked again in person.*
