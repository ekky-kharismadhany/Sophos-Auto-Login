# Sophos Auto-Login

Automatic re-authentication for Sophos captive portal. Designed for headless servers (e.g. Mac Mini GitLab runner) that get periodically disconnected by Sophos network policy.

The tool detects internet connectivity loss and replays a previously recorded login sequence against the Sophos portal over LAN.

## How It Works

1. **Record** — You open a real browser on the portal and perform the login steps once. The tool saves the actions as a Playwright script.
2. **Run** — The tool periodically checks internet connectivity. When blocked, it replays your recorded login with real credentials substituted in.

No internet connection is needed after initial setup.

## Setup

```bash
# Install (requires internet once)
uv sync
uv run playwright install chromium

# Configure
cp .env.example .env
# Edit .env with your portal URL and credentials
```

## Configuration

Set these in `.env` or as environment variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `SOPHOS_PORTAL_URL` | Yes | — | Portal URL, e.g. `http://10.0.0.1:8090` |
| `SOPHOS_USERNAME` | Yes | — | Portal username |
| `SOPHOS_PASSWORD` | Yes | — | Portal password |
| `SOPHOS_RUN_MODE` | No | `cron` | `cron` (single run) or `periodic` (loop) |
| `SOPHOS_CHECK_INTERVAL` | No | `60` | Seconds between checks (periodic mode) |
| `SOPHOS_CONNECTIVITY_URL` | No | `https://www.google.com/generate_204` | URL to test internet |
| `SOPHOS_LOG_LEVEL` | No | `INFO` | Logging level |
| `SOPHOS_SCRIPT_PATH` | No | `./recorded_login.py` | Path to saved recorded script |

## Usage

### Record login steps

```bash
uv run python -m sophos_auto_login record
```

A browser opens on the portal. Perform the login using `__USERNAME__` as the username and `__PASSWORD__` as the password. Close the browser when done.

### Run (check + login if needed)

```bash
# Cron mode (default) — single check, exits with 0 (ok) or 1 (failed)
uv run python -m sophos_auto_login

# Periodic mode — loops forever, set SOPHOS_RUN_MODE=periodic
uv run python -m sophos_auto_login run
```

### macOS launchd

Copy and edit the plist for your environment:

```bash
sudo mkdir -p /var/log/sophos-auto-login
cp launchd/com.office.sophos-auto-login.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.office.sophos-auto-login.plist
```
