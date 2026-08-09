## Infraestructura y Docker 

Configurar Docker y levantar servicios (PostgreSQL como Data Warehouse y Apache Airflow como orquestador).

## Ingesta de Datos (Capa Raw / Ingestion)

Carga de conjunto de datos iniciales en la base de datos PostgreSQL desde Python/SQL.

## Transformación y Modelamiento con dbt

Modelado de datos en un esquema estrella (Star Schema con capas de Staging y Marts: Tablas de Hechos y Dimensiones) usando dbt.

## Orquestación Automática con Apache Airflow
DAG (Directed Acyclic Graph) que ejecuta la ingesta, las transformaciones de dbt y las pruebas de calidad de datos automáticamente.



# 1. Clonar el repositorio
git clone https://github.com/GermanMundaca/ecommerce-de-pipeline.git
cd ecommerce-de-pipeline

# 2. Copiar la plantilla de variables de entorno para crear tu .env local
cp .env.example .env

# 3. Levantar la infraestructura
docker compose up -d --build