from flask import request, jsonify, abort
from datetime import datetime
from flask import Flask

app = Flask(__name__)
from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)



import app
from models import db, Category, DiscountCoupon, FavoriteWishlist, Order, OrderItem, Product, Review, User

# Utility function to handle 404 not found
def get_or_404(model, id):
    instance = model.query.get(id)
    if not instance:
        abort(404, description=f"{model.__name__} not found.")
    return instance

# CRUD for Categories
@app.route('/categories', methods=['POST'])
def create_category():
    name = request.json.get('name')
    if not name:
        abort(400, description="Name is required.")
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.id), 201

@app.route('/categories/<int:id>', methods=['GET'])
def read_category(id):
    category = get_or_404(Category, id)
    return jsonify({'id': category.id, 'name': category.name})

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = get_or_404(Category, id)
    category.name = request.json.get('name', category.name)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name})

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = get_or_404(Category, id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'}), 200

# CRUD for DiscountCoupon
@app.route('/discount_coupons', methods=['POST'])
def create_discount_coupon():
    code = request.json.get('code')
    percentage = request.json.get('percentage')
    valid_from = request.json.get('valid_from')
    valid_to = request.json.get('valid_to')
    if not all([code, percentage, valid_from, valid_to]):
        abort(400, description="All fields are required.")
    new_coupon = DiscountCoupon(code=code, percentage=percentage, valid_from=datetime.strptime(valid_from, '%Y-%m-%d'),
                                valid_to=datetime.strptime(valid_to, '%Y-%m-%d'))
    db.session.add(new_coupon)
    db.session.commit()
    return jsonify(new_coupon.id), 201

@app.route('/discount_coupons/<int:id>', methods=['GET'])
def read_discount_coupon(id):
    coupon = get_or_404(DiscountCoupon, id)
    return jsonify({'id': coupon.id, 'code': coupon.code, 'percentage': coupon.percentage,
                    'valid_from': coupon.valid_from.isoformat(), 'valid_to': coupon.valid_to.isoformat()})

@app.route('/discount_coupons/<int:id>', methods=['PUT'])
def update_discount_coupon(id):
    coupon = get_or_404(DiscountCoupon, id)
    coupon.code = request.json.get('code', coupon.code)
    coupon.percentage = request.json.get('percentage', coupon.percentage)
    coupon.valid_from = datetime.strptime(request.json.get('valid_from', coupon.valid_from.isoformat()), '%Y-%m-%d')
    coupon.valid_to = datetime.strptime(request.json.get('valid_to', coupon.valid_to.isoformat()), '%Y-%m-%d')
    db.session.commit()
    return jsonify({'message': 'Coupon updated successfully'})

@app.route('/discount_coupons/<int:id>', methods=['DELETE'])
def delete_discount_coupon(id):
    coupon = get_or_404(DiscountCoupon, id)
    db.session.delete(coupon)
    db.session.commit()
    return jsonify({'message': 'Coupon deleted'}), 200

# CRUD for FavoriteWishlist
@app.route('/favorites_wishlist', methods=['POST'])
def create_favorite_wishlist():
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    if not all([user_id, product_id]):
        abort(400, description="User ID and Product ID are required.")
    new_favorite = FavoriteWishlist(user_id=user_id, product_id=product_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.id), 201

@app.route('/favorites_wishlist/<int:id>', methods=['GET'])
def read_favorite_wishlist(id):
    favorite = get_or_404(FavoriteWishlist, id)
    return jsonify({'id': favorite.id, 'user_id': favorite.user_id, 'product_id': favorite.product_id})

@app.route('/favorites_wishlist/<int:id>', methods=['PUT'])
def update_favorite_wishlist(id):
    favorite = get_or_404(FavoriteWishlist, id)
    favorite.user_id = request.json.get('user_id', favorite.user_id)
    favorite.product_id = request.json.get('product_id', favorite.product_id)
    db.session.commit()
    return jsonify({'message': 'Favorite/Wishlist updated successfully'})

@app.route('/favorites_wishlist/<int:id>', methods=['DELETE'])
def delete_favorite_wishlist(id):
    favorite = get_or_404(FavoriteWishlist, id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite/Wishlist deleted'}), 200

# CRUD for Order
@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json.get('user_id')
    order_date = request.json.get('order_date')  # Assuming order_date is passed as 'YYYY-MM-DD'
    status = request.json.get('status')
    total_amount = request.json.get('total_amount')
    if not all([user_id, order_date, status, total_amount]):
        abort(400, description="All order fields are required.")
    new_order = Order(user_id=user_id, order_date=datetime.strptime(order_date, '%Y-%m-%d'), status=status, total_amount=total_amount)
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.id), 201

@app.route('/orders/<int:id>', methods=['GET'])
def read_order(id):
    order = get_or_404(Order, id)
    return jsonify({'id': order.id, 'user_id': order.user_id, 'order_date': order.order_date.isoformat(),
                    'status': order.status, 'total_amount': order.total_amount})

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = get_or_404(Order, id)
    order.user_id = request.json.get('user_id', order.user_id)
    order.order_date = datetime.strptime(request.json.get('order_date', order.order_date.isoformat()), '%Y-%m-%d')
    order.status = request.json.get('status', order.status)
    order.total_amount = request.json.get('total_amount', order.total_amount)
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = get_or_404(Order, id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200

# CRUD for OrderItem
@app.route('/order_items', methods=['POST'])
def create_order_item():
    order_id = request.json.get('order_id')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    price = request.json.get('price')
    discount = request.json.get('discount')
    if not all([order_id, product_id, quantity, price]):
        abort(400, description="All order item fields are required.")
    new_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price, discount=discount)
    db.session.add(new_order_item)
    db.session.commit()
    return jsonify(new_order_item.id), 201

@app.route('/order_items/<int:id>', methods=['GET'])
def read_order_item(id):
    order_item = get_or_404(OrderItem, id)
    return jsonify({'id': order_item.id, 'order_id': order_item.order_id, 'product_id': order_item.product_id,
                    'quantity': order_item.quantity, 'price': order_item.price, 'discount': order_item.discount})

@app.route('/order_items/<int:id>', methods=['PUT'])
def update_order_item(id):
    order_item = get_or_404(OrderItem, id)
    order_item.order_id = request.json.get('order_id', order_item.order_id)
    order_item.product_id = request.json.get('product_id', order_item.product_id)
    order_item.quantity = request.json.get('quantity', order_item.quantity)
    order_item.price = request.json.get('price', order_item.price)
    order_item.discount = request.json.get('discount', order_item.discount)
    db.session.commit()
    return jsonify({'message': 'Order item updated successfully'})

@app.route('/order_items/<int:id>', methods=['DELETE'])
def delete_order_item(id):
    order_item = get_or_404(OrderItem, id)
    db.session.delete(order_item)
    db.session.commit()
    return jsonify({'message': 'Order item deleted'}), 200

# CRUD for Product
@app.route('/products', methods=['POST'])
def create_product():
    name = request.json.get('name')
    category_id = request.json.get('category_id')
    brand = request.json.get('brand')
    price = request.json.get('price')
    description = request.json.get('description')
    image_url = request.json.get('image_url')
    if not all([name, category_id, brand, price, description, image_url]):
        abort(400, description="All product fields are required.")
    new_product = Product(name=name, category_id=category_id, brand=brand, price=price, description=description, image_url=image_url)
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.id), 201

