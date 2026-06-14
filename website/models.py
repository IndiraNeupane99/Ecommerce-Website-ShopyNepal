# from . import db
# from flask_login import UserMixin
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash


# class Customer(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     username = db.Column(db.String(100))
#     password_hash = db.Column(db.String(150))
#     date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

#     cart_items = db.relationship('Cart', backref=db.backref('customer', lazy=True))
#     orders = db.relationship('Order', backref=db.backref('customer', lazy=True))

#     @property
#     def password(self):
#         raise AttributeError('Password is not a readable Attribute')

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password=password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password=password)

#     def __str__(self):
#         return '<Customer %r>' % Customer.id


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_name = db.Column(db.String(100), nullable=False)
#     current_price = db.Column(db.Float, nullable=False)
#     previous_price = db.Column(db.Float, nullable=False)
#     in_stock = db.Column(db.Integer, nullable=False)
#     product_picture = db.Column(db.String(1000), nullable=False)
#     flash_sale = db.Column(db.Boolean, default=False)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)

#     carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
#     orders = db.relationship('Order', backref=db.backref('product', lazy=True))

#     def __str__(self):
#         return '<Product %r>' % self.product_name


# class Cart(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quantity = db.Column(db.Integer, nullable=False)

#     customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#     product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

#     # customer product

#     def __str__(self):
#         return '<Cart %r>' % self.id


# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quantity = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(100), nullable=False)
#     payment_id = db.Column(db.String(1000), nullable=False)

#     customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#     product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

#     # customer

#     def __str__(self):
#         return '<Order %r>' % self.id




from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
 
 
CATEGORIES = [
    'Supermarket',
    'Health & Beauty',
    'Home & Office',
    'Fashion',
    'Electronics',
    'Gaming',
    'Baby Products',
    'Sporting Goods',
    'Garden & Outdoor',
]
 
SUBCATEGORY_MAP = {
    'Supermarket': ['Rice & Staples', 'Snacks & Packaged Food', 'Beverages', 'Dairy Products', 'Cooking Essentials'],
    'Health & Beauty': ['Skincare', 'Haircare', 'Makeup', 'Fragrances', 'Personal Care'],
    'Home & Office': ['Furniture', 'Kitchen & Dining', 'Home Decor', 'Cleaning Supplies', 'Office Supplies'],
    'Fashion': ['Men’s Wear', 'Women’s Wear', 'Footwear', 'Bags', 'Accessories'],
    'Electronics': ['Televisions', 'Home Appliances', 'Audio Devices', 'Computer Accessories', 'Gadgets'],
    'Gaming': ['Consoles', 'Controllers', 'PC Gaming', 'Video Games', 'Gaming Accessories'],
    'Baby Products': ['Baby Clothing', 'Diapers & Wipes', 'Toys', 'Feeding Essentials', 'Baby Care'],
    'Sporting Goods': ['Fitness Equipment', 'Gym Accessories', 'Outdoor Sports', 'Sportswear', 'Cycling'],
    'Garden & Outdoor': ['Plants & Seeds', 'Gardening Tools', 'Outdoor Furniture', 'Camping & BBQ', 'Planters'],
}
 
 
class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
 
    # Profile information for orders
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    street_address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))

    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)
 
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)
 
    def __str__(self):
        return '<Customer %r>' % Customer.id
 
 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=True, default=None)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    # NEW: category field
    category = db.Column(db.String(100), nullable=False, default='Supermarket')
    subcategory = db.Column(db.String(100), nullable=True, default='')
    is_taxable = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)
    sku = db.Column(db.String(50), unique=True, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
 
    @property
    def is_low_stock(self):
        return self.in_stock < 10
 
    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    order_items = db.relationship('Order', back_populates='product')
 
    def __str__(self):
        return '<Product %r>' % self.product_name
 
 
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
 
    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
 
    def __str__(self):
        return '<Cart %r>' % self.id
 
 
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    vat_amount = db.Column(db.Float, nullable=True)
    delivery_fee = db.Column(db.Float, nullable=True)
    total_amount_paid = db.Column(db.Float, nullable=True)
    tax_rate_applied = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(100), nullable=False, default='Pending')
    payment_id = db.Column(db.String(1000))
    payment_method = db.Column(db.String(50), nullable=False, default='stripe')  # 'stripe' or 'cod'

    # Delivery information
    delivery_full_name = db.Column(db.String(100))
    delivery_phone = db.Column(db.String(20))
    delivery_street = db.Column(db.String(200))
    delivery_city = db.Column(db.String(100))
    delivery_zip = db.Column(db.String(20))

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', back_populates='order_items')

    def __str__(self):
        return '<Order %r>' % self.id


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    customer = db.relationship('Customer', backref=db.backref('wishlist_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('wishlist_entries', lazy=True))

    def __str__(self):
        return f'<Wishlist {self.customer.username} - {self.product.product_name}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # 'customer' or 'admin'
    subject = db.Column(db.String(200))
    message_text = db.Column(db.Text, nullable=False)
    read_status = db.Column(db.Boolean, default=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', backref=db.backref('messages', lazy=True))

    def __str__(self):
        return f'<Message from {self.sender_type} to Customer {self.customer_id}>'


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_subscribed = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __str__(self):
        return f'<Subscriber {self.email}>'