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
> - **"You're not eligible"**: the offer is for full-time students aged 18+, verified through the school email. If you're a part-time student or the verification fails, tell me before Lab 01. You'll work in a pair, and that's fine.
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
4. Test one of them in Cloud Shell. A resource group is free, so this costs nothing:

```bash
az group create --name lab0-test --location <one-of-your-regions> -o table
az group delete --name lab0-test --yes
```

Use the region's short name in lowercase without spaces, e.g. `westeurope`, `northeurope`, `swedencentral`, `germanywestcentral`, `italynorth`. Run `az account list-locations -o table` to see how each display name maps to its short name.

> [!NOTE]
> **Expected output**
>
> ```
> Location       Name
> -------------  ---------
> swedencentral  lab0-test
> ```
>
> The delete runs without output and takes a few seconds.

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
> - [ ] `az group create` worked in one of those regions, and you deleted the test group.
> - [ ] (For Lab 03) GitHub account created and the student pack applied for.

Lab 00 is not graded, but it is a **prerequisite** for Lab 01 (Monday 5 October). If something doesn't work, email me **before** the lab, not at the start of it, so we can solve it in time.