@app.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = get_or_404(Product, id)
    return jsonify({'id': product.id, 'name': product.name, 'category_id': product.category_id,
                    'brand': product.brand, 'price': product.price, 'description': product.description,
                    'image_url': product.image_url})

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = get_or_404(Product, id)
    product.name = request.json.get('name', product.name)
    product.category_id = request.json.get('category_id', product.category_id)
    product.brand = request.json.get('brand', product.brand)
    product.price = request.json.get('price', product.price)
    product.description = request.json.get('description', product.description)
    product.image_url = request.json.get('image_url', product.image_url)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = get_or_404(Product, id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

# CRUD for Review
@app.route('/reviews', methods=['POST'])
def create_review():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    rating = request.json.get('rating')
    review_text = request.json.get('review_text')
    review_date = request.json.get('review_date')  # Assuming review_date is passed as 'YYYY-MM-DD'
    reviewscol = request.json.get('reviewscol')
    if not all([product_id, user_id, rating, review_text, review_date]):
        abort(400, description="All review fields are required.")
    new_review = Review(product_id=product_id, user_id=user_id, rating=rating, review_text=review_text,
                        review_date=datetime.strptime(review_date, '%Y-%m-%d'), reviewscol=reviewscol)
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.id), 201

@app.route('/reviews/<int:id>', methods=['GET'])
def read_review(id):
    review = get_or_404(Review, id)
    return jsonify({'id': review.id, 'product_id': review.product_id, 'user_id': review.user_id,
                    'rating': review.rating, 'review_text': review.review_text,
                    'review_date': review.review_date.isoformat(), 'reviewscol': review.reviewscol})

@app.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    review = get_or_404(Review, id)
    review.product_id = request.json.get('product_id', review.product_id)
    review.user_id = request.json.get('user_id', review.user_id)
    review.rating = request.json.get('rating', review.rating)
    review.review_text = request.json.get('review_text', review.review_text)
    review.review_date = datetime.strptime(request.json.get('review_date', review.review_date.isoformat()), '%Y-%m-%d')
    review.reviewscol = request.json.get('reviewscol', review.reviewscol)
    db.session.commit()
    return jsonify({'message': 'Review updated successfully'})

@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = get_or_404(Review, id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200

# CRUD for User
@app.route('/users', methods=['POST'])
def create_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    is_admin = request.json.get('is_admin')
    userscol = request.json.get('userscol')
    if not all([first_name, last_name, email, password_hash, is_admin]):
        abort(400, description="All user fields are required.")
    new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password_hash,
                    is_admin=is_admin, userscol=userscol)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.id), 201

@app.route('/users/<int:id>', methods=['GET'])
def read_user(id):
    user = get_or_404(User, id)
    return jsonify({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
                    'email': user.email, 'password_hash': user.password_hash,
                    'is_admin': user.is_admin, 'userscol': user.userscol})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = get_or_404(User, id)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)
    user.email = request.json.get('email', user.email)
    user.password_hash = request.json.get('password_hash', user.password_hash)
    user.is_admin = request.json.get('is_admin', user.is_admin)
    user.userscol = request.json.get('userscol', user.userscol)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
