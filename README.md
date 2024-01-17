***
# DESAFIO DE TRIPULACIONES - THE BRIDGE
## Grupo 3 - Cloud & DevOps   

### Indice:

1. [Gestión de permisos y control de versiones](##1.-Gestión-de-permisos-y-control-de-versiones:)

2. [Diseño de la Arquitectura](##2.-Diseño-de-la-Arquitectura)

3. [Infraestructura como código (IaC)](##3.-Infraestructura-como-código-(IaC))

4. [Despliegue e implementación contínuos (CI/CD)](##4.-Despliegue-e-implementación-contínuos-(CI/CD))

5. [Monitorización](##5.-Monitorización)

6. [Memoria de proyecto](##6.-Memoria-de-proyecto)

## 1. Gestión de permisos y control de versiones:

Para limitar a la mínima cantidad de usuarios que puedan alterar la infraestrucura desplegada, los permisos de acceso a la plataforma de Azure se limitarón a los imprescindibles para cada vertical. Para poder asignar permisos en bloque, el comienzo de ésta fase consistió en crear tres grupos de usuarios, uno para ciberseguridad, uno para data science y uno para full-stack; y a crear cuentas de invitado a los miembros del equipo que tendrán acceso.

Para facilitar la comprensión de la plataforma de azure y el funcionamiento de ésta, a todos los miembros de las verticales técnicas se les ha asignado el rol de "reader" sobre la suscripción al completo. El enfoque a la hora de asignar permisos ha tenido en cuenta tanto el desconocimiento de la plataforma por parte del resto de compañeros, como la buena práctica de configurar nuestra arquitectura utilizando código como infraestructura. De ésta forma se llegó a la conclusión que no deberían de recibir ningún permiso adicional, a menos que se presentase la necesidad. La excepción ha sido la vertical de ciberseguridad, a la cuál, una vez documentados sobre la nube de azure, se les asignó los roles de *Security Admin* y *App Compliance Automation Administrator* para poder mantener monitorizada la aplicación.

Se ha tomado un enfoque similar a la hora de aprovisionar el grupo con control de versiones. Utilizando github, se ha creado una organización para albergar el proyecto. Se creó un repositorio principal para el trabajo de puesta en común entre verticales y entorno de desarrollo, y submódulos para que cada vertical tenga un espacio aislado donde desarrollar entre ellos. Finalmente, un último submódulo para albergar la versión de la aplicación que se despliega en producción. 

Para gestionar los permisos se han creado equipos dentro de la organización, de tal forma que cada vertical tenga permisos de lectura sobre todo el proyecto, pero solo permisos de escritura sobre su propio repositorio y la rama principal. Finalmente, la rama de producción no pertenece a ningún equipo y solo tienen permiso de escritura sobre el la vertical de cloud, que se encargan de desplegar la app.

## 2. Diseño de la Arquitectura

### Arquitectura lograda durante la fase 1:

![Alt text](Arquitectura/diagrama-arquitectura-Lograda.png)

El diagrama muestra de forma esquemática nuestra arquitectura actualmente desarrollada. Consiste en una orquestación de contenedores, utilizando azure container apps, conectada a una base de datos de PostgreSQL, y apoyada por APIs que se despliegan en Azure Functions. Vamos a analizar cada elemento:

**Region**: Nos limitamos a una sola región debido al uso exclusivo dentro de España. Si la empresa expande al mercado internacional, se puede plantear una arquitectura multi-región.

**Usuario**: Asesor de Several que utiliza la tabla como herramienta de trabajo.

**Entorno Container Apps**: Espacio donde los contenedores están interconectados entre ellos, y permitiendo el escalado horizontal.

**Client**: Front-end de React, contenida en Docker y desplegada con container apps.

**Server**: API para el backend, contenida en una imágen de Docker y desplegada con container apps.

**API Factura**: API para interpretar una factura en pdf o imágen y devolver al client los datos para poblar la tabla.

**API Candela**: API para automatizar la recuperación de datos desde la web de Candela, utilizando el CUPS.

**Actualizar Tabla**: API para automatizar la actualización de la tabla con información pertinente de la base de datos.

**BBDD**: La base de datos de PostgreSQL, levantada en un servidor de Azure.

**Backup**: Copia de seguridad automática realizada por la base de datos. 

**Secretos**: Container Apps tiene la función de guardar secretos para que cuando esa información se requiera, esté encriptada.

**Monitorización**: Analitica de logs y visión de un dashboard del estado de la infraestructura.

**Customer**: Potencial cliente que atrae la vertical de marketing.

**Landing**: Web de wordpress desarrollada por marketing para informar a los potenciales clientes de que ofrece la empresa.

### Arquitectura propuesta para fase final

En una fase mas avanzada del proyecto se puede seguir desarrollando la infraestructura para que sea mas segura y con conexiones mas eficientes. Para lograrlo, la API para actualizar la tabla se volvería una Azure function, agregariamos una ingesta de datos que actualice automáticamente la base de datos con los nuevos precios semanales y se implementaría una red virtual pública y otra privada, permitiendo solo acceso a la segunda desde el client. Un firewall protegería el ingress de nuestra aplicación y un Dominio privado aportaría elegancia a la URL. 

![Alt text](Arquitectura/diagrama-arquitectura-Propuesta.png)


## 3. Infraestructura como código (IaC)

Creación de la infraestructura utilizando Terraform y Teraform Cloud para almacenar el estado de nuestra infraestructura y las variables que queremos encriptar. El proces de la creación de la infraestructura se realizó paso a paso, a medida que avanzaba el proyecto.

Los primeros recursos que creamos en la subscripción de Azure son el grupo de recursos y la base de Datos:

**main.tf**:
´´´terraform {
  cloud {
    organization = "Several-energy"
    workspaces {
      name = "Calculadora-Several"
    }
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.87.0"
    }
  }
}

provider "azurerm" {
  subscription_id = "8981aa87-5078-479f-802f-cf78ed73bdf0"
  features {    
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}


# Grupo de recursos
resource azurerm_resource_group Resource-Group {
  name = local.resource-group-name
  location = local.location
}

# Base de datos
resource "azurerm_postgresql_flexible_server" "pg-flex-server" {
  name                   = var.pg-flex-name
  resource_group_name    = var.resource-group-name
  location               = var.location
  administrator_login    = var.login
  administrator_password = var.password
  storage_mb             = var.storage-mb
  sku_name               = var.sku-name
  zone                   = 1
  
  lifecycle {
    prevent_destroy = true
  }
}
´´´

Con una imagen de Docker vacia podemos crear las container apps. Para evitar repetición excesiva, se crea un módulo para el entorno y uno para la creación. Empecemos por crear el entorno de las container apps. Necesitamos un registro de contenedores, log analytics, container app environment y conexión externa para la base de datos (con dapr):

**Modules/Container-apps-environment/main-cont-app-env.tf**:

```terraform
# Container registry
resource "azurerm_container_registry" "my_containers" {
  name                = var.container_registry_name
  resource_group_name = var.resource-group-name
  location            = var.location
  sku                 = "Basic"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_log_analytics_workspace" "ws-log-analytics" {
  name                = var.log_analytics_workspace_name
  location            = var.location
  resource_group_name = var.resource-group-name
}

# Crea el Environment para las container-apps
resource "azurerm_container_app_environment" "container_env" {
  name                       = var.container_app_environment_name
  location                   = var.location
  resource_group_name        = var.resource-group-name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.ws-log-analytics.id
}

# Conexión dapr para base de datos
resource "azurerm_container_app_environment_dapr_component" "dapr" {
  component_type               = var.dapr_component_type
  container_app_environment_id = azurerm_container_app_environment.container_env.id
  name                         = var.dapr_component_name
  version = "v1"
}
```


**Modules/Container-apps-environment/output-cont-app-env.tf**:

```terraform
output "container-registry-prin-ID" {
  value = azurerm_container_registry.my_containers.identity[0].principal_id
}

# container_app_environment_id
output "container_app_environment_id" {
  value = azurerm_container_app_environment.container_env.id
}

# dapr_app_id
output "dapr_app_id" {
  value = azurerm_container_app_environment_dapr_component.dapr.name
}

```

Ahora que tenemos el entorno configurado, podemos crear los contenedores vacios. Los poblaremos con código en nuestra pipeline mas adelante:

**Modules/Container-apps/main-cont-app.tf**:

```terraform
resource "azurerm_container_app" "container_app" {
  for_each = var.container_app

  container_app_environment_id = var.container_app_environment_id
  name                         = each.value.name
  resource_group_name          = var.resource-group-name
  revision_mode                = "Single"

  template {
    max_replicas    = each.value.template.max_replicas
    min_replicas    = each.value.template.min_replicas

    container {
      image   = each.value.template.image
      name    = each.value.template.name
      cpu     = each.value.template.cpu
      memory  = "${each.value.template.memory_gigaBytes}Gi"

      dynamic "env" {
        for_each = each.value.template.env

        content {
          name        = env.value["name"]
          secret_name = env.value["secret_name"]
        }
      }
    }

    http_scale_rule {
      name = each.value.http_scale_rule.name
      concurrent_requests = each.value.http_scale_rule.concurrent_requests
    }
  }

  dapr {
    app_id = var.dapr_app_id
  }

  ingress {
    target_port                = each.value.ingress.target_port
    allow_insecure_connections = each.value.ingress.allow_insecure_connections
    external_enabled           = each.value.ingress.external_enabled
    transport                  = "http"

    traffic_weight {
      percentage = 100
      latest_revision = true
      }
  }

  dynamic "secret" {
    for_each = each.value.secret

    content {
      name  = secret.value["name"]
      value = secret.value["sec-value"]
    }
  }

  identity {
    type = "SystemAssigned"
  }

  timeouts {
    create = "20m" # Set the create timeout to 20 minutes
  }
}
```

**Modules/Container-apps/variables-cont-app.tf**

```terraform
variable "container_app_environment_id" {
  type        = string
  description = "(Required) ID del entorno donde se desplegará."
  nullable    = false
}

variable "location" {
  type = string
}

variable "resource-group-name" {
  type        = string
  description = "(Required) The name of the resource group in which the resources will be created."
  nullable    = false
}

variable "dapr_app_id" {
  type        = string
  description = "(Required) ID del dapr binding con el que se conecta."
  nullable    = false
}

variable "container_app" {
  default     = {}
  description = "(Optional) The Dapr component to deploy."
  nullable    = false

  type = map(object({
    name = string,

    template = object({
      max_replicas    = optional(number),
      min_replicas    = optional(number),

      image             = string,
      name              = string,
      cpu               = optional(number),
      memory_gigaBytes  = optional(number),

      env = optional(list(object({
        name        = string,
        secret_name = string,
      })))
    }),

    http_scale_rule = optional(object({
      name = string
      concurrent_requests = number
    }))

    ingress = optional(object({
      target_port                = number,
      allow_insecure_connections = optional(bool, false),
      external_enabled           = optional(bool, false),
    })),

    secret = optional(list(object({
      name  = string,
      sec-value = string,
    }))),
  }))
}
```

**Modules/cont-apps/output.tf**:

```terraform
output "url" {
  value = [ for name, container in azurerm_container_app.container_app : "https://${try(container.ingress[0].fqdn, "")}" if can(container.ingress[0].fqdn) ]
}
```

Ya tenemos nuestros módulos. Ahora podemos ejecutarlos para conseguir nuestra arquitectura:

**main.tf**:

```terraform
# Creación del entorno para Container Apps
module "container_app_environment" {
  source = "./Modules/Container-apps-environment"
  location = local.location
  resource-group-name = local.resource-group-name
  container_registry_name = local.container_registry_name
  container_app_environment_name = local.container_app_environment_name_dev
  dapr_component_type = local.dapr_component_type
  dapr_component_name = local.dapr_component_name
}

# Creación de la API candela
module "Container_app_candela_dev" {
  source = "./Modules/Container-apps"
  location = local.location
  resource-group-name = local.resource-group-name
  container_app_environment_id = module.container_app_environment.container_app_environment_id
  dapr_app_id = module.container_app_environment.dapr_app_id
  container_app = local.container_app_candela_dev
  depends_on = [ module.container_app_environment ]
}

# Creación de la API invoice
module "Container_app_invoice_dev" {
  source = "./Modules/Container-apps"
  location = local.location
  resource-group-name = local.resource-group-name
  container_app_environment_id = module.container_app_environment.container_app_environment_id
  dapr_app_id = module.container_app_environment.dapr_app_id
  container_app = local.container_app_invoice_dev
  depends_on = [ module.container_app_environment ]
}

# Creación de la API invoice
module "Container_app_update_dev" {
  source = "./Modules/Container-apps"
  location = local.location
  resource-group-name = local.resource-group-name
  container_app_environment_id = module.container_app_environment.container_app_environment_id
  dapr_app_id = module.container_app_environment.dapr_app_id
  container_app = local.container_app_update_dev
  depends_on = [ module.container_app_environment ]
}

# Creación de server
module "Container_app_server_dev" {
  source = "./Modules/Container-apps"
  location = local.location
  resource-group-name = local.resource-group-name
  container_app_environment_id = module.container_app_environment.container_app_environment_id
  dapr_app_id = module.container_app_environment.dapr_app_id
  container_app = local.container_app_server_dev
  depends_on = [ module.container_app_environment, module.database ]
}

# Creación de client
module "Container_app_client_dev" {
  source = "./Modules/Container-apps"
  location = local.location
  resource-group-name = local.resource-group-name
  container_app_environment_id = module.container_app_environment.container_app_environment_id
  dapr_app_id = module.container_app_environment.dapr_app_id
  container_app = local.container_app_client_dev
  depends_on = [ module.container_app_environment, module.Container_app_candela_dev, module.Container_app_invoice_dev, module.Container_app_server_dev ]
}
```

Aprovechamos los outputs de nuestros primeros cuatro contenedores para designar al client las URL mediante variables de entorno.




## 4. Despliegue e implementación contínuos (CI/CD)



## 5. Monitorización



## 6. Memoria de proyecto



Submódulo para el desarrollo de la parte de cloud &amp; DevOps del proyecto "Desafio-theBridge-sep23-grupo3"

## Variables de entorno:

Documentación: https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings?tabs=kudu%2Cdotnet

## Container apps

**Bye bye Azure Functions, Hello Azure Container Apps: Introduction**

https://endjin.com/blog/2022/09/bye-bye-azure-functions-hello-azure-container-apps-part-1-introduction

**Azure container apps pricing**

https://azure.microsoft.com/en-us/pricing/details/container-apps/

**CORS**

https://learn.microsoft.com/en-us/azure/container-apps/cors?tabs=yaml&pivots=azure-cli

## Creación de pipeline CI/CD

### paso 1 - Requisitos

**1.1 - Creación de un "container registry"**

**1.2 - Configurar sonarQube para sanetización del código**

Documentación SonarQube: https://docs.sonarsource.com/sonarqube/10.3/devops-platform-integration/azure-devops-integration/

### Paso 2 - Pipeline artefacto:

Crea nueva pipeline desde un repositorio de github. Una vez seleccionado el repositorio deseado, seleccionamos la opción de "**Docker** *Build and push an image to azure container registry*":

![Docker Build and push an image to azure container registry](img/Screenshot_1-Pipeline-github-01.png)

Ahora seleccionamos la suscripción donde tenemos nuestro registro de contenedores y rellenamos con el nombre de la imagen que vamos a crear y la ubicación del Dockerfile dentro de nuestro repositorio:

![Configurar imagen](img/Screenshot_2-Pipeline-github-02.png)

 Revisamos que la información del YAML es correcta y agregaremos tareas de SonarQube para que Ciberseguridad pueda sanetizar el código.



Finalizamos

### Paso 3 - Release Pipeline de desarrollo:

En despliegues, vamos a crear una nueva pipeline de despliegue y elegimos la plantilla de *Azure App Service Deployment*

![Azure App Service Deployment](img/Screenshot_3-Pipeline-dev-01.png)

Agrgaremos el artefacto que creamos en la pipeline con github y activamos el trigger de implementación continua:

![Artefacto y tareas](img/Screenshot_4-Pipeline-dev-02.png)

Seguidamente modificamos las condiciones de pre-despliegue para que se lance solo con una nueva version de nuestra imagen:

![Pre deploy conditions](img/Screenshot_5-Pipeline-dev-03.png)

Antes de preparar las tareas, vamos a preparar unas cuantas variables:

- app-service-plan-name: Nombre del *service plan* que vamos a crear
- app-service-name: Nombre de la *web app* que estamos creando
- container-registry: El registro donde se encuentra la imagen del contenedor
- container-image-name: El nombre de la imagen del contenedor
- resource-group-name: El grupo de recursos donde estamos trabajando

![Variables](img/Screenshot_6-Pipeline-dev-variables.png)

Ahora nos concentramos en las tareas. En primer lugar rellenamos los parámetros requeridos del escenario *stage 1*, asegurandonos que elegimos el tipo *Web App for Containers (Linux)*:

![parametros para la Web App](img/Screenshot_7-Pipeline-dev-tasks-01.png)

A continuación modificaremos el agente de ejecución para que utilice ubuntu:

![Agent Ubuntu](img/Screenshot_8-Pipeline-dev-tasks-02.png)

Es hora de crear nuestro *app service plan*. Para ello creamos una tarea de *Azure CLI* e introducimos el comando siguiente:

```
az appservice plan create -n $(app-service-plan-name) -g $(resource-group-name) --sku F1 --is-linux
```

![Azure CLI](img/Screenshot_9-Pipeline-dev-tasks-03.png)
![Crear service plan](img/Screenshot_10-Pipeline-dev-tasks-04.png)

Ahora toca crear nuestro App service utilizando otra tarea de *Azure CLI* y el siguiente comando:

```
az webapp create -n $(app-service-name) -p $(app-service-plan-name) -g $(resource-group-name) -i $(container-registry)/$(container-image-name) --public-network-access Enabled
```

![Crear App Service](img/Screenshot_11-Pipeline-dev-tasks-05.png)

Seguidamente modificaremos el Deploy Azure App Service para introducir el puerto por el que se expone la imagen en el apartado *Application and Configuration Settings*:

![Puerto expuesto](img/Screenshot_12-Pipeline-dev-tasks-06.png)

FALTAN LOS TESTS

## MEMORIA

### 08 de enero, 2024

- Primera reunión con Cliente
- Crear usuarios invitados y grupos de seguridad en suscripción de azure para Data, Ciber y Fullstack
- Gestionar permisos sobre el grupo de recursos para cada grupo de seguridad
- Reunión con Ciber: 
    - Decisión de crear una imágen de Docker securizada de alpine 3.19 como base para los despliegues
    - Pentest de máquina hola, mundo
- Creación de servidor para base de datos PostgreSQL

### 09 de enero, 2024

- Creación de container registry
- Creación de pipeline para creación de imágenes de client y server
- Comienza pipeline de despliegue para app service de client y server pre-producción
- Reunión con Data:
    - Propuesta de Api Centers para api de actualización de la tabla con Azure Functions
- Reunión con Ciber:
    - Backup de la base de datos
    - Logs para ciber

### 10 de enero, 2024

- Reunión con Ciber:
    - Intento de despliegue automático de sonarqube en pipeline. Conclusión: ejecución en local no tiene acceso a Azure Pipelines. Ciber busca solución con repo en local.
    - Plantilla de imágen Iron-Alpine encontrada. Test de la imágen, todo funcional.
- Reunión con Data:
    - Api para actualización automática de la tabla. La Api solo actualizará campos complejos. Los campos sencillos de la tabla se manejan desde front end.
    - Necesidad de Hostear Api para el scrapping de Candela
- Bloqueo de pipeline de despliegue por exceso de intentos. Desbloqueo en 48 horas. Solución temporal: ejecución manual del despliegue a petición de FULLSTACK.


### 11 de enero, 2024

- Reunión con Ciber:
    - Recibido documento hardening-v3. Implementados los cambios en el Dockerfile listo para desplegar.
    - Crear firewall y VPC publica y privada.
- Continuación con host de API scraping

### 12 de enero, 2024

- ALERTA! Gastos de Firewall desorbitados. Recurso eliminado.
    - Descartado el uso de firewall en la fase inicial.
    - Proponer a ciber un estudio teórico para que la empresa lo valore en el futuro.
- Pipeline para API de webscrapping candela                                                                         POR HACER
- Variables de entorno para API webscrapping                                                                        POR HACER
- Reunión con Data:
    - Colaborar para completar API de webscrapping (Container Apps)                                                 POR HACER
    - Desplegar endpoints (Cloud functions vs container apps)                                                       POR HACER
- Reunión con Fullstack:
    - Hosting API de guardado con API centers (container apps)                                                      POR HACER
    - Preparar variables de entorno y secretos                                                                      POR HACER
    - Prueba versión 1.0 de app estable (Client donde? server en container apps)                                    POR HACER

### 13 de enero, 2024

- Completar pipeline de CI/CD para Client y Server                                                                  POR HACER
- Reunión con Data:
    - Desplegar APIs para la tabla                                                                                  POR HACER
- Diseño de esquema Arquitectura final                                                                              POR HACER


### --------------PERSONAL----------------
- Documentarme sobre uso de variables de entorno y secretos en azure
- Monitorización (MARKETING? CIBER?)
- nota: CodeQL para anialisis de codigo mientras se desarrolla