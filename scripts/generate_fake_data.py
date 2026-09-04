import csv
import random
from faker import Faker
from datetime import datetime
import os

# Configuración
NUM_RECORDS = 500000
BATCH_SIZE = 10000
OUTPUT_FILE = '/opt/airflow/data/raw_transactions.csv'

fake = Faker('es_CL') # Datos localizados para Chile

def generate_data():
    print(f"Iniciando generación de {NUM_RECORDS} registros...")
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Abrir archivo en modo escritura
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir cabeceras
        writer.writerow(['order_id', 'customer_name', 'email', 'city', 'product_name', 'category', 'unit_price', 'quantity', 'order_date', 'order_status'])
        
        # Categorías y Estados simulados
        categories = ['Electrónica', 'Hogar', 'Alimentos', 'Ropa', 'Deportes']
        statuses = ['COMPLETED', 'PENDING', 'CANCELLED', 'REFUNDED']
        
        # Generación por lotes para no saturar la RAM
        for i in range(0, NUM_RECORDS, BATCH_SIZE):
            batch = []
            for j in range(BATCH_SIZE):
                row = [
                    i + j + 1,                                       # order_id
                    fake.name(),                                     # customer_name
                    fake.ascii_safe_email(),                         # email
                    fake.city(),                                     # city
                    f"Producto {fake.ean8()}",                       # product_name
                    random.choice(categories),                       # category
                    round(random.uniform(5.0, 500.0), 2),            # unit_price
                    random.randint(1, 10),                           # quantity
                    fake.date_time_between(start_date='-1y', end_date='now').isoformat(), # order_date
                    random.choice(statuses)                          # order_status
                ]
                batch.append(row)
            
            # Escribir el lote en el CSV
            writer.writerows(batch)
            print(f"Progreso: {i + BATCH_SIZE} / {NUM_RECORDS} generados...")

    print("✅ Archivo CSV generado con éxito.")

if __name__ == "__main__":
    generate_data()