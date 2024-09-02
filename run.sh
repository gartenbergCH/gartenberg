#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

BUILDKIT_PROGRESS=plain docker compose up --build
