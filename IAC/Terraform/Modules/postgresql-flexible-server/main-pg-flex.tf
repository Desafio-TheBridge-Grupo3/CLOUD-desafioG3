resource "azurerm_postgresql_flexible_server" "pg-flex-server" {
  name                   = var.pg-flex-name
  resource_group_name    = var.resource-group-name
  location               = var.location
  version                = "15"
  administrator_login    = "psqladmin"
  administrator_password = "H@Sh1CoR3!"
  storage_mb             = 32768
  sku_name               = "GP_Standard_D4s_v3"
}