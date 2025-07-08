import boto3, json
from src.validarToken import validar_token

dynamo = boto3.resource('dynamodb')
tabla = dynamo.Table('t_compras-dev')  # usar ${stage} si deseas dinámico

def handler(event, context):
    try:
        headers = event['headers']
        payload = validar_token(headers)

        resp = tabla.query(
            KeyConditionExpression="tenant_id = :t AND alumno_id = :a",
            ExpressionAttributeValues={
                ":t": payload['tenant_id'],
                ":a": payload['alumno_id']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(resp.get("Items", []))
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
