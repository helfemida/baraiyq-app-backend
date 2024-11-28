import os

DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASS", "postgres123")
DB_NAME = "baraiyq"
DB_CONNECTION_NAME = "baraiyq-app:us-central1:database"
DB_IP = "34.28.210.195"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_IP}/{DB_NAME}"


#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"
