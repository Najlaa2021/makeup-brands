from flask import Flask, render_template, request, render_template_string
from flask import Flask, jsonify
from models import *
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/finaldb'  # Replace with your database URI
@app.route ("/")
def hello_w():
    return render_template ("home.html")

    # Initialize the database
db.init_app(app)

    # Create the database tables
with app.app_context():
        db.create_all()

def add_product_to_database(product_id, product_name, category_id, brand, price, description, image_url):
    new_product = Product(
        Product_id=product_id,
        Product_name=product_name,
        Category_id=category_id,
        Brand=brand,
        Price=price,
        Discription=description,
        image_url=image_url
    )
    db.session.add(new_product)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Failed to add product to database: {e}")
        return False
@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        try:
            product_id = int(request.form.get('Product_id', ''))
            product_name = request.form.get('Product_name', '')
            category_id = request.form.get('Category_id', '')
            brand = request.form.get('Brand', '')
            price = float(request.form.get('Price', '0'))
            description = request.form.get('Description', '')
            image_url = request.form.get('image_url', '')

            if not all([product_id, product_name, category_id, brand, price, description, image_url]):
                return jsonify({"error": "All fields must be provided and valid."}), 400

            add_product_to_database(product_id, product_name, category_id, brand, price, description, image_url)
            return jsonify({"message": "Product added successfully!"}), 201
        except ValueError as e:
            return jsonify({"error": f"Invalid input data: {e}"}), 400

    return render_template_string('''
        <form method="post">
            Product ID: <input type="number" name="Product_id"><br>
            Product Name: <input type="text" name="Product_name"><br>
            Category ID: <input type="text" name="Category_id"><br>
            Brand: <input type="text" name="Brand"><br>
            Price: <input type="text" name="Price"><br>
            Description: <input type="text" name="Description"><br>
            Image URL: <input type="text" name="image_url"><br>
            <input type="submit" value="Add Product">
        </form>
    ''')


@app.route('/products', methods=['GET'])
def get_products():
    # Query all products from the database
    products = Product.query.all()
    # Convert the query result to a list of dictionaries
    product_list = [{
        'Product_id': product.Product_id,
        'Product_name': product.Product_name,
        'Category_id': product.Category_id,
        'Brand': product.Brand,
        'Price': float(product.Price),
        'Discription': product.Discription,
        'image_url': product.image_url
    } for product in products]
    return jsonify(product_list)

@app.route('/Products/<int:product_id>', methods=['GET','POST'])
def update_product(product_id):
    if request.method == 'POST':
        try:
            product = Product.query.filter_by(Product_id=product_id).first()
            if not product:
                return jsonify({"error": "Product not found"}), 404

            # Retrieve data from the form
            product.Product_name = request.form.get('Product_name')
            product.Category_id = request.form.get('Category_id')
            product.Brand = request.form.get('Brand')
            product.Price = float(request.form.get('Price'))
            product.Discription = request.form.get('Discription')
            product.image_url = request.form.get('image_url')

            db.session.commit()

            return jsonify({"message": "Product updated successfully!"}), 200
        except ValueError as e:
            return jsonify({"error": f"Invalid input data: {e}"}), 400

    # Retrieve the existing product data
    product = Product.query.filter_by(Product_id=product_id).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Render the update form with the existing product details
    return '''
        <h1>Update Product</h1>
        <form method="post">
            Product Name: <input type="text" name="Product_name" value="{0}"><br>
            Category ID: <input type="text" name="Category_id" value="{1}"><br>
            Brand: <input type="text" name="Brand" value="{2}"><br>
            Price: <input type="text" name="Price" value="{3}"><br>
            Discription: <input type="text" name="Discription" value="{4}"><br>
            Image URL: <input type="text" name="image_url" value="{5}"><br>
            <input type="submit" value="Update Product">
        </form>
    '''.format(product.Product_name, product.Category_id, product.Brand, product.Price, product.Discription, product.image_url)

@app.route('/Productss/<int:product_id>',methods=['GET','POST','DELETE'])
def delete_product(product_id):
    # Retrieve the product from the database
    product = Product.query.get(product_id)

    # Check if the product exists
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete product: {str(e)}"}), 500
    finally:
        db.session.close()




