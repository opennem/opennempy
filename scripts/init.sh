#!/usr/bin/env bash
set -exo pipefail

pwd > .venv/lib/python3.8/site-packages/local.pth

if [ -z "$VIRTUAL_ENV" ]
then
  echo "Running in $VIRTUAL_ENV"
else
  source .venv/bin/activate
fi
