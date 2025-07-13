API Compras - Farmacia

Este microservicio permite registrar y listar compras en una farmacia, usando AWS Lambda, DynamoDB, S3, Glue y Swagger UI.

🚀 Instrucciones para clonar y desplegar

Clona este repositorio:

git clone https://github.com/DylanCabezas/ApiCompras-Farmacia.git
cd ApiCompras-Farmacia

Instala Serverless Framework y dependencias:

npm install -g serverless

Reemplaza en serverless.yml tu propio ARN del LabRole si es necesario:

iam:
  role: arn:aws:iam::<TU_ID>:role/LabRole  # <-- reemplazar aquí

Despliega en el entorno deseado:

sls deploy --stage dev
sls deploy --stage prod
sls deploy --stage test

📦 Funcionalidad por Lambda

Función

Endpoint

Descripción

RegistrarCompra

POST /compras/registrar

Registra una compra (requiere token)

ListarCompras

GET /compras/listar

Lista las compras del usuario autenticado

ActualizarCompras

Stream desde DynamoDB

Guarda cada compra como JSON en S3

EjecutarCrawler

Trigger S3 → Glue

Activa Glue crawler al subir un JSON a S3

Docs

GET /docs

Sirve el archivo OpenAPI YAML directamente

DocsUI

GET /docs-ui

Muestra Swagger UI ya listo sin necesidad de copiar nada

🌐 Documentación Swagger

Swagger YAML: /docs

Swagger UI visual: /docs-ui

Puedes consultar, probar y explorar la API directamente en /docs-ui sin necesidad de copiar el YAML manualmente.

🧪 Cómo probar

Registrar usuario en el microservicio api-usuarios

Hacer login en /login con:

{
  "tenant_id": "Inkafarma",
  "user_id": "user1@gmail.com",
  "password": "password"
}

Copia el token recibido y úsalo en Postman:

En la pestaña Authorization elige Bearer Token

Pega el token

Prueba los endpoints /compras/registrar y /compras/listar

📝 Reemplazos que debes hacer

Cambiar tu ARN de LabRole en serverless.yml

Crear los buckets manualmente o dejar que Serverless los cree (por stage)

Asegúrate de tener un crawler por stage en Glue con nombre compras-crawler-dev, compras-crawler-prod, compras-crawler-test 

Verifica que el nombre del bucket (farmacia-compras-dc-${sls:stage}) coincida con el que estás usando en Glue y Lambda

✅ Requisitos previos

AWS CLI configurado (aws configure)

Cuenta de AWS Academy o IAM con permisos para:

Lambda

API Gateway

DynamoDB

Glue

S3

