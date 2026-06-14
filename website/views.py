# from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for
# from .models import Product, Cart, Order
# from flask_login import login_required, current_user
# from . import db
# from .config import DELIVERY_CHARGE, VAT_RATE
# import stripe
# import os

# views = Blueprint('views', __name__)

# stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', )
# STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', )


# # @views.route('/')
# # def home():
# #     items = (
# #         Product.query.filter_by(flash_sale=True)
# #         .order_by(Product.date_added.desc())
# #         .all()
# #     )
# #     if not items:
# #         items = Product.query.order_by(Product.date_added.desc()).limit(12).all()
# #         # items = Product.query.order_by(Product.date_added.desc()).limit(8).all()
# #         # items = Product.query.filter_by(product_name="Smart Watch").all()

# #     return render_template(
# #         'home.html',
# #         items=items,
# #         cart=Cart.query.filter_by(customer_link=current_user.id).all()
# #         if current_user.is_authenticated else [],
# #     )


# # @views.route('/add-to-cart/<int:item_id>')
# # @login_required
# # def add_to_cart(item_id):
# #     item_to_add = Product.query.get(item_id)
# #     if item_to_add is None:
# #         flash('That product is not available.')
# #         return redirect(request.referrer or '/')

# #     item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
# #     if item_exists:
# #         try:
# #             item_exists.quantity += 1
# #             db.session.commit()
# #             flash(f'Quantity of {item_exists.product.product_name} has been updated')
# #             return redirect(request.referrer or '/')
# #         except Exception as e:
# #             print('Quantity not updated:', e)
# #             flash(f'Quantity of {item_exists.product.product_name} not updated')
# #             return redirect(request.referrer or '/')

# #     new_cart_item = Cart()
# #     new_cart_item.quantity = 1
# #     new_cart_item.product_link = item_to_add.id
# #     new_cart_item.customer_link = current_user.id

# #     try:
# #         db.session.add(new_cart_item)
# #         db.session.commit()
# #         flash(f'{new_cart_item.product.product_name} added to cart')
# #     except Exception as e:
# #         print('Item not added to cart:', e)
# #         flash(f'{new_cart_item.product.product_name} has not been added to cart')

# #     return redirect(request.referrer or '/')


# # @views.route('/cart')
# # @login_required
# # def show_cart():
# #     cart = Cart.query.filter_by(customer_link=current_user.id).all()
# #     amount = sum(item.product.current_price * item.quantity for item in cart)
# #     return render_template(
# #         'cart.html',
# #         cart=cart,
# #         amount=amount,
# #         total=amount + 200,
# #         stripe_publishable_key=STRIPE_PUBLISHABLE_KEY
# #     )


# # @views.route('/pluscart')
# # @login_required
# # def plus_cart():
# #     cart_id = request.args.get('cart_id')
# #     cart_item = Cart.query.get(cart_id)
# #     if not cart_item or cart_item.customer_link != current_user.id:
# #         return jsonify({'error': 'Cart item not found'}), 404

# #     cart_item.quantity += 1
# #     db.session.commit()

# #     cart = Cart.query.filter_by(customer_link=current_user.id).all()
# #     amount = sum(item.product.current_price * item.quantity for item in cart)

# #     return jsonify({
# #         'quantity': cart_item.quantity,
# #         'amount': amount,
# #         'total': amount + 200
# #     })


# # @views.route('/minuscart')
# # @login_required
# # def minus_cart():
# #     cart_id = request.args.get('cart_id')
# #     cart_item = Cart.query.get(cart_id)
# #     if not cart_item or cart_item.customer_link != current_user.id:
# #         return jsonify({'error': 'Cart item not found'}), 404

# #     if cart_item.quantity > 1:
# #         cart_item.quantity -= 1
# #         new_qty = cart_item.quantity
# #     else:
# #         new_qty = 0
# #         db.session.delete(cart_item)

# #     db.session.commit()

# #     cart = Cart.query.filter_by(customer_link=current_user.id).all()
# #     amount = sum(item.product.current_price * item.quantity for item in cart)

# #     return jsonify({
# #         'quantity': new_qty,
# #         'amount': amount,
# #         'total': amount + 200
# #     })


# # @views.route('/removecart')
# # @login_required
# # def remove_cart():
# #     cart_id = request.args.get('cart_id')
# #     cart_item = Cart.query.get(cart_id)
# #     if not cart_item or cart_item.customer_link != current_user.id:
# #         return jsonify({'error': 'Cart item not found'}), 404

# #     quantity_in_cart = cart_item.quantity
# #     db.session.delete(cart_item)
# #     db.session.commit()

# #     cart = Cart.query.filter_by(customer_link=current_user.id).all()
# #     amount = sum(item.product.current_price * item.quantity for item in cart)

# #     return jsonify({
# #         'quantity': quantity_in_cart,
# #         'amount': amount,
# #         'total': amount + 200
# #     })


# # @views.route('/create-checkout-session', methods=['POST'])
# # @login_required
# # def create_checkout_session():
# #     customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
# #     if not customer_cart:
# #         flash('Your cart is empty')
# #         return redirect('/')

# #     for item in customer_cart:
# #         product = Product.query.get(item.product_link)
# #         if product is None or product.in_stock < item.quantity:
# #             flash(f'Product "{item.product.product_name}" is out of stock or has insufficient quantity.')
# #             return redirect('/cart')

# #     line_items = []
# #     for item in customer_cart:
# #         line_items.append({
# #             'price_data': {
# #                 'currency': 'npr',  # Nepali Rupee
# #                 'product_data': {
# #                     'name': item.product.product_name,
# #                 },
# #                 'unit_amount': int(item.product.current_price * 100),
# #             },
# #             'quantity': item.quantity,
# #         })

# #     # Delivery charge
# #     line_items.append({
# #         'price_data': {
# #             'currency': 'npr',  # Nepali Rupee
# #             'product_data': {
# #                 'name': 'Delivery Charge',
# #             },
# #             'unit_amount': 20000,  # NPR 200 in cents
# #         },
# #         'quantity': 1,
# #     })

# #     try:
# #         session = stripe.checkout.Session.create(
# #             payment_method_types=['card'],
# #             line_items=line_items,
# #             mode='payment',
# #             success_url=url_for('views.payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
# #             cancel_url=url_for('views.payment_cancel', _external=True),
# #             customer_email=current_user.email,
# #         )
# #         return redirect(session.url, code=303)
# #     except Exception as e:
# #         print('Stripe session error:', e)
# #         flash('Payment session could not be created. Please try again.')
# #         return redirect('/cart')


# # @views.route('/payment-success')
# # @login_required
# # def payment_success():
# #     session_id = request.args.get('session_id')

# #     try:
# #         session = stripe.checkout.Session.retrieve(session_id)

# #         if session.payment_status == 'paid':
# #             customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()

# #             if not customer_cart:
# #                 flash('Order already processed or cart is empty.')
# #                 return redirect('/orders')

# #             for item in customer_cart:
# #                 product = Product.query.get(item.product_link)
# #                 if product and product.in_stock >= item.quantity:
# #                     new_order = Order(
# #                         quantity=item.quantity,
# #                         price=item.product.current_price,
# #                         status='Paid',
# #                         payment_id=session_id,
# #                         product_link=item.product_link,
# #                         customer_link=item.customer_link
# #                     )
# #                     db.session.add(new_order)
# #                     product.in_stock -= item.quantity
# #                     db.session.delete(item)

# #             db.session.commit()
# #             flash('Payment successful! Your order has been placed.')
# #             return redirect('/orders')
# #         else:
# #             flash('Payment was not completed.')
# #             return redirect('/cart')

# #     except Exception as e:
# #         print('Payment verification error:', e)
# #         db.session.rollback()
# #         flash('There was an error verifying your payment.')
# #         return redirect('/cart')


# # @views.route('/payment-cancel')
# # @login_required
# # def payment_cancel():
# #     flash('Payment was cancelled. Your cart is saved.')
# #     return redirect('/cart')


# # @views.route('/orders')
# # @login_required
# # def order():
# #     orders = Order.query.filter_by(customer_link=current_user.id).all()
# #     return render_template('orders.html', orders=orders)


# # @views.route('/search', methods=['GET', 'POST'])
# # def search():
# #     if request.method == 'POST':
# #         search_query = request.form.get('search')
# #         items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
# #         return render_template(
# #             'search.html',
# #             items=items,
# #             cart=Cart.query.filter_by(customer_link=current_user.id).all()
# #             if current_user.is_authenticated else []
# #         )
# #     return render_template('search.html')



# # views.py
# from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for, session
# from flask_login import login_required, current_user
# from .models import Product, Cart, Order, Wishlist, Customer, Message
# from . import db
# from .config import DELIVERY_CHARGE, VAT_RATE
# import stripe
# import os
# from datetime import datetime, timezone, timedelta
# import uuid

# # Nepal Standard Time (UTC+5:45)
# NEPAL_TZ = timezone(timedelta(hours=5, minutes=45))

# def get_nepal_time():
#     "Return current Nepal time."
#     return datetime.now(NEPAL_TZ).strftime('%b %d, %Y %I:%M %p NPT')


# def to_nepal_time(dt):
#     "Convert UTC datetime → Nepal time."
#     if not dt:
#         return 

#     # If naive, assume it's UTC (correct for your DB)
#     if dt.tzinfo is None:
#         dt = dt.replace(tzinfo=timezone.utc)

#     return dt.astimezone(NEPAL_TZ).strftime('%b %d, %Y %I:%M %p NPT')

# views = Blueprint('views', __name__)

# @views.app_template_filter('nst')
# def nst_filter(dt):
#     "Jinja2 filter: {{ order.date_ordered | nst }} → Nepal time string"
#     return to_nepal_time(dt)

