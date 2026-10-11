"""A tiny web app for Lab 03: a visit counter that keeps its state in a second container (Redis)."""
import os
import signal
import socket
import sys

from flask import Flask
from redis import Redis

app = Flask(__name__)

# "redis" is not a real hostname: it's the name of the service in compose.yaml.
# Compose puts both containers on one network where service names resolve to container IPs.
store = Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379)


@app.route("/")
def index():
    visits = store.incr("visits")
    name = os.environ.get("STUDENT_NAME") or "nobody yet"
    codespace = os.environ.get("CODESPACE_NAME") or "not set"
    return f"""<!doctype html>
<meta charset="utf-8">
<title>Visit counter</title>
<h1>Hello from {name}</h1>
<ul>
  <li>Visits: <b>{visits}</b></li>
  <li>Web container (hostname): <code>{socket.gethostname()}</code></li>
  <li>Codespace: <code>{codespace}</code></li>
</ul>
"""


if __name__ == "__main__":
    # As the first process in a container, Python ignores "stop" (SIGTERM) unless told otherwise,
    # and Docker would wait 10 s before killing it. Exit at once instead.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    app.run(host="0.0.0.0", port=8000)
