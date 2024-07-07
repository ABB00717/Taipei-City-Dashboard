from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os

def get_db():
    db_uri = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
        user=get_env_or_default('DB_DASHBOARD_USER', 'postgres'),
        password=get_env_or_default('DB_DASHBOARD_PASSWORD', 'Abb00717717abb'),
        host=get_env_or_default('DB_DASHBOARD_HOST', 'postgres-data'),
        port=get_env_or_default('DB_DASHBOARD_PORT', '5432'),
        dbname=get_env_or_default('DB_DASHBOARD_DBNAME', 'dashboard')
    )
    return SQLDatabase.from_uri(db_uri)

def get_env_or_default(key, default):
    value = os.getenv(key)
    if value is None or value.strip() == '':
        print(f"Warning: Environment variable {key} is not set. Using default value: {default}")
        return default
    return value