# @views.app_template_global('nepal_now')
# def nepal_now():
#     "Jinja2 global: {{ nepal_now() }} → current Nepal time string"
#     return get_nepal_time()
 
# stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', )
# STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', )
 
 
# def get_cart():
#     if current_user.is_authenticated:
#         return Cart.query.filter_by(customer_link=current_user.id).all()
#     else:
#         return session.get('guest_cart', [])

 
 
# @views.route('/')
# def home():
#     items = (
#         Product.query.filter_by(flash_sale=True)
#         .order_by(Product.date_added.desc())
#         .all()
#     )
#     if not items:
#         items = Product.query.order_by(Product.date_added.desc()).limit(12).all()
 
#     return render_template('home.html', items=items, cart=get_cart())
 
 
# @views.route('/subscribe', methods=['POST'])
# def subscribe():
#     email = request.form.get('email')
#     if not email:
#         return jsonify({'success': False, 'message': 'Email is required'}), 400
    
#     # Check if already subscribed
#     from .models import Subscriber
#     existing = Subscriber.query.filter_by(email=email).first()
#     if existing:
#         if existing.is_active:
#             return jsonify({'success': False, 'message': 'You are already subscribed'}), 400
#         else:
#             # Reactivate
#             existing.is_active = True
#             db.session.commit()
#             return jsonify({'success': True, 'message': 'Subscription reactivated successfully!'})
    
#     # Add new subscriber
#     new_subscriber = Subscriber(email=email)
#     try:
#         db.session.add(new_subscriber)
#         db.session.commit()
#         return jsonify({'success': True, 'message': 'Successfully subscribed to newsletter!'})
#     except Exception as e:
#         db.session.rollback()
#         print('Subscription error:', e)
#         return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500



# @views.route('/supermarket')
# def supermarket():
#     items = Product.query.filter_by(category='Supermarket').order_by(Product.date_added.desc()).all()
#     return render_template('supermarket.html', items=items, cart=get_cart(), category='Supermarket')


# @views.route('/health-beauty')
# def health_beauty():
#     items = Product.query.filter_by(category='Health & Beauty').order_by(Product.date_added.desc()).all()
#     return render_template('healthbeauty.html', items=items, cart=get_cart(), category='Health & Beauty')


# @views.route('/home-office')
# def home_office():
#     items = Product.query.filter_by(category='Home & Office').order_by(Product.date_added.desc()).all()
#     return render_template('homeoffice.html', items=items, cart=get_cart(), category='Home & Office')
 
 
# @views.route('/fashion')
# def fashion():
#     items = Product.query.filter_by(category='Fashion').order_by(Product.date_added.desc()).all()
#     return render_template('fashion.html', items=items, cart=get_cart(), category='Fashion')
 
 
# @views.route('/electronics')
# def electronics():
#     items = Product.query.filter_by(category='Electronics').order_by(Product.date_added.desc()).all()
#     return render_template('Electronic.html', items=items, cart=get_cart(), category='Electronics')
 
 
# @views.route('/gaming')
# def gaming():
#     items = Product.query.filter_by(category='Gaming').order_by(Product.date_added.desc()).all()
#     return render_template('gaming.html', items=items, cart=get_cart(), category='Gaming')
 
 
# @views.route('/baby-products')
# def baby_products():
#     items = Product.query.filter_by(category='Baby Products').order_by(Product.date_added.desc()).all()
#     return render_template('babyproducts.html', items=items, cart=get_cart(), category='Baby Products')
 
 
# @views.route('/sporting-goods')
# def sporting_goods():
#     items = Product.query.filter_by(category='Sporting Goods').order_by(Product.date_added.desc()).all()
#     return render_template('sport.html', items=items, cart=get_cart(), category='Sporting Goods')
 
 
# @views.route('/garden-outdoor')
# def garden_outdoor():
#     items = Product.query.filter_by(category='Garden & Outdoor').order_by(Product.date_added.desc()).all()
#     return render_template('garden.html', items=items, cart=get_cart(), category='Garden & Outdoor')
 
 
# # ── Cart & Checkout ──────────────────────────────────────────────────────────
 
# @views.route('/add-to-cart/<int:item_id>')
# # @login_required
# def add_to_cart(item_id):
#     item_to_add = Product.query.get(item_id)
#     is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
#     if item_to_add is None:
#         if is_ajax:
#             return jsonify({'success': False, 'message': 'That product is not available.'}), 404
#         flash('That product is not available.', 'error')
#         return redirect(request.referrer or '/')
 
#     item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
#     if item_exists:
#         try:
#             item_exists.quantity += 1
#             db.session.commit()
#             success_message = f'Quantity of {item_exists.product.product_name} has been updated'
#             if is_ajax:
#                 cart = Cart.query.filter_by(customer_link=current_user.id).all()
#                 cart_total = len(cart)
#                 return jsonify({
#                     'success': True,
#                     'message': success_message,
#                     'product_name': item_exists.product.product_name,
#                     'product_id': item_to_add.id,
#                     'quantity': item_exists.quantity,
#                     'price': item_to_add.current_price,
#                     'cart_count': cart_total,
#                     'is_new': False
#                 })
#             else:
#                 flash(success_message)
#                 return redirect(request.referrer or '/')
#         except Exception as e:
#             error_msg = f'Quantity of {item_exists.product.product_name} not updated'
#             print('Quantity not updated:', e)
#             if is_ajax:
#                 return jsonify({'success': False, 'message': error_msg}), 500
#             flash(error_msg)
#             return redirect(request.referrer or '/')
 
#     new_cart_item = Cart()
#     new_cart_item.quantity = 1
#     new_cart_item.product_link = item_to_add.id
#     new_cart_item.customer_link = current_user.id
 
#     try:
#         db.session.add(new_cart_item)
#         db.session.commit()
#         success_message = f'{new_cart_item.product.product_name} added to cart'
#         if is_ajax:
#             cart = Cart.query.filter_by(customer_link=current_user.id).all()
#             cart_total = len(cart)
#             return jsonify({
#                 'success': True,
#                 'message': success_message,
#                 'product_name': new_cart_item.product.product_name,
#                 'product_id': item_to_add.id,
#                 'quantity': new_cart_item.quantity,
#                 'price': item_to_add.current_price,
#                 'product_image': item_to_add.product_picture,
#                 'cart_count': cart_total,
#                 'is_new': True
#             })
#         else:
#             flash(success_message, 'success')
#     except Exception as e:
#         error_msg = f'{new_cart_item.product.product_name} has not been added to cart'
#         print('Item not added to cart:', e)
#         if is_ajax:
#             return jsonify({'success': False, 'message': error_msg}), 500
#         flash(error_msg, 'error')
 
#     return redirect(request.referrer or '/')
 
 
# @views.route('/cart')
# # @login_required
# def show_cart():
#     cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     base_amount = sum(item.product.current_price * item.quantity for item in cart)
#     vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#     total_amount = base_amount + vat_amount + DELIVERY_CHARGE
#     return render_template(
#         'cart.html',
#         cart=cart,
#         amount=base_amount,
#         vat_amount=vat_amount,
#         total=total_amount,
#         stripe_publishable_key=STRIPE_PUBLISHABLE_KEY
#     )


# @views.route('/checkout', methods=['GET', 'POST'])
# @login_required
# def checkout():
#     from .forms import CheckoutForm

#     cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     if not cart:
#         flash('Your cart is empty.', 'error')
#         return redirect('/cart')

#     base_amount = sum(item.product.current_price * item.quantity for item in cart)
#     vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#     total_amount = base_amount + vat_amount + DELIVERY_CHARGE

#     form = CheckoutForm()

#     # Pre-fill form with existing customer data if available
#     if current_user.full_name:
#         form.full_name.data = current_user.full_name
#     if current_user.phone_number:
#         form.phone_number.data = current_user.phone_number
#     if current_user.street_address:
#         form.street_address.data = current_user.street_address
#     if current_user.city:
#         form.city.data = current_user.city
#     if current_user.zip_code:
#         form.zip_code.data = current_user.zip_code

#     if form.validate_on_submit():
#         # Update customer profile information
#         current_user.full_name = form.full_name.data
#         current_user.phone_number = form.phone_number.data
#         current_user.street_address = form.street_address.data
#         current_user.city = form.city.data
#         current_user.zip_code = form.zip_code.data

#         payment_method = form.payment_method.data

#         if payment_method == 'stripe':
#             # Redirect to Stripe checkout
#             return redirect('/create-checkout-session')
#         elif payment_method == 'cod':
#             # Process Cash on Delivery order
#             try:
#                 # Calculate totals
#                 base_amount = sum(item.product.current_price * item.quantity for item in cart)
#                 vat_amount_total = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#                 total_paid = base_amount + vat_amount_total + DELIVERY_CHARGE

#                 for i, item in enumerate(cart):
#                     product = Product.query.get(item.product_link)
#                     if product and product.in_stock >= item.quantity:
#                         # Generate unique order number for each item
#                         import uuid
#                         order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
#                         item_vat = (item.product.current_price * VAT_RATE * item.quantity) if item.product.is_taxable else 0
#                         item_delivery = DELIVERY_CHARGE if i == 0 else 0
#                         item_total = item.product.current_price * item.quantity + item_vat + item_delivery
#                         new_order = Order(
#                             order_number=order_number,
#                             quantity=item.quantity,
#                             price=item.product.current_price,
#                             vat_amount=item_vat,
#                             delivery_fee=item_delivery,
#                             total_amount_paid=item_total,
#                             tax_rate_applied=VAT_RATE,
#                             status='Pending',
#                             payment_method='cod',
#                             delivery_full_name=form.full_name.data,
#                             delivery_phone=form.phone_number.data,
#                             delivery_street=form.street_address.data,
#                             delivery_city=form.city.data,
#                             delivery_zip=form.zip_code.data,
#                             product_link=item.product_link,
#                             customer_link=item.customer_link
#                         )
#                         db.session.add(new_order)
#                         product.in_stock -= item.quantity
#                     else:
#                         flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
#                         db.session.rollback()
#                         return redirect('/cart')

