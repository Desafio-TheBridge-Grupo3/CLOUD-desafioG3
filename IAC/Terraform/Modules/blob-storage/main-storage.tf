resource "azurerm_storage_account" "storage_account" {
  name = "${var.resource-group-name}storage"
  resource_group_name = var.resource-group-name
  location = var.location
  account_tier = "Standard"
  account_replication_type = "LRS"
}