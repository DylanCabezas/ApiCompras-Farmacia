import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
tokens_table = dynamodb.Table(os.environ['TOKENS_TABLE'])

def validar_token(headers):
    token = headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        raise Exception("Falta token")

    response = tokens_table.get_item(Key={'token': token})
    item = response.get("Item")

    if not item:
        raise Exception("Token inválido")

    # Validar tiempo de expiración
    expires_str = item["expires"]
    expires_dt = datetime.strptime(expires_str, "%Y-%m-%dT%H:%M:%SZ")
    if expires_dt < datetime.utcnow():
        raise Exception("Token expirado")

    # Retornar datos del usuario autenticado
    return {
        "tenant_id": item["tenant_id"],
        "alumno_id": item["user_id"]
    }
