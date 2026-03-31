# Local AI Inference Setup

This document describes how to start the advanced Local AI capabilities of the `based-workspace`.

The workspace ships with a fully containerized GPU-accelerated local inference engine (using Ollama), separated from the core infrastructure for performance and modularity.

## Prerequisites

- **Host System**: You need an NVIDIA GPU with sufficient VRAM (ideally 32GB+ for 30B parameter models). 
- **Drivers**: Ensure you have the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed on your host system so Podman/Docker can allocate GPU resources to containers.
- **Base Infrastructure**: Ensure your base infrastructure is running (`infrastructure/core/docker-compose.yaml`).

## Quick Start

1. Start your base workspace (if not already running):
   ```bash
   podman compose -f infrastructure/core/docker-compose.yaml up -d
   ```

2. Start the AI Inference engine:
   ```powershell
   podman compose -f infrastructure/ai/docker-compose.yaml up -d
   ```

3. Pull the recommended model:
   ```powershell
   podman exec -it ollama ollama pull qwen3:30b-a3b-thinking-2507-q4_K_M
   ```

4. Verify your models are loaded:
   Open [http://localhost:11434/api/tags](http://localhost:11434/api/tags) in your browser or run:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:11434/api/tags" | Select-Object -ExpandProperty models | Select-Object name, size
   ```

## What happens under the hood?

When you run the AI docker-compose file, the **`ollama`** service is created. This is the main inference server, running with GPU acceleration (NVIDIA).

Unlike the core infrastructure, the AI model pulling is handled manually to give you better control over which version and quantization level of the model you want to use.

You can track the download progress directly in your terminal after running the `pull` command above.

## Integrating with n8n

The main AI usage is likely interacting with workflows via **n8n**.
Because both the core services and the AI services share the same `based-workspace-net` docker network, n8n can directly talk to the local inference engine.

1. Create an **AI Agent** or **Basic LLM Chain** node in n8n.
2. Select **Ollama Chat Model** as the model provider.
3. Base URL: `http://ollama:11434`
4. Model Name: `qwen3:30b-a3b-thinking-2507-q4_K_M`

## Troubleshooting

- **No GPU found error**: Check if you have properly installed the NVIDIA Container toolkit and that your container engine (Podman) is configured to use it. Run `nvidia-smi` inside the container to verify:
  ```powershell
  podman exec -it ollama nvidia-smi
  ```
- **Out of memory / Slow inference**: Check your VRAM availability. The `q4_K_M` quantization for a 30B model typically requires ~18-20GB of VRAM. If it's slow, it might be offloading to system RAM.
