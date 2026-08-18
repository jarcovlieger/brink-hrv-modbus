# Development

This repo ships a lightweight [dev container](https://containers.dev/) for working on the integration without needing a full Home Assistant Core checkout.

## Prerequisites

- [VS Code](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Getting started

1. Open this repo's folder in VS Code.
2. Run **Dev Containers: Reopen in Container** (VS Code usually prompts for this automatically). This builds a Python 3.14 container and runs `scripts/setup`, which installs Home Assistant and this integration's dependencies.
3. In the integrated terminal, start Home Assistant:

   ```bash
   scripts/develop
   ```

   On first run this also creates a `config/` test instance. HA logs to the terminal; leave it running.
4. Open [http://localhost:8123](http://localhost:8123) (VS Code forwards the port automatically) and go through onboarding.
5. Add the integration via **Settings → Devices & Services → + Add Integration → Brink HRV Modbus**, pointing it at a real or test Modbus gateway.

Code changes under `custom_components/brink_ventilation` require restarting `scripts/develop` (Ctrl+C, then rerun) to take effect — there is no hot reload.

## What's in here

| Path | Purpose |
|---|---|
| `.devcontainer.json` | Container definition (Python 3.14 + a few apt packages). Forwards port 8123. |
| `scripts/setup` | Installs `requirements_common.txt` and `requirements_dev.txt`. Runs automatically on container create. |
| `scripts/develop` | Creates `config/` on first run, puts `custom_components` on `PYTHONPATH`, and starts `hass --debug`. |
| `scripts/lint` | Runs `ruff format .` and `ruff check . --fix`. |
| `config/configuration.yaml` | The only tracked file under `config/` — everything else there is runtime state and gitignored. |
| `requirements_dev.txt` | Pinned `homeassistant` and `pymodbus` versions used for local development. |

## Why `configuration.yaml` doesn't use `default_config:`

The [integration_blueprint](https://github.com/ludeeus/integration_blueprint) template this setup is based on normally uses `default_config:`, but that pulls in components unrelated to a Modbus integration — camera/stream, cloud, Bluetooth, DHCP/SSDP discovery, hassio-supervisor stubs, and more. None of those ship as hard pip dependencies of the base `homeassistant` package; Home Assistant installs them on demand the first time it imports them. On a fresh container that means a dozen components racing their own pip install on first boot, several of them failing with `ModuleNotFoundError` before the install finishes.

`configuration.yaml` here instead enables just `frontend:`, which already pulls in what the UI and config-flow onboarding need (`config`, `api`, `auth`, `onboarding`, `lovelace`, `websocket_api`). Add other components explicitly only if you actually need them for testing.

## Troubleshooting

**`PermissionError: [Errno 13] Permission denied: '.../config/.ha_run.lock'`**
Something wrote to `config/` as a different user than the one running `scripts/develop` in your terminal (normally `vscode`) — e.g. a `docker exec` run as root. Fix from a terminal with root access inside the container:

```bash
sudo chown -R vscode:vscode config
```

**A component fails to import on first boot, then works after a restart**
Expected for any component not covered by `requirements_dev.txt` — Home Assistant installs its dependency live and only succeeds once that install finishes. Either restart `scripts/develop`, or pin the missing package in `requirements_dev.txt` so `scripts/setup` installs it upfront.
