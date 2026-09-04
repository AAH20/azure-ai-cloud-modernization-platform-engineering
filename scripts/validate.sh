#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m modernization_factory.cli examples/order-api.json --output evidence/order-api-analysis.json >/dev/null
python3 -m json.tool evidence/order-api-analysis.json >/dev/null

if command -v az >/dev/null 2>&1; then
  az bicep build --file infra/main.bicep --outfile /tmp/modernization-main.json
else
  echo "SKIP: Azure CLI not installed; Bicep compilation was not executed locally."
fi

if command -v terraform >/dev/null 2>&1; then
  terraform -chdir=terraform fmt -check
else
  echo "SKIP: Terraform not installed; formatting was not executed locally."
fi
