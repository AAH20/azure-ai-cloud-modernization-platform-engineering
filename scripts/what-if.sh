#!/usr/bin/env bash
set -euo pipefail

subscription_id="${AZURE_SUBSCRIPTION_ID:?Set AZURE_SUBSCRIPTION_ID}"
location="${AZURE_LOCATION:-westeurope}"

az account set --subscription "$subscription_id"
az deployment sub what-if \
  --name modernization-foundation-preview \
  --location "$location" \
  --template-file infra/main.bicep \
  --parameters location="$location" environment=dev workloadName=modernization
