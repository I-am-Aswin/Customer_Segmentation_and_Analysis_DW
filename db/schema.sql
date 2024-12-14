-- Create tables for the star schema

-- Customer Tiers Table
CREATE TABLE customer_tiers (
    tier_id SERIAL PRIMARY KEY,
    tier_name VARCHAR(20),
    discount_rate DECIMAL(5, 2)
);

-- Product Categories Table
CREATE TABLE product_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50)
);

-- Payment Methods Table
CREATE TABLE payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    payment_method_name VARCHAR(50)
);

-- Customers Table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    gender VARCHAR(10),
    dob DATE,
    age INTEGER,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    signup_date DATE,
    is_active BOOLEAN,
    customer_tier INTEGER REFERENCES customer_tiers(tier_id)
);

-- Transactions Table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    transaction_date TIMESTAMP,
    amount DECIMAL(10, 2),
    payment_method INTEGER REFERENCES payment_methods(payment_method_id),
    product_id VARCHAR(50),
    product_category INTEGER REFERENCES product_categories(category_id),
    quantity INTEGER,
    discount_applied BOOLEAN,
    transaction_status VARCHAR(20)
);

-- Engagements Table
CREATE TABLE engagements (
    engagement_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    engagement_date DATE,
    login_frequency INTEGER,
    time_spent DECIMAL(5, 2),
    pages_visited INTEGER,
    purchase_clicks INTEGER,
    feedback_score INTEGER,
    email_open_rate DECIMAL(5, 2),
    promo_redemptions INTEGER
);
