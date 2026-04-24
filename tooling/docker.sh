#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "$CMD" in
  manage)
    # Run any Django management command, e.g.: ./tooling/docker.sh manage makemigrations gartenberg
    docker run --rm -i \
      -v "${PROJECT_ROOT}:/opt" \
      -w /opt \
      -e JUNTAGRICO_SECRET_KEY=dummy \
      python:3.11 \
      sh -c "pip install --quiet -r requirements.txt && python manage.py ${*:2}"
    ;;
  *)
    echo "Usage: $0 {manage <django-command> [args...]}"
    echo ""
    echo "Examples:"
    echo "  $0 manage makemigrations gartenberg"
    echo "  $0 manage migrate"
    echo "  $0 manage showmigrations"
    exit 1
    ;;
esac
