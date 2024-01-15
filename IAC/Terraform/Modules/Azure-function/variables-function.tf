variable "resource-group-name" {
  description = "nombre del grupo de recursos"
  type        = string
}

variable "location" {
  description = "Region de la función"
  type        = string
}

variable "storage-accountname" {
  description = "Nombre del almacenamiento"
  type        = string
}

variable "function-plan" {
  description = "nombre del plan para la función"
  type        = string  
}

variable "application-type" {
  description = "Lenguaje que usa la aplicación"
  type        = string  
}

variable "function-name" {
  description = "nombre de la función"
  type        = string
}


variable "source-code" {
  description = "directorio del .zip del codigo fuente"
  type        = string
}