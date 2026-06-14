from flask import Blueprint, render_template, flash, redirect, request
from .forms import LoginForm, SignUpForm, PasswordChangeForm, DeliveryInfoForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password2

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully. You can now log in.', 'success')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account not created. The email may already be registered.', 'error')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                if customer.id == 1:
                    flash('Welcome back, admin! You are now logged in.', 'success')
                else:
                    flash('Login successful. Welcome back!', 'success')
                return redirect('/')
            else:
                flash('Incorrect Email or Password', 'error')

        else:
            flash('Account does not exist. Please sign up.', 'error')

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect('/')


@auth.route('/profile/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def profile(customer_id):
    from flask_login import current_user
    from website.utils import is_admin
    
    customer = Customer.query.get(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect('/')
    
    # Check authorization: own profile or admin
    if current_user.id != customer_id and not is_admin(current_user):
        flash('Unauthorized access', 'error')
        return redirect('/')
    
    form = DeliveryInfoForm()
    
    if form.validate_on_submit():
        customer.full_name = form.full_name.data
        customer.phone_number = form.phone_number.data
        customer.street_address = form.street_address.data
        customer.city = form.city.data
        customer.zip_code = form.zip_code.data
        
        try:
            db.session.commit()
            flash('Delivery information updated successfully!', 'success')
            return redirect(f'/profile/{customer_id}')
        except Exception as e:
            print('Error updating delivery info:', e)
            db.session.rollback()
            flash('Error updating delivery information', 'error')
    
    # Pre-fill form with existing data
    if request.method == 'GET':
        if customer.full_name:
            form.full_name.data = customer.full_name
        if customer.phone_number:
            form.phone_number.data = customer.phone_number
        if customer.street_address:
            form.street_address.data = customer.street_address
        if customer.city:
            form.city.data = customer.city
        if customer.zip_code:
            form.zip_code.data = customer.zip_code
    
    return render_template('profile.html', customer=customer, form=form)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    from flask_login import current_user
    from website.utils import is_admin
    
    customer = Customer.query.get(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect('/')
    
    # Check authorization: own account or admin
    if current_user.id != customer_id and not is_admin(current_user):
        flash('Unauthorized access', 'error')
        return redirect('/')
    
    form = PasswordChangeForm()
    
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        
        # Verify current password
        if not customer.verify_password(current_password):
            flash('Current password is incorrect', 'error')
            return render_template('change_password.html', form=form)
        
        # Password validation is done by form validators
        try:
            customer.password = new_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(f'/profile/{customer.id}')
        except Exception as e:
            print('Password change error:', e)
            db.session.rollback()
            flash('Error updating password. Please try again.', 'error')

    return render_template('change_password.html', form=form)