#                 # Clear cart after successful order
#                 for item in cart:
#                     db.session.delete(item)

#                 db.session.commit()
#                 flash('Order placed successfully! You will pay cash on delivery.', 'success')
#                 return redirect('/orders')

#             except Exception as e:
#                 print('COD order error:', e)
#                 db.session.rollback()
#                 flash('There was an error placing your order. Please try again.', 'error')
#                 return redirect('/cart')
#         elif payment_method == 'demo':
#             # Process Demo Payment order
#             try:
#                 # Calculate totals
#                 base_amount = sum(item.product.current_price * item.quantity for item in cart)
#                 vat_amount_total = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#                 total_paid = base_amount + vat_amount_total + DELIVERY_CHARGE

#                 for i, item in enumerate(cart):
#                     product = Product.query.get(item.product_link)
#                     if product and product.in_stock >= item.quantity:
#                         # Generate unique order number for each item
#                         import uuid
#                         order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
#                         item_vat = (item.product.current_price * VAT_RATE * item.quantity) if item.product.is_taxable else 0
#                         item_delivery = DELIVERY_CHARGE if i == 0 else 0
#                         item_total = item.product.current_price * item.quantity + item_vat + item_delivery
#                         new_order = Order(
#                             order_number=order_number,
#                             quantity=item.quantity,
#                             price=item.product.current_price,
#                             vat_amount=item_vat,
#                             delivery_fee=item_delivery,
#                             total_amount_paid=item_total,
#                             tax_rate_applied=VAT_RATE,
#                             status='Paid',
#                             payment_method='demo',
#                             payment_id=f"DEMO-{uuid.uuid4().hex[:8].upper()}",
#                             delivery_full_name=form.full_name.data,
#                             delivery_phone=form.phone_number.data,
#                             delivery_street=form.street_address.data,
#                             delivery_city=form.city.data,
#                             delivery_zip=form.zip_code.data,
#                             product_link=item.product_link,
#                             customer_link=item.customer_link
#                         )
#                         db.session.add(new_order)
#                         product.in_stock -= item.quantity
#                     else:
#                         flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
#                         db.session.rollback()
#                         return redirect('/cart')

#                 # Clear cart after successful order
#                 for item in cart:
#                     db.session.delete(item)

#                 db.session.commit()
#                 flash('Demo payment successful! Your order has been placed.', 'success')
#                 return redirect('/orders')

#             except Exception as e:
#                 print('Demo payment order error:', e)
#                 db.session.rollback()
#                 flash('There was an error placing your order. Please try again.', 'error')
#                 return redirect('/cart')

#     return render_template('checkout.html', form=form, cart=cart, amount=base_amount, vat_amount=vat_amount, total=total_amount)


# @views.route('/checkout-single/<int:cart_id>', methods=['GET', 'POST'])
# @login_required
# def checkout_single(cart_id):
#     "Checkout a single item from the cart"
#     from .forms import CheckoutForm
    
#     cart_item = Cart.query.get(cart_id)
#     if not cart_item or cart_item.customer_link != current_user.id:
#         flash('Item not found in your cart.', 'error')
#         return redirect('/cart')
    
#     product = Product.query.get(cart_item.product_link)
#     if not product:
#         flash('Product not found.', 'error')
#         return redirect('/cart')
    
#     # Calculate amount for single item
#     base_amount = product.current_price * cart_item.quantity
#     vat_amount = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
#     total_amount = base_amount + vat_amount + DELIVERY_CHARGE
    
#     form = CheckoutForm()
    
#     # Pre-fill form with existing customer data if available
#     if current_user.full_name:
#         form.full_name.data = current_user.full_name
#     if current_user.phone_number:
#         form.phone_number.data = current_user.phone_number
#     if current_user.street_address:
#         form.street_address.data = current_user.street_address
#     if current_user.city:
#         form.city.data = current_user.city
#     if current_user.zip_code:
#         form.zip_code.data = current_user.zip_code
    
#     if form.validate_on_submit():
#         # Update customer profile information
#         current_user.full_name = form.full_name.data
#         current_user.phone_number = form.phone_number.data
#         current_user.street_address = form.street_address.data
#         current_user.city = form.city.data
#         current_user.zip_code = form.zip_code.data
        
#         payment_method = form.payment_method.data
        
#         if payment_method == 'stripe':
#             # Store cart_id in session for Stripe callback
#             session['single_checkout_cart_id'] = cart_id
#             return redirect('/create-checkout-session-single')
#         elif payment_method == 'cod':
#             # Process Cash on Delivery order for single item
#             try:
#                 if product.in_stock >= cart_item.quantity:
#                     # Generate order number
#                     import uuid
#                     order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                    
#                     item_vat = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
#                     item_total = product.current_price * cart_item.quantity + item_vat + DELIVERY_CHARGE
                    
#                     new_order = Order(
#                         order_number=order_number,
#                         quantity=cart_item.quantity,
#                         price=product.current_price,
#                         vat_amount=item_vat,
#                         delivery_fee=DELIVERY_CHARGE,
#                         total_amount_paid=item_total,
#                         tax_rate_applied=VAT_RATE,
#                         status='Pending',
#                         payment_method='cod',
#                         delivery_full_name=form.full_name.data,
#                         delivery_phone=form.phone_number.data,
#                         delivery_street=form.street_address.data,
#                         delivery_city=form.city.data,
#                         delivery_zip=form.zip_code.data,
#                         product_link=cart_item.product_link,
#                         customer_link=cart_item.customer_link
#                     )
#                     db.session.add(new_order)
#                     product.in_stock -= cart_item.quantity
#                     db.session.delete(cart_item)
#                     db.session.commit()
                    
#                     flash(f'Order placed successfully for {product.product_name}!', 'success')
#                     return redirect('/orders')
#                 else:
#                     flash(f'Insufficient stock for {product.product_name}.', 'error')
#                     return redirect('/cart')
#             except Exception as e:
#                 print('Single COD order error:', e)
#                 db.session.rollback()
#                 flash('There was an error placing your order. Please try again.', 'error')
#                 return redirect('/cart')
#         elif payment_method == 'demo':
#             # Process Demo Payment order for single item
#             try:
#                 if product.in_stock >= cart_item.quantity:
#                     # Generate order number
#                     import uuid
#                     order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                    
#                     item_vat = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
#                     item_total = product.current_price * cart_item.quantity + item_vat + DELIVERY_CHARGE
                    
#                     new_order = Order(
#                         order_number=order_number,
#                         quantity=cart_item.quantity,
#                         price=product.current_price,
#                         vat_amount=item_vat,
#                         delivery_fee=DELIVERY_CHARGE,
#                         total_amount_paid=item_total,
#                         tax_rate_applied=VAT_RATE,
#                         status='Paid',
#                         payment_method='demo',
#                         payment_id=f"DEMO-{uuid.uuid4().hex[:8].upper()}",
#                         delivery_full_name=form.full_name.data,
#                         delivery_phone=form.phone_number.data,
#                         delivery_street=form.street_address.data,
#                         delivery_city=form.city.data,
#                         delivery_zip=form.zip_code.data,
#                         product_link=cart_item.product_link,
#                         customer_link=cart_item.customer_link
#                     )
#                     db.session.add(new_order)
#                     product.in_stock -= cart_item.quantity
#                     db.session.delete(cart_item)
#                     db.session.commit()
                    
#                     flash(f'Demo payment successful! Order placed for {product.product_name}!', 'success')
#                     return redirect('/orders')
#                 else:
#                     flash(f'Insufficient stock for {product.product_name}.', 'error')
#                     return redirect('/cart')
#             except Exception as e:
#                 print('Single demo payment order error:', e)
#                 db.session.rollback()
#                 flash('There was an error placing your order. Please try again.', 'error')
#                 return redirect('/cart')
    
#     return render_template(
#         'checkout-single.html',
#         form=form,
#         cart_item=cart_item,
#         product=product,
#         amount=base_amount,
#         vat_amount=vat_amount,
#         total=total_amount,
#         stripe_publishable_key=STRIPE_PUBLISHABLE_KEY
#     )


# @views.route('/create-checkout-session-single', methods=['GET', 'POST'])
# @login_required
# def create_checkout_session_single():
#     "Create Stripe checkout session for single item"
#     cart_id = session.get('single_checkout_cart_id')
#     if not cart_id:
#         flash('Cart item not found.', 'error')
#         return redirect('/cart')
    
#     cart_item = Cart.query.get(cart_id)
#     if not cart_item or cart_item.customer_link != current_user.id:
#         flash('Cart item not found.', 'error')
#         return redirect('/cart')
    
#     product = Product.query.get(cart_item.product_link)
#     if not product or product.in_stock < cart_item.quantity:
#         flash(f'Product "{product.product_name if product else "Unknown"}" is out of stock.', 'error')
#         return redirect('/cart')
    
#     try:
#         line_items = [
#             {
#                 'price_data': {
#                     'currency': 'npr',
#                     'product_data': {'name': product.product_name},
#                     'unit_amount': int(product.current_price * 100),
#                 },
#                 'quantity': cart_item.quantity,
#             },
#             {
#                 'price_data': {
#                     'currency': 'npr',
#                     'product_data': {'name': 'Delivery Charge'},
#                     'unit_amount': DELIVERY_CHARGE * 100,
#                 },
#                 'quantity': 1,
#             }
#         ]
        
