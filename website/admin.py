# from flask import Blueprint, render_template, flash, send_from_directory, redirect
# from flask_login import login_required, current_user
# from .forms import ShopItemsForm, OrderForm
# from werkzeug.utils import secure_filename
# from .models import Product, Order, Customer
# from . import db


# admin = Blueprint('admin', __name__)


# @admin.route('/media/<path:filename>')
# def get_image(filename):
#     return send_from_directory('../media', filename)


# @admin.route('/add-shop-items', methods=['GET', 'POST'])
# @login_required
# def add_shop_items():
#     if current_user.id == 1:
#         form = ShopItemsForm()

#         if form.validate_on_submit():
#             product_name = form.product_name.data
#             current_price = form.current_price.data
#             previous_price = form.previous_price.data
#             in_stock = form.in_stock.data
#             flash_sale = form.flash_sale.data

#             file = form.product_picture.data

#             file_name = secure_filename(file.filename)

#             file_path = f'./media/{file_name}'

#             file.save(file_path)

#             new_shop_item = Product()
#             new_shop_item.product_name = product_name
#             new_shop_item.current_price = current_price
#             new_shop_item.previous_price = previous_price
#             new_shop_item.in_stock = in_stock
#             new_shop_item.flash_sale = flash_sale

#             new_shop_item.product_picture = file_path

#             try:
#                 db.session.add(new_shop_item)
#                 db.session.commit()
#                 flash(f'{product_name} added Successfully')
#                 print('Product Added')
#                 return render_template('add_shop_items.html', form=form)
#             except Exception as e:
#                 print(e)
#                 flash('Product Not Added!!')

#         return render_template('add_shop_items.html', form=form)

#     return render_template('404.html')


# @admin.route('/shop-items', methods=['GET', 'POST'])
# @login_required
# def shop_items():
#     if current_user.id == 1:
#         items = Product.query.order_by(Product.date_added).all()
#         return render_template('shop_items.html', items=items)
#     return render_template('404.html')


# @admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
# @login_required
# def update_item(item_id):
#     if current_user.id == 1:
#         form = ShopItemsForm()

#         item_to_update = Product.query.get(item_id)

#         form.product_name.render_kw = {'placeholder': item_to_update.product_name}
#         form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
#         form.current_price.render_kw = {'placeholder': item_to_update.current_price}
#         form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
#         form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

#         if form.validate_on_submit():
#             product_name = form.product_name.data
#             current_price = form.current_price.data
#             previous_price = form.previous_price.data
#             in_stock = form.in_stock.data
#             flash_sale = form.flash_sale.data

#             file = form.product_picture.data

#             file_name = secure_filename(file.filename)
#             file_path = f'./media/{file_name}'

#             file.save(file_path)

#             try:
#                 Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
#                                                                 current_price=current_price,
#                                                                 previous_price=previous_price,
#                                                                 in_stock=in_stock,
#                                                                 flash_sale=flash_sale,
#                                                                 product_picture=file_path))

#                 db.session.commit()
#                 flash(f'{product_name} updated Successfully')
#                 print('Product Upadted')
#                 return redirect('/shop-items')
#             except Exception as e:
#                 print('Product not Upated', e)
#                 flash('Item Not Updated!!!')

#         return render_template('update_item.html', form=form)
#     return render_template('404.html')


# @admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
# @login_required
# def delete_item(item_id):
#     if current_user.id == 1:
#         try:
#             item_to_delete = Product.query.get(item_id)
#             db.session.delete(item_to_delete)
#             db.session.commit()
#             flash('One Item deleted')
#             return redirect('/shop-items')
#         except Exception as e:
#             print('Item not deleted', e)
#             flash('Item not deleted!!')
#         return redirect('/shop-items')

#     return render_template('404.html')


# @admin.route('/view-orders')
# @login_required
# def order_view():
#     if current_user.id == 1:
#         orders = Order.query.all()
#         return render_template('view_orders.html', orders=orders)
#     return render_template('404.html')


# @admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
# @login_required
# def update_order(order_id):
#     if current_user.id == 1:
#         form = OrderForm()

#         order = Order.query.get(order_id)

#         if form.validate_on_submit():
#             status = form.order_status.data
#             order.status = status

