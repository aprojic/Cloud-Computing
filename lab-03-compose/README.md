<!-- kicker: Lab 03 · Containers -->
# Lab 03 — Many containers: Docker Compose

*Run a web app and a database as two containers described in one file, see how they find each other by name, and find out what each stop command does to your data.*

`45 min` · `Codespaces · Docker Compose · Redis` · `level: intro` · `submit: Merlin`

## Scenario

The agency's app from Lab 02 now counts visitors. A counter kept inside the web container would vanish every time the container is replaced (remember `/note.txt` in Lab 01), so the count lives in a second container: **Redis**, a small, fast database. Two containers mean two `docker run` commands with the right network, names, ports, variables and volume, in the right order, every time. Instead, you'll describe the whole app once in a `compose.yaml` file and start it with one command.

## Learning outcomes

- Read a **`compose.yaml`** file and explain what each part does: services, build, ports, environment, volumes, healthcheck.
- Start, inspect and stop a multi-container app with `docker compose`.
- Explain how containers in one Compose project find each other **by service name**.
- Tell apart what `restart`, `down` and `down -v` do to containers, networks and data.

## Prerequisites

- [ ] **[Lab 02](../lab-02-own-image/README.md) done:** you can read a Dockerfile, and you know `-p`, `-e` and how to make a port public in Codespaces.

> [!TIP]
> **Use the copy button** at the top right of each code block, so multi-line commands stay intact.

## Part 1 — Two containers, one file · ~12 min

### 1.1 Open your machine and get the app