#         stripe_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=url_for('views.payment_success_single', _external=True) + f'?session_id={{CHECKOUT_SESSION_ID}}&cart_id={cart_id}',
#             cancel_url=url_for('views.payment_cancel', _external=True),
#             customer_email=current_user.email,
#         )
        
#         # Clean up session
#         session.pop('single_checkout_cart_id', None)
        
#         return redirect(stripe_session.url, code=303)
#     except Exception as e:
#         print('Stripe single session error:', e)
#         flash('Payment session could not be created. Please try again.', 'error')
#         return redirect('/cart')


# @views.route('/payment-success-single')
# @login_required
# def payment_success_single():
#     "Handle successful Stripe payment for single item"
#     session_id = request.args.get('session_id')
#     cart_id = request.args.get('cart_id')
    
#     if not session_id or not cart_id:
#         flash('Invalid payment session.', 'error')
#         return redirect('/cart')
    
#     try:
#         stripe_session = stripe.checkout.Session.retrieve(session_id)
        
#         if stripe_session.payment_status == 'paid':
#             cart_item = Cart.query.get(cart_id)
#             if not cart_item or cart_item.customer_link != current_user.id:
#                 flash('Cart item not found.', 'error')
#                 return redirect('/orders')
            
#             product = Product.query.get(cart_item.product_link)
#             if product and product.in_stock >= cart_item.quantity:
#                 # Generate order number
#                 import uuid
#                 order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                
#                 item_vat = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
#                 item_total = product.current_price * cart_item.quantity + item_vat + DELIVERY_CHARGE
                
#                 new_order = Order(
#                     order_number=order_number,
#                     quantity=cart_item.quantity,
#                     price=product.current_price,
#                     vat_amount=item_vat,
#                     delivery_fee=DELIVERY_CHARGE,
#                     total_amount_paid=item_total,
#                     tax_rate_applied=VAT_RATE,
#                     status='Paid',
#                     payment_id=session_id,
#                     payment_method='stripe',
#                     product_link=cart_item.product_link,
#                     customer_link=cart_item.customer_link
#                 )
#                 db.session.add(new_order)
#                 product.in_stock -= cart_item.quantity
#                 db.session.delete(cart_item)
#                 db.session.commit()
                
#                 flash('Payment successful! Your order has been placed.', 'success')
#                 return redirect('/orders')
#             else:
#                 flash('Product is out of stock.', 'error')
#                 return redirect('/cart')
#         else:
#             flash('Payment was not completed.', 'error')
#             return redirect('/cart')
    
#     except Exception as e:
#         print('Payment verification error:', e)
#         db.session.rollback()
#         flash('There was an error verifying your payment.', 'error')
#         return redirect('/cart')


# @views.route('/pluscart')
# @login_required
# def plus_cart():
#     cart_id = request.args.get('cart_id')
#     cart_item = Cart.query.get(cart_id)
#     if not cart_item or cart_item.customer_link != current_user.id:
#         return jsonify({'error': 'Cart item not found'}), 404
#     cart_item.quantity += 1
#     db.session.commit()
#     cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     base_amount = sum(item.product.current_price * item.quantity for item in cart)
#     vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#     total_amount = base_amount + vat_amount + DELIVERY_CHARGE
#     return jsonify({'quantity': cart_item.quantity, 'amount': base_amount + vat_amount, 'total': total_amount})
 
 
# @views.route('/minuscart')
# @login_required
# def minus_cart():
#     cart_id = request.args.get('cart_id')
#     cart_item = Cart.query.get(cart_id)
#     if not cart_item or cart_item.customer_link != current_user.id:
#         return jsonify({'error': 'Cart item not found'}), 404
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         new_qty = cart_item.quantity
#     else:
#         new_qty = 0
#         db.session.delete(cart_item)
#     db.session.commit()
#     cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     base_amount = sum(item.product.current_price * item.quantity for item in cart)
#     vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#     total_amount = base_amount + vat_amount + DELIVERY_CHARGE
#     return jsonify({'quantity': new_qty, 'amount': base_amount + vat_amount, 'total': total_amount})
 
 
# @views.route('/removecart')
# @login_required
# def remove_cart():
#     cart_id = request.args.get('cart_id')
#     cart_item = Cart.query.get(cart_id)
#     if not cart_item or cart_item.customer_link != current_user.id:
#         return jsonify({'error': 'Cart item not found'}), 404
#     quantity_in_cart = cart_item.quantity
#     db.session.delete(cart_item)
#     db.session.commit()
#     cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     base_amount = sum(item.product.current_price * item.quantity for item in cart)
#     vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
#     total_amount = base_amount + vat_amount + DELIVERY_CHARGE
#     return jsonify({'quantity': quantity_in_cart, 'amount': base_amount + vat_amount, 'total': total_amount})
 
 
# @views.route('/create-checkout-session', methods=['GET', 'POST'])
# @login_required
# def create_checkout_session():
#     customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     if not customer_cart:
#         flash('Your cart is empty.', 'error')
#         return redirect('/')

#     for item in customer_cart:
#         product = Product.query.get(item.product_link)
#         if product is None or product.in_stock < item.quantity:
#             flash(f'Product "{item.product.product_name}" is out of stock or has insufficient quantity.', 'error')
#             return redirect('/cart')

#     # Check if customer has delivery information
#     if not current_user.full_name or not current_user.phone_number or not current_user.street_address:
#         flash('Please complete your delivery information before proceeding with payment.', 'error')
#         return redirect('/checkout')

#     line_items = []
#     for item in customer_cart:
#         product = Product.query.get(item.product_link)
#         if product:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'npr',
#                     'product_data': {'name': product.product_name},
#                     'unit_amount': int(product.current_price * 100),
#                 },
#                 'quantity': item.quantity,
#             })

#     line_items.append({
#         'price_data': {
#             'currency': 'npr',
#             'product_data': {'name': 'Delivery Charge'},
#             'unit_amount': DELIVERY_CHARGE * 100,
#         },
#         'quantity': 1,
#     })
 
