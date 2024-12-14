import psycopg2

# Database connection settings
DB_HOST = "localhost"  # Change to your database host
DB_NAME = "CustomerDW"  # Your database name
DB_USER = "postgres"  # Your database user
DB_PASSWORD = "1234"  # Your database password
DB_PORT = "5432"  # Default PostgreSQL port

# Create a database connection
def create_db_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None
