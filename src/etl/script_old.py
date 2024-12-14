import pandas as pd
from sqlalchemy import create_engine
from ..db_connection import *

# Function to load cleaned data into the database
def load_data_to_db(csv_file, table_name, engine):
    try:
        # Read the cleaned CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Insert data into the PostgreSQL table
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data loaded successfully into {table_name} table.")
    except Exception as error:
        print(f"Error loading data into {table_name}: {error}")

# Create a database connection engine
def create_db_engine():
    try:
        # SQLAlchemy engine connection string
        engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        return engine
    except Exception as error:
        print(f"Error creating database engine: {error}")
        return None

# ETL process for customers
def etl_customers():
    # Define cleaned customers CSV file and table name
    cleaned_customers_file =  r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_customers.csv'
    table_name = 'customers'

    # Create DB engine connection
    engine = create_db_engine()
    if engine:
        load_data_to_db(cleaned_customers_file, table_name, engine)

# ETL process for engagement data
def etl_engagements():
    # Define cleaned engagements CSV file and table name
    cleaned_engagements_file = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_engagements.csv'
    table_name = 'engagements'

    # Create DB engine connection
    engine = create_db_engine()
    if engine:
        load_data_to_db(cleaned_engagements_file, table_name, engine)

# ETL process for transactions data
def etl_transactions():
    # Define cleaned transactions CSV file and table name
    cleaned_transactions_file = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_transactions.csv'
    table_name = 'transactions'

    # Create DB engine connection
    engine = create_db_engine()
    if engine:
        load_data_to_db(cleaned_transactions_file, table_name, engine)

# Main function to run all ETL processes
def main():
    # Run ETL for each dataset
    etl_customers()
    etl_engagements()
    etl_transactions()

if __name__ == '__main__':
    main()
