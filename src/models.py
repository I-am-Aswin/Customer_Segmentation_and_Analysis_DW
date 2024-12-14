from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

class CustomerTier(Base):
    """
    Represents customer tier information
    """
    __tablename__ = 'customer_tiers'
    
    tier_id = Column(Integer, primary_key=True, autoincrement=True)
    tier_name = Column(String(20), nullable=False, unique=True)
    discount_rate = Column(Numeric(5, 2), nullable=True)
    
    # Relationship to customers
    customers = relationship("Customer", back_populates="tier")

class ProductCategory(Base):
    """
    Represents product category information
    """
    __tablename__ = 'product_categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), nullable=False, unique=True)
    
    # Relationship to transactions
    transactions = relationship("Transaction", back_populates="category")

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    payment_method_id = Column(Integer, primary_key=True, autoincrement=True)
    payment_method_name = Column(String(50), nullable=False, unique=True)

    transactions = relationship(
        "Transaction",
        back_populates="payment_method_rel",
        foreign_keys="[Transaction.payment_method]"
    )

class Customer(Base):
    """
    Represents customer information
    """
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    phone_number = Column(String(15))
    gender = Column(String(10))
    dob = Column(Date)
    age = Column(Integer)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    signup_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    # Foreign key to customer tier
    customer_tier = Column(Integer, ForeignKey('customer_tiers.tier_id'))
    
    # Relationship to customer tier
    tier = relationship("CustomerTier", back_populates="customers")
    
    # Relationships to other tables
    transactions = relationship("Transaction", back_populates="customer")
    engagements = relationship("Engagement", back_populates="customer")

class Transaction(Base):
    """
    Represents transaction information
    """
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    payment_method = Column(Integer, ForeignKey('payment_methods.payment_method_id'))
    product_category = Column(Integer, ForeignKey('product_categories.category_id'))
    
    transaction_date = Column(DateTime)
    amount = Column(Numeric(10, 2))
    product_id = Column(String(50))
    quantity = Column(Integer)
    discount_applied = Column(Boolean)
    transaction_status = Column(String(20))
    
    # Relationships
    customer = relationship("Customer", back_populates="transactions")
    payment_method_rel = relationship("PaymentMethod", back_populates="transactions")
    category = relationship("ProductCategory", back_populates="transactions")

class Engagement(Base):
    """
    Represents customer engagement information
    """
    __tablename__ = 'engagements'
    
    engagement_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    engagement_date = Column(Date)
    login_frequency = Column(Integer)
    time_spent = Column(Numeric(5, 2))
    pages_visited = Column(Integer)
    purchase_clicks = Column(Integer)
    feedback_score = Column(Numeric(3, 1))
    email_open_rate = Column(Numeric(5, 2))
    promo_redemptions = Column(Integer)
    
    # Relationship to customer
    customer = relationship("Customer", back_populates="engagements")