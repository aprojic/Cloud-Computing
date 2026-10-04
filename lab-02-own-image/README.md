<!-- kicker: Lab 02 · Containers · 19 October 2026 -->
# Lab 02 — Build your own image

*Package a small Python web app with a Dockerfile, run it anywhere Docker runs, see how layers make rebuilds fast, and publish the image to a registry so any machine can pull it.*

`45 min` · `Codespaces · Docker · GHCR` · `level: intro` · `submit: Merlin`

## Scenario

The Split agency from Lab 01 now has a small Python app instead of a static page. It runs on the developer's laptop, but the server they want to use doesn't even have Python installed. You are going to write the recipe that turns the app into an image, run it, change it and rebuild it, and push it to a registry so the server (or anyone you allow) can pull exactly the same thing.

## Learning outcomes

- Write a **Dockerfile** and explain what each instruction does.
- Build an image, tag it with a version, and run it with environment variables and a published port.
- Explain how **layer caching** works and why the order of instructions matters.
- Push an image to a **container registry** with a scoped, short-lived token, and pull it back.

## Prerequisites

- [ ] **[Lab 01](../lab-01-first-container/README.md) done:** you know `docker run`, `-p`, `docker ps` and how to make a port public in Codespaces.
- [ ] Your GitHub account. You'll create a token in Part 4, so make sure you can log in to <https://github.com> in the browser.

> [!TIP]
> **Copy commands from this GitHub page** (copy button on each code block), not from the PDF. PDF viewers often break multi-line commands.

## Part 1 — It works on my machine · ~5 min

### 1.1 Open your machine and get the app

