# Dockerfile
# This is the recipe Docker follows to build your app into an image.
# Each line creates a new "layer" — Docker caches layers that haven't changed,
# making rebuilds fast.

# ── Layer 1: Base image ──────────────────────────────────────────────────────
# We start from an official slim Python image (smaller = faster, safer)
FROM mirror.gcr.io/library/python:3.11-slim

# ── Layer 2: Working directory ───────────────────────────────────────────────
# All following commands run from this folder INSIDE the container
WORKDIR /app

# ── Layer 3: Dependencies ────────────────────────────────────────────────────
# We copy requirements.txt FIRST (before our code) on purpose.
# Why? If our code changes but requirements don't, Docker reuses this
# cached layer and skips re-installing packages. Saves minutes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Layer 4: App code ────────────────────────────────────────────────────────
# Now copy everything else (our actual code)
COPY . .

# ── Layer 5: Port declaration ────────────────────────────────────────────────
# Tell Docker this container listens on port 5000 (documentation only —
# the actual port mapping happens in "docker run")
EXPOSE 5000

# ── Layer 6: Start command ───────────────────────────────────────────────────
# This runs when the container starts.
# We turn off debug mode for "production" — debug mode is only for local dev.
CMD ["python", "run.py"]