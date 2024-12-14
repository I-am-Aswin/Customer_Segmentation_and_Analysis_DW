import pandas as pd
from numpy.random import randint
from datetime import datetime

def convert_date(date_str):
    try:
        return pd.to_datetime(date_str, format="%m/%d/%Y")
    except:
        return None

def clean_customers(file_path, dest_path):
    customers = pd.read_csv(file_path)

    customers['city'] = customers['city'].fillna('Unknown')
    customers['state'] = customers['state'].fillna('Unknown')
    customers['country'] = customers['country'].fillna('Unknown')

    customers['is_active'] = customers['is_active'].apply( lambda x: True if ( x ) else False )

    customers['dob'] = customers['dob'].apply(convert_date)
    customers['signup_date'] = customers['signup_date'].apply(convert_date)

    customers.drop_duplicates(subset='customer_id', inplace=True)

    valid_genders = ['Male', 'Female', 'Other']
    customers['gender'] = customers['gender'].apply(lambda x: x if x in valid_genders else 'Other')

    customers.to_csv(dest_path, index=False)
    print("Cleaned customers.csv saved!")


def clean_engagement(file_path, dest_path):
    engagements = pd.read_csv(file_path)

    engagements['customer_id'] = engagements['customer_id'].apply( lambda x: randint(1,1000) )

    engagements.fillna(0, inplace=True)

    engagements['engagement_date'] = engagements['engagement_date'].apply(convert_date)

    numeric_columns = ['login_frequency', 'time_spent', 'pages_visited', 
                       'purchase_clicks', 'feedback_score', 'email_open_rate', 
                       'promo_redemptions']
    engagements[numeric_columns] = engagements[numeric_columns].apply(pd.to_numeric)

    engagements['time_spent'] = ( engagements['time_spent'] / 60 ).round(2)

    engagements.drop_duplicates(subset='engagement_id', inplace=True)

    engagements.to_csv(dest_path, index=False)
    print("Cleaned engagements.csv saved!")

def clean_transactions(file_path, dest_path):
    transactions = pd.read_csv(file_path)

    transactions['customer_id'] = transactions['customer_id'].apply( lambda x: randint(1,1000) )

    transactions['product_category'] = transactions['product_category'].fillna('Unknown')
    transactions['transaction_status'] = transactions['transaction_status'].fillna('unknown')

    transactions['transaction_date'] = transactions['transaction_date'].apply(convert_date)

    numeric_columns = ['amount', 'quantity']
    transactions[numeric_columns] = transactions[numeric_columns].apply(pd.to_numeric)

    transactions['discount_applied'] = transactions['discount_applied'].apply( lambda x: True if x > 0 else False )

    transactions.drop_duplicates(subset='transaction_id', inplace=True)

    valid_statuses = ['completed', 'pending', 'refunded']
    transactions['transaction_status'] = transactions['transaction_status'].apply(
        lambda x: x if x in valid_statuses else 'unknown'
    )

    transactions.to_csv(dest_path, index=False)
    print("Cleaned transactions.csv saved!")

customers_path = r'E:\Programs\CustomerSegmentation_DW\data\raw\customers.csv'
engagements_path = r'E:\Programs\CustomerSegmentation_DW\data\raw\engagements.csv'
transactions_path = r'E:\Programs\CustomerSegmentation_DW\data\raw\transactions.csv'

customers_dest = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_customers.csv'
engagements_dest = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_engagements.csv'
transactions_dest = r'E:\Programs\CustomerSegmentation_DW\data\processed\cleaned_transactions.csv'

clean_customers(customers_path, customers_dest)
clean_engagement(engagements_path, engagements_dest)
clean_transactions(transactions_path, transactions_dest)
