---
name: run-colab-ollama
description: Use when running Ollama or an OpenAI-compatible LLM server on a Google Colab GPU, starting, stopping, or checking Colab sessions with google-colab-cli, configuring SSH access or local port forwarding to a Colab VM, sizing a Colab GPU for a model to save compute units, or pulling, inspecting, and querying models hosted on Colab.
---

# Run Colab Ollama

Manage an Ollama server on a Google Colab GPU VM through `google-colab-cli` and expose it locally over an encrypted OpenSSH tunnel as a drop-in OpenAI-compatible API (`http://127.0.0.1:<port>/v1`).

Commands that talk to Colab (`colab`, `ssh`) require outbound network access; run them outside a network-isolated sandbox when needed.

## 1. Prerequisites and SSH setup

Check and bootstrap locally before provisioning a VM:

1. **CLI:** look for `colab` on `$PATH` or `$HOME/.local/bin/colab`. If missing, install with `uv tool install google-colab-cli && uv tool update-shell` (fallback: `pip install google-colab-cli`).
2. **Auth and balance:** run `colab usage`. First run triggers OAuth2 browser login. If the user needs headless GCP credentials instead, use `--auth adc`.
3. **SSH key:** check for `~/.ssh/id_ed25519.pub` (or another existing public key). If none exists, generate one:
   ```bash
   mkdir -p ~/.ssh && chmod 700 ~/.ssh
   ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
   ```
4. **SSH config (`~/.ssh/config`):** ensure a host block exists for the target session name (default `llm`, host alias `colab-<session>`). **Always write the resolved absolute path** to `colab` (from `command -v colab` or `$HOME/.local/bin/colab`), because OpenSSH's non-interactive `ProxyCommand` shell often omits `~/.local/bin` from `$PATH`.
   ```ssh-config
   Host colab-llm
       User root
       ProxyCommand /ABS/PATH/TO/colab ssh --proxy-mode -s llm -i ~/.ssh/id_ed25519.pub
       StrictHostKeyChecking no
       UserKnownHostsFile /dev/null
   ```
   Set `chmod 600 ~/.ssh/config` when creating it. Each fresh Colab VM generates a new host key, so disabling strict host checking for `colab-*` avoids spurious host-key failures.

## 2. Choose the GPU tier (ask before provisioning)

Before running `colab new`, run `colab sessions` and `colab usage` so you do not duplicate an already-running runtime.

If the user has not specified a GPU or model yet, ask which GPU tier and model they want using this sizing guide (leave at least 2 GB of VRAM headroom for KV cache):

| GPU flag | VRAM | Approx. burn rate | Sweet spot (Q4 quants) |
| :--- | :--- | :--- | :--- |
| `--gpu T4` | 15 GB | ~1.1–1.6 CU/hr | Fast, cheap iteration; dense models up to ~14B |
| `--gpu L4` | 22.5 GB | ~3.0–4.8 CU/hr | Best speed/quality per credit; 24B–32B dense or 30B–35B MoE |
| `--gpu A100` | 40 / 80 GB | ~5.4–12+ CU/hr | 70B+ Q4, Q8 quants, very long contexts, or concurrent requests |

- Omit `--high-mem` by default: Ollama loads quantized weights straight into GPU VRAM, and high-RAM VMs burn extra compute units.
- Exact burn rates fluctuate with load and plan tier; confirm live balance with `colab usage`.

## 3. Session lifecycle

| Action | Command |
| :--- | :--- |
| Start runtime | `colab new -s <session> --gpu <T4\|L4\|A100>` |
| List active runtimes | `colab sessions` |
| Inspect session info | `colab status -s <session>` |
| Check compute units | `colab usage` |
| Run one remote command | `colab ssh -s <session> -- <cmd>` (or `ssh colab-<session> "<cmd>"`) |
| Stop runtime | `colab stop -s <session>` |

