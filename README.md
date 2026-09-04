#  E-Commerce End-to-End Data Engineering Pipeline

![Data Engineering](https://img.shields.io/badge/Domain-Data_Engineering-blue)
![Python](https://img.shields.io/badge/Python-3.10-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![dbt](https://img.shields.io/badge/dbt--core-1.7+-orange)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-2.8-teal)
![Docker](https://img.shields.io/badge/Docker_Compose-Supported-blue)

End-to-end **Data Engineering pipeline** diseñado para ingerir, transformar, validar y orquestar datos transaccionales de una plataforma de E-Commerce a escala.

El proyecto implementa una arquitectura por capas basada en el enfoque **Medallion Architecture**, utilizando **PostgreSQL como Data Warehouse**, **Python con Faker para simulación de datos masivos**, **dbt para transformación y calidad de datos** y **Apache Airflow para la orquestación**.

La capa analítica se estructura mediante un **Star Schema**, preparando los datos para consumo analítico y herramientas de Business Intelligence (BI).

---

## Objetivo del Proyecto

Simular un pipeline de datos utilizado en un entorno productivo de E-Commerce, cubriendo los desafíos reales de la ingeniería de datos moderna:

* Generación y procesamiento de volúmenes masivos de datos sintéticos (500,000+ registros).
* Ingesta optimizada mediante control de memoria RAM (*Chunking*).
* Almacenamiento de datos en una capa RAW con diseño idempotente.
* Limpieza, estandarización y modelado dimensional (Star Schema) mediante dbt.
* Validación automática de calidad de datos (*dbt Tests*).
* Orquestación robusta del pipeline mediante Apache Airflow.
* Containerización completa de la infraestructura mediante Docker Compose.

---

##  Estructura del Proyecto

```text
ecommerce-pipeline/
│
├── dags/
│   └── ecommerce_etl_dag.py
│
├── dbt_ecommerce/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   │
│   ├── tests/
│   ├── macros/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── scripts/
│   ├── generate_fake_data.py
│   └── load_raw_data.py
│
├── data/
│   └── raw_transactions.csv
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

```

---

## Arquitectura

```text
                 ┌──────────────────────┐
                 │    Faker (Python)    │
                 │  500,000 Transactions│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────┐
                 │ Python / Pandas  │
                 │ Chunked Ingestion│
                 └────────┬─────────┘
                          │
                          ▼
             ┌──────────────────────────────┐
             │         RAW Layer            │
             │         PostgreSQL           │
             │         Schema: raw          │
             └──────────────┬───────────────┘
                            │
                            ▼
                     ┌─────────────────┐
                     │    dbt / SQL    │
                     │ Transformations │
                     └────────┬────────┘
                              │
                              ▼
             ┌──────────────────────────────┐
             │        STAGING Layer         │
             │          PostgreSQL          │
             │       Schema: staging        │
             └──────────────┬───────────────┘
                            │
                            ▼
                     ┌─────────────────┐
                     │   dbt / Jinja   │
                     │ Dimensional SQL │
                     └────────┬────────┘
                              │
                              ▼
             ┌──────────────────────────────┐
             │         MARTS Layer          │
             │          PostgreSQL          │
             │      Schema: analytics       │
             │                              │
             │         Star Schema          │
             └──────────────────────────────┘

                            ▲
                            │
                     ┌──────┴──────────┐
                     │ Apache Airflow  │
                     │   DAG Workflow  │
                     └─────────────────┘

```

---

##  Simulación de Datos Masivos & Rendimiento

Para validar el comportamiento del pipeline ante escenarios de alto volumen, el proyecto incorpora un script generador basado en **Faker** capaz de simular **500,000 registros transaccionales**.

* **Optimización de Memoria:** La ingesta masiva implementa lectura y escritura por bloques (*chunks* de 10,000 a 50,000 filas) utilizando Pandas, evitando la saturación de la memoria RAM del contenedor.
* **Idempotencia:** El script de ingesta automatiza la limpieza previa de tablas (`DROP TABLE IF EXISTS`) antes de cada carga por lotes, garantizando que reejecuciones del DAG no generen registros duplicados.

---

##  Stack Tecnológico

| Tecnología | Uso |
| --- | --- |
| **Python 3.10** | Generación sintética y procesamiento de datos |
| **Faker** | Simulación de transacciones y perfiles de usuarios |
| **Pandas / SQLAlchemy** | Manipulación por lotes y operaciones con PostgreSQL |
| **PostgreSQL 15** | Data Warehouse relacional |
| **dbt Core** | Transformaciones, modelado modular y testing |
| **SQL / Jinja** | Transformación analítica y plantillas dinámicas |
| **Apache Airflow 2.8** | Orquestación y gestión de dependencias del DAG |
| **Docker / Compose** | Containerización y aislamiento de entornos |
| **Git / GitHub** | Control de versiones (Feature Branch Workflow) |

---

##  Guía de Ejecución Local

### Requisitos Previos

* Docker Desktop instalado y en ejecución.
* Git.

---

### 1. Clonar el repositorio y cambiar a la rama de desarrollo

```bash
git clone [https://github.com/GermanAbrilot/ecommerce-pipeline.git](https://github.com/GermanAbrilot/ecommerce-pipeline.git)
cd ecommerce-pipeline
git checkout -b feature/data-generator-500k

```

### 2. Configurar variables de entorno

```bash
cp .env.example .env

```

### 3. Levantar la infraestructura con Docker

```bash
docker compose up -d --build

```

### 4. Generar datos masivos e iniciar el flujo en Airflow

1. Abrir la interfaz web de Airflow en: `http://localhost:8080` (Credenciales: `admin` / contraseña generada o asignada).
2. El DAG `ecommerce_end_to_end_pipeline` ejecutará automáticamente:
* **Generación de 500k registros** mediante `generate_fake_data.py`.
* **Carga masiva por lotes** a la capa RAW mediante `load_raw_data.py`.
* **Transformaciones y modelado** en Staging y Marts con `dbt run`.
* **Validación de calidad** con `dbt test`.



---

##  Pruebas de Calidad de Datos (dbt Tests)

Las pruebas automáticas garantizan la integridad analítica del modelo:

```bash
docker exec -it airflow_standalone dbt test --project-dir /opt/airflow/dbt_ecommerce --profiles-dir /opt/airflow/dbt_ecommerce

```

---

##  Autor

* **Germán Abrilot**
* [GitHub Profile](https://www.google.com/search?q=https://github.com/GermanAbrilot)
* [LinkedIn](https://www.linkedin.com/in/german-dev/)


