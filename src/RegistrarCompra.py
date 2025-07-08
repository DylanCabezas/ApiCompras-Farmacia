import boto3
import uuid
import json
import datetime
from src.validarToken import validar_token

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('t_compras-dev')  # Cambia el nombre si usas otro stage

def handler(event, context):
    try:
        # Leer el body
        body = event['body']
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        # Leer headers y validar token
        headers = event.get('headers', {})
        payload = validar_token(headers)  # Devuelve tenant_id y alumno_id

        # Validar estructura del body
        if 'productos' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Falta campo productos'})
            }

        productos = data['productos']
        total = sum(p['precio'] * p['cantidad'] for p in productos)

        # Crear objeto compra
        compra_id = str(uuid.uuid4())
        fecha = datetime.datetime.utcnow().isoformat()

        item = {
            'tenant_id': payload['tenant_id'],
            'alumno_id': payload['alumno_id'],
            'compra_id': compra_id,
            'fecha': fecha,
            'productos': productos,
            'total': total
        }

        # Guardar en DynamoDB
        tabla.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Compra registrada',
                'data': item
            })
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
