import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

# Import database connection details
from ..db_connection import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Import ORM models
from ..models import (
    Base, 
    CustomerTier, 
    PaymentMethod, 
    ProductCategory, 
    Customer, 
    Transaction, 
    Engagement
)

def create_db_engine():
    """
    Create a database engine connection
    """
    try:
        # SQLAlchemy engine connection string
        connection_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = create_engine(connection_string)
        return engine
    except Exception as error:
        print(f"Error creating database engine: {error}")
        return None

def get_or_create_reference_data(session, model, name_column, value):
    """
    Get or create a reference data record
    """
    # Check if the record exists
    existing = session.query(model).filter(
        getattr(model, name_column) == value
    ).first()
    
    if existing:
        return existing
    
    # Create new record if it doesn't exist
    new_record = model(**{name_column: value})
    session.add(new_record)
    session.commit()
    return new_record

def process_customers_data(session, df):
    """
    Process and insert customer data
    """
    for _, row in df.iterrows():
        # Get or create customer tier
        tier = get_or_create_reference_data(
            session, 
            CustomerTier, 
            'tier_name', 
            row['customer_tier']
        )
        
        # Create customer record
        customer = Customer(
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            phone_number=row['phone_number'],
            gender=row['gender'],
            dob=row['dob'],
            age=row['age'],
            city=row['city'],
            state=row['state'],
            country=row['country'],
            signup_date=row['signup_date'],
            is_active=row['is_active'],
            customer_tier=tier.tier_id
        )
        
        session.add(customer)
    
    session.commit()

def process_transactions_data(session, df):
    """
    Process and insert transaction data
    """
    for _, row in df.iterrows():
        # Get or create payment method
        payment_method = get_or_create_reference_data(
            session, 
            PaymentMethod, 
            'payment_method_name', 
            row['payment_method']
        )
        
        # Get or create product category
        product_category = get_or_create_reference_data(
            session, 
            ProductCategory, 
            'category_name', 
            row['product_category']
        )
        
        # Create transaction record
        transaction = Transaction(
            customer_id=row['customer_id'],
            transaction_date=row['transaction_date'],
            amount=row['amount'],
            payment_method=payment_method.payment_method_id,
            product_id=row['product_id'],
            product_category=product_category.category_id,
            quantity=row['quantity'],
            discount_applied=row['discount_applied'],
            transaction_status=row['transaction_status']
        )
        
        session.add(transaction)
    
    session.commit()

def process_engagements_data(session, df):
    """
    Process and insert engagement data
    """
    for _, row in df.iterrows():
        # Find the corresponding customer
        customer = session.query(Customer).filter_by(
            customer_id=row['customer_id']
        ).first()
        
        # Create engagement record
        engagement = Engagement(
            customer_id=row['customer_id'],
            engagement_date=row['engagement_date'],
            login_frequency=row['login_frequency'],
            time_spent=row['time_spent'],
            pages_visited=row['pages_visited'],
            purchase_clicks=row['purchase_clicks'],
            feedback_score=row['feedback_score'],
            email_open_rate=row['email_open_rate'],
            promo_redemptions=row['promo_redemptions']
        )
        
        session.add(engagement)
    
    session.commit()

def etl_process(csv_file, process_function):
    """
    Main ETL process function
    """
    try:
        # Create database engine
        engine = create_db_engine()
        if not engine:
            return
        
        # Create tables if they don't exist
        Base.metadata.create_all(engine)
        
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Process data based on the provided function
        process_function(session, df)
        
        # Close session
        session.close()
        
        print(f"Data loaded successfully from {csv_file}")
    
    except Exception as error:
        print(f"Error in ETL process: {error}")

def main():
    """
    Main function to run ETL processes
    """
    # Define file paths
    customers_file = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_customers.csv'
    transactions_file = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_transactions.csv'
    engagements_file = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_engagements.csv'
    
    # Run ETL processes
    etl_process(customers_file, process_customers_data)
    etl_process(transactions_file, process_transactions_data)
    etl_process(engagements_file, process_engagements_data)

if __name__ == '__main__':
    main()