if __name__ == '__main__':
    app.run(debug=True)








#
#
#
#
#
#
#
#
#
#








# @app.route('/categories', methods=['POST'])
# class Category(db.Model):
#     __tablename__ = 'categories'
#     Categories_ID = db.Column(db.Integer, primary_key=True)
#     Categories_name = db.Column(db.String(255))
#
# def create_category():
#     data = request.get_json()
#     new_category = Category(Categories_name=data['Categories_name'])
#     db.session.add(new_category)
#     db.session.commit()
#     return jsonify({'message': 'Category created successfully', 'Categories_ID': new_category.Categories_ID}), 201
#
# @app.route('/categories', methods=['GET'])
# def get_categories():
#     categories = Category.query.all()
#     categories_list = [{'Categories_ID': cat.categories_ID, 'Category_name': cat.Categories_name} for cat in categories]
#     return jsonify(categories_list)
#
# @app.route('/categories/<int:Category_ID>', methods=['GET'])
# def add_category(Categories_ID):
#     category = Category.query.get_or_404(Categories_ID)
#     return jsonify({'Categories_ID': category.categories_ID, 'category_name': category.Categories_name})
#
# @app.route('/categories/<int:Categories_IDD>', methods=['PUT'])
# def update_category(Categories_ID):
#     category = Category.query.get_or_404(Categories_ID)
#     data = request.get_json()
#     category.categories_name = data.get('Categories_name', category.categories_name)
#     db.session.commit()
#     return jsonify({'message': 'Category updated successfully'})
#
# @app.route('/categories/<int:Categories_ID>', methods=['DELETE'])
# def delete_category(Categories_ID):
#     category = Category.query.get_or_404(Categories_ID)
#     db.session.delete(category)
#     db.session.commit()
#     return jsonify({'message': 'Category deleted successfully'}), 200
#
#
# if __name__ == '__main__':
#     app.run(debug=True)










#
# from flask import Flask, jsonify, request, render_template_string
# from models import db, Order
# from sqlalchemy.exc import SQLAlchemyError
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/finaldb'
#
# # Initialize the database
# db.init_app(app)
#
# # Create the database tables
# with app.app_context():
#     db.create_all()
#
# def add_order_to_database(order_id, user_id, order_date, status, total_amount):
#     new_order = Order(
#         order_id=order_id,
#         user_id=user_id,
#         order_date=order_date,
#         status=status,
#         total_amount=total_amount
#     )
#     db.session.add(new_order)
#     try:
#         db.session.commit()
#         return True
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         app.logger.error(f"Failed to add order to database: {e}")
#         return False
#
# @app.route('/add_order', methods=['POST', 'GET'])
# def add_order():
#     if request.method == 'POST':
#         try:
#             order_id = int(request.form.get('order_id', ''))
#             user_id = request.form.get('user_id', '')
#             order_date = request.form.get('order_date', '')
#             status = request.form.get('status', '')
#             total_amount = request.form.get('Total_amount', '')
#
#             if not all([order_id, user_id, order_date, status, total_amount]):
#                 return jsonify({"error": "All fields must be provided and valid."}), 400
#
#             result = add_order_to_database(order_id, user_id, order_date, status, total_amount)
#             if result:
#                 return jsonify({"message": "Order added successfully!"}), 201
#             else:
#                 return jsonify({"error": "Failed to add order to the database"}), 500
#         except ValueError as e:
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     return render_template_string('''
#         <!-- Form for adding order -->
#         <form method="post">
#             Order ID: <input type="number" name="order_id"><br>
#             User ID: <input type="text" name="user_id"><br>
#             Order Date: <input type="text" name="order_date"><br>
#             Status: <input type="text" name="status"><br>
#             Total Amount: <input type="text" name="Total_amount"><br>
#             <input type="submit" value="Add Order">
#         </form>
#     ''')
#
# @app.route('/orders', methods=['GET'])
# def get_orders():
#     # Query all orders from the database
#     orders = Order.query.all()
#     # Convert the query result to a list of dictionaries
#     order_list = [{
#         'order_id': order.order_id,
#         'user_id': order.user_id,
#         'order_date': order.order_date,
#         'status': order.status,
#         'total_amount': order.total_amount
#     } for order in orders]
#     return jsonify(order_list)
#
# @app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_order(order_id):
#     order = Order.query.get(order_id)
#     if not order:
#         return jsonify({"error": "Order not found"}), 404
#
#     if request.method == 'PUT':
#         try:
#             order.user_id = request.form.get('user_id', order.user_id)
#             order.order_date = request.form.get('order_date', order.order_date)
#             order.status = request.form.get('status', order.status)
#             order.total_amount = request.form.get('Total_amount', order.total_amount)
#             db.session.commit()
#             return jsonify({"message": "Order updated successfully!"}), 200
#         except ValueError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(order)
#             db.session.commit()
#             return jsonify({"message": "Order deleted successfully!"}), 200
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Failed to delete order: {str(e)}"}), 500
#     else:
#         # GET method to retrieve order details
#         return jsonify({
#             'order_id': order.order_id,
#             'user_id': order.user_id,
#             'order_date': order.order_date,
#             'status': order.status,
#             'total_amount': order.total_amount
#         })
#
# if __name__ == '__main__':
#     app.run(debug=True)











