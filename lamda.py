import csv
import io
import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Reemplaza con los nombres exactos de los buckets y la ruta del CSV en S3
    input_bucket = 'bld-tseed.workshop-input-semillero2026-q4-d'
    input_key = 'JuanGrajales/users_dataset_100.csv'
    
    output_bucket = 'bld-tseed-workshop-output-semillero-2026-q4-d'
    output_folder = 'JuanGrajales'

    # 2. Leer el archivo CSV desde S3
    response = s3.get_object(Bucket=input_bucket, Key=input_key)
    csv_content = response['Body'].read().decode('utf-8')
    
    # 3. Convertir cada fila en un diccionario y subirla como JSON individual
    reader = csv.DictReader(io.StringIO(csv_content))
    count = 0
    
    for idx, row in enumerate(reader, start=1):
        json_key = f"{output_folder}/fila_{idx}.json"
        s3.put_object(
            Bucket=output_bucket,
            Key=json_key,
            Body=json.dumps(row, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        count += 1

    return {
        'statusCode': 200,
        'body': json.dumps(f'Proceso exitoso: se subieron {count} archivos JSON a {output_folder}/')
    }