#     try:
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=url_for('views.payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url=url_for('views.payment_cancel', _external=True),
#             customer_email=current_user.email,
#         )
#         return redirect(session.url, code=303)
#     except Exception as e:
#         print('Stripe session error:', e)
#         flash('Payment session could not be created. Please try again.', 'error')
#         return redirect('/cart')
 
 
# @views.route('/payment-success')
# @login_required
# def payment_success():
#     session_id = request.args.get('session_id')
#     try:
#         session = stripe.checkout.Session.retrieve(session_id)
#         if session.payment_status == 'paid':
#             customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
#             if not customer_cart:
#                 flash('Order already processed or cart is empty.', 'error')
#                 return redirect('/orders')

#             # Generate order number
#             import uuid
#             order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

#             # Calculate totals
#             base_amount = sum(item.product.current_price * item.quantity for item in customer_cart)
#             vat_amount_total = sum((item.product.current_price * VAT_RATE * item.quantity) for item in customer_cart if item.product.is_taxable)
#             total_paid = base_amount + vat_amount_total + DELIVERY_CHARGE

#             for i, item in enumerate(customer_cart):
#                 product = Product.query.get(item.product_link)
#                 if product and product.in_stock >= item.quantity:
#                     item_vat = (item.product.current_price * VAT_RATE * item.quantity) if item.product.is_taxable else 0
#                     item_delivery = DELIVERY_CHARGE if i == 0 else 0  # Delivery on first item
#                     item_total = item.product.current_price * item.quantity + item_vat + item_delivery
#                     new_order = Order(
#                         order_number=order_number,
#                         quantity=item.quantity,
#                         price=item.product.current_price,
#                         vat_amount=item_vat,
#                         delivery_fee=item_delivery,
#                         total_amount_paid=item_total,
#                         tax_rate_applied=VAT_RATE,
#                         status='Paid',
#                         payment_id=session_id,
#                         payment_method='stripe',
#                         delivery_full_name=current_user.full_name,
#                         delivery_phone=current_user.phone_number,
#                         delivery_street=current_user.street_address,
#                         delivery_city=current_user.city,
#                         delivery_zip=current_user.zip_code,
#                         product_link=item.product_link,
#                         customer_link=item.customer_link
#                     )
#                     db.session.add(new_order)
#                     product.in_stock -= item.quantity
#                 else:
#                     flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
#                     db.session.rollback()
#                     return redirect('/cart')

#             # Clear cart after successful order
#             for item in customer_cart:
#                 db.session.delete(item)

#             db.session.commit()
#             flash('Payment successful! Your order has been placed.', 'success')
#             return redirect('/orders')
#         else:
#             flash('Payment was not completed.', 'error')
#             return redirect('/cart')
#     except Exception as e:
#         print('Payment verification error:', e)
#         db.session.rollback()
#         flash('There was an error verifying your payment.', 'error')
#         return redirect('/cart')
 
 
# @views.route('/payment-cancel')
# @login_required
# def payment_cancel():
#     flash('Payment was cancelled. Your cart is saved.', 'info')
#     return redirect('/cart')
 
 
# @views.route('/orders')
# @login_required
# def order():
#     orders = Order.query.filter_by(customer_link=current_user.id).all()
#     return render_template('orders.html', orders=orders)
 
 
# @views.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         search_query = request.form.get('search')
#         items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
#         return render_template('search.html', items=items, cart=get_cart())
#     return render_template('search.html')


# # ── Wishlist Routes ──────────────────────────────────────────────────────────

# @views.route('/add-to-wishlist/<int:item_id>')
# @login_required
# def add_to_wishlist(item_id):
#     item_to_add = Product.query.get(item_id)
#     if item_to_add is None:
#         flash('That product is not available.', 'error')
#         return redirect(request.referrer or '/')

#     wishlist_exists = Wishlist.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
#     if wishlist_exists:
#         flash(f'{item_to_add.product_name} is already in your wishlist.', 'info')
#         return redirect(request.referrer or '/')

#     new_wishlist_item = Wishlist()
#     new_wishlist_item.product_link = item_to_add.id
#     new_wishlist_item.customer_link = current_user.id

#     try:
#         db.session.add(new_wishlist_item)
#         db.session.commit()
#         flash(f'{new_wishlist_item.product.product_name} added to wishlist.', 'success')
#     except Exception as e:
#         print('Item not added to wishlist:', e)
#         flash('Item not added to wishlist.', 'error')
#     return redirect(request.referrer or '/')


# @views.route('/remove-from-wishlist/<int:item_id>')
# @login_required
# def remove_from_wishlist(item_id):
#     wishlist_item = Wishlist.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
#     if not wishlist_item:
#         flash('Item not found in wishlist.', 'error')
#         return redirect(request.referrer or '/wishlist')

#     try:
#         db.session.delete(wishlist_item)
#         db.session.commit()
#         flash('Item removed from wishlist.', 'success')
#     except Exception as e:
#         print('Item not removed from wishlist:', e)
#         flash('Item not removed from wishlist.', 'error')
#     return redirect(request.referrer or '/wishlist')


# @views.route('/wishlist')
# @login_required
# def wishlist():
#     wishlist_items = Wishlist.query.filter_by(customer_link=current_user.id).all()
#     return render_template('wishlist.html', wishlist_items=wishlist_items, cart=get_cart())


# # ── Static Pages ─────────────────────────────────────────────────────────────

# @views.route('/about')
# def about():
#     return render_template('about.html', cart=get_cart())


# @views.route('/contact', methods=['GET', 'POST'])
# @login_required
# def contact():
#     from .forms import MessageForm
#     form = MessageForm()
#     if form.validate_on_submit():
#         try:
#             new_message = Message(
#                 customer_id=current_user.id,
#                 sender_type='customer',
#                 subject=form.subject.data,
#                 message_text=form.message_text.data
#             )
#             db.session.add(new_message)
#             db.session.commit()
#             flash('Your message has been sent to the admin!', 'success')
#             return redirect('/contact')
#         except Exception as e:
#             print('Message error:', e)
#             flash('Error sending message.', 'error')
#     return render_template('contact.html', form=form, cart=get_cart())


# # from .utils.time import to_nepal_time 
#  # make this helper

# @views.route('/messages')
# @login_required
# def messages():
#     customer_messages = Message.query.filter_by(
#         customer_id=current_user.id
#     ).order_by(Message.date_sent.desc()).all()

#     # Mark all as read
#     for msg in customer_messages:
#         if not msg.read_status:
#             msg.read_status = True

#     db.session.commit()

#     # 🔥 ADD THIS: convert time
#     for msg in customer_messages:
#         msg.nepali_time = to_nepal_time(msg.date_sent)

#     return render_template(
#         'messages.html',
#         messages=customer_messages,
#         cart=get_cart()
#     )

# @views.route('/admin/customer-details/<int:customer_id>')
# @login_required
# def admin_customer_details(customer_id):
#     if current_user.id != 1:
#         flash('Admin access only', 'error')
#         return redirect('/')
    
#     customer = Customer.query.get(customer_id)
#     if not customer:
#         flash('Customer not found', 'error')
#         return redirect('/admin-page')
    
#     orders = Order.query.filter_by(customer_link=customer_id).all()
#     customer_messages = Message.query.filter_by(customer_id=customer_id).order_by(Message.date_sent.desc()).all()
    
#     return render_template('admin_customer_details.html', 
#                          customer=customer, 
#                          orders=orders,
#                          messages=customer_messages,
#                          cart=get_cart())


# @views.route('/admin/send-message/<int:customer_id>', methods=['POST'])
# @login_required
# def admin_send_message(customer_id):
#     if current_user.id != 1:
#         flash('Admin access only', 'error')
#         return redirect('/')
    
#     customer = Customer.query.get(customer_id)
#     if not customer:
#         flash('Customer not found', 'error')
#         return redirect('/admin-page')
    
#     subject = request.form.get('subject')
#     message_text = request.form.get('message_text')
    
#     if not subject or not message_text:
#         flash('Subject and message are required', 'error')
#         return redirect(f'/admin/customer-details/{customer_id}')
    
#     new_message = Message(
#         customer_id=customer_id,
#         sender_type='admin',
#         subject=subject,
#         message_text=message_text,
#         read_status=False
#     )
    
#     try:
#         db.session.add(new_message)
#         db.session.commit()
#         flash('Message sent to customer successfully!', 'success')
#     except Exception as e:
#         print('Error sending admin message:', e)
#         db.session.rollback()
#         flash('Error sending message', 'error')
    
#     return redirect(f'/admin/customer-details/{customer_id}')


# # Chat API Routes for Real-time Communication
# @views.route('/api/chat/messages', methods=['GET'])
# @login_required
# def get_chat_messages():
#     "Fetch all messages for the current user"
#     messages = Message.query.filter_by(customer_id=current_user.id).order_by(Message.date_sent.asc()).all()
#     messages_data = []
#     for msg in messages:
#         messages_data.append({
#             'id': msg.id,
#             'sender_type': msg.sender_type,
#             'subject': msg.subject,
#             'message_text': msg.message_text,
#             'date_sent': to_nepal_time(msg.date_sent),
#             # 'date_sent': msg.date_sent.strftime('%B %d, %Y at %I:%M %p'),
#             'read_status': msg.read_status
#         })
#     return jsonify(messages_data)


# @views.route('/api/chat/send', methods=['POST'])
# @login_required
# def send_chat_message():
#     "Send a message from customer to admin"
#     data = request.get_json()
#     subject = data.get('subject')
#     message_text = data.get('message_text')
    
#     if not subject or not message_text:
#         return jsonify({'error': 'Subject and message are required'}), 400
    
#     if len(message_text) < 10:
#         return jsonify({'error': 'Message must be at least 10 characters'}), 400
    
#     new_message = Message(
#         customer_id=current_user.id,
#         sender_type='customer',
#         subject=subject,
#         message_text=message_text,
#         read_status=False
#     )
    
#     try:
#         db.session.add(new_message)
#         db.session.commit()
#         return jsonify({
#             'success': True,
#             'message': {
#                 'id': new_message.id,
#                 'sender_type': new_message.sender_type,
#                 'subject': new_message.subject,
#                 'message_text': new_message.message_text,
#                 # 'date_sent': new_message.date_sent.strftime('%B %d, %Y at %I:%M %p')
#                 'date_sent': to_nepal_time(new_message.date_sent)
#             }
#         })
#     except Exception as e:
#         print('Error sending chat message:', e)
#         return jsonify({'error': 'Failed to send message'}), 500


from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for, session
from flask_login import login_required, current_user
from .models import Product, Cart, Order, Wishlist, Customer, Message
from . import db
from .config import DELIVERY_CHARGE, VAT_RATE, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY
import stripe
from datetime import datetime, timezone, timedelta
import uuid

# ──────────────────────────────────────────────────────────────────────────────
# Nepal Timezone helpers
NEPAL_TZ = timezone(timedelta(hours=5, minutes=45))

def get_nepal_time():
    return datetime.now(NEPAL_TZ).strftime('%b %d, %Y %I:%M %p NPT')

def to_nepal_time(dt):
    if not dt:
        return 
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(NEPAL_TZ).strftime('%b %d, %Y %I:%M %p NPT')

views = Blueprint('views', __name__)

@views.app_template_filter('nst')
def nst_filter(dt):
    return to_nepal_time(dt)

@views.app_template_global('nepal_now')
def nepal_now():
    return get_nepal_time()

stripe.api_key = STRIPE_SECRET_KEY or ''
if not STRIPE_SECRET_KEY:
    print('Warning: STRIPE_SECRET_KEY is not configured. Stripe payments will fail until it is set.')
# ──────────────────────────────────────────────────────────────────────────────
# Helper: get cart items (DB for logged-in, session for guest)
def get_cart():
    if current_user.is_authenticated:
        return Cart.query.filter_by(customer_link=current_user.id).all()
    else:
        return session.get('guest_cart', [])

# ──────────────────────────────────────────────────────────────────────────────
# Public routes (no login required)
@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True).order_by(Product.date_added.desc()).all()
    if not items:
        items = Product.query.order_by(Product.date_added.desc()).limit(12).all()
    return render_template('home.html', items=items, cart=get_cart())

@views.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    from .models import Subscriber
    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        if existing.is_active:
            return jsonify({'success': False, 'message': 'Already subscribed'}), 400
        existing.is_active = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subscription reactivated!'})
    new_sub = Subscriber(email=email)
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Subscribed successfully!'})

# Category pages
@views.route('/supermarket')
def supermarket():
    items = Product.query.filter_by(category='Supermarket').order_by(Product.date_added.desc()).all()
    return render_template('supermarket.html', items=items, cart=get_cart(), category='Supermarket')

@views.route('/health-beauty')
def health_beauty():
    items = Product.query.filter_by(category='Health & Beauty').order_by(Product.date_added.desc()).all()
    return render_template('healthbeauty.html', items=items, cart=get_cart(), category='Health & Beauty')

@views.route('/home-office')
def home_office():
    items = Product.query.filter_by(category='Home & Office').order_by(Product.date_added.desc()).all()
    return render_template('homeoffice.html', items=items, cart=get_cart(), category='Home & Office')

@views.route('/fashion')
def fashion():
    items = Product.query.filter_by(category='Fashion').order_by(Product.date_added.desc()).all()
    return render_template('fashion.html', items=items, cart=get_cart(), category='Fashion')