#
#
# from flask import Flask, jsonify, request, render_template_string
# from models import db, Coupon
# from sqlalchemy.exc import SQLAlchemyError
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/finaldb'
#
# # Initialize the database
# db.init_app(app)
#
# # Create the database tables
# with app.app_context():
#     db.create_all()
#
# def add_coupon_to_database(coupon_id, coupon_code, valid_from, valid_to, discount_percentage, max_usage):
#     new_coupon = Coupon(
#         coupon_id=coupon_id,
#         coupon_code=coupon_code,
#         valid_from=valid_from,
#         valid_to=valid_to,
#         discount_percentage=discount_percentage,
#         max_usage=max_usage
#     )
#     db.session.add(new_coupon)
#     try:
#         db.session.commit()
#         return True
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         app.logger.error(f"Failed to add coupon to database: {e}")
#         return False
#
# @app.route('/add_coupon', methods=['POST', 'GET'])
# def add_coupon():
#     if request.method == 'POST':
#         try:
#             coupon_id = int(request.form.get('coupon_id', ''))
#             coupon_code = request.form.get('coupon_code', '')
#             valid_from = request.form.get('valid_from', '')
#             valid_to = request.form.get('valid_to', '')
#             discount_percentage = request.form.get('discount_percentage', '')
#             max_usage = request.form.get('max_usage', '')
#
#             if not all([coupon_id, coupon_code, valid_from, valid_to, discount_percentage, max_usage]):
#                 return jsonify({"error": "All fields must be provided and valid."}), 400
#
#             result = add_coupon_to_database(coupon_id, coupon_code, valid_from, valid_to, discount_percentage, max_usage)
#             if result:
#                 return jsonify({"message": "Coupon added successfully!"}), 201
#             else:
#                 return jsonify({"error": "Failed to add coupon to the database"}), 500
#         except ValueError as e:
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     return render_template_string('''
#         <!-- Form for adding coupon -->
#         <form method="post">
#             Coupon ID: <input type="number" name="coupon_id"><br>
#             Coupon Code: <input type="text" name="coupon_code"><br>
#             Valid From: <input type="text" name="valid_from"><br>
#             Valid To: <input type="text" name="valid_to"><br>
#             Discount Percentage: <input type="text" name="discount_percentage"><br>
#             Max Usage: <input type="text" name="max_usage"><br>
#             <input type="submit" value="Add Coupon">
#         </form>
#     ''')
#
# @app.route('/coupons', methods=['GET'])
# def get_coupons():
#     # Query all coupons from the database
#     coupons = Coupon.query.all()
#     # Convert the query result to a list of dictionaries
#     coupon_list = [{
#         'coupon_id': coupon.coupon_id,
#         'coupon_code': coupon.coupon_code,
#         'valid_from': coupon.valid_from,
#         'valid_to': coupon.valid_to,
#         'discount_percentage': coupon.discount_percentage,
#         'max_usage': coupon.max_usage
#     } for coupon in coupons]
#     return jsonify(coupon_list)
#
# @app.route('/coupons/<int:coupon_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_coupon(coupon_id):
#     coupon = Coupon.query.get(coupon_id)
#     if not coupon:
#         return jsonify({"error": "Coupon not found"}), 404
#
#     if request.method == 'PUT':
#         try:
#             coupon.coupon_code = request.form.get('coupon_code', coupon.coupon_code)
#             coupon.valid_from = request.form.get('valid_from', coupon.valid_from)
#             coupon.valid_to = request.form.get('valid_to', coupon.valid_to)
#             coupon.discount_percentage = request.form.get('discount_percentage', coupon.discount_percentage)
#             coupon.max_usage = request.form.get('max_usage', coupon.max_usage)
#             db.session.commit()
#             return jsonify({"message": "Coupon updated successfully!"}), 200
#         except ValueError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(coupon)
#             db.session.commit()
#             return jsonify({"message": "Coupon deleted successfully!"}), 200
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Failed to delete coupon: {str(e)}"}), 500
#     else:
#         # GET method to retrieve coupon details
#         return jsonify({
#             'coupon_id': coupon.coupon_id,
#             'coupon_code': coupon.coupon_code,
#             'valid_from': coupon.valid_from,
#             'valid_to': coupon.valid_to,
#             'discount_percentage': coupon.discount_percentage,
#             'max_usage': coupon.max_usage
#         })
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
#
#
#
#
#
#
#
#
#
# from flask import Flask, jsonify, request, render_template_string
# from models import db, Order
# from sqlalchemy.exc import SQLAlchemyError
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/finaldb'
#
# # Initialize the database
# db.init_app(app)
#
# # Create the database tables
# with app.app_context():
#     db.create_all()
#
# def add_order_to_database(order_id, user_id, order_date, status, total_amount):
#     new_order = Order(
#         order_id=order_id,
#         user_id=user_id,
#         order_date=order_date,
#         status=status,
#         total_amount=total_amount
#     )
#     db.session.add(new_order)
#     try:
#         db.session.commit()
#         return True
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         app.logger.error(f"Failed to add order to database: {e}")
#         return False
#
# @app.route('/add_order', methods=['POST', 'GET'])
# def add_order():
#     if request.method == 'POST':
#         try:
#             order_id = int(request.form.get('order_id', ''))
#             user_id = request.form.get('user_id', '')
#             order_date = request.form.get('order_date', '')
#             status = request.form.get('status', '')
#             total_amount = request.form.get('Total_amount', '')
#
#             if not all([order_id, user_id, order_date, status, total_amount]):
#                 return jsonify({"error": "All fields must be provided and valid."}), 400
#
#             result = add_order_to_database(order_id, user_id, order_date, status, total_amount)
#             if result:
#                 return jsonify({"message": "Order added successfully!"}), 201
#             else:
#                 return jsonify({"error": "Failed to add order to the database"}), 500
#         except ValueError as e:
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     return render_template_string('''
#         <!-- Form for adding order -->
#         <form method="post">
#             Order ID: <input type="number" name="order_id"><br>
#             User ID: <input type="text" name="user_id"><br>
#             Order Date: <input type="text" name="order_date"><br>
#             Status: <input type="text" name="status"><br>
#             Total Amount: <input type="text" name="Total_amount"><br>
#             <input type="submit" value="Add Order">
#         </form>
#     ''')
#
# @app.route('/orders', methods=['GET'])
# def get_orders():
#     # Query all orders from the database
#     orders = Order.query.all()
#     # Convert the query result to a list of dictionaries
#     order_list = [{
#         'order_id': order.order_id,
#         'user_id': order.user_id,
#         'order_date': order.order_date,
#         'status': order.status,
#         'total_amount': order.total_amount
#     } for order in orders]
#     return jsonify(order_list)
#
# @app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_order(order_id):
#     order = Order.query.get(order_id)
#     if not order:
#         return jsonify({"error": "Order not found"}), 404
#
#     if request.method == 'PUT':
#         try:
#             order.user_id = request.form.get('user_id', order.user_id)
#             order.order_date = request.form.get('order_date', order.order_date)
#             order.status = request.form.get('status', order.status)
#             order.total_amount = request.form.get('Total_amount', order.total_amount)
#             db.session.commit()
#             return jsonify({"message": "Order updated successfully!"}), 200
#         except ValueError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(order)
#             db.session.commit()
#             return jsonify({"message": "Order deleted successfully!"}), 200
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Failed to delete order: {str(e)}"}), 500
#     else:
#         # GET method to retrieve order details
#         return jsonify({
#             'order_id': order.order_id,
#             'user_id': order.user_id,
#             'order_date': order.order_date,
#             'status': order.status,
#             'total_amount': order.total_amount
#         })
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
#
#
#
#
#
#
#
#
# from flask import Flask, jsonify, request, render_template_string
# from models import db, Review
# from sqlalchemy.exc import SQLAlchemyError
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/finaldb'
#
# # Initialize the database
# db.init_app(app)
#
# # Create the database tables
# with app.app_context():
#     db.create_all()
#
# def add_review_to_database(review_id, product_id, user_id, rating, review_text, review_date, reviewscol):
#     new_review = Review(
#         review_id=review_id,
#         product_id=product_id,
#         user_id=user_id,
#         rating=rating,
#         review_text=review_text,
#         review_date=review_date,
#         reviewscol=reviewscol
#     )
#     db.session.add(new_review)
#     try:
#         db.session.commit()
#         return True
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         app.logger.error(f"Failed to add review to database: {e}")
#         return False
#
# @app.route('/add_review', methods=['POST', 'GET'])
# def add_review():
#     if request.method == 'POST':
#         try:
#             review_id = int(request.form.get('review_id', ''))
#             product_id = request.form.get('product_id', '')
#             user_id = request.form.get('user_id', '')
#             rating = request.form.get('rating', '')
#             review_text = request.form.get('review_text', '')
#             review_date = request.form.get('review_date', '')
#             reviewscol = request.form.get('reviewscol', '')
#
#             if not all([review_id, product_id, user_id, rating, review_text, review_date, reviewscol]):
#                 return jsonify({"error": "All fields must be provided and valid."}), 400
#
#             result = add_review_to_database(review_id, product_id, user_id, rating, review_text, review_date, reviewscol)
#             if result:
#                 return jsonify({"message": "Review added successfully!"}), 201
#             else:
#                 return jsonify({"error": "Failed to add review to the database"}), 500
#         except ValueError as e:
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     return render_template_string('''
#         <!-- Form for adding review -->
#         <form method="post">
#             Review ID: <input type="number" name="review_id"><br>
#             Product ID: <input type="text" name="product_id"><br>
#             User ID: <input type="text" name="user_id"><br>
#             Rating: <input type="text" name="rating"><br>
#             Review Text: <input type="text" name="review_text"><br>
#             Review Date: <input type="text" name="review_date"><br>
#             Additional Info: <input type="text" name="reviewscol"><br>
#             <input type="submit" value="Add Review">
#         </form>
#     ''')
#
# @app.route('/reviews', methods=['GET'])
# def get_reviews():
#     # Query all reviews from the database
#     reviews = Review.query.all()
#     # Convert the query result to a list of dictionaries
#     review_list = [{
#         'review_id': review.review_id,
#         'product_id': review.product_id,
#         'user_id': review.user_id,
#         'rating': review.rating,
#         'review_text': review.review_text,
#         'review_date': review.review_date,
#         'reviewscol': review.reviewscol
#     } for review in reviews]
#     return jsonify(review_list)
#
# @app.route('/reviews/<int:review_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_review(review_id):
#     review = Review.query.get(review_id)
#     if not review:
#         return jsonify({"error": "Review not found"}), 404
#
#     if request.method == 'PUT':
#         try:
#             review.product_id = request.form.get('product_id', review.product_id)
#             review.user_id = request.form.get('user_id', review.user_id)
#             review.rating = request.form.get('rating', review.rating)
#             review.review_text = request.form.get('review_text', review.review_text)
#             review.review_date = request.form.get('review_date', review.review_date)
#             review.reviewscol = request.form.get('reviewscol', review.reviewscol)
#             db.session.commit()
#             return jsonify({"message": "Review updated successfully!"}), 200
#         except ValueError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     elif request.method == 'DELETE':
#         try {
#             db.session.delete(review)
#             db.session.commit()
#             return jsonify({"message": "Review deleted successfully!"}), 200
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Failed to delete review: {str(e)}"}), 500
#     else:
#         # GET method to retrieve review details
#         return jsonify({
#             'review_id': review.review_id,
#             'product_id': review.product_id,
#             'user_id': review.user_id,
#             'rating': review.rating,
#             'review_text': review.review_text,
#             'review_date': review.review_date,
#             'reviewscol': review.reviewscol
#         })
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#




