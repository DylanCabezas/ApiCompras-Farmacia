import boto3
import os

glue = boto3.client('glue')

CRAWLER_NAME = os.environ.get('GLUE_CRAWLER_NAME')

def handler(event, context):
    print("🧪 Evento recibido:", event)

    try:
        response = glue.start_crawler(Name=CRAWLER_NAME)
        print("✅ Crawler ejecutado:", CRAWLER_NAME)
        return {
            "statusCode": 200,
            "body": f"Crawler {CRAWLER_NAME} started successfully"
        }
    except glue.exceptions.CrawlerRunningException:
        print("⚠️ El crawler ya está corriendo. Ignorando...")
        return {
            "statusCode": 200,
            "body": f"Crawler {CRAWLER_NAME} ya está en ejecución"
        }
    except Exception as e:
        print("❌ Error:", str(e))
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