#             try:
#                 db.session.commit()
#                 flash(f'Order {order_id} Updated successfully')
#                 return redirect('/view-orders')
#             except Exception as e:
#                 print(e)
#                 flash(f'Order {order_id} not updated')
#                 return redirect('/view-orders')

#         return render_template('order_update.html', form=form)

#     return render_template('404.html')


# @admin.route('/customers')
# @login_required
# def display_customers():
#     if current_user.id == 1:
#         customers = Customer.query.all()
#         return render_template('customers.html', customers=customers)
#     return render_template('404.html')


# @admin.route('/admin-page')
# @login_required
# def admin_page():
#     if current_user.id == 1:
#         return render_template('admin.html')
#     return render_template('404.html')



from flask import Blueprint, render_template, flash, send_from_directory, redirect, request, jsonify
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, Message, SUBCATEGORY_MAP
from . import db
 
 
admin = Blueprint('admin', __name__)
 
 
@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)
 
 
@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = ShopItemsForm()
        selected_category = form.category.data or next(iter(SUBCATEGORY_MAP))
        form.subcategory.choices = [(sub, sub) for sub in SUBCATEGORY_MAP.get(selected_category, [])]
 
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            is_taxable = form.is_taxable.data
            category = form.category.data
            subcategory = form.subcategory.data
 
            file = form.product_picture.data
            if not file or not getattr(file, 'filename', None):
                flash('Product image is required when adding a new item.', 'error')
                return render_template('add_shop_items.html', form=form)

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_shop_item = Product(
                product_name=product_name,
                current_price=current_price,
                previous_price=previous_price,
                in_stock=in_stock,
                flash_sale=flash_sale,
                is_taxable=is_taxable,
                category=category,
                subcategory=subcategory,
                product_picture=file_path
            )

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added successfully.', 'success')
                return render_template('add_shop_items.html', form=form)
            except Exception as e:
                print(e)
                flash('Product could not be added. Please try again.', 'error')
 
        return render_template('add_shop_items.html', form=form)
 
    return render_template('404.html')
 
 
@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        # Get all items for stats
        all_items = Product.query.all()
        
        # Calculate stats
        total_stock = sum(item.in_stock for item in all_items)
        total_products = len(all_items)
        total_low_stock = len([item for item in all_items if item.in_stock < 10])
        total_high_stock = len([item for item in all_items if item.in_stock > 20])
        
        # Find products with highest, lowest, and average stock
        if all_items:
            product_highest = max(all_items, key=lambda p: p.in_stock)
            product_lowest = min(all_items, key=lambda p: p.in_stock)
            average_stock_level = round(total_stock / total_products, 2) if total_products > 0 else 0
            product_average = min(all_items, key=lambda p: abs(p.in_stock - average_stock_level))
        else:
            product_highest = product_lowest = product_average = None
            average_stock_level = 0
        
        items = Product.query.order_by(Product.date_added).all()
        
        return render_template('shop_items.html', 
                             items=items,
                             total_stock=total_stock,
                             total_products=total_products,
                             total_low_stock=total_low_stock,
                             total_high_stock=total_high_stock,
                             product_highest=product_highest,
                             product_lowest=product_lowest,
                             product_average=product_average,
                             categories=list(SUBCATEGORY_MAP.keys()))
    return render_template('404.html')
 
 