@views.route('/electronics')
def electronics():
    items = Product.query.filter_by(category='Electronics').order_by(Product.date_added.desc()).all()
    return render_template('Electronic.html', items=items, cart=get_cart(), category='Electronics')

@views.route('/gaming')
def gaming():
    items = Product.query.filter_by(category='Gaming').order_by(Product.date_added.desc()).all()
    return render_template('gaming.html', items=items, cart=get_cart(), category='Gaming')

@views.route('/baby-products')
def baby_products():
    items = Product.query.filter_by(category='Baby Products').order_by(Product.date_added.desc()).all()
    return render_template('babyproducts.html', items=items, cart=get_cart(), category='Baby Products')

@views.route('/sporting-goods')
def sporting_goods():
    items = Product.query.filter_by(category='Sporting Goods').order_by(Product.date_added.desc()).all()
    return render_template('sport.html', items=items, cart=get_cart(), category='Sporting Goods')

@views.route('/garden-outdoor')
def garden_outdoor():
    items = Product.query.filter_by(category='Garden & Outdoor').order_by(Product.date_added.desc()).all()
    return render_template('garden.html', items=items, cart=get_cart(), category='Garden & Outdoor')

# Search
@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=get_cart())
    return render_template('search.html')

# About & Contact
@views.route('/about')
def about():
    return render_template('about.html', cart=get_cart())

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    from .forms import MessageForm
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            customer_id=current_user.id,
            sender_type='customer',
            subject=form.subject.data,
            message_text=form.message_text.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect('/contact')
    return render_template('contact.html', form=form, cart=get_cart())

