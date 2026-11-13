"""Crea únicamente la base del proyecto; no altera bases existentes."""
import os
from pathlib import Path
import MySQLdb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / '.env')
name = os.getenv('DB_NAME', 'examenfinal_vehiculos')
if not name.replace('_', '').isalnum():
    raise ValueError('DB_NAME solo puede contener letras, números y guiones bajos.')
connection = MySQLdb.connect(host=os.getenv('DB_HOST', '127.0.0.1'),
    port=int(os.getenv('DB_PORT', '3306')), user=os.getenv('DB_USER', 'root'),
    passwd=os.getenv('DB_PASSWORD', ''), charset='utf8mb4')
with connection.cursor() as cursor:
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
connection.close()
print(f'Base disponible: {name}')
