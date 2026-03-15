# infraestructura-hospital-cloud
Proyecto de infraestructura cloud hospitalaria
# Infraestructura Hospital Cloud

Proyecto académico de cómputo en la nube.

Este repositorio contiene la infraestructura del sistema hospitalario
implementada con herramientas de infraestructura como código.

## Integrantes del equipo

-  Bricio Maceda Muñoz ........
-  Julio Alberto Ortiz Pacheco
-  Mendoza Contreras Azucena
-  Alexis Ortega Dehesa
-  Raúl Hernández Hernández

## Herramientas utilizadas

- Terraform
- Visual Studio Code
- Git
- Sistema operativo Windows (ya que los proveedores incluyen ejecutables para Windows)

## Archivos Incluidos 

| Archivo                         | Descripción                                              |
| ------------------------------- | -------------------------------------------------------- |
| `main.tf`                       | Archivo principal con la definición de infraestructura.  |
| `terraform.tfstate`             | Estado de Terraform, registra la infraestructura creada. |
| `infraestructura/servidor1.txt` | Detalles del servidor 1.                                 |
| `infraestructura/servidor2.txt` | Detalles del servidor 2.                                 |
| `infraestructura/red.txt`       | Configuración de red local.                              |
| `infraestructura/README.md`     | Documentación adicional del proyecto.                    |
| `.terraform.lock.hcl`           | Bloqueo de versiones de proveedores de Terraform.        |
| `.terraform/providers/...`      | Ejecutables de los proveedores de Terraform.             |


Estos archivos representan servidores y una red simulada.

## Pasos para ejecutar el proyecto

1. Clonar el repositorio

git clone (URL DEL REPOSITORIO)

2. Entrar a la carpeta del proyecto

cd terraform-proyecto

3. Inicializar Terraform

terraform init:
Descarga los proveedores necesarios y prepara el proyecto.

4. Ver el plan de infraestructura

terraform plan :
Muestra qué recursos se crearán.
Permite verificar antes de aplicar.

5. Crear la infraestructura

terraform apply:
Terraform pedirá confirmación. Escribe yes y presiona Enter.

Esto creará todos los recursos definidos en main.tf y los archivos .txt en infraestructura/.

6. Verificar la infraestructura creada

terraform show:
Muestra todos los recursos y archivos creados por Terraform.

Luego de ejecutar estos comandos, Terraform creará la infraestructura definida en el archivo main.tf.
