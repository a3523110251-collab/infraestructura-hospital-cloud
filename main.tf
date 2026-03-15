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
tags = {
  Name = "infraestructura-hospital"
  Proyecto = "cloud-hospital"
  Responsable = "Beto"
}