@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemsForm()
        item_to_update = Product.query.get(item_id)

        if not item_to_update:
            flash('Product not found.', 'error')
            return redirect('/shop-items')

        # Pre-fill form fields on GET
        if request.method == 'GET':
            form.product_name.data = item_to_update.product_name
            form.current_price.data = item_to_update.current_price
            form.previous_price.data = item_to_update.previous_price
            form.in_stock.data = item_to_update.in_stock
            form.flash_sale.data = item_to_update.flash_sale
            form.is_taxable.data = item_to_update.is_taxable
            form.category.data = item_to_update.category
            form.subcategory.data = item_to_update.subcategory

        selected_category = form.category.data or item_to_update.category
        form.subcategory.choices = [(sub, sub) for sub in SUBCATEGORY_MAP.get(selected_category, [])]

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            is_taxable = form.is_taxable.data
            category = form.category.data
            subcategory = form.subcategory.data

            # Handle optional image update: keep existing if not provided
            if form.product_picture.data:
                file = form.product_picture.data
                file_name = secure_filename(file.filename)
                file_path = f'./media/{file_name}'
                file.save(file_path)
                product_image_path = file_path
            else:
                product_image_path = item_to_update.product_picture

            try:
                Product.query.filter_by(id=item_id).update(dict(
                    product_name=product_name,
                    current_price=current_price,
                    previous_price=previous_price,
                    in_stock=in_stock,
                    flash_sale=flash_sale,
                    is_taxable=is_taxable,
                    category=category,
                    subcategory=subcategory,
                    product_picture=product_image_path
                ))
                db.session.commit()
                flash(f'{product_name} updated successfully.', 'success')
                return redirect('/shop-items')
            except Exception as e:
                db.session.rollback()
                print('Product not updated', e)
                flash('Item could not be updated. Please try again.', 'error')

        return render_template('update_item.html', form=form, item=item_to_update)
    return render_template('404.html')
 
 
@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            if not item_to_delete:
                flash('Product not found.', 'error')
                return redirect('/shop-items')
            
            # Delete related records first to avoid foreign key constraints
            from .models import Cart, Order, Wishlist
            carts = Cart.query.filter_by(product_link=item_id).all()
            for cart in carts:
                db.session.delete(cart)
            
            orders = Order.query.filter_by(product_link=item_id).all()
            for order in orders:
                db.session.delete(order)
            
            wishlists = Wishlist.query.filter_by(product_link=item_id).all()
            for wishlist in wishlists:
                db.session.delete(wishlist)
            
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Product deleted successfully.', 'success')
            return redirect('/shop-items')
        except Exception as e:
            db.session.rollback()
            print('Item not deleted', e)
            flash('Product could not be deleted. Please try again.', 'error')
        return redirect('/shop-items')
    return render_template('404.html')
 
 
@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')
 
 
@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id != 1:
        return render_template('404.html')

    order = Order.query.get(order_id)
    if not order:
        flash('Order not found.', 'error')
        return redirect('/view-orders')

    # Support modal button query params for quick update from view_orders
    new_status = request.args.get('status')
    if new_status:
        order.status = new_status
        try:
            db.session.commit()
            flash(f'Order #{order_id} updated to {new_status}.', 'success')
            return redirect('/view-orders')
        except Exception as e:
            db.session.rollback()
            print('Order not updated:', e)
            flash(f'Order #{order_id} could not be updated.', 'error')
            return redirect('/view-orders')

    form = OrderForm(obj=order)

    if form.validate_on_submit():
        order.status = form.order_status.data
        try:
            db.session.commit()
            flash(f'Order #{order_id} updated successfully.', 'success')
            return redirect('/view-orders')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f'Order #{order_id} could not be updated.', 'error')
            return redirect('/view-orders')

    return render_template('order_update.html', form=form)
 
 
@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')
 
 
@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        # Get statistics for dashboard
        total_customers = Customer.query.count()
        total_products = Product.query.count()
        total_orders = Order.query.count()
        low_stock_items = Product.query.filter(Product.in_stock < 10).all()
        unread_messages = Message.query.filter_by(read_status=False).count()
        
        # Additional Inventory Management Statistics
        out_of_stock_items = Product.query.filter(Product.in_stock == 0).all()
        out_of_stock_count = len(out_of_stock_items)
        
        # Calculate total inventory value
        all_products = Product.query.all()
        total_inventory_value = sum(product.in_stock * product.current_price for product in all_products)
        
        # Calculate average stock level
        total_stock = sum(product.in_stock for product in all_products)
        average_stock_level = round(total_stock / total_products, 2) if total_products > 0 else 0
        
        # Calculate min and max stock levels
        if all_products:
            min_stock = min(product.in_stock for product in all_products)
            max_stock = max(product.in_stock for product in all_products)
        else:
            min_stock = max_stock = 0

        return render_template('admin.html',
                             total_customers=total_customers,
                             total_products=total_products,
                             total_orders=total_orders,
                             low_stock_items=low_stock_items,
                             unread_messages=unread_messages,
                             out_of_stock_count=out_of_stock_count,
                             out_of_stock_items=out_of_stock_items,
                             total_inventory_value=total_inventory_value,
                             total_stock=total_stock,
                             min_stock=min_stock,
                             max_stock=max_stock,
                             average_stock_level=average_stock_level)
    return render_template('404.html')


