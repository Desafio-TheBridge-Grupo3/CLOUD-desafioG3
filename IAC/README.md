# Infraestructura como código

## Crea Subnet:



## Log Analytics workspace:

Crea con Azure CLI:

```bash
az monitor log-analytics workspace create --name $(logs-name) --resource-group $(grupo-recursos)
```

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