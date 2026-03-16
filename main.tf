terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

provider "local" {}

resource "local_file" "servidor1" {
  filename = "${path.module}/infraestructura/servidor1.txt"
  content  = "Servidor 1 creado con Terraform"
}

resource "local_file" "servidor2" {
  filename = "${path.module}/infraestructura/servidor2.txt"
  content  = "Servidor 2 creado con Terraform"
}

resource "local_file" "red" {
  filename = "${path.module}/infraestructura/red.txt"
  content  = "Red virtual creada con Terraform"
}

feature-Bricio
# --- Contribución de Bricio ---

resource "local_file" "backup_storage" {
  filename = "${path.module}/infraestructura/backup_s3.txt"
  content  = "Bucket S3 para backups creado por Bricio. Estado: Seguro (Acceso Privado)"
}

resource "local_file" "politica_seguridad" {
  filename = "${path.module}/infraestructura/seguridad_red.txt"
  content  = "Politicas de ciberseguridad aplicadas: Public Access Block activo."

# Nuevo recurso agregado para la red.
resource "local_file" "subred" {
  filename = "${path.module}/infraestructura/subred.txt"
  content  = "Subred privada creada para servicios internos"
main
}

# Recurso de monitoreo - métricas del sistema hospitalario
resource "local_file" "config_monitoreo" {
  filename = "${path.module}/infraestructura/monitoreo.txt"
  content  = "Configuración de monitoreo: métricas de CPU, memoria y disco para servidores hospitalarios"
}

# Recurso de alertas - notificaciones del sistema
resource "local_file" "alertas" {
  filename = "${path.module}/infraestructura/alertas.txt"
  content  = "Sistema de alertas configurado para umbrales críticos de disponibilidad"
}