#!/usr/bin/env bash
set -e

git submodule update --init --recursive

curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

mkdir -p ~/.config/nix

cat > ~/.config/nix/nix.conf <<EOF
experimental-features = nix-command flakes
EOF

uv sync
