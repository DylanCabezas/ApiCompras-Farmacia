import boto3, uuid, json, datetime
from src.validarToken import validar_token

dynamo = boto3.resource('dynamodb')
tabla = dynamo.Table('t_compras-dev')  # usar ${stage} si deseas dinámico

def handler(event, context):
    try:
        headers = event['headers']
        data = json.loads(event['body'])
        payload = validar_token(headers)

        compra_id = str(uuid.uuid4())
        fecha = datetime.datetime.now().isoformat()

        total = sum(p['precio'] * p['cantidad'] for p in data['productos'])

        item = {
            'tenant_id': payload['tenant_id'],
            'alumno_id': payload['alumno_id'],
            'compra_id': compra_id,
            'fecha': fecha,
            'productos': data['productos'],
            'total': total
        }

        tabla.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Compra registrada', 'data': item})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
