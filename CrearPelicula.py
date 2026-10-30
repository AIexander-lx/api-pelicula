import boto3
import uuid
import os
import json


def imprimir_log(tipo, log_datos):
    # Formato json de log estándar (una sola línea para que CloudWatch lo indexe como JSON)
    log = {
        "tipo": tipo,           # "INFO" o "ERROR"
        "log_datos": log_datos
    }
    print(json.dumps(log, ensure_ascii=False, default=str))


def lambda_handler(event, context):
    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de ejecución correcta
        imprimir_log("INFO", pelicula)

        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log de error
        imprimir_log("ERROR", {
            "error_tipo": type(e).__name__,
            "error_mensaje": str(e),
            "entrada": event.get('body') if isinstance(event, dict) else str(event)
        })

        # Salida (json)
        return {
            'statusCode': 500,
            'error_tipo': type(e).__name__,
            'error_mensaje': str(e)
        }
