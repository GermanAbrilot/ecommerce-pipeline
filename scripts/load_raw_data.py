import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv(encoding="utf-8")

# Configuración de conexión leyendo del .env o usando fallbacks
DB_USER = os.getenv("POSTGRES_USER", "data_engineer")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "data_password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce_dw")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    """Crea y retorna el motor de conexión a SQLAlchemy."""
    return create_engine(DATABASE_URL)

def create_raw_schema(engine):
    """Garantiza la existencia del esquema 'raw' en el Data Warehouse."""
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    print("Schema 'raw' verificado/creado con éxito.")

def ingest_csv_to_raw(file_name, table_name, engine, chunk_size=50000):
    """Lee un CSV masivo por lotes y lo carga en la tabla del esquema raw protegiendo la RAM."""
    file_path = os.path.join("data", file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe.")
        return

    print(f"Iniciando ingesta masiva de '{file_name}' en 'raw.{table_name}'...")
    
    try:
        first_chunk = True
        # Leer el CSV en bloques
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            
            # Agregar columna de auditoría/trazabilidad al lote actual
            chunk["_ingested_at"] = datetime.now()

            # El primer lote reemplaza la tabla (limpia datos viejos), los siguientes hacen append
            mode = "replace" if first_chunk else "append"
            
            chunk.to_sql(
                name=table_name,
                con=engine,
                schema="raw",
                if_exists=mode,
                index=False
            )
            
            first_chunk = False
            print(f"Lote procesado para la tabla 'raw.{table_name}'...")

        print(f"Tabla 'raw.{table_name}' ingestada correctamente por completo.")
        
    except Exception as e:
        print(f"Error crítico al procesar {file_name}: {e}")
        raise

def main():
    print("Iniciando proceso de ingesta masiva en la Capa RAW...")
    engine = get_engine()
    create_raw_schema(engine)

    # Mapeo de archivos CSV a tablas objetivo
    files_to_ingest = [
        ("raw_customers.csv", "customers"),
        ("raw_products.csv", "products"),
        ("raw_orders.csv", "orders"),
        ("raw_order_items.csv", "order_items")
    ]

    for file_name, table_name in files_to_ingest:
        ingest_csv_to_raw(file_name, table_name, engine)

    print("Proceso de ingesta masiva completado exitosamente.")

if __name__ == "__main__":
    main()