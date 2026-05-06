# Local LLM endpoint (llama-swap + llama.cpp, containerized)

OpenAI-compatible local endpoint at `http://127.0.0.1:11434/v1`, hot-swapping
between Gemma 3 4B and 12B based on the `model` field in the request body.
Runs in podman alongside Postgres on `based-workspace-net`.

## Architecture

```
caller ──► http://127.0.0.1:11434/v1/chat/completions
              { "model": "gemma-3-4b" | "gemma-3-12b", ... }
              │
              ▼
         based-workspace-llama-swap (podman, port 8080)
              │  llama-swap proxy + bundled llama.cpp Vulkan binary
              │
              ├─ "gemma-3-4b"  → llama-server -m /models/gemma-3-4b-it-Q4_K_M.gguf
              └─ "gemma-3-12b" → llama-server -m /models/gemma-3-12b-it-Q4_K_M.gguf
                                 (models bind-mounted RO from ~/models/)
```

## Files

| Path | Purpose |
| --- | --- |
| `Containerfile` | builds `based-workspace/llama-swap:vulkan` (debian-slim + libvulkan + llama.cpp `b9037` + llama-swap `v211`) |
| `docker-compose.yaml` | service definition; joins `based-workspace-net`; binds `~/models` and `config.yaml` |
| `config.yaml` | per-model `cmd` lines, in-container paths; `-watch-config` reloads in ~2 s |
| `~/models/*.gguf` | model files (host-side; mounted RO at `/models/`) |

The image is reproducible — versions are pinned via `ARG LLAMA_CPP_VERSION` /
`ARG LLAMA_SWAP_VERSION` in the Containerfile. Bump and rebuild to upgrade.

## Daily ops

```bash
# Bring everything up (Postgres compose creates the network):
podman compose -f infrastructure/core/docker-compose.yaml up -d based-workspace-postgres
podman compose -f infrastructure/llm/docker-compose.yaml up -d

# Status / logs
podman ps --filter name=based-workspace-
podman logs -f based-workspace-llama-swap

# Edit config.yaml on host → llama-swap reloads automatically (~2 s, -watch-config)

# Restart / stop
podman compose -f infrastructure/llm/docker-compose.yaml restart
podman compose -f infrastructure/llm/docker-compose.yaml down

# Smoke test
curl http://127.0.0.1:11434/v1/models
curl -s -X POST http://127.0.0.1:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma-3-4b","messages":[{"role":"user","content":"hi"}]}'
```

## How recipes pick a model

Recipe frontmatter declares `execution.model: gemma-3-4b` (or `gemma-3-12b`).
The dispatcher passes that string straight to `/v1/chat/completions`. If a
recipe omits it, the runtime falls back to `RECIPE_DEFAULT_MODEL` from
`.env` (currently `gemma-3-4b`).

## Switching backends (CPU ↔ iGPU ↔ dGPU)

Edit `config.yaml` and llama-swap auto-reloads in ~2 s — no rebuild, no
restart needed. The image bundles the Vulkan-capable llama.cpp binary, so
the same container handles all three states.

| State | What to set on each model's `cmd` line |
| --- | --- |
| **CPU only (current default)** | `-t 16` (no `-ngl`) |
| **iGPU offload (no reboot)** | `-ngl 99 --device Vulkan0` — works today via the Radeon 890M |
| **dGPU offload (after re-enabling 4060 + reboot)** | `-ngl 99 --device Vulkan0` (or `Vulkan1`); verify ordering with `vulkaninfo --summary` |

Re-enabling the dGPU on this Asus G16 2024:
- Via BIOS / Armoury Crate: set GPU mode to Standard / Optimus / Auto, reboot.
- Via Linux userspace (after installing `asusctl` + `supergfxctl` from the
  `lukenukem/asus-linux` Fedora COPR): `supergfxctl -m Hybrid`, reboot.

For GPU passthrough into the container you'll also need to add a `devices:`
entry to `docker-compose.yaml`:
- iGPU (DRM): `- /dev/dri:/dev/dri`
- dGPU (CDI): set up NVIDIA CDI, then `- nvidia.com/gpu=all`

## Tuning notes

- **Context size.** 4B is `-c 8192`, 12B is `-c 4096`. Bumping context costs
  RAM/VRAM (~50 MB / 1k tokens for 4B at Q4, ~120 MB / 1k for 12B).
- **Threads.** `-t 16` matches physical cores on the HX 370. Going higher
  (24, hyperthreaded) typically slows CPU inference.
- **TTL.** Each model unloads after 600 s idle and reloads on next request.
  First request after unload pays a ~3–5 s warm-up.
- **Speed (CPU only, measured in container):** 4B Q4_K_M ≈ 29 tok/s gen,
  ~80 tok/s prompt. 12B expected ~9 tok/s gen.

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| `Error loading config: open /etc/llama-swap/config.yaml: permission denied` | SELinux relabel needed on the bind mount. Already handled (`:ro,Z` on the config in `docker-compose.yaml`). If you change the mount, keep the `:Z` / `:z` suffixes. |
| `network based-workspace-net not found` | Bring the Postgres compose up first — it creates the shared network. |
| Long pause on first request | Model loading from disk; check `podman logs based-workspace-llama-swap` for `llama_model_loader` lines. |
| `error loading model: out of memory` | Lower `-c` or switch to a smaller quant (e.g., Q4_K_S). |

## Why containerized

Single `podman ps` lists Postgres + llama-swap together; same lifecycle
commands; same network; the LLM endpoint travels with the repo (compose
file, Containerfile, config.yaml are all under `infrastructure/llm/`)
instead of living in scattered systemd-user units and `~/.config/`.
