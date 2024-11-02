from google.cloud import bigquery
from google.cloud import storage  
from datetime import datetime

def registrar_archivos_procesados(bucket_name: str, prefix: str, project_id: str, dataset: str) -> None:
    client = bigquery.Client()
    storage_client = storage.Client() 
    table_id = f"{project_id}.{dataset}.archivos_procesados"

    # Listar archivos en el bucket GCS con el prefijo especificado
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    archivos = [blob.name for blob in blobs] 

    rows_to_insert = []
    for nombre_archivo in archivos:
        rows_to_insert.append({
            "nombre_archivo": nombre_archivo,
            "fecha_carga": datetime.now()
        })

    # Insertar los archivos en la tabla de BigQuery
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print(f"Error al insertar los archivos procesados: {errors}")
    else:
        print("Archivos registrados exitosamente.")