# ──────────────────────────────────────────────────────────────────────────────
# Cart routes – NO LOGIN REQUIRED
@views.route('/add-to-cart/<int:item_id>')
def add_to_cart(item_id):
    product = Product.query.get(item_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not product:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Product not available'}), 404
        flash('Product not available', 'error')
        return redirect(request.referrer or '/')

    if current_user.is_authenticated:
        # Logged in user → database cart
        existing = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
        if existing:
            existing.quantity += 1
            db.session.commit()
            msg = f'Quantity of {existing.product.product_name} updated'
        else:
            new_item = Cart(quantity=1, product_link=item_id, customer_link=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            msg = f'{new_item.product.product_name} added to cart'
        cart_count = Cart.query.filter_by(customer_link=current_user.id).count()
    else:
        # Guest → session cart
        guest_cart = session.get('guest_cart', [])
        found = False
        for item in guest_cart:
            if item['product_id'] == item_id:
                item['quantity'] += 1
                found = True
                break
        if not found:
            guest_cart.append({
                'product_id': item_id,
                'quantity': 1,
                'price': product.current_price,
                'name': product.product_name,
                'image': product.product_picture
            })
        session['guest_cart'] = guest_cart
        cart_count = sum(item['quantity'] for item in guest_cart)
        msg = f'{product.product_name} added to cart (guest)'

    if is_ajax:
        return jsonify({'success': True, 'message': msg, 'cart_count': cart_count})
    flash(msg, 'success')
    return redirect(request.referrer or '/')

@views.route('/cart')
def show_cart():
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
        base_amount = sum(i.product.current_price * i.quantity for i in cart_items)
        vat_amount = sum(
            (i.product.current_price * VAT_RATE * i.quantity)
            for i in cart_items if i.product.is_taxable
        )
        # For template compatibility, add 'product' attribute to each item (already there)
    else:
        guest_cart = session.get('guest_cart', [])
        cart_items = []
        base_amount = 0
        vat_amount = 0
        for item in guest_cart:
            prod = Product.query.get(item['product_id'])
            if prod:
                # Attach product object so template works
                item['product'] = prod
                cart_items.append(item)
                base_amount += prod.current_price * item['quantity']
                if prod.is_taxable:
                    vat_amount += prod.current_price * VAT_RATE * item['quantity']
    total = base_amount + vat_amount + DELIVERY_CHARGE
    return render_template(
        'cart.html',
        cart=cart_items,
        amount=base_amount,
        vat_amount=vat_amount,
        total=total,
        stripe_publishable_key=STRIPE_PUBLISHABLE_KEY
    )

@views.route('/pluscart')
def plus_cart():
    cart_id = request.args.get('cart_id')
    if current_user.is_authenticated:
        cart_item = Cart.query.get(cart_id)
        if not cart_item or cart_item.customer_link != current_user.id:
            return jsonify({'error': 'Item not found'}), 404
        cart_item.quantity += 1
        db.session.commit()
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        base = sum(i.product.current_price * i.quantity for i in cart)
        vat = sum((i.product.current_price * VAT_RATE * i.quantity) for i in cart if i.product.is_taxable)
        return jsonify({
            'quantity': cart_item.quantity,
            'amount': base + vat,
            'total': base + vat + DELIVERY_CHARGE
        })
    else:
        guest_cart = session.get('guest_cart', [])
        for item in guest_cart:
            if str(item['product_id']) == cart_id:
                item['quantity'] += 1
                break
        session['guest_cart'] = guest_cart
        base = 0
        vat = 0
        for item in guest_cart:
            prod = Product.query.get(item['product_id'])
            if prod:
                base += prod.current_price * item['quantity']
                if prod.is_taxable:
                    vat += prod.current_price * VAT_RATE * item['quantity']
        return jsonify({
            'quantity': item['quantity'],
            'amount': base + vat,
            'total': base + vat + DELIVERY_CHARGE
        })

@views.route('/minuscart')
def minus_cart():
    cart_id = request.args.get('cart_id')
    if current_user.is_authenticated:
        cart_item = Cart.query.get(cart_id)
        if not cart_item or cart_item.customer_link != current_user.id:
            return jsonify({'error': 'Item not found'}), 404
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            new_qty = cart_item.quantity
        else:
            new_qty = 0
            db.session.delete(cart_item)
        db.session.commit()
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        base = sum(i.product.current_price * i.quantity for i in cart)
        vat = sum((i.product.current_price * VAT_RATE * i.quantity) for i in cart if i.product.is_taxable)
        return jsonify({
            'quantity': new_qty,
            'amount': base + vat,
            'total': base + vat + DELIVERY_CHARGE
        })
    else:
        guest_cart = session.get('guest_cart', [])
        new_qty = 0
        for i, item in enumerate(guest_cart):
            if str(item['product_id']) == cart_id:
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                    new_qty = item['quantity']
                else:
                    new_qty = 0
                    guest_cart.pop(i)
                break
        session['guest_cart'] = guest_cart
        base = 0
        vat = 0
        for item in guest_cart:
            prod = Product.query.get(item['product_id'])
            if prod:
                base += prod.current_price * item['quantity']
                if prod.is_taxable:
                    vat += prod.current_price * VAT_RATE * item['quantity']
        return jsonify({
            'quantity': new_qty,
            'amount': base + vat,
            'total': base + vat + DELIVERY_CHARGE
        })

@views.route('/removecart')
def remove_cart():
    cart_id = request.args.get('cart_id')
    if current_user.is_authenticated:
        cart_item = Cart.query.get(cart_id)
        if not cart_item or cart_item.customer_link != current_user.id:
            return jsonify({'error': 'Item not found'}), 404
        db.session.delete(cart_item)
        db.session.commit()
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        base = sum(i.product.current_price * i.quantity for i in cart)
        vat = sum((i.product.current_price * VAT_RATE * i.quantity) for i in cart if i.product.is_taxable)
        return jsonify({
            'quantity': 0,
            'amount': base + vat,
            'total': base + vat + DELIVERY_CHARGE
        })
    else:
        guest_cart = session.get('guest_cart', [])
        for i, item in enumerate(guest_cart):
            if str(item['product_id']) == cart_id:
                guest_cart.pop(i)
                break
        session['guest_cart'] = guest_cart
        base = 0
        vat = 0
        for item in guest_cart:
            prod = Product.query.get(item['product_id'])
            if prod:
                base += prod.current_price * item['quantity']
                if prod.is_taxable:
                    vat += prod.current_price * VAT_RATE * item['quantity']
        return jsonify({
            'quantity': 0,
            'amount': base + vat,
            'total': base + vat + DELIVERY_CHARGE
        })

# ──────────────────────────────────────────────────────────────────────────────
# Checkout routes – LOGIN REQUIRED
@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    from .forms import CheckoutForm

    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect('/cart')

    base_amount = sum(item.product.current_price * item.quantity for item in cart)
    vat_amount = sum((item.product.current_price * VAT_RATE * item.quantity) for item in cart if item.product.is_taxable)
    total_amount = base_amount + vat_amount + DELIVERY_CHARGE

    form = CheckoutForm()

    if current_user.full_name:
        form.full_name.data = current_user.full_name
    if current_user.phone_number:
        form.phone_number.data = current_user.phone_number
    if current_user.street_address:
        form.street_address.data = current_user.street_address
    if current_user.city:
        form.city.data = current_user.city
    if current_user.zip_code:
        form.zip_code.data = current_user.zip_code

    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone_number = form.phone_number.data
        current_user.street_address = form.street_address.data
        current_user.city = form.city.data
        current_user.zip_code = form.zip_code.data
        db.session.commit()

        payment_method = form.payment_method.data

        if payment_method == 'stripe':
            return redirect('/create-checkout-session')
        elif payment_method == 'cod':
            try:
                for i, item in enumerate(cart):
                    product = Product.query.get(item.product_link)
                    if product and product.in_stock >= item.quantity:
                        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                        item_vat = (item.product.current_price * VAT_RATE * item.quantity) if item.product.is_taxable else 0
                        item_delivery = DELIVERY_CHARGE if i == 0 else 0
                        item_total = item.product.current_price * item.quantity + item_vat + item_delivery
                        new_order = Order(
                            order_number=order_number,
                            quantity=item.quantity,
                            price=item.product.current_price,
                            vat_amount=item_vat,
                            delivery_fee=item_delivery,
                            total_amount_paid=item_total,
                            tax_rate_applied=VAT_RATE,
                            status='Pending',
                            payment_method='cod',
                            delivery_full_name=form.full_name.data,
                            delivery_phone=form.phone_number.data,
                            delivery_street=form.street_address.data,
                            delivery_city=form.city.data,
                            delivery_zip=form.zip_code.data,
                            product_link=item.product_link,
                            customer_link=item.customer_link
                        )
                        db.session.add(new_order)
                        product.in_stock -= item.quantity
                    else:
                        flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
                        db.session.rollback()
                        return redirect('/cart')
                for item in cart:
                    db.session.delete(item)
                db.session.commit()
                flash('Order placed successfully! You will pay cash on delivery.', 'success')
                return redirect('/orders')
            except Exception as e:
                db.session.rollback()
                flash('Error placing order.', 'error')
                return redirect('/cart')
        elif payment_method == 'demo':
            try:
                for i, item in enumerate(cart):
                    product = Product.query.get(item.product_link)
                    if product and product.in_stock >= item.quantity:
                        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                        item_vat = (item.product.current_price * VAT_RATE * item.quantity) if item.product.is_taxable else 0
                        item_delivery = DELIVERY_CHARGE if i == 0 else 0
                        item_total = item.product.current_price * item.quantity + item_vat + item_delivery
                        new_order = Order(
                            order_number=order_number,
                            quantity=item.quantity,
                            price=item.product.current_price,
                            vat_amount=item_vat,
                            delivery_fee=item_delivery,
                            total_amount_paid=item_total,
                            tax_rate_applied=VAT_RATE,
                            status='Paid',
                            payment_method='demo',
                            payment_id=f"DEMO-{uuid.uuid4().hex[:8].upper()}",
                            delivery_full_name=form.full_name.data,
                            delivery_phone=form.phone_number.data,
                            delivery_street=form.street_address.data,
                            delivery_city=form.city.data,
                            delivery_zip=form.zip_code.data,
                            product_link=item.product_link,
                            customer_link=item.customer_link
                        )
                        db.session.add(new_order)
                        product.in_stock -= item.quantity
                    else:
                        flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
                        db.session.rollback()
                        return redirect('/cart')
                for item in cart:
                    db.session.delete(item)
                db.session.commit()
                flash('Demo payment successful! Your order has been placed.', 'success')
                return redirect('/orders')
            except Exception as e:
                db.session.rollback()
                flash('Error placing order.', 'error')
                return redirect('/cart')
    return render_template('checkout.html', form=form, cart=cart, amount=base_amount, vat_amount=vat_amount, total=total_amount, stripe_publishable_key=STRIPE_PUBLISHABLE_KEY)

@views.route('/checkout-single/<int:cart_id>', methods=['GET', 'POST'])
@login_required
def checkout_single(cart_id):
    from .forms import CheckoutForm
    cart_item = Cart.query.get(cart_id)
    if not cart_item or cart_item.customer_link != current_user.id:
        flash('Item not found in your cart.', 'error')
        return redirect('/cart')
    product = Product.query.get(cart_item.product_link)
    if not product:
        flash('Product not found.', 'error')
        return redirect('/cart')
    base_amount = product.current_price * cart_item.quantity
    vat_amount = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
    total_amount = base_amount + vat_amount + DELIVERY_CHARGE
    form = CheckoutForm()
    if current_user.full_name:
        form.full_name.data = current_user.full_name
    if current_user.phone_number:
        form.phone_number.data = current_user.phone_number
    if current_user.street_address:
        form.street_address.data = current_user.street_address
    if current_user.city:
        form.city.data = current_user.city
    if current_user.zip_code:
        form.zip_code.data = current_user.zip_code
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone_number = form.phone_number.data
        current_user.street_address = form.street_address.data
        current_user.city = form.city.data
        current_user.zip_code = form.zip_code.data
        db.session.commit()
        payment_method = form.payment_method.data
        if payment_method == 'stripe':
            session['single_checkout_cart_id'] = cart_id
            return redirect('/create-checkout-session-single')
        elif payment_method == 'cod':
            try:
                if product.in_stock >= cart_item.quantity:
                    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                    item_vat = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
                    item_total = product.current_price * cart_item.quantity + item_vat + DELIVERY_CHARGE
                    new_order = Order(
                        order_number=order_number,
                        quantity=cart_item.quantity,
                        price=product.current_price,
                        vat_amount=item_vat,
                        delivery_fee=DELIVERY_CHARGE,
                        total_amount_paid=item_total,
                        tax_rate_applied=VAT_RATE,
                        status='Pending',
                        payment_method='cod',
                        delivery_full_name=form.full_name.data,
                        delivery_phone=form.phone_number.data,
                        delivery_street=form.street_address.data,
                        delivery_city=form.city.data,
                        delivery_zip=form.zip_code.data,
                        product_link=cart_item.product_link,
                        customer_link=cart_item.customer_link
                    )
                    db.session.add(new_order)
                    product.in_stock -= cart_item.quantity
                    db.session.delete(cart_item)
                    db.session.commit()
                    flash(f'Order placed successfully for {product.product_name}!', 'success')
                    return redirect('/orders')
                else:
                    flash(f'Insufficient stock for {product.product_name}.', 'error')
                    return redirect('/cart')
            except Exception as e:
                db.session.rollback()
                flash('Error placing order.', 'error')
                return redirect('/cart')
        elif payment_method == 'demo':
            try:
                if product.in_stock >= cart_item.quantity:
                    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                    item_vat = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
                    item_total = product.current_price * cart_item.quantity + item_vat + DELIVERY_CHARGE
                    new_order = Order(
                        order_number=order_number,
                        quantity=cart_item.quantity,
                        price=product.current_price,
                        vat_amount=item_vat,
                        delivery_fee=DELIVERY_CHARGE,
                        total_amount_paid=item_total,
                        tax_rate_applied=VAT_RATE,
                        status='Paid',
                        payment_method='demo',
                        payment_id=f"DEMO-{uuid.uuid4().hex[:8].upper()}",
                        delivery_full_name=form.full_name.data,
                        delivery_phone=form.phone_number.data,
                        delivery_street=form.street_address.data,
                        delivery_city=form.city.data,
                        delivery_zip=form.zip_code.data,
                        product_link=cart_item.product_link,
                        customer_link=cart_item.customer_link
                    )
                    db.session.add(new_order)
                    product.in_stock -= cart_item.quantity
                    db.session.delete(cart_item)
                    db.session.commit()
                    flash(f'Demo payment successful! Order placed for {product.product_name}!', 'success')
                    return redirect('/orders')
                else:
                    flash(f'Insufficient stock for {product.product_name}.', 'error')
                    return redirect('/cart')
            except Exception as e:
                db.session.rollback()
                flash('Error placing order.', 'error')
                return redirect('/cart')
    return render_template('checkout-single.html', form=form, cart_item=cart_item, product=product,
                           amount=base_amount, vat_amount=vat_amount, total=total_amount,
                           stripe_publishable_key=STRIPE_PUBLISHABLE_KEY)

@views.route('/create-checkout-session-single', methods=['GET', 'POST'])
@login_required
def create_checkout_session_single():
    cart_id = session.get('single_checkout_cart_id')
    if not cart_id:
        flash('Cart item not found.', 'error')
        return redirect('/cart')
    cart_item = Cart.query.get(cart_id)
    if not cart_item or cart_item.customer_link != current_user.id:
        flash('Cart item not found.', 'error')
        return redirect('/cart')
    product = Product.query.get(cart_item.product_link)
    if not product or product.in_stock < cart_item.quantity:
        flash(f'Product "{product.product_name if product else "Unknown"}" is out of stock.', 'error')
        return redirect('/cart')
    try:
        line_items = [
            {
                'price_data': {
                    'currency': 'npr',
                    'product_data': {'name': product.product_name},
                    'unit_amount': int(product.current_price * 100),
                },
                'quantity': cart_item.quantity,
            },
            {
                'price_data': {
                    'currency': 'npr',
                    'product_data': {'name': 'Delivery Charge'},
                    'unit_amount': DELIVERY_CHARGE * 100,
                },
                'quantity': 1,
            }
        ]
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('views.payment_success_single', _external=True) + f'?session_id={{CHECKOUT_SESSION_ID}}&cart_id={cart_id}',
            cancel_url=url_for('views.payment_cancel', _external=True),
            customer_email=current_user.email,
        )
        session.pop('single_checkout_cart_id', None)
        return redirect(stripe_session.url, code=303)
    except Exception as e:
        print('Stripe single session error:', e)
        flash('Payment session could not be created.', 'error')
        return redirect('/cart')

@views.route('/payment-success-single')
@login_required
def payment_success_single():
    session_id = request.args.get('session_id')
    cart_id = request.args.get('cart_id')
    if not session_id or not cart_id:
        flash('Invalid payment session.', 'error')
        return redirect('/cart')
    try:
        stripe_session = stripe.checkout.Session.retrieve(session_id)
        if stripe_session.payment_status == 'paid':
            cart_item = Cart.query.get(cart_id)
            if not cart_item or cart_item.customer_link != current_user.id:
                flash('Cart item not found.', 'error')
                return redirect('/orders')
            product = Product.query.get(cart_item.product_link)
            if product and product.in_stock >= cart_item.quantity:
                order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                item_vat = (product.current_price * VAT_RATE * cart_item.quantity) if product.is_taxable else 0
                item_total = product.current_price * cart_item.quantity + item_vat + DELIVERY_CHARGE
                new_order = Order(
                    order_number=order_number,
                    quantity=cart_item.quantity,
                    price=product.current_price,
                    vat_amount=item_vat,
                    delivery_fee=DELIVERY_CHARGE,
                    total_amount_paid=item_total,
                    tax_rate_applied=VAT_RATE,
                    status='Paid',
                    payment_id=session_id,
                    payment_method='stripe',
                    product_link=cart_item.product_link,
                    customer_link=cart_item.customer_link
                )
                db.session.add(new_order)
                product.in_stock -= cart_item.quantity
                db.session.delete(cart_item)
                db.session.commit()
                flash('Payment successful! Your order has been placed.', 'success')
                return redirect('/orders')
            else:
                flash('Product is out of stock.', 'error')
                return redirect('/cart')
        else:
            flash('Payment was not completed.', 'error')
            return redirect('/cart')
    except Exception as e:
        print('Payment verification error:', e)
        db.session.rollback()
        flash('Error verifying payment.', 'error')
        return redirect('/cart')

@views.route('/create-checkout-session', methods=['GET', 'POST'])
@login_required
def create_checkout_session():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if not customer_cart:
        flash('Your cart is empty.', 'error')
        return redirect('/')
    for item in customer_cart:
        product = Product.query.get(item.product_link)
        if product is None or product.in_stock < item.quantity:
            flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
            return redirect('/cart')
    if not current_user.full_name or not current_user.phone_number or not current_user.street_address:
        flash('Please complete your delivery information before proceeding with payment.', 'error')
        return redirect('/checkout')
    line_items = []
    for item in customer_cart:
        product = Product.query.get(item.product_link)
        if product:
            line_items.append({
                'price_data': {
                    'currency': 'npr',
                    'product_data': {'name': product.product_name},
                    'unit_amount': int(product.current_price * 100),
                },
                'quantity': item.quantity,
            })
    line_items.append({
        'price_data': {
            'currency': 'npr',
            'product_data': {'name': 'Delivery Charge'},
            'unit_amount': DELIVERY_CHARGE * 100,
        },
        'quantity': 1,
    })
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('views.payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('views.payment_cancel', _external=True),
            customer_email=current_user.email,
        )
        return redirect(session.url, code=303)
    except Exception as e:
        print('Stripe session error:', e)
        flash('Payment session could not be created.', 'error')
        return redirect('/cart')

@views.route('/payment-success')
@login_required
def payment_success():
    session_id = request.args.get('session_id')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
            if not customer_cart:
                flash('Order already processed or cart is empty.', 'error')
                return redirect('/orders')
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            for i, item in enumerate(customer_cart):
                product = Product.query.get(item.product_link)
                if product and product.in_stock >= item.quantity:
                    item_vat = (item.product.current_price * VAT_RATE * item.quantity) if item.product.is_taxable else 0
                    item_delivery = DELIVERY_CHARGE if i == 0 else 0
                    item_total = item.product.current_price * item.quantity + item_vat + item_delivery
                    new_order = Order(
                        order_number=order_number,
                        quantity=item.quantity,
                        price=item.product.current_price,
                        vat_amount=item_vat,
                        delivery_fee=item_delivery,
                        total_amount_paid=item_total,
                        tax_rate_applied=VAT_RATE,
                        status='Paid',
                        payment_id=session_id,
                        payment_method='stripe',
                        delivery_full_name=current_user.full_name,
                        delivery_phone=current_user.phone_number,
                        delivery_street=current_user.street_address,
                        delivery_city=current_user.city,
                        delivery_zip=current_user.zip_code,
                        product_link=item.product_link,
                        customer_link=item.customer_link
                    )
                    db.session.add(new_order)
                    product.in_stock -= item.quantity
                else:
                    flash(f'Product "{item.product.product_name}" is out of stock.', 'error')
                    db.session.rollback()
                    return redirect('/cart')
            for item in customer_cart:
                db.session.delete(item)
            db.session.commit()
            flash('Payment successful! Your order has been placed.', 'success')
            return redirect('/orders')
        else:
            flash('Payment was not completed.', 'error')
            return redirect('/cart')
    except Exception as e:
        print('Payment verification error:', e)
        db.session.rollback()
        flash('Error verifying payment.', 'error')
        return redirect('/cart')

@views.route('/payment-cancel')
@login_required
def payment_cancel():
    flash('Payment was cancelled. Your cart is saved.', 'info')
    return redirect('/cart')

@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)

