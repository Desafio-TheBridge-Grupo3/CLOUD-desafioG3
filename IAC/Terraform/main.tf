terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.87.0"
    }
  }
}

provider "azurerm" {
  features {    
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}

# Grupo de recursos del proyecto
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

# Almacenamiento

# 