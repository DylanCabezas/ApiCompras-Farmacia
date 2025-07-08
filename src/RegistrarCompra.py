import boto3
import uuid
import json
import datetime
from decimal import Decimal
from src.validarToken import validar_token

# Recurso DynamoDB
dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('t_compras_dev')  # Cambia a tu stage si es necesario

def handler(event, context):
    try:
        # Leer body del evento
        body = event['body']
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        # Obtener y validar token
        headers = event.get('headers', {})
        payload = validar_token(headers)  # ← valida el token UUID desde DynamoDB

        # Validar campo obligatorio
        if 'productos' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Falta el campo productos'})
            }

        productos = data['productos']
        productos_decimal = []
        total = Decimal("0.0")

        # Convertir a Decimal y calcular total
        for p in productos:
            precio = Decimal(str(p['precio']))
            cantidad = Decimal(str(p['cantidad']))
            subtotal = precio * cantidad
            total += subtotal

            productos_decimal.append({
                'codigo': p['codigo'],
                'nombre': p['nombre'],
                'precio': precio,
                'cantidad': cantidad
            })

        # Crear objeto compra
        compra_id = str(uuid.uuid4())
        fecha = datetime.datetime.utcnow().isoformat()

        item = {
            'tenant_id': payload['tenant_id'],
            'alumno_id': payload['alumno_id'],
            'compra_id': compra_id,
            'fecha': fecha,
            'productos': productos_decimal,
            'total': total
        }

        # Guardar en DynamoDB
        tabla.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Compra registrada',
                'data': {
                    'tenant_id': item['tenant_id'],
                    'alumno_id': item['alumno_id'],
                    'compra_id': item['compra_id'],
                    'fecha': item['fecha'],
                    'productos': [
                        {
                            'codigo': p['codigo'],
                            'nombre': p['nombre'],
                            'precio': float(p['precio']),
                            'cantidad': float(p['cantidad'])
                        } for p in productos_decimal
                    ],
                    'total': float(total)
                }
            })
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
