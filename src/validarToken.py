import boto3
import jwt

dynamo = boto3.resource('dynamodb')
tabla = dynamo.Table('t_tokens_acceso-dev')  # usar ${stage} si deseas dinámico

SECRET = "secreto_compartido"

def validar_token(headers):
    token = headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise Exception("Falta token")
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    return payload  # debe incluir tenant_id, alumno_id
