"""A tiny web app for Lab 02: it shows who built it and which container is answering."""
import os
import platform
import socket
from datetime import datetime, timezone

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    name = os.environ.get("STUDENT_NAME", "nobody yet")
    version = os.environ.get("APP_VERSION", "dev")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"""<!doctype html>
<meta charset="utf-8">
<title>Hello, cloud</title>
<h1>Hello from {name}</h1>
<ul>
  <li>Version: <b>{version}</b></li>
  <li>Container (hostname): <code>{socket.gethostname()}</code></li>
  <li>Python: {platform.python_version()}</li>
  <li>Time: {now}</li>
</ul>
"""


if __name__ == "__main__":
    # 0.0.0.0 = listen on every network interface, not only inside the container.
    app.run(host="0.0.0.0", port=8000)
