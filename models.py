from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)

class DiscountCoupon(db.Model):
    __tablename__ = 'discount_coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(45), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)  # Assuming percentage is an integer
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)

class FavoriteWishlist(db.Model):
    __tablename__ = 'favorites_wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.String(45), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(45), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(45), nullable=False)
    total_amount = db.Column(db.String(45), nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.String(45), nullable=False)
    quantity = db.Column(db.String(45), nullable=False)
    price = db.Column(db.String(45), nullable=False)
    discount = db.Column(db.String(45))

class Product(db.Model):
    __tablename__ = 'Product'
    Product_id = db.Column(db.Integer, primary_key=True)  # Attribute name here must match exactly in your function
    Product_name = db.Column(db.String(45))
    Category_id = db.Column(db.String(45))
    Brand = db.Column(db.String(45))
    Price = db.Column(db.Numeric(10, 2))
    Discription = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.String(45), nullable=False)
    rating = db.Column(db.String(45), nullable=False)
    review_text = db.Column(db.String(45), nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    reviewscol = db.Column(db.String(45))  # Assuming this is a placeholder

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password_hash = db.Column(db.String(45), nullable=False)
    is_admin = db.Column(db.String(45), nullable=False)  # Boolean might be more appropriate here
    userscol = db.Column(db.String(45))  # Assuming this is a placeholder
