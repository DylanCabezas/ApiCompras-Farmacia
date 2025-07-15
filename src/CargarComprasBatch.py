import boto3
import json
import os
import uuid
from datetime import datetime
from decimal import Decimal

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
COMPRAS_TABLE = os.environ["COMPRAS_TABLE"]

def handler(event, context):
    print("🚀 Evento recibido:", event)

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key    = record['s3']['object']['key']

        print(f"📥 Leyendo archivo desde: s3://{bucket}/{key}")

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            contenido = response['Body'].read().decode('utf-8')
            compras = json.loads(contenido)

            tabla = dynamodb.Table(COMPRAS_TABLE)
            total_insertadas = 0

            for compra in compras:
                tenant_id = compra['tenant_id']
                alumno_id = compra['alumno_id']
                productos = compra['productos']

                # Calcular total
                total = sum(p['precio'] * p['cantidad'] for p in productos)

                item = {
                    'tenant_id': tenant_id,
                    'alumno_id': alumno_id,
                    'compra_id': str(uuid.uuid4()),
                    'fecha': datetime.utcnow().isoformat(),
                    'productos': json.loads(json.dumps(productos), parse_float=Decimal),
                    'total': Decimal(str(total))
                }

                tabla.put_item(Item=item)
                total_insertadas += 1

            print(f"✅ Compras insertadas: {total_insertadas}")

        except Exception as e:
            print("❌ Error procesando archivo:", str(e))
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Carga exitosa de compras desde archivo"})
    }