# from flask import Flask, jsonify, request, render_template_string
# from models import db, Wishlist
# from sqlalchemy.exc import SQLAlchemyError
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/finaldb'
#
# # Initialize the database
# db.init_app(app)
#
# # Create the database tables
# with app.app_context():
#     db.create_all()
#
# def add_wishlist_entry_to_database(favorite_id, user_id, pr oduct_id):
#     new_wishlist_entry = Wishlist(
#         favorite_id=favorite_id,
#         user_id=user_id,
#         product_id=product_id
#     )
#     db.session.add(new_wishlist_entry)
#     try:
#         db.session.commit()
#         return True
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         app.logger.error(f"Failed to add wishlist entry to database: {e}")
#         return False
#
# @app.route('/add_wishlist', methods=['POST', 'GET'])
# def add_wishlist():
#     if request.method == 'POST':
#         try:
#             favorite_id = int(request.form.get('favorite_id', ''))
#             user_id = request.form.get('user_id', '')
#             product_id = request.form.get('product_id', '')
#
#             if not all([favorite_id, user_id, product_id]):
#                 return jsonify({"error": "All fields must be provided and valid."}), 400
#
#             result = add_wishlist_entry_to_database(favorite_id, user_id, product_id)
#             if result:
#                 return jsonify({"message": "Wishlist entry added successfully!"}), 201
#             else:
#                 return jsonify({"error": "Failed to add wishlist entry to the database"}), 500
#         except ValueError as e:
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     return render_template_string('''
#         <!-- Form for adding wishlist entry -->
#         <form method="post">
#             Favorite ID: <input type="number" name="favorite_id"><br>
#             User ID: <input type="text" name="user_id"><br>
#             Product ID: <input type="text" name="product_id"><br>
#             <input type="submit" value="Add to Wishlist">
#         </form>
#     ''')
#
# @app.route('/wishlist', methods=['GET'])
# def get_wishlist():
#     # Query all wishlist entries from the database
#     wishlist_entries = Wishlist.query.all()
#     # Convert the query result to a list of dictionaries
#     wishlist_list = [{
#         'favorite_id': entry.favorite_id,
#         'user_id': entry.user_id,
#         'product_id': entry.product_id
#     } for entry in wishlist_entries]
#     return jsonify(wishlist_list)
#
# @app.route('/wishlist/<int:favorite_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_wishlist_entry(favorite_id):
#     wishlist_entry = Wishlist.query.get(favorite_id)
#     if not wishlist_entry:
#         return jsonify({"error": "Wishlist entry not found"}), 404
#
#     if request.method == 'PUT':
#         try:
#             wishlist_entry.user_id = request.form.get('user_id', wishlist_entry.user_id)
#             wishlist_entry.product_id = request.form.get('product_id', wishlist_entry.product_id)
#             db.session.commit()
#             return jsonify({"message": "Wishlist entry updated successfully!"}), 200
#         except ValueError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Invalid input data: {e}"}), 400
#
#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(wishlist_entry)
#             db.session.commit()
#             return jsonify({"message": "Wishlist entry deleted successfully!"}), 200
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({"error": f"Failed to delete wishlist entry: {str(e)}"}), 500
#     else:
#         # GET method to retrieve wishlist entry details
#         return jsonify({
#             'favorite_id': wishlist_entry.favorite_id,
#             'user_id': wishlist_entry.user_id,
#             'product_id': wishlist_entry.product_id
#         })
#
# if __name__ == '__main__':
#     app.run(debug=True)








