import boto3
import json
from decimal import Decimal
from src.validarToken import validar_token

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('t_compras_dev')

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Tipo no serializable: {type(obj)}")

def handler(event, context):
    try:
        headers = event.get('headers', {})
        payload = validar_token(headers)

        tenant_id = payload['tenant_id']
        alumno_id = payload['alumno_id']

        response = tabla.scan(
            FilterExpression='tenant_id = :t AND alumno_id = :a',
            ExpressionAttributeValues={
                ':t': tenant_id,
                ':a': alumno_id
            }
        )

        compras = response.get("Items", [])

        return {
            'statusCode': 200,
            'body': json.dumps(compras, default=decimal_serializer)
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