Open the [repository's main page](../README.md), click **Open in GitHub Codespaces** and create a codespace. Open a terminal (**☰ → Terminal → New Terminal**) and copy the app into your home folder, so you work outside the repository:

```bash
cp -r /workspaces/Cloud-Computing/lab-02-own-image/app ~/lab02
cd ~/lab02
ls
cat app.py
```

The app ([`app/app.py`](app/app.py)) is a few lines of Flask: it shows a name, a version, the container's hostname and the time. [`requirements.txt`](app/requirements.txt) lists the one library it needs.

### 1.2 Try to run it

```bash
python3 app.py
```

> [!NOTE]
> **Expected output**
>
> ```
> bash: python3: command not found
> ```

The codespace has no Python at all, just like the agency's server. You could install Python and Flask by hand, on every machine, in the right versions. Or you could ship the app **together with** everything it needs. That's what an image is.

## Part 2 — Write the Dockerfile and build · ~12 min

### 2.1 The recipe

Create a file called `Dockerfile` (no extension) in `~/lab02`. You can open it in the editor with `code Dockerfile`, then paste:

```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV APP_VERSION=1.0
EXPOSE 8000
CMD ["python", "app.py"]
```

Save it (**Ctrl+S** / **Cmd+S**). Line by line:

| Instruction | What it does |
|---|---|
| `FROM python:3.14-slim` | Start from an existing image: a small Debian Linux with Python 3.14 installed. |
| `WORKDIR /app` | Create `/app` inside the image and work there. |
| `COPY requirements.txt .` | Copy the list of libraries from your folder into the image. |
| `RUN pip install …` | Run a command **while building**: install Flask into the image. |
| `COPY app.py .` | Copy the app itself. |
| `ENV APP_VERSION=1.0` | Set an environment variable that the app reads. |
| `EXPOSE 8000` | Document that the app listens on port 8000. It doesn't open or publish anything. |
| `CMD ["python", "app.py"]` | What to run when a container **starts** from this image. |

### 2.2 Build it

```bash
docker build -t hello-cloud:1.0 .
docker images
```

`-t hello-cloud:1.0` gives the image a name and a **tag** (here a version). The `.` at the end is the *build context*: the folder whose files `COPY` can see.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> [+] Building 8.8s (10/10) FINISHED
>  => [1/5] FROM docker.io/library/python:3.14-slim@sha256:…
>  => [2/5] WORKDIR /app
>  => [3/5] COPY requirements.txt .
>  => [4/5] RUN pip install --no-cache-dir -r requirements.txt
>  => [5/5] COPY app.py .
>  => exporting to image
> IMAGE             ID             DISK USAGE   CONTENT SIZE   EXTRA
> hello-cloud:1.0   b0d8ad80b984        212MB           52MB
> ```

> [!TIP]
> **Common errors**
>
> - `failed to read dockerfile: open Dockerfile: no such file or directory`: you're not in `~/lab02`, or the file is called `Dockerfile.txt` or `dockerfile`. Run `cd ~/lab02 && ls`.
> - `"/requirements.txt": not found`: you forgot the `.` at the end of `docker build`, or you're in the wrong folder.

### 2.3 Look at the layers

```bash
docker history hello-cloud:1.0 | head -9
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> IMAGE          CREATED         CREATED BY                                      SIZE
> b0d8ad80b984   2 seconds ago   CMD ["python" "app.py"]                         0B
> <missing>      2 seconds ago   EXPOSE [8000/tcp]                               0B
> <missing>      2 seconds ago   ENV APP_VERSION=1.0                             0B
> <missing>      2 seconds ago   COPY app.py . # buildkit                        12.3kB
> <missing>      2 seconds ago   RUN /bin/sh -c pip install --no-cache-dir -r…   16.9MB
> <missing>      4 seconds ago   COPY requirements.txt . # buildkit              12.3kB
> <missing>      4 seconds ago   WORKDIR /app                                    8.19kB
> <missing>      2 days ago      CMD ["python3"]                                 0B
> ```

Each instruction became a **layer**. Your four lines sit on top of the layers of `python:3.14-slim`, which someone else built two days ago. An image is a stack of these read-only layers, and a container adds one thin writable layer on top. That's the layer that disappeared with `/note.txt` in Lab 01.

> [!IMPORTANT]
> **In the report**
>
> The image size from `docker images`, and the size of the `pip install` layer from `docker history`.

## Part 3 — Run it, change it, rebuild · ~10 min

### 3.1 Run your image

Replace **Your Name** with your name:

```bash
docker run -d --name app -p 80:8000 -e STUDENT_NAME="Your Name" hello-cloud:1.0
curl -s localhost
```

`-p 80:8000` connects port 80 on the codespace to port 8000 in the container: the two numbers don't have to match. `-e` sets an environment variable that the app reads.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> <!doctype html>
> <meta charset="utf-8">
> <title>Hello, cloud</title>
> <h1>Hello from Your Name</h1>
> <ul>
>   <li>Version: <b>1.0</b></li>
>   <li>Container (hostname): <code>094ed9f960fb</code></li>
>   <li>Python: 3.14.8</li>
>   <li>Time: 2026-10-19 16:31:25 UTC</li>
> </ul>
> ```

Python 3.14 is running, on a machine where `python3` doesn't exist. It lives in the image.

Now make the page reachable: **Ports** tab → port **80** → right-click → **Port Visibility → Public**. Open the **Forwarded Address** in a browser.

**Take Screenshot A now:** the browser with the **forwarded address in the address bar** and your page (name, version, container hostname).

> [!TIP]
> **`curl: (56) Recv failure: Connection reset by peer`?**
>
> Wait two seconds and try again: the app needs a moment to start. If it keeps failing, `docker logs app` shows why. An app that listens only on `127.0.0.1` can't be reached from outside its container. That's why `app.py` uses `host="0.0.0.0"`.

### 3.2 Change the code and rebuild

Change the greeting in the app, then build a new version:

```bash
sed -i 's/Hello from/Greetings from/' app.py
docker build -t hello-cloud:1.1 .
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> [+] Building 2.1s (10/10) FINISHED
>  => [1/5] FROM docker.io/library/python:3.14-slim@sha256:…
>  => CACHED [2/5] WORKDIR /app
>  => CACHED [3/5] COPY requirements.txt .
>  => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt
>  => [5/5] COPY app.py .
> ```

**Take Screenshot B now:** this build output with the `CACHED` lines.

Docker reuses a layer if its instruction **and everything before it** is unchanged. You only changed `app.py`, so the slow `pip install` layer came from the cache and the build was several times faster. With a real app and dozens of libraries, the difference is minutes. Now think about it: what would happen on every code change if the Dockerfile copied `app.py` **before** running `pip install`?

### 3.3 Run the new version next to the old one

```bash
docker run -d --name app11 -p 8080:8000 -e STUDENT_NAME="Your Name" -e APP_VERSION=1.1 hello-cloud:1.1
curl -s localhost:8080 | grep -E "h1|Version"
docker ps
```

Two versions of the same app, from two images, side by side. `-e APP_VERSION=1.1` overrides the `ENV` from the Dockerfile at run time.

> [!IMPORTANT]
> **In the report**
>
> The build time of 1.0 and of 1.1 (the `Building …s` line), and why they differ so much.

## Part 4 — Publish it to a registry · ~12 min

Right now your image exists only in this codespace. Delete the codespace and it's gone. A **registry** stores images so any machine can pull them. You'll use the **GitHub Container Registry** (`ghcr.io`), which comes with your GitHub account.

### 4.1 Create a short-lived token

A codespace can pull images from GitHub automatically, but pushing needs a token you create yourself.

1. Open <https://github.com/settings/tokens/new> (GitHub → *Settings* → *Developer settings* → *Personal access tokens* → **Tokens (classic)** → *Generate new token (classic)*).
2. **Note:** `lab02`. **Expiration:** 7 days.
3. Tick **only** `write:packages` (it ticks `read:packages` for you). Nothing else.
4. Click **Generate token** and copy it. GitHub shows it only once.

> [!WARNING]
> **A token is a password**
>
> Anyone who has it can push images as you until it expires. Never paste it into a file, a screenshot, your report, an issue or a chat. That's why it gets the smallest scope and the shortest life that do the job, and why you delete it in Part 5.

### 4.2 Log in to the registry

```bash
read -s -p "Paste your token: " CR_PAT; echo
echo "$CR_PAT" | docker login ghcr.io -u "$GITHUB_USER" --password-stdin
```

`read -s` doesn't show what you paste, and `--password-stdin` keeps the token out of your shell history.

> [!NOTE]
> **Expected output**
>
> ```
> Login Succeeded
> ```

### 4.3 Tag and push

Registry image names must be lowercase, and your GitHub username may not be:

```bash
OWNER=$(echo "$GITHUB_USER" | tr A-Z a-z)
docker tag hello-cloud:1.1 ghcr.io/$OWNER/hello-cloud:1.1
docker push ghcr.io/$OWNER/hello-cloud:1.1
```

`docker tag` doesn't copy anything: it gives the same image a second name that says **where** it belongs.

> [!TIP]
> **`denied: permission_denied` or `unauthorized`?**
>
> The token is missing the `write:packages` scope, has expired, or you pasted it incompletely. Create a new one and repeat 4.2.

### 4.4 Prove it lives in the registry

Delete every local copy, then run the image by its registry name:

```bash
docker rm -f app app11
docker image rm hello-cloud:1.0 hello-cloud:1.1 ghcr.io/$OWNER/hello-cloud:1.1
docker images
docker run -d --name app -p 80:8000 -e STUDENT_NAME="Your Name" ghcr.io/$OWNER/hello-cloud:1.1
docker images
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> IMAGE     ID        DISK USAGE   CONTENT SIZE   EXTRA
> Unable to find image 'ghcr.io/yourname/hello-cloud:1.1' locally
> 1.1: Pulling from yourname/hello-cloud
> …
> IMAGE                              ID             DISK USAGE   CONTENT SIZE   EXTRA
> ghcr.io/yourname/hello-cloud:1.1   5c1f…               212MB           52MB
> ```

The image list was empty, and Docker pulled your image back from the registry. Some layers may say `Already exists`: Docker still had the Python base layers on disk and only downloaded what was missing. Reload the page in your browser: it shows *Greetings from…* again, from a container whose hostname is new.

Now open your profile on GitHub → **Packages**. `hello-cloud` is there, **private** by default, so only you can pull it.

**Take Screenshot C now:** the package page on GitHub, showing your username, `hello-cloud` and the tag `1.1`.

## Part 5 — Clean up · ~6 min

### 5.1 Containers, images, login

```bash
docker rm -f app
docker image rm ghcr.io/$OWNER/hello-cloud:1.1
docker logout ghcr.io
unset CR_PAT
docker ps -a
```

`docker ps -a` must be empty. Your image stays in the registry: that's the point. You'll use registries again when containers move to the cloud.

### 5.2 Delete the token

Open <https://github.com/settings/tokens>, find `lab02` and click **Delete**. A token you no longer need is a risk with no benefit, even with a short expiry.

### 5.3 Delete the codespace

<https://github.com/codespaces> → **⋯** next to your codespace → **Delete**.

> [!WARNING]
> **Why this matters**
>
> A running codespace uses your free core-hours, and a forgotten token keeps working until it expires.

## Submission · by 2 November, before Lab 03

> [!IMPORTANT]
> **To Merlin**
>
> `lab02_<surname>.pdf` with:
>
> 1. **Your data:** GitHub username, the image size and the `pip install` layer size (2.3), and the build times of 1.0 and 1.1 (3.2).
> 2. **Your Dockerfile**, as text.
> 3. **Screenshot A:** your app in a browser, with the **forwarded address in the address bar** (3.1).
> 4. **Screenshot B:** the 1.1 build output with the `CACHED` lines (3.2).
> 5. **Screenshot C:** your `hello-cloud` package page on GitHub with tag `1.1` (4.4).
> 6. **Short answers**, in your own words:
>    - What is the difference between `RUN` and `CMD`?
>    - Why was the 1.1 build so fast? What would change if `COPY app.py .` came before `RUN pip install`?
>    - `EXPOSE 8000` is in the Dockerfile. Why did you still need `-p 80:8000`?
>    - Why did you give the token only `write:packages` and 7 days, and why delete it at the end?

| Item | Required |
|---|:-:|
| Your data, Dockerfile and screenshots A–C, consistent with each other (same username, image name, times) | ✓ |
| No token visible anywhere in the report | ✓ |
| Short answers, using your own outputs | ✓ |

*Your report is about **your** run: your username, your image, your times. Reports that don't match each other or look copied will be checked again, and I may ask you to walk me through your report.*