**Credit safety:** closing an SSH shell or port-forward tunnel does **not** stop the Colab VM — it keeps burning compute units until idle timeout. When stopping a session, terminate both the remote VM (`colab stop -s <session>`) and any local SSH tunnel pointing to it. Always remind the user how to stop the session once it is up, and offer to stop it when they finish.

## 4. Bootstrap Ollama and manage models over SSH

Colab VM filesystems are ephemeral: every `colab new` starts clean without Ollama or cached weights.

1. **Inspect the VM** (GPU, disk, running daemon):
   ```bash
   ssh colab-<session> 'nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader; df -h /; command -v ollama || echo ollama-missing'
   ```
2. **Install Ollama if missing:**
   ```bash
   ssh colab-<session> 'command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh'
   ```
3. **Start the Ollama daemon** bound to VM loopback with flash attention and `q8_0` KV cache (halves KV-cache VRAM at long contexts). Redirect stdin/stdout/stderr with `</dev/null`, or non-interactive `ssh` will hang waiting for the background process to close file descriptors:
   ```bash
   ssh colab-<session> 'pgrep -x ollama >/dev/null || nohup env OLLAMA_HOST=127.0.0.1:11434 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve > /tmp/ollama.log 2>&1 </dev/null &'
   ssh colab-<session> 'for i in $(seq 1 15); do curl -sf http://127.0.0.1:11434/api/tags >/dev/null && exit 0; sleep 1; done; tail -n 30 /tmp/ollama.log; exit 1'
   ```
4. **Find, pull, and inspect models:**
   - Before pulling an unfamiliar model, check available tags and file sizes (on `ollama.com` or Hugging Face) to confirm it fits the VM's VRAM with ≥2 GB headroom.
   - Pull from the Ollama library (`ollama pull <model>:<tag>`) or directly from a Hugging Face GGUF repo (`ollama pull hf.co/<org>/<repo>:<quant>`).
   - Pull directly onto the VM rather than mounting Google Drive: Colab datacenter bandwidth downloads 10–20 GB in under a minute and avoids Drive quota and I/O bottlenecks.
   - Inspect or clean up on the VM: `ollama list`, `ollama ps`, `ollama rm <model>`, `tail -n 40 /tmp/ollama.log`.

## 5. Expose locally and verify

1. **Pick a free local port:** check whether `11434` is already bound locally (for example, a local Ollama daemon):
   ```bash
   lsof -nP -iTCP:11434 -sTCP:LISTEN
   ```
   Use `11434` if free; otherwise pick the next free port (`11435`, etc.) or the port the user asked for.
2. **Start the SSH port-forward tunnel** as a persistent background process (bound strictly to `127.0.0.1` so it is never exposed to the LAN):
   ```bash
   ssh -N \
     -o ExitOnForwardFailure=yes \
     -o ServerAliveInterval=30 \
     -o ServerAliveCountMax=3 \
     -L 127.0.0.1:<LOCAL_PORT>:127.0.0.1:11434 \
     colab-<session>
   ```
3. **Verify end to end from the local machine** before handing off:
   ```bash
   curl -sf http://127.0.0.1:<LOCAL_PORT>/v1/models
   ```
   Optionally run a short smoke prompt against `/v1/chat/completions` when the user wants confirmation that inference loads on GPU (verify with `ollama ps` on the VM that the processor shows `100% GPU`, not CPU offload).

## 6. Hand-off format

Whenever the server is ready, report concisely:
- **Session & GPU:** session name, GPU model/VRAM, loaded model(s).
- **OpenAI-compatible base URL:** `http://127.0.0.1:<LOCAL_PORT>/v1` (API key: any non-empty string, e.g. `ollama`).
- **Native Ollama URL:** `http://127.0.0.1:<LOCAL_PORT>`.
- **Quick query snippet** (`curl` or Python `OpenAI(base_url=..., api_key="ollama")`) using the active model tag.
- **Stop reminder:** exact `colab stop -s <session>` command (or offer to stop it when done).
