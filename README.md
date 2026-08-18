# E-Commerce End-to-End Data Engineering Pipeline

![Data Engineering](https://img.shields.io/badge/Domain-Data_Engineering-blue)
![Python](https://img.shields.io/badge/Python-3.10-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![dbt](https://img.shields.io/badge/dbt--core-1.7+-orange)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-2.8-teal)
![Docker](https://img.shields.io/badge/Docker_Compose-Supported-blue)

End-to-end **Data Engineering pipeline** diseñado para ingerir, transformar, validar y orquestar datos transaccionales de una plataforma de E-Commerce.

El proyecto implementa una arquitectura por capas basada en el enfoque **Medallion Architecture**, utilizando **PostgreSQL como Data Warehouse**, **Python para la ingesta**, **dbt para transformación y calidad de datos** y **Apache Airflow para la orquestación**.

La capa analítica se estructura mediante un **Star Schema**, preparando los datos para consumo analítico y herramientas de Business Intelligence (BI).

---

##  Objetivo del Proyecto

Simular un pipeline de datos utilizado en un entorno productivo de E-Commerce, cubriendo las principales etapas de un flujo moderno de ingeniería de datos:

- Ingesta de datos desde archivos CSV.
- Almacenamiento de datos en una capa RAW.
- Limpieza y estandarización mediante dbt.
- Transformación de datos transaccionales en modelos analíticos.
- Implementación de un modelo dimensional Star Schema.
- Validación automática de calidad de datos.
- Orquestación del pipeline mediante Apache Airflow.
- Containerización de la infraestructura mediante Docker.
- Reproducibilidad del entorno de desarrollo.
---
#  Estructura del Proyecto

```text
ecommerce-pipeline/
│
├── dags/
│   └── ecommerce_pipeline.py
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
│   └── load_raw_data.py
│
├── data/
│   └── *.csv
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

#  Arquitectura

```text
                    ┌──────────────────────┐
                    │     Fuentes CSV      │
                    └──────────┬───────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │ Python / Pandas  │
                     │    SQLAlchemy    │
                     └────────┬─────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │        RAW Layer             │
              │        PostgreSQL            │
              │        Schema: raw           │
              └──────────────┬───────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   dbt / SQL     │
                    │ Transformations │
                    └────────┬────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │       STAGING Layer          │
              │        PostgreSQL            │
              │      Schema: staging        │
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
              │        MARTS Layer           │
              │        PostgreSQL            │
              │      Schema: analytics       │
              │                              │
              │        Star Schema            │
              └──────────────────────────────┘

                             ▲
                             │
                    ┌────────┴────────┐
                    │  Apache Airflow │
                    │   DAG Workflow  │
                    └─────────────────┘
````

### Data Flow

```text
CSV
 │
 ▼
Python Ingestion
 │
 ▼
PostgreSQL RAW
 │
 ▼
dbt Staging
 │
 ▼
dbt Marts
 │
 ▼
Analytics / BI
```

Apache Airflow coordina la ejecución de las diferentes etapas y sus dependencias.

---

# Stack Tecnológico

| Tecnología             | Uso                                        |
| ---------------------- | ------------------------------------------ |
| **Python 3.10**        | Ingesta y procesamiento de datos           |
| **Pandas**             | Manipulación y preparación de datos        |
| **SQLAlchemy**         | Conexión y operaciones con PostgreSQL      |
| **PostgreSQL 15**      | Data Warehouse                             |
| **dbt Core**           | Transformaciones, modelado y testing       |
| **SQL**                | Transformación y modelado de datos         |
| **Jinja**              | Templates y reutilización de lógica en dbt |
| **Apache Airflow 2.8** | Orquestación del pipeline                  |
| **Docker**             | Containerización                           |
| **Docker Compose**     | Gestión de servicios                       |
| **Git / GitHub**       | Control de versiones                       |

---

#  Arquitectura de Datos

El proyecto utiliza una arquitectura de tres capas:

## 1. RAW Layer

Contiene los datos ingeridos desde las fuentes originales con transformaciones mínimas.

```text
PostgreSQL
└── raw
    ├── customers
    ├── products
    ├── orders
    └── order_items
```

El objetivo de esta capa es conservar una representación cercana a los datos originales y servir como punto de entrada para las transformaciones posteriores.

---

## 2. STAGING Layer

La capa staging utiliza **dbt** para limpiar, estandarizar y preparar los datos para el modelado analítico.

Principales transformaciones:

* Estandarización de nombres de columnas.
* Conversión de tipos de datos.
* Tratamiento de valores nulos.
* Limpieza de datos.
* Preparación de relaciones entre entidades.
* Cálculo de campos derivados cuando corresponde.

```text
PostgreSQL
└── staging
    ├── stg_customers
    ├── stg_products
    ├── stg_orders
    └── stg_order_items
```

---

## 3. MARTS / ANALYTICS Layer

La capa final contiene modelos orientados al análisis y consumo de información.

Los modelos se organizan utilizando un **Star Schema**, separando hechos y dimensiones.

```text
PostgreSQL
└── analytics
    ├── fct_orders
    ├── dim_customers
    └── dim_products
```

---

#  Modelo Dimensional — Star Schema

El modelo dimensional transforma los datos transaccionales en estructuras optimizadas para análisis.

### Fact Table

#### `fct_orders`

Tabla de hechos que consolida información relacionada con los pedidos.

Incluye métricas y atributos como:

* Monto total de la orden.
* Cantidad total de ítems.
* Estado del pedido.
* Identificador del cliente.
* Fecha del pedido.

### Dimension Tables

#### `dim_customers`

Contiene atributos descriptivos de los clientes:

* Identificador del cliente.
* Nombre.
* Ubicación.
* Fecha de registro.

#### `dim_products`

Contiene información descriptiva del catálogo:

* Identificador del producto.
* Nombre.
* Categoría.
* Precio unitario.

---

#  Orquestación

**Apache Airflow** se utiliza para coordinar las diferentes etapas del pipeline mediante un DAG.

Flujo conceptual:

```text
Start
  │
  ▼
Ingest CSV Data
  │
  ▼
Load RAW Data
  │
  ▼
Run dbt Models
  │
  ▼
Run dbt Tests
  │
  ▼
Pipeline Completed
```

El objetivo es centralizar la ejecución del pipeline y establecer dependencias entre las distintas tareas.

---

#  Data Quality

La calidad de los datos se valida utilizando **dbt Tests**.

Entre las validaciones implementadas se encuentran:

* `unique`
* `not_null`
* Integridad referencial mediante relaciones entre modelos.
* Validación de claves primarias y relaciones entre entidades.

Estas pruebas permiten detectar problemas de calidad antes de que los datos lleguen a la capa analítica.

---

#  Infraestructura

El proyecto utiliza **Docker Compose** para reproducir el entorno de ejecución local.

Los principales servicios son:

```text
Docker Compose
│
├── PostgreSQL
│   └── Data Warehouse
│
└── Apache Airflow
    └── Pipeline Orchestration
```

Esto permite evitar configuraciones manuales diferentes entre entornos y facilita la ejecución del proyecto.

---

# 🚀 Ejecución Local

## Requisitos

Antes de ejecutar el proyecto es necesario tener instalado:

* Docker Desktop
* Git

Docker Desktop debe estar ejecutándose.

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/GermanMundaca/ecommerce-pipeline.git
cd ecommerce-pipeline
```

## 2. Configurar variables de entorno

Crear el archivo `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

Configurar las variables necesarias de acuerdo con el entorno local.

---

## 3. Levantar la infraestructura

```bash
docker compose up -d
```

Verificar que los contenedores estén ejecutándose:

```bash
docker compose ps
```

---

## 4. Acceder a Airflow

Abrir:

```text
http://localhost:8080
```

Desde la interfaz de Airflow:

1. Localizar el DAG `ecommerce_end_to_end_pipeline`.
2. Activarlo.
3. Ejecutar `Trigger DAG`.
4. Revisar el estado de las tareas.
5. Verificar la ejecución de los modelos y tests.

---

# 🧪 Ejecutar Tests de dbt

Los tests pueden ejecutarse dentro del entorno de Airflow utilizando:

```bash
docker exec -it airflow_standalone dbt test --project-dir /opt/airflow/dbt_ecommerce
```

> El nombre del contenedor y la ruta del proyecto deben coincidir con la configuración definida en `docker-compose.yml`.

---



---

# 🔍 Principales Conceptos Demostrados

Este proyecto demuestra experiencia práctica con conceptos fundamentales de Data Engineering:

* ETL / ELT Pipelines
* Data Warehouse
* Medallion Architecture
* Data Ingestion
* Data Transformation
* Data Modeling
* Star Schema
* Fact & Dimension Tables
* SQL
* Python
* dbt
* Data Quality
* Data Testing
* Workflow Orchestration
* Apache Airflow
* Docker
* PostgreSQL
* Git / GitHub

---


#  Autor

**Germán Mundaca**

Ingeniero en Informática | Data Engineering

[GitHub](https://github.com/GermanMundaca)

[LinkedIn](https://www.linkedin.com/in/german-dev/)

