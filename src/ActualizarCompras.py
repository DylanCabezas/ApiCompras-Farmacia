import boto3
import os
import json
from decimal import Decimal

s3 = boto3.client("s3")
bucket_name = os.environ['S3_BUCKET']

def deserialize(attr):
    tipo = list(attr.keys())[0]
    valor = attr[tipo]
    if tipo == 'S':
        return valor
    elif tipo == 'N':
        return Decimal(valor)
    elif tipo == 'M':
        return {k: deserialize(v) for k, v in valor.items()}
    elif tipo == 'L':
        return [deserialize(i) for i in valor]
    elif tipo == 'BOOL':
        return bool(valor)
    else:
        return valor

def handler(event, context):
    try:
        for record in event['Records']:
            if record['eventName'] not in ['INSERT', 'MODIFY']:
                continue

            new_image = record['dynamodb']['NewImage']
            data = {k: deserialize(v) for k, v in new_image.items()}

            tenant_id = data['tenant_id']
            alumno_id = data['alumno_id']
            compra_id = data['compra_id']
            productos = data.get('productos', [])

            for i, producto in enumerate(productos):
                producto['tenant_id'] = tenant_id
                producto['alumno_id'] = alumno_id
                producto['compra_id'] = compra_id
                producto['producto_index'] = i  # Para evitar sobrescribir

                def decimal_serializer(o):
                    if isinstance(o, Decimal):
                        return float(o)
                    raise TypeError

                s3_key = f"compras/{tenant_id}/{alumno_id}/{compra_id}_{i}.json"

                s3.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=json.dumps(producto, default=decimal_serializer),
                    ContentType='application/json'
                )

                print(f"✅ Producto guardado en s3://{bucket_name}/{s3_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Productos procesados y guardados en S3'})
        }

    except Exception as e:
        print("❌ Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
