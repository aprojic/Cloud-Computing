<!-- kicker: Lab 01 · Containers · 5 October 2026 -->
# Lab 01 — Your first container

*Start containers in a second, find out why they forget everything, serve your own web page from one, and learn what a container really sees of the machine it runs on.*

`45 min` · `Codespaces · Docker · nginx` · `level: intro` · `submit: Merlin`

## Scenario

A small Split agency wants a web page online **tonight**, and the developer who built it says "it works on my machine". You are going to package the server so it runs the same way everywhere, show the client the page from a phone, check what the package can and can't see of the machine under it, and then clean up so nothing keeps running.

## Learning outcomes

- Explain the difference between an **image** and a **container**, and run, list, inspect and remove both.
- Show why a container's own files are temporary, and keep data with a **volume** instead.
- Publish a container's **port** so a web page is reachable from the internet.
- Explain what a container sees of its host's CPU and memory, and where a limit actually lives.

## Prerequisites

- [ ] **[Lab 00](../lab-00-setup/README.md), Part A done:** you can open a codespace from this repository and run `docker run --rm alpine echo "Hello from a container"`.
- [ ] A phone (or a second browser tab) to open your page.

> [!TIP]
> **Copy commands from this GitHub page** (copy button on each code block), not from the PDF. PDF viewers often break multi-line commands.

## Part 1 — Images and containers · ~8 min

### 1.1 Open your machine

