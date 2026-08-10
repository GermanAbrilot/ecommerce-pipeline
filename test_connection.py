import psycopg2
import traceback
import sys

print("Python:", sys.version)
print("psycopg2:", psycopg2.__version__)
print("libpq:", psycopg2.__libpq_version__)

try:
    print("Conectando...")

    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="ecommerce_dw",
        user="data_engineer",
        password="mi_clave_secreta_123",
        connect_timeout=5
    )

    print("CONEXION EXITOSA")
    conn.close()

except Exception as e:
    print("TIPO:", type(e))
    print("ARGS:", repr(e.args))
    print("STR:", repr(str(e)))
    traceback.print_exc()