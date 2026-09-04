from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Definición de argumentos por defecto para el DAG
default_args = {
    'owner': 'German_Mundaca',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,                            # Reintenta 1 vez si la tarea falla
    'retry_delay': timedelta(minutes=1),      # Espera 1 minuto antes de reintentar
}

# Declaración del DAG
with DAG(
    dag_id='ecommerce_end_to_end_pipeline',
    default_args=default_args,
    description='Pipeline completo de E-Commerce: Ingesta Raw -> dbt Run -> dbt Test',
    schedule_interval='@daily',              # Se ejecuta una vez al día
    start_date=datetime(2026, 1, 1),
    catchup=False,                           # No ejecuta fechas pasadas acumuladas
    tags=['ecommerce', 'dbt', 'postgres', 'portfolio'],
) as dag:
    
    # NUEVA TAREA: Generar medio millón de registros falsos
    task_generate_data = BashOperator(
        task_id='generate_fake_transactions',
        bash_command='python /opt/airflow/scripts/generate_fake_data.py'
    )
    # Tarea 1: Ingesta de datos crudos (Python Script)
    task_ingest_raw = BashOperator(
        task_id='ingest_raw_data',
        bash_command='python /opt/airflow/scripts/load_raw_data.py'
    )

    # Tarea 2: Transformación y Modelado Dimensional con dbt
    task_dbt_run = BashOperator(
        task_id='dbt_run_transformations',
        bash_command='dbt run --project-dir /opt/airflow/dbt_ecommerce --profiles-dir /opt/airflow/dbt_ecommerce'
    )

    # Tarea 3: Pruebas de Calidad de Datos con dbt
    task_dbt_test = BashOperator(
        task_id='dbt_test_quality_checks',
        bash_command='dbt test --project-dir /opt/airflow/dbt_ecommerce --profiles-dir /opt/airflow/dbt_ecommerce'
    )

    # Definición de dependencias (Flujo de ejecución)
    # Ingesta -> Transformación -> Pruebas de Calidad
    task_ingest_raw >> task_dbt_run >> task_dbt_test