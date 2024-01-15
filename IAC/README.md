# Infraestructura como código

## Import existing infrastructure:

https://charotamine.medium.com/terraform-azure-importing-an-existing-infrastructure-cab697ec37e6

## Container Apps:

Revisions: https://learn.microsoft.com/en-us/azure/container-apps/revisions

Deployment: https://learn.microsoft.com/en-us/azure/container-apps/application-lifecycle-management

Monitoring: https://learn.microsoft.com/en-us/azure/container-apps/observability

What are Bindings?

Step 1: Crear un container Apps Environment

Crea con CLI:

```bash
az containerapp env create --name $(cont-env-name) --resource-group $(grupo-recursos) --logs-destination azure-monitor 
```

Step 2: Create container apps in single environment

Crea App
```bash
az containerapp up --name $(app-nombre)
```

Step 3: Add secrets to Apps

## LAST: azure pipelines on teraform:

https://itnext.io/creating-azure-devops-pipelines-using-terraform-48877c6419a1