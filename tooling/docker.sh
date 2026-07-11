#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

CURRENT_USER="$(id -u):$(id -g)"
PYTHON_USER_ARGS=(--user "${CURRENT_USER}" -e HOME=/tmp)

case "$CMD" in
  test)
    docker run --rm -i \
      "${PYTHON_USER_ARGS[@]}" \
      -v "${PROJECT_ROOT}:/opt" \
      -w /opt \
      -e JUNTAGRICO_SECRET_KEY=dummy \
      python:3.11 \
      sh -c "pip install --quiet -r requirements.txt && python manage.py test gartenberg"
    ;;
  manage)
    # Run any Django management command, e.g.: ./tooling/docker.sh manage makemigrations gartenberg
    docker run --rm -i \
      "${PYTHON_USER_ARGS[@]}" \
      -v "${PROJECT_ROOT}:/opt" \
      -w /opt \
      -e JUNTAGRICO_SECRET_KEY=dummy \
      python:3.11 \
      sh -c "pip install --quiet -r requirements.txt && python manage.py ${*:2}"
    ;;
  *)
    echo "Usage: $0 {test|manage <django-command> [args...]}"
    echo ""
    echo "Examples:"
    echo "  $0 test"
    echo "  $0 manage makemigrations gartenberg"
    echo "  $0 manage migrate"
    echo "  $0 manage showmigrations"
    exit 1
    ;;
esac
