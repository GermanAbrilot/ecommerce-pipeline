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
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        connection.commit()
        print("Schema 'raw' verificado/creado con éxito.")

def ingest_csv_to_raw(file_name, table_name, engine):
    """Lee un CSV de la carpeta data y lo carga en la tabla especificada del esquema raw."""
    file_path = os.path.join("data", file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe.")
        return

    # Leer CSV con Pandas
    df = pd.read_csv(file_path)
    
    # Agregar columna de auditoría/trazabilidad (Metadata essential in DE)
    df["_ingested_at"] = datetime.now()

    # Ingestar en la base de datos (Estrategia: Replace para asegurar Idempotencia)
    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False
    )
    print(f"Tabla 'raw.{table_name}' ingestada correctamente ({len(df)} registros).")

def main():
    print("Iniciando proceso de ingesta en la Capa RAW...")
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

    print("Proceso de ingesta completado exitosamente.")

if __name__ == "__main__":
    main()