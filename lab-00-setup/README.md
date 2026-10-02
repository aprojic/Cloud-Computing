<!-- kicker: Lab 00 · setup -->
# Lab 00 — Set Up Your Cloud

*Your own Azure subscription with $100 credit, a terminal in the browser, and the regions you're allowed to use. Set it up once and use it all semester.*

`~20–30 min` · `Azure for Students · Cloud Shell · GitHub` · `once, at home` · `prerequisite for Lab 01`

## Why

In this course you work on **real cloud infrastructure**, not a simulation: you create servers, apps and containers in a Microsoft data centre and delete them again. For that you need your own subscription. **Azure for Students** gives you one with no credit card. When the credit runs out the subscription is switched off and you are never billed. Everything runs in the browser, so you don't need to install anything.

## Outcomes

- Activate an Azure for Students subscription with your Aspira email.
- Open Azure Cloud Shell and run your first `az` command.
- Find the regions your subscription is allowed to use, and test one.
- (For later labs) Set up GitHub and apply for the student benefits.

## Prerequisites

- [ ] Access to your **@aspira.hr** mailbox (you'll receive a verification email).
- [ ] A computer with a modern browser (Chrome, Edge, Firefox or Safari).
- [ ] Your phone (you may be asked to verify a phone number or set up sign-in security).

> [!TIP]
> **Copy commands from this GitHub page** (copy button at the top right of each code block), not from the PDF. PDF viewers often break multi-line commands.

> **Do this at home, before Monday 5 October.** Activation sometimes takes a while, and in class there's no time to wait for it.

## Part 1 — Activate Azure for Students · ~10 min

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
> - **"You're not eligible"**: the offer is for full-time students aged 18+, verified through the school email. If you're a part-time student or the verification fails, tell me before Lab 01. You'll do the lab on your own in GitHub Codespaces instead ([Plan B](../lab-01-first-server/plan-b.md)), so make sure Part 4 below works.
> - **Already used the offer before** (e.g. at another school): one subscription per person. Tell me.
> - You can check how much credit is left at <https://www.microsoftazuresponsorships.com/>.

## Part 2 — Open Cloud Shell · ~5 min

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

## Part 3 — Find your allowed regions · ~5 min

Student subscriptions may only create resources in a small set of regions, usually about five, and **the list is different for each student**. If you use a region that isn't on your list, every lab command fails with `RequestDisallowedByAzure` or `RequestDisallowedByPolicy`.

1. In the portal search bar, type **Policy** and open it.
2. Go to **Authoring → Assignments** and open **Allowed resource deployment regions**.
3. Look at the **Allowed locations** parameter. **Write the list down.** You'll need it in every lab.
4. Test one of them in Cloud Shell. Replace `swedencentral` with one of **your** regions. Everything here is free:

```bash
LOC=swedencentral   # ← change to one of YOUR allowed regions
az group create --name lab0-test --location $LOC -o table
az network vnet create --resource-group lab0-test --name lab0-vnet --location $LOC -o none
az vm list-skus --location $LOC --size Standard_B2ats_v2 --query "[].restrictions[].reasonCode" -o tsv
az group delete --name lab0-test --yes
```

The network test matters because the region policy is checked when a **resource** is created, not the group. The `list-skus` line checks that the VM size we use in Lab 01 is available to you there.

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

## Part 4 — GitHub (needed from Lab 03, start now) · ~5 min

From November we work with containers in **GitHub Codespaces**. Student verification can take a few days, so apply now.

1. Create a GitHub account at <https://github.com>, or use the one you have, and add your **@aspira.hr** email under *Settings → Emails*.
2. Apply for the **GitHub Student Developer Pack** at <https://education.github.com/pack>. Verified students get more free Codespaces hours (the same as GitHub Pro) and many other offers.

## Check — are you ready for Lab 01

> [!IMPORTANT]
> **Must work**
>
> - [ ] **Subscriptions** shows *Azure for Students* as *Active*.
> - [ ] Cloud Shell opens and `az account show -o table` shows *Enabled*.
> - [ ] You have **your list of allowed regions** written down.
> - [ ] In one of those regions the network test worked, `list-skus` printed nothing, and you deleted the test group. **Write this region down as your Lab 01 region.**
> - [ ] (For Lab 03) GitHub account created and the student pack applied for.

Lab 00 is not graded, but it is a **prerequisite** for Lab 01 (Monday 5 October). If something doesn't work, email me **before** the lab, not at the start of it, so we can solve it in time.