@admin.route('/reports')
@login_required
def reports():
    if current_user.id != 1:
        return render_template('404.html')

    total_customers = Customer.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.price * Order.quantity)).scalar() or 0.0
    pending_orders = Order.query.filter_by(status='Pending').count()
    paid_orders = Order.query.filter_by(status='Paid').count()
    delivered_orders = Order.query.filter_by(status='Delivered').count()
    low_stock_items = Product.query.filter(Product.in_stock < 10).all()
    out_of_stock_items = Product.query.filter(Product.in_stock == 0).all()
    out_of_stock_count = len(out_of_stock_items)

    all_products = Product.query.all()
    total_stock = sum(product.in_stock for product in all_products)
    total_inventory_value = sum(product.in_stock * product.current_price for product in all_products)
    average_stock_level = round(total_stock / total_products, 2) if total_products > 0 else 0

    # Calculate min and max stock levels
    if all_products:
        min_stock = min(product.in_stock for product in all_products)
        max_stock = max(product.in_stock for product in all_products)
    else:
        min_stock = max_stock = 0

    top_products = (
        db.session.query(Product.product_name, db.func.sum(Order.quantity).label('sold'))
        .join(Order, Order.product_link == Product.id)
        .group_by(Product.id)
        .order_by(db.func.sum(Order.quantity).desc())
        .limit(10)
        .all()
    )

    return render_template('reports.html',
                           total_customers=total_customers,
                           total_products=total_products,
                           total_orders=total_orders,
                           total_revenue=total_revenue,
                           pending_orders=pending_orders,
                           paid_orders=paid_orders,
                           delivered_orders=delivered_orders,
                           low_stock_items=low_stock_items,
                           out_of_stock_items=out_of_stock_items,
                           out_of_stock_count=out_of_stock_count,
                           total_inventory_value=total_inventory_value,
                           total_stock=total_stock,
                           min_stock=min_stock,
                           max_stock=max_stock,
                           average_stock_level=average_stock_level,
                           top_products=top_products)


@admin.route('/subscribers')
@login_required
def subscribers():
    if current_user.id == 1:
        from .models import Subscriber
        subscribers = Subscriber.query.order_by(Subscriber.date_subscribed.desc()).all()
        return render_template('subscribers.html', subscribers=subscribers)
    return render_template('404.html')


@admin.route('/admin/toggle-subscriber/<int:subscriber_id>', methods=['POST'])
@login_required
def toggle_subscriber(subscriber_id):
    if current_user.id == 1:
        from .models import Subscriber
        subscriber = Subscriber.query.get(subscriber_id)
        if subscriber:
            data = request.get_json()
            subscriber.is_active = data.get('activate', True)
            try:
                db.session.commit()
                return jsonify({'success': True, 'message': f'Subscriber {"activated" if subscriber.is_active else "deactivated"} successfully'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': 'Database error'})
        return jsonify({'success': False, 'message': 'Subscriber not found'})
    return jsonify({'success': False, 'message': 'Unauthorized'})


@admin.route('/admin/delete-subscriber/<int:subscriber_id>', methods=['POST'])
@login_required
def delete_subscriber(subscriber_id):
    if current_user.id == 1:
        from .models import Subscriber
        subscriber = Subscriber.query.get(subscriber_id)
        if subscriber:
            try:
                db.session.delete(subscriber)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Subscriber deleted successfully'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': 'Database error'})
        return jsonify({'success': False, 'message': 'Subscriber not found'})
    return jsonify({'success': False, 'message': 'Unauthorized'})


@admin.route('/admin/messages')
@login_required
def admin_messages():
    if current_user.id == 1:
        # Get all messages from customers
        customer_messages = Message.query.filter_by(sender_type='customer').order_by(Message.date_sent.desc()).all()
        
        # Mark all as read
        for msg in customer_messages:
            if not msg.read_status:
                msg.read_status = True
        db.session.commit()
        
        return render_template('admin_messages.html', messages=customer_messages)
    return render_template('404.html')