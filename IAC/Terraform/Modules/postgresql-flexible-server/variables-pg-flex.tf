variable "resource-group-name" {
  description = "nombre del grupo de recursos"
  type        = string
}

variable "location" {
  description = "Region de la función"
  type        = string
}

variable "pg-flex-name" {
  description = "PostgreSQL flexible server name"
  type = string
}