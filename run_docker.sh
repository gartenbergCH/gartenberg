#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

read -p "Enter juntagrico username: " juntagrico_username
export juntagrico_username
read -p "Enter juntagrico email: " juntagrico_email
export juntagrico_email
read -p "Enter juntagrico password: " juntagrico_password
export juntagrico_password
read -p "Enter juntagrico secret key: " juntagrico_secret_key
export juntagrico_secret_key
docker build --build-arg juntagrico_username=$juntagrico_username --build-arg juntagrico_email=$juntagrico_email --build-arg juntagrico_password=$juntagrico_password --build-arg juntagrico_secret_key=$juntagrico_secret_key . --tag "gartenberg:local" 2>&1 | tee build.log
docker run -it --rm -p 8000:8000 gartenberg:local
