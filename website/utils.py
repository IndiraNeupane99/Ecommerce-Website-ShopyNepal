import os
import re
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from .config import VAT_RATE, DELIVERY_CHARGE, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function

def is_admin(user):
    return user.id == 1

def validate_file_upload(file):
    if not file:
        return False, 'No file provided'
    
    if file.filename == '':
        return False, 'No file selected'
    
    if not allowed_file(file.filename):
        return False, 'File type not allowed'
    
    if file.content_length and file.content_length > MAX_FILE_SIZE:
        return False, f'File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit'
    
    return True, None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_cart_totals(cart_items):
    base_amount = sum(item.product.current_price * item.quantity for item in cart_items)
    vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart_items if item.product.is_taxable)
    delivery_charge = DELIVERY_CHARGE
    total_amount = base_amount + vat_amount + delivery_charge
    return base_amount, vat_amount, total_amount

def create_order_from_cart(cart_items, customer, payment_id=None, payment_method='stripe'):
    from .models import Order, db
    orders = []
    for item in cart_items:
        order = Order(
            order_number=f"ORD-{customer.id}-{item.product.id}-{item.id}",
            quantity=item.quantity,
            price=item.product.current_price,
            status='Pending',
            payment_id=payment_id or '',
            payment_method=payment_method,
            delivery_full_name=customer.full_name,
            delivery_phone=customer.phone_number,
            delivery_street=customer.street_address,
            delivery_city=customer.city,
            delivery_zip=customer.zip_code,
            customer_link=customer.id,
            product_link=item.product.id
        )
        db.session.add(order)
        orders.append(order)
    
    # Remove cart items
    for item in cart_items:
        db.session.delete(item)
    
    db.session.commit()
    return orders

def validate_password_strength(password):
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter'
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain at least one lowercase letter'
    if not re.search(r'\d', password):
        return False, 'Password must contain at least one digit'
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, 'Password must contain at least one special character'
    return True, None

def sanitize_input(text):
    if not text:
        return text
    # Remove potentially dangerous characters
    return re.sub(r'[<>]', '', text).strip()