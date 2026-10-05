<!-- kicker: Lab 00 · setup -->
# Lab 00 — Set Up Your Cloud

*A Linux machine with Docker in your browser for the container labs, and your own Azure subscription for the real-cloud labs. Set it up once and use it all semester.*

`~30 min` · `GitHub · Codespaces · Azure for Students` · `once, at home` · `prerequisite for Lab 01`

## Why

The first labs teach **containers**, the way almost all cloud software is packaged and shipped today. You run them in **GitHub Codespaces**: a Linux machine in a data centre, with Docker installed, opened in your browser. Later in the semester (Lab 04) you rent a real server in a Microsoft data centre, and for that you need your own **Azure for Students** subscription. Neither needs a credit card, and you don't need to install anything.

## Outcomes

- Open a codespace from the course repository and run your first container.
- Apply for the GitHub Student Developer Pack (more free Codespaces hours).
- Activate an Azure for Students subscription with your Aspira email, and find the regions it allows (needed for Lab 04).

## Prerequisites

- [ ] Access to your **@aspira.hr** mailbox (you'll receive verification emails).
- [ ] A computer with a modern browser (Chrome, Edge, Firefox or Safari).
- [ ] Your phone (you may be asked to verify a phone number or set up sign-in security).

> [!TIP]
> **Copy commands from this GitHub page** (copy button at the top right of each code block), not from the PDF. PDF viewers often break multi-line commands.

> **Part A before Monday 5 October** (Lab 01). Part B can wait until Lab 04 on 16 November, but student verification sometimes takes days, so start it now. If you already activated Azure this week, Part B is done.

## Part A — GitHub and Codespaces (needed for Lab 01) · ~15 min

### A.1 Your GitHub account

Create an account at <https://github.com>, or use the one you have. Add your **@aspira.hr** email under *Settings → Emails*. Pick a username you're happy to show: it appears in your lab reports.

### A.2 Open a codespace and run a container

1. Open the course repository <https://github.com/aprojic/Cloud-Computing> and click **Open in GitHub Codespaces**, then **Create new codespace**. The first start takes a minute or two.
2. When VS Code opens in the browser, open a terminal: menu **☰ → Terminal → New Terminal**.
3. Run:

```bash
docker run --rm alpine echo "Hello from a container"
```

> [!NOTE]
> **Expected output**
>
> ```
> Unable to find image 'alpine:latest' locally
> latest: Pulling from library/alpine
> ...
> Status: Downloaded newer image for alpine:latest
> Hello from a container
> ```
>
> The last line is what matters. You'll learn what the rest means in Lab 01.

4. **Stop the codespace** when you're done: <https://github.com/codespaces> → **⋯** next to it → **Stop codespace**. A running codespace uses your free monthly hours even when you're not looking at it. (It also stops by itself after 30 minutes without activity.)

> [!TIP]
> **Common pitfalls**
>
> - **`Cannot connect to the Docker daemon`**: Docker is still starting. Wait 30 seconds and try again.
> - **No "Open in GitHub Codespaces" button?** Use **Code → Codespaces → Create codespace on main**.
> - **GitHub says you reached your Codespaces usage limit:** you've used up the free monthly hours. Delete codespaces you don't need at <https://github.com/codespaces>.

### A.3 Apply for the GitHub Student Developer Pack

Apply at <https://education.github.com/pack> with your @aspira.hr email. Verified students get more free Codespaces hours (the same as GitHub Pro) and other offers we use later, such as LocalStack for AWS. Verification can take a few days.

### A.4 Star and watch the course repository (optional, 1 min)

On the [course repository](https://github.com/aprojic/Cloud-Computing), at the top right:

1. Click **⭐ Star**. It's a bookmark: the repo then appears under *Your stars* in your profile, so you can always find the labs.
2. Click **Watch → Custom**, tick **Releases** and click **Apply**. GitHub then emails you when a new lab is published. (A star alone doesn't send notifications.)

## Part B — Azure for Students (needed for Lab 04) · ~15 min

In Lab 04 you rent a virtual machine in Azure. Azure for Students gives you $100 credit with **no credit card**. When the credit runs out the subscription is switched off and you are never billed.

### B.1 Activate Azure for Students

1. Open <https://aka.ms/azure4students> and click **Start free**.
2. Sign in with a Microsoft account, or create one. When asked to verify your academic status, use your **@aspira.hr** address and confirm the email you receive.
3. Fill in the form. **No credit card is required.** If a page asks for one, you're on the wrong offer: go back to the link in step 1.
4. When it finishes, you land in the Azure portal (<https://portal.azure.com>). Check your subscription: type **Subscriptions** in the search bar at the top.

> [!NOTE]
> **Expected**
>
> A subscription called **Azure for Students** with status **Active**.

> [!TIP]
> **Common pitfalls**
>
> - **"You're not eligible"**: the offer is for full-time students aged 18+, verified through the school email. If you're a part-time student or the verification fails, tell me before Lab 04. You'll do that lab without Azure, so nothing is lost.
> - **Already used the offer before** (e.g. at another school): one subscription per person. Tell me.
> - You can check how much credit is left at <https://www.microsoftazuresponsorships.com/>.

### B.2 Open Cloud Shell

Cloud Shell is a Linux terminal in your browser with the Azure CLI (`az`) already installed and logged in. It's free.

1. In the portal, click the **`>_`** icon in the top bar.
2. Choose **Bash**.
3. When asked about storage, choose **No storage account required** (an *ephemeral* session), select your **Azure for Students** subscription and click **Apply**.
4. Run:

```bash
az account show -o table
```

> [!NOTE]
> **Expected**
>
> A table with one row where **Name** is `Azure for Students` and **State** is `Enabled`.

> [!TIP]
> **Good to know**
>
> - An ephemeral session keeps **nothing**: files, variables and SSH keys are gone when it ends, after 20 minutes without activity. In the labs we only need the terminal, so that's fine.
> - If Cloud Shell refuses to start with an error about a *resource provider*, open **Subscriptions → Azure for Students → Resource providers**, search for `Microsoft.CloudShell`, click **Register**, wait a minute and try again.

### B.3 Find your allowed regions

Student subscriptions may only create resources in a small set of regions, usually about five, and **the list is different for each student**. If you use a region that isn't on your list, every lab command fails with `RequestDisallowedByAzure` or `RequestDisallowedByPolicy`.

1. In the portal search bar, type **Policy** and open it.
2. Go to **Authoring → Assignments** and open **Allowed resource deployment regions**.
3. Look at the **Allowed locations** parameter. **Write the list down.** You'll need it in Lab 04.
4. Test one of them in Cloud Shell. Replace `swedencentral` with one of **your** regions. Everything here is free:

```bash
LOC=swedencentral   # ← change to one of YOUR allowed regions
az group create --name lab0-test --location $LOC -o table
az network vnet create --resource-group lab0-test --name lab0-vnet --location $LOC -o none
az vm list-skus --location $LOC --size Standard_B2ats_v2 --query "[].restrictions[].reasonCode" -o tsv
az group delete --name lab0-test --yes
```

The network test matters because the region policy is checked when a **resource** is created, not the group. The `list-skus` line checks that the VM size we use in Lab 04 is available to you there.

Use the region's short name in lowercase without spaces, e.g. `westeurope`, `swedencentral`, `italynorth`. Your list may look completely different (e.g. `eastus`, `centralindia`), and that's fine. Run `az account list-locations -o table` to see how each display name maps to its short name.

> [!NOTE]
> **Expected output**
>
> ```
> Location       Name
> -------------  ---------
> swedencentral  lab0-test
> ```
>
> The network command prints nothing if it worked. The `list-skus` line must also print **nothing**: if it prints `NotAvailableForSubscription`, that size isn't available to you in this region, so try another region from your list. The delete runs without output.

> [!TIP]
> **`RequestDisallowedByAzure` or `RequestDisallowedByPolicy`?** That region isn't on your list. Delete the group (`az group delete --name lab0-test --yes`) and try another region.
>
> **`syntax error near unexpected token`?** You left `<` `>` in a command. Replace the whole placeholder, brackets included.

## Check — are you ready

> [!IMPORTANT]
> **For Lab 01 (Monday 5 October)**
>
> - [ ] You can open a codespace from the course repository, and `docker run --rm alpine echo "Hello from a container"` prints the greeting.
> - [ ] You stopped the codespace afterwards.
> - [ ] You applied for the GitHub Student Developer Pack.
> - [ ] (Optional) You starred the repo and watch its releases.

> [!IMPORTANT]
> **For Lab 04 (Monday 16 November)**
>
> - [ ] **Subscriptions** shows *Azure for Students* as *Active*.
> - [ ] Cloud Shell opens and `az account show -o table` shows *Enabled*.
> - [ ] You have **your list of allowed regions** written down.
> - [ ] In one of those regions the network test worked, `list-skus` printed nothing, and you deleted the test group. **Write this region down as your Lab 04 region.**

Lab 00 is not graded, but Part A is a **prerequisite** for Lab 01. If something doesn't work, email me **before** the lab, not at the start of it, so we can solve it in time.
