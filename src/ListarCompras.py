import boto3
import json
from src.validarToken import validar_token

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('t_compras_dev')  # Ajusta según tu stage

def handler(event, context):
    try:
        # Validar token
        headers = event.get('headers', {})
        payload = validar_token(headers)

        tenant_id = payload['tenant_id']
        alumno_id = payload['alumno_id']

        # Buscar todas las compras de este usuario
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
            'body': json.dumps(compras)
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
