# AiCIV Proof-Style Docker Container
# Base image for M2.7 (MiniMax) AI civilizations
#
# Build: docker build -t aiciv-m27:latest .
# Run:   docker run -d --name {civ-name} \
#          -e ANTHROPIC_API_KEY=your_key_here \
#          -e CIV_NAME={civ-name} \
#          -v {data-volume}:/home/civ/civ-data \
#          aiciv-m27:latest

FROM ubuntu:22.04

# === Prevent interactive prompts during package install ===
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color

# === Install core dependencies ===
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    tmux \
    vim \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# === Install Claude Code CLI ===
# Download the CLI binary (architecture detection)
RUN arch=$(dpkg --print-architecture) \
    && case "$arch" in \
        amd64) Claude_ARCH="amd64" ;; \
        arm64) Claude_ARCH="arm64" ;; \
        *) Claude_ARCH="amd64" ;; \
    esac \
    && curl -fsSL https://storage.googleapis.com/claude-code-stable/claude-code-$Claude_ARCH -o /usr/local/bin/claude \
    && chmod +x /usr/local/bin/claude

# === Install Python packages (duckduckgo-search for search, nacl for auth, requests+cryptography for HUB) ===
RUN pip3 install --no-cache-dir \
    duckduckgo-search \
    pynacl \
    httpx \
    python-dotenv \
    requests \
    cryptography

# === Create non-root user for Claude Code ===
# (Claude Code blocks --dangerously-skip-permissions when running as root)
RUN useradd -m -s /bin/bash civ
RUN usermod -aG sudo civ
RUN echo "civ ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# === Configure Claude Code as a command ===
ENV PATH="/usr/local/bin:${PATH}"

# === Set default env vars (can be overridden at runtime) ===
ENV ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic"
ENV ANTHROPIC_MODEL="MiniMax-M2.7"
ENV ANTHROPIC_SMALL_FAST_MODEL="MiniMax-M2.7"
ENV ANTHROPIC_DEFAULT_SONNET_MODEL="MiniMax-M2.7"
ENV ANTHROPIC_DEFAULT_OPUS_MODEL="MiniMax-M2.7"
ENV ANTHROPIC_DEFAULT_HAIKU_MODEL="MiniMax-M2.7"
ENV CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS="1"
ENV CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
ENV API_TIMEOUT_MS="300000"

# === Working directory ===
WORKDIR /home/civ

# === TMUX configuration ===
RUN echo "set -g default-terminal screen-256color" >> /home/civ/.tmux.conf \
    && chown civ:civ /home/civ/.tmux.conf

# === Copy template files into container ===
# Hooks must be at .claude/hooks/ for Claude Code to find them (per settings.json)
COPY hooks/ /home/civ/.claude/hooks/
COPY config/ /home/civ/config/
COPY launch-scripts/ /home/civ/launch-scripts/
COPY fork-template/ /home/civ/fork-template/

# Fix ownership
RUN chown -R civ:civ /home/civ/.claude /home/civ/config /home/civ/launch-scripts /home/civ/fork-template

# Switch to non-root user
USER civ

# Default command: keep container alive with tmux
CMD ["tail", "-f", "/dev/null"]