# ──────────────────────────────────────────────────────────────────────────────
# Wishlist (login required)
@views.route('/add-to-wishlist/<int:item_id>')
def add_to_wishlist(item_id):
    item_to_add = Product.query.get(item_id)
    if not item_to_add:
        flash('Product not available.', 'error')
        return redirect(request.referrer or '/')

    if current_user.is_authenticated:
        if Wishlist.query.filter_by(product_link=item_id, customer_link=current_user.id).first():
            flash(f'{item_to_add.product_name} already in wishlist.', 'info')
            return redirect(request.referrer or '/')
        new_item = Wishlist(product_link=item_id, customer_link=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        flash(f'{item_to_add.product_name} added to wishlist.', 'success')
        return redirect(request.referrer or '/')

    guest_wishlist = session.get('guest_wishlist', [])
    if item_id in guest_wishlist:
        flash(f'{item_to_add.product_name} already in wishlist.', 'info')
    else:
        guest_wishlist.append(item_id)
        session['guest_wishlist'] = guest_wishlist
        flash(f'{item_to_add.product_name} added to wishlist.', 'success')
    return redirect(request.referrer or '/')

@views.route('/remove-from-wishlist/<int:item_id>')
def remove_from_wishlist(item_id):
    if current_user.is_authenticated:
        wishlist_item = Wishlist.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
        if not wishlist_item:
            flash('Item not found in wishlist.', 'error')
            return redirect(request.referrer or '/wishlist')
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Item removed from wishlist.', 'success')
        return redirect(request.referrer or '/wishlist')

    guest_wishlist = session.get('guest_wishlist', [])
    if item_id in guest_wishlist:
        guest_wishlist.remove(item_id)
        session['guest_wishlist'] = guest_wishlist
        flash('Item removed from wishlist.', 'success')
    else:
        flash('Item not found in wishlist.', 'error')
    return redirect(request.referrer or '/wishlist')

@views.route('/wishlist')
def wishlist():
    if current_user.is_authenticated:
        wishlist_items = Wishlist.query.filter_by(customer_link=current_user.id).all()
    else:
        guest_wishlist = session.get('guest_wishlist', [])
        wishlist_items = []
        from types import SimpleNamespace
        for item_id in guest_wishlist:
            product = Product.query.get(item_id)
            if product:
                wishlist_items.append(SimpleNamespace(product=product))
    return render_template('wishlist.html', wishlist_items=wishlist_items, cart=get_cart())

# ──────────────────────────────────────────────────────────────────────────────
# Messages & Admin (login required)
@views.route('/messages')
@login_required
def messages():
    customer_messages = Message.query.filter_by(customer_id=current_user.id).order_by(Message.date_sent.desc()).all()
    for msg in customer_messages:
        if not msg.read_status:
            msg.read_status = True
    db.session.commit()
    for msg in customer_messages:
        msg.nepali_time = to_nepal_time(msg.date_sent)
    return render_template('messages.html', messages=customer_messages, cart=get_cart())

@views.route('/admin/customer-details/<int:customer_id>')
@login_required
def admin_customer_details(customer_id):
    if current_user.id != 1:
        flash('Admin access only', 'error')
        return redirect('/')
    customer = Customer.query.get(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect('/admin-page')
    orders = Order.query.filter_by(customer_link=customer_id).all()
    customer_messages = Message.query.filter_by(customer_id=customer_id).order_by(Message.date_sent.desc()).all()
    return render_template('admin_customer_details.html', customer=customer, orders=orders, messages=customer_messages, cart=get_cart())

@views.route('/admin/send-message/<int:customer_id>', methods=['POST'])
@login_required
def admin_send_message(customer_id):
    if current_user.id != 1:
        flash('Admin access only', 'error')
        return redirect('/')
    customer = Customer.query.get(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect('/admin-page')
    subject = request.form.get('subject')
    message_text = request.form.get('message_text')
    if not subject or not message_text:
        flash('Subject and message are required', 'error')
        return redirect(f'/admin/customer-details/{customer_id}')
    new_message = Message(customer_id=customer_id, sender_type='admin', subject=subject, message_text=message_text, read_status=False)
    db.session.add(new_message)
    db.session.commit()
    flash('Message sent to customer successfully!', 'success')
    return redirect(f'/admin/customer-details/{customer_id}')

@views.route('/api/chat/messages', methods=['GET'])
@login_required
def get_chat_messages():
    messages = Message.query.filter_by(customer_id=current_user.id).order_by(Message.date_sent.asc()).all()
    messages_data = [{
        'id': msg.id,
        'sender_type': msg.sender_type,
        'subject': msg.subject,
        'message_text': msg.message_text,
        'date_sent': to_nepal_time(msg.date_sent),
        'read_status': msg.read_status
    } for msg in messages]
    return jsonify(messages_data)

@views.route('/api/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    data = request.get_json()
    subject = data.get('subject')
    message_text = data.get('message_text')
    if not subject or not message_text:
        return jsonify({'error': 'Subject and message are required'}), 400
    if len(message_text) < 10:
        return jsonify({'error': 'Message must be at least 10 characters'}), 400
    new_message = Message(customer_id=current_user.id, sender_type='customer', subject=subject, message_text=message_text, read_status=False)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': {
            'id': new_message.id,
            'sender_type': new_message.sender_type,
            'subject': new_message.subject,
            'message_text': new_message.message_text,
            'date_sent': to_nepal_time(new_message.date_sent)
        }
    })