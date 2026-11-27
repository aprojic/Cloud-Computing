<!-- kicker: Lab 00 · setup -->
# Lab 00 — Set Up Your Cloud

*A Linux machine with Docker in your browser, for every lab in this course. Set it up once and use it all semester.*

`~15 min` · `GitHub · Codespaces` · `once, at home` · `prerequisite for Lab 01`

## Why

The first labs teach **containers**, the way almost all cloud software is packaged and shipped today. You run them in **GitHub Codespaces**: a Linux machine in a data centre, with Docker installed, opened in your browser. It needs no credit card, and you don't need to install anything.

## Outcomes

- Open a codespace from the course repository and run your first container.
- Apply for the GitHub Student Developer Pack (more free Codespaces hours).

## Prerequisites

- [ ] Access to your **@aspira.hr** mailbox (you'll receive verification emails).
- [ ] A computer with a modern browser (Chrome, Edge, Firefox or Safari).
- [ ] Your phone (you may be asked to verify a phone number or set up sign-in security).

> [!TIP]
> **Use the copy button** at the top right of each code block, so multi-line commands stay intact.

## Part 1 — GitHub and Codespaces · ~15 min

### 1.1 Your GitHub account

Create an account at <https://github.com>, or use the one you have. Add your **@aspira.hr** email under *Settings → Emails*. Pick a username you're happy to show: it appears in your lab reports.

### 1.2 Open a codespace and run a container

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

### 1.3 Apply for the GitHub Student Developer Pack

Apply at <https://education.github.com/pack> with your @aspira.hr email. Verified students get more free Codespaces hours (the same as GitHub Pro) and other offers we use later, such as LocalStack for AWS. Verification can take a few days.

### 1.4 Star and watch the course repository (optional, 1 min)

On the [course repository](https://github.com/aprojic/Cloud-Computing), at the top right:

1. Click **⭐ Star**. It's a bookmark: the repo then appears under *Your stars* in your profile, so you can always find the labs.
2. Click **Watch → Custom**, tick **Releases** and click **Apply**. GitHub then emails you when a new lab is published. (A star alone doesn't send notifications.)

## Check — are you ready

> [!IMPORTANT]
> **For Lab 01**
>
> - [ ] You can open a codespace from the course repository, and `docker run --rm alpine echo "Hello from a container"` prints the greeting.
> - [ ] You stopped the codespace afterwards.
> - [ ] You applied for the GitHub Student Developer Pack.
> - [ ] (Optional) You starred the repo and watch its releases.

Lab 00 is not graded, but it is a **prerequisite** for Lab 01. If something doesn't work, email me **before** the lab, not at the start of it, so we can solve it in time.
