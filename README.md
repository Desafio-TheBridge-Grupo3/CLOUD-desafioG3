# CLOUD-desafioG3
Submódulo para el desarrollo de la parte de cloud &amp; DevOps del proyecto "Desafio-theBridge-sep23-grupo3"

## Variables de entorno:

Documentación: https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings?tabs=kudu%2Cdotnet

## Power BI en web apps

https://www.youtube.com/watch?v=XSAHwE21Buk

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
    - Colaborar para completar API de webscrapping                                                                  POR HACER
    - Desplegar endpoints                                                                                           POR HACER
- Reunión con Fullstack:
    - Hosting API de guardado con API centers                                                                       POR HACER
    - Preparar variables de entorno y secretos                                                                      POR HACER
    - Prueba versión 1.0 de app estable                                                                             POR HACER

### 13 de enero, 2024

- Completar pipeline de CI/CD para Client y Server                                                                  POR HACER
- Reunión con Ciber:
    - Preparar VPC, firewalls y recursos necesarios para hacerlos funcionales                                       POR HACER
- Reunión con Data:
    - Desplegar APIs para la tabla                                                                                  POR HACER
- Diseño de esquema Arquitectura final                                                                              POR HACER


### --------------PERSONAL----------------
- Documentarme sobre uso de variables de entorno y secretos en azure
- Monitorización (MARKETING? CIBER?)
- nota: CodeQL para anialisis de codigo mientras se desarrolla