# Guide Followed: https://www.maxivanov.io/deploy-azure-functions-with-terraform/
#                 https://medium.com/@abhimanyubajaj98/deploying-azure-functions-with-terraform-and-visual-studio-code-d7bd6d629aa5

# Service plan para las funciones - Doc: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/service_plan
resource "azurerm_service_plan" "service-plan" {
  name                = var.function-plan
  resource_group_name = var.resource-group-name
  location            = var.location
  kind                = "FunctionApp"
  reserved            = true
  os_type             = "Linux"
  sku_name            = "Y1"
}

# Crea application insights para monitorizar - Doc: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_insights
resource "azurerm_application_insights" "application_insights" {
  name                = "${var.resource-group-name}-application-insights"
  location            = var.location
  resource_group_name = var.resource-group-name
  application_type    = var.application-type
}

# Creación de la función - doc: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_function_app
#                               https://build5nines.com/terraform-deploy-azure-function-app-with-consumption-plan/
resource "azurerm_linux_function_app" "function" {
  name                = var.function-name
  resource_group_name = var.resource-group-name
  location            = var.location
  service_plan_id = azurerm_service_plan.service-plan.id

  site_config {
    application_insights_key = azurerm_application_insights.application_insights.instrumentation_key
    application_stack {
        python_version = 3.11 #FUNCTIONS_WORKER_RUNTIME        
    }
  }

  storage_account {
    name = ""
    account_name = var.storage-accountname
    access_key = ""
    share_name = ""
    type = "azureblob"
  }

  public_network_access_enabled = false
}