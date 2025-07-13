import os

def handler(event, context):
    try:
        ruta = os.path.join(os.path.dirname(__file__), 'openapi.yaml')
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/yaml'
            },
            'body': contenido
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al cargar la documentación: {str(e)}'
        }
