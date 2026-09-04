variable "location" {
  type    = string
  default = "westeurope"
}

variable "environment" {
  type    = string
  default = "dev"
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test, or prod"
  }
}

variable "workload_name" {
  type    = string
  default = "modernization"
}

resource "azurerm_resource_group" "workload" {
  name     = "rg-${var.workload_name}-${var.environment}"
  location = var.location
  tags = {
    environment    = var.environment
    workload       = var.workload_name
    managedBy      = "terraform"
    evidenceStatus = "requires-post-deployment-verification"
  }
}

resource "azurerm_log_analytics_workspace" "workload" {
  name                = "log-${var.workload_name}-${var.environment}"
  location            = azurerm_resource_group.workload.location
  resource_group_name = azurerm_resource_group.workload.name
  sku                 = "PerGB2018"
  retention_in_days   = var.environment == "prod" ? 90 : 30
}

output "resource_group_id" {
  value = azurerm_resource_group.workload.id
}