Open the [repository's main page](../README.md), click **Open in GitHub Codespaces** and open the codespace you created in Lab 00 (or create a new one). Open a terminal: menu **☰ → Terminal → New Terminal**.

### 1.2 Run a container, twice

```bash
time docker run --rm alpine echo "Hello from a container"
time docker run --rm alpine echo "Hello from a container"
```

The first run may **pull** (download) the `alpine` **image** if it isn't on this machine yet. An image is a read-only package: a small Linux file system plus a program to start. Every `docker run` makes a new **container** from it, which is a running process with its own view of that file system. `--rm` deletes the container when the program ends.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> Hello from a container
>
> real    0m0.240s
> user    0m0.013s
> sys     0m0.016s
> ```

> [!IMPORTANT]
> **In the report**
>
> The `real` time of the second run. In Lab 04 you'll time how long a cloud provider needs to give you a whole virtual machine, and compare.

### 1.3 Look inside

```bash
docker images
head -2 /etc/os-release
docker run --rm alpine head -2 /etc/os-release
docker run --rm alpine ps
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> IMAGE           ID             DISK USAGE   CONTENT SIZE   EXTRA
> alpine:latest   294b683cb724         13MB         3.94MB
> PRETTY_NAME="Ubuntu 24.04.3 LTS"
> NAME="Ubuntu"
> NAME="Alpine Linux"
> ID=alpine
> PID   USER     TIME  COMMAND
>     1 root      0:00 ps
> ```

Your codespace runs Ubuntu, but the container says it's Alpine Linux, and inside it `ps` is the **only** process, with ID 1. The container has its own file system and its own process list, yet it shares the codespace's Linux kernel. That's why it starts in a fraction of a second: nothing has to boot.

## Part 2 — Containers forget · ~6 min

Start a container that stays running, write a file inside it, then delete the container and start a new one from the same image:

```bash
docker run -d --name box alpine sleep 3600
docker exec box sh -c 'echo "my notes" > /note.txt; cat /note.txt'
docker rm -f box
docker run --rm alpine cat /note.txt
```

`-d` runs the container in the background, `--name` gives it a name, `exec` runs a command inside a running container, and `rm -f` stops and deletes it.

> [!NOTE]
> **Expected output**
>
> ```
> 3f1c…   (a long container ID)
> my notes
> box
> cat: can't open '/note.txt': No such file or directory
> ```

The file lived in the first container's own writable layer, and it went away with that container. The image never changed. This is a feature: you can throw a container away and start an identical one at any time. But anything you want to keep must live **outside** the container.

## Part 3 — Serve your page from a container · ~15 min

### 3.1 Write the page on the codespace

Make a folder on the codespace, **outside** any container, and write your page into it. Replace **Your Name** with your name (č, ć, š, ž, đ are fine):

```bash
mkdir -p ~/site
echo "<meta charset=utf-8><h1>Your Name</h1><p>$GITHUB_USER · $CODESPACE_NAME · $(date -u '+%Y-%m-%d %H:%M UTC')</p>" > ~/site/index.html
cat ~/site/index.html
```

The page carries your GitHub username, your codespace's name and the time you wrote it.

### 3.2 Start nginx with a volume and a port

```bash
docker run -d --name web -p 80:80 -v ~/site:/usr/share/nginx/html:ro nginx:alpine
docker ps
curl -s localhost
```

- `-v ~/site:/usr/share/nginx/html:ro` mounts your folder into the container where nginx looks for web pages (`ro` = read-only). This is a **volume**: the data stays on the codespace, the container only borrows it.
- `-p 80:80` **publishes** the container's port 80 on the codespace's port 80. Without it, nginx would be listening inside the container where nobody can reach it.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                                 NAMES
> e2d739876acf   nginx:alpine   "/docker-entrypoint.…"   3 seconds ago   Up 2 seconds   0.0.0.0:80->80/tcp, [::]:80->80/tcp   web
> <meta charset=utf-8><h1>Your Name</h1><p>yourname · fluffy-space-acorn-9jw47… · 2026-10-05 16:44 UTC</p>
> ```

**Take Screenshot B now:** the terminal with the `docker ps` output and your page from `curl`.

> [!TIP]
> **Common errors**
>
> - `Conflict. The container name "/web" is already in use`: you already started one. Remove it with `docker rm -f web` and run the command again.
> - `Bind for 0.0.0.0:80 failed: port is already allocated`: something else uses port 80, often a `web` container from an earlier try. `docker ps` shows it; remove it.

### 3.3 Open it from the internet

Open the **Ports** tab (next to *Terminal*). Port **80** is in the list. Right-click it → **Port Visibility → Public**, then copy the **Forwarded Address** and open it in a browser. Your phone works too.

**Take Screenshot A now:** the browser with the **forwarded address in the address bar** and your page. The address contains your codespace's name, the same one that is printed on the page.

> [!TIP]
> **Page doesn't load, or asks you to log in to GitHub?**
>
> The port is still **Private**. Set it to **Public** as above and reload. If port 80 isn't listed at all, check `docker ps`: the `web` container must be *Up* with `0.0.0.0:80->80/tcp`.

### 3.4 Change the page without touching the container

```bash
echo "<p>Edited at $(date -u '+%H:%M:%S UTC'), container untouched.</p>" >> ~/site/index.html
```

Reload the page in the browser. The new line is there, because nginx reads the file from your volume. Now look at the container from the inside, and at its access log, one line per visitor (`2>/dev/null` hides the start-up messages):

```bash
docker exec web ps
docker logs web 2>/dev/null | tail -3
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> PID   USER     TIME  COMMAND
>     1 root      0:00 nginx: master process nginx -g daemon off;
>    30 nginx     0:00 nginx: worker process
>    31 nginx     0:00 nginx: worker process
>    39 root      0:00 ps
> … "GET / HTTP/1.1" 200 …
> ```

## Part 4 — What does a container see? · ~8 min

### 4.1 CPU and memory: codespace vs. container

```bash
nproc; free -h | head -2
docker run --rm alpine sh -c 'nproc; free -h | head -2'
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> 2
>                total        used        free      shared  buff/cache   available
> Mem:           7.8Gi       1.3Gi       191Mi        61Mi       6.7Gi       6.5Gi
> 2
>               total        used        free      shared  buff/cache   available
> Mem:           7.8G      959.9M      171.2M       62.0M        6.7G        6.4G
> ```

The container reports the same cores and the same memory as the machine it runs on. It isn't a smaller computer: it's a process that sees the host's hardware.

### 4.2 Set a limit, then look for it

Now give a container half a CPU core and 256 MB of memory, and ask it again:

```bash
docker run --rm --cpus 0.5 --memory 256m alpine \
  sh -c 'nproc; cat /sys/fs/cgroup/cpu.max /sys/fs/cgroup/memory.max'
```

> [!NOTE]
> **Expected output**
>
> ```
> 2
> 50000 100000
> 268435456
> ```

`nproc` still says 2. The limit isn't hidden hardware: the Linux kernel enforces it through **cgroups**. `50000 100000` means "50 ms of CPU time in every 100 ms", which is half a core, and `268435456` bytes is 256 MB. Programs that size themselves by counting cores can be fooled by this, which is something you'll meet again with cloud containers.

> [!IMPORTANT]
> **In the report**
>
> What `nproc` printed in 4.1 and 4.2, and where the half-core limit actually lives.

## Part 5 — Clean up and prove it · ~8 min

### 5.1 Remove containers and images

```bash
docker rm -f web
docker image rm nginx:alpine alpine
docker ps -a
docker system df
```

`docker ps -a` lists **all** containers, including stopped ones. After the cleanup it must be empty, and `docker system df` must show 0 images and 0 containers.

> [!NOTE]
> **Expected output**
>
> ```
> CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
> TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
> Images          0         0         0B        0B
> Containers      0         0         0B        0B
> Local Volumes   0         0         0B        0B
> Build Cache     0         0         0B        0B
> ```

### 5.2 What does it cost?

Your codespace is a 2-core machine rented by the hour. Find the **price per hour** of a 2-core codespace in the [GitHub Codespaces billing docs](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), and how many free **core-hours** per month your account gets. How many hours of this lab could you run for free each month?

### 5.3 Delete the codespace

Go to <https://github.com/codespaces> → **⋯** next to your codespace → **Delete**. Your `~/site` folder goes with it, which is fine: the page is in your screenshots.

**Take Screenshot C now:** your codespace list without the deleted codespace.

> [!WARNING]
> **Why this matters**
>
> A stopped codespace still takes up storage, and a running one uses your free core-hours even when you're not looking at it. When the free quota runs out, you can't open a codespace until next month.

## Submission · by 19 October, before Lab 02

> [!IMPORTANT]
> **To Merlin**
>
> `lab01_<surname>.pdf` with:
>
> 1. **Your data:** your GitHub username, your codespace's name and the `real` time from 1.2.
> 2. **Screenshot A:** your page in a browser, with the **forwarded address in the address bar** (3.3).
> 3. **Screenshot B:** `docker ps` showing the `web` container with `0.0.0.0:80->80/tcp`, and your page from `curl` (3.2).
> 4. **Screenshot C:** your codespace list without the deleted codespace (5.3).
> 5. **Your cost answer** from 5.2: price per hour, free core-hours, and how many lab hours that covers.
> 6. **Short answers**, in your own words:
>    - What is the difference between an image and a container? Use what happened in Part 2.
>    - Why did your edit in 3.4 show up without touching the container, while `/note.txt` in Part 2 was lost?
>    - What does `-p 80:80` do, and what would happen without it?
>    - What did `nproc` print in 4.1 and 4.2, and where does the half-core limit actually live?

| Item | Required |
|---|:-:|
| Your data and screenshots A–C, consistent with each other (same codespace name, username, times) | ✓ |
| Cost answer | ✓ |
| Short answers, using your own outputs | ✓ |

*Your report is about **your** run: your username, your codespace, your times. Reports that don't match each other or look copied will be checked again, and I may ask you to walk me through your report.*
