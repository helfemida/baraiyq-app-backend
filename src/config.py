import os

DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASS", "postgres123")
DB_NAME = "baraiyq-db" 
DB_CONNECTION_NAME = "baraiyq-app-438307:us-central1:baraiyq-db"  

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{DB_CONNECTION_NAME}"

#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"


