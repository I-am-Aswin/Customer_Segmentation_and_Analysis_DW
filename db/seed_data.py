import psycopg2

# Connection details
CONN_DETAILS = {
    'dbname': 'CustomerDW',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': 5432
}

# Static data to seed
CUSTOMER_TIERS = [
    ('Bronze', 0.05),
    ('Silver', 0.10),
    ('Gold', 0.15)
]

PRODUCT_CATEGORIES = [
    'electronics',
    'clothing',
    'home goods'
]

PAYMENT_METHODS = [
    'credit card',
    'PayPal',
    'debit card'
]

def seed_data():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**CONN_DETAILS)
        cursor = conn.cursor()

        # Seed Customer Tiers
        cursor.executemany(
            "INSERT INTO customer_tiers (tier_name, discount_rate) VALUES (%s, %s)",
            CUSTOMER_TIERS
        )

        # Seed Product Categories
        cursor.executemany(
            "INSERT INTO product_categories (category_name) VALUES (%s)",
            [(category,) for category in PRODUCT_CATEGORIES]
        )

        # Seed Payment Methods
        cursor.executemany(
            "INSERT INTO payment_methods (payment_method_name) VALUES (%s)",
            [(method,) for method in PAYMENT_METHODS]
        )

        # Commit and close
        conn.commit()
        print("Data seeded successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_data()