Open the [repository's main page](../README.md), click **Open in GitHub Codespaces** and create a codespace. Open a terminal (**☰ → Terminal → New Terminal**) and copy the app into your home folder:

```bash
cp -r /workspaces/Cloud-Computing/lab-03-compose/app ~/lab03
cd ~/lab03
ls
```

You'll see four files. [`app.py`](app/app.py) is a Flask app like the one in Lab 02, but every visit adds one to a counter stored in Redis. [`Dockerfile`](app/Dockerfile) is almost the same recipe you wrote in Lab 02. The new file is [`compose.yaml`](app/compose.yaml):

```bash
cat compose.yaml
```

```yaml
services:
  web:
    build: .
    ports:
      - "80:8000"
    environment:
      STUDENT_NAME: ${STUDENT_NAME}
      CODESPACE_NAME: ${CODESPACE_NAME}
    depends_on:
      redis:
        condition: service_healthy

  redis:
    image: redis:8-alpine
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 2s
      retries: 10

volumes:
  redis-data:
```

| Part | What it means |
|---|---|
| `services:` | The containers that make up the app. Each service has a name: `web` and `redis`. |
| `build: .` | Build the `web` image from the Dockerfile in this folder, like `docker build .` |
| `image: redis:8-alpine` | Don't build `redis`: pull a ready-made image from Docker Hub. |
| `ports: "80:8000"` | Same as `-p 80:8000`. Only `web` publishes a port; `redis` has none. |
| `environment:` | Same as `-e`. `${STUDENT_NAME}` is filled in from a `.env` file or your shell when Compose starts. |
| `depends_on: … service_healthy` | Start `web` only after `redis` reports that it's healthy. |
| `healthcheck:` | How Docker checks that Redis is ready: run `redis-cli ping` every 2 s until it answers. |
| `volumes: redis-data:/data` | Keep Redis's files in a **named volume** called `redis-data`, outside the container. |

<details>
<summary><b>The same app without Compose</b> (read, don't run)</summary>

<br>

```bash
docker network create lab03_default
docker volume create lab03_redis-data
docker run -d --name redis --network lab03_default -v lab03_redis-data:/data redis:8-alpine
# wait until Redis answers, by hand: no healthcheck does it for you
docker build -t lab03-web .
docker run -d --name web --network lab03_default -p 80:8000 \
  -e STUDENT_NAME="Your Name" -e CODESPACE_NAME="$CODESPACE_NAME" lab03-web
```

Five commands and a manual wait, in the right order, and the same again in reverse to delete it all. Forget `--network` on one of them and `web` can't find `redis`. Compose keeps all of this in one file that you can read, share and put in Git, and turns it into `up` and `down`.

</details>

> [!TIP]
> **Older tutorials look different.** They often start with `version: "3.8"` and use the command `docker-compose` with a hyphen. Both are outdated: Compose ignores the `version:` line and warns that it is obsolete, and Compose is now part of Docker as `docker compose`. Use the form in this lab.

### 1.2 Put your name in a `.env` file

Compose reads a file called `.env` in the same folder and uses it to fill in `${…}` variables. Replace **Your Name** with your name:

```bash
echo 'STUDENT_NAME=Your Name' > .env
cat .env
```

`CODESPACE_NAME` needs no file: every codespace already has it as an environment variable, and Compose takes it from your shell.

### 1.3 Start the whole app

```bash
docker compose up -d --build
docker compose ps
```

`up` creates everything in `compose.yaml` and starts it, `-d` returns your terminal, and `--build` builds the `web` image first.

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> [+] up 15/15
>  ✔ Image redis:8-alpine    Pulled                                           4.5s
>  ✔ Image lab03-web         Built                                            1.4s
>  ✔ Network lab03_default   Created                                          0.0s
>  ✔ Volume lab03_redis-data Created                                          0.0s
>  ✔ Container lab03-redis-1 Healthy                                          3.0s
>  ✔ Container lab03-web-1   Started                                          2.7s
> NAME            IMAGE            COMMAND                  SERVICE   CREATED         STATUS                   PORTS
> lab03-redis-1   redis:8-alpine   "docker-entrypoint.s…"   redis     8 seconds ago   Up 7 seconds (healthy)   6379/tcp
> lab03-web-1     lab03-web        "python app.py"          web       8 seconds ago   Up 2 seconds             0.0.0.0:80->8000/tcp, [::]:80->8000/tcp
> ```

Every name starts with `lab03`, the folder you're in: that's the **project name**. Notice the order in the STATUS column: `redis` has been up longer and is *healthy*, because `web` only started once `redis` passed its healthcheck.

> [!TIP]
> **Common errors**
>
> - `no configuration file provided: not found`: you're not in `~/lab03`. Run `cd ~/lab03`.
> - `Bind for 0.0.0.0:80 failed: port is already allocated`: a container from Lab 01 or 02 is still running on port 80. Remove it with `docker rm -f $(docker ps -q)` and run `docker compose up -d` again.
> - `The "STUDENT_NAME" variable is not set. Defaulting to a blank string.` and the page says *Hello from nobody yet*: the `.env` file is missing or not in `~/lab03`. Fix it and run `docker compose up -d` again. Compose recreates only `web`.

### 1.4 Open it in the browser

```bash
curl -s localhost
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> <!doctype html>
> <meta charset="utf-8">
> <title>Visit counter</title>
> <h1>Hello from Your Name</h1>
> <ul>
>   <li>Visits: <b>1</b></li>
>   <li>Web container (hostname): <code>0967c235c4fe</code></li>
>   <li>Codespace: <code>fuzzy-space-giggle-x5r4…</code></li>
> </ul>
> ```

> [!TIP]
> **`curl: (56) Recv failure: Connection reset by peer`?** Wait two seconds and try again: Flask needs a moment to start. `docker compose logs web` shows why if it keeps failing.

Make the page reachable: **Ports** tab → port **80** → right-click → **Port Visibility → Public**. Open the **Forwarded Address** in a browser and reload the page a few times. The counter goes up.

**Take Screenshot A now:** the browser with the **forwarded address in the address bar** and your page (your name, the visit count, the web container's hostname and your codespace name).

## Part 2 — What Compose built for you · ~8 min

### 2.1 One network, one volume

```bash
docker network ls
docker volume ls
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> NETWORK ID     NAME            DRIVER    SCOPE
> 411ea992b282   bridge          bridge    local
> 8a0c4127e978   host            host      local
> 36271ae0b62a   lab03_default   bridge    local
> 1ed2786be49d   none            null      local
> DRIVER    VOLUME NAME
> local     lab03_redis-data
> ```

You never wrote a network into `compose.yaml`, but Compose made one for the project, `lab03_default`, and attached both containers to it. The volume got the project name in front: `lab03_redis-data`.

### 2.2 How does `web` find `redis`?

Look at `app.py`: it connects to the host `redis`. There's no server with that name on the internet. Ask the `web` container what it means:

```bash
grep -n "Redis(" app.py
docker compose exec web getent hosts redis
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> 14:store = Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379)
> 172.19.0.2      redis
> ```

`docker compose exec web …` runs a command inside the running `web` container. On a Compose network, Docker runs a small DNS server that turns **service names into container IP addresses**. That's why the app can say `redis` and never needs an IP address, which can change whenever the container is recreated.

### 2.3 Read the logs

```bash
docker compose logs redis | tail -3
```

> [!NOTE]
> **Expected output (your values will differ)**
>
> ```
> redis-1  | 1:M … * Server initialized
> redis-1  | 1:M … * Ready to accept connections tcp
> redis-1  | 1:M … # WARNING: Redis does not require authentication and is not protected by network restrictions. Redis will accept connections from any IP address on any network interface.
> ```

Redis warns that anyone who can reach it can read and change the data, without a password. Keep that warning in mind, and look at the `ports:` lines in `compose.yaml` again: which service publishes a port, and which doesn't?

> [!IMPORTANT]
> **In the report**
>
> The network and volume names (2.1), the IP address that `redis` resolves to (2.2), and when your volume was created:
>
> ```bash
> docker volume inspect lab03_redis-data --format '{{.CreatedAt}}'
> ```

## Part 3 — Where does the state live? · ~19 min

Three commands look similar but do different things to your data. **Predict first, then check.**

### 3.0 Predict

Clear the terminal and make the terminal panel bigger (drag its top edge up), so Screenshot B fits later:

```bash
clear
curl -s localhost | grep -E "Visits|hostname"
```

This check fills the first row. **Every check is itself a visit**, so each prediction is the number the *next* check will print. Now, **before you run anything below**, copy this table into your report and fill in the *Predicted visits* column. A wrong prediction is fine; you'll explain it later.

| Step | Predicted visits | Actual visits | Web hostname | Same web container as before? |
|---|---|---|---|---|
| Now (3.0) | — | | | |
| After `restart` (3.1) | | | | |
| After `down` + `up` (3.2) | | | | |
| After `down -v` + `up` (3.3) | | | | |

Each step below ends with the same check. Fill in the rest of the row from its output.

### 3.1 Restart

```bash
docker compose restart
curl -s localhost | grep -E "Visits|hostname"
```

`restart` stops and starts the **same** containers. Compare the hostname with the one before.

### 3.2 Down and up

```bash
docker compose down
docker compose ps -a
docker compose up -d
curl -s localhost | grep -E "Visits|hostname"
```

> [!NOTE]
> **Expected output of `down` (your values will differ)**
>
> ```
> [+] down 3/3
>  ✔ Container lab03-web-1   Removed                                          0.1s
>  ✔ Container lab03-redis-1 Removed                                          0.1s
>  ✔ Network lab03_default   Removed                                          0.1s
> ```

`down` **deletes** both containers and the network: `docker compose ps -a` shows only the header line. `up` creates brand new ones, so the web container's hostname is different. Did the count survive? Redis keeps the count in memory and writes it to a file, `/data/dump.rdb`, when it stops. Where is `/data`?

### 3.3 Down with volumes

```bash
docker compose down -v
docker compose up -d
curl -s localhost | grep -E "Visits|hostname"
```

`-v` also deletes the named volume `lab03_redis-data`.

**Take Screenshot B now:** your terminal showing the three steps (3.1 to 3.3) with their `Visits` and hostname lines. If it doesn't fit on one screen, take two (B1 and B2).

### 3.4 Experiment: take the volume away

Is it really the volume that keeps the count? Test it. Reload the page in the browser until the counter is **at least 5**, then note the count:

```bash
curl -s localhost | grep Visits
```

Now delete the four `volumes` / `redis-data` lines from your copy of `compose.yaml` and apply the change:

```bash
sed -i '/redis-data/d; /^ *volumes:/d' compose.yaml
cat compose.yaml
docker compose up -d
curl -s localhost | grep Visits
```

`cat` shows that `redis` has no `volumes:` any more. Compose noticed that `redis` changed and replaced only that container. Reload a few times, then do what you did in 3.2:

```bash
docker compose down
docker compose up -d
curl -s localhost | grep Visits
```

Now put the original file back and apply it once more:

```bash
cp /workspaces/Cloud-Computing/lab-03-compose/app/compose.yaml .
docker compose up -d
curl -s localhost | grep Visits
```

> [!IMPORTANT]
> **In the report**
>
> The table with all columns filled in, and the four `Visits` values from 3.4 (before the edit, after the edit, after `down` + `up`, after putting the file back). Explain the last one: where was that number while the volume wasn't in `compose.yaml`?

### 3.5 Try to scale

What if one `web` container isn't enough? Ask Compose for three:

```bash
docker compose up -d --scale web=3
docker compose ps -a
```

Copy the error line into your report. Then go back to one:

```bash
docker compose up -d --scale web=1
```

> [!IMPORTANT]
> **In the report**
>
> The error line, and which `web` containers were running and which only *Created* in `docker compose ps -a`.

## Part 4 — Clean up · ~5 min

### 4.1 Containers, network, volume, image

```bash
docker compose down -v
docker image rm lab03-web
docker ps -a
docker volume ls
```

`docker ps -a` must be empty and `lab03_redis-data` must be gone.

### 4.2 Delete the codespace

<https://github.com/codespaces> → **⋯** next to your codespace → **Delete**.

> [!WARNING]
> **Why this matters**
>
> A running codespace uses your free core-hours. With Compose it's easy to leave several containers running without noticing.

## Submission · any time before the first exam period

Submit on Merlin whenever you're ready. The only hard deadline: **all labs must be in before the first exam period begins**, if you pass the course through the midterms or your seminar paper. Submitting within about two weeks works best, while the lab is still fresh and before the lectures build on it.

> [!IMPORTANT]
> **To Merlin**
>
> `lab03_<surname>.pdf` with:
>
> 1. **Your data:** GitHub username, codespace name, the network and volume names, the `redis` IP address and the volume's creation time (Part 2).
> 2. **Screenshot A:** your page in a browser, with the **forwarded address in the address bar** (1.4).
> 3. **The table from Part 3** (predicted and actual), **Screenshot B** (3.3), **the four counts from 3.4** and **the error from 3.5**.
> 4. **Short answers**, in your own words:
>    - Use your table to explain where the count was stored after each step, and why. Which of your predictions were wrong, and what did you assume?
>    - How did the `web` container find `redis` without an IP address? Why would a hard-coded IP address be a bad idea?
>    - Redis warned that it has no password (2.3). Who can reach it in this app, and why? Which line in `compose.yaml` would change that?
>    - Why did `--scale web=3` fail in 3.5, and why did one `web` container keep working? What would you need in front of several `web` containers so they could share port 80?

| Item | Required |
|---|:-:|
| Your data, table, 3.4 counts, 3.5 error and screenshots A–B, consistent with each other (same codespace, hostnames, counts, volume time) | ✓ |
| Short answers, using your own outputs | ✓ |

*Your report is about **your** run: your codespace, your containers, your counts. Reports that don't match each other or look copied will be checked again, and I may ask you to walk me through your report.*
