import boto3
import json
from decimal import Decimal

s3 = boto3.client("s3")
bucket_name = "farmacia-compras"  # nombre real de tu bucket

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

            s3_key = f"compras/{tenant_id}/{alumno_id}/{compra_id}.json"

            def decimal_serializer(o):
                if isinstance(o, Decimal):
                    return float(o)
                raise TypeError

            s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=json.dumps(data, default=decimal_serializer),
                ContentType='application/json'
            )

            print(f"✅ Guardado en: s3://{bucket_name}/{s3_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Cambios procesados'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
