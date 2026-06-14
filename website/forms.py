from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length, NumberRange, Optional, Regexp, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from .models import CATEGORIES, Customer
from .config import MIN_PASSWORD_LENGTH, MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[
        DataRequired(),
        length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH),
        Regexp(r'^[a-zA-Z][a-zA-Z0-9_]*$', message='Username must start with a letter and contain only letters, numbers, and underscores.')
    ])
    password1 = PasswordField('Password', validators=[
        DataRequired(),
        length(min=MIN_PASSWORD_LENGTH, message=f'Password must be at least {MIN_PASSWORD_LENGTH} characters'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])',
               message='Password must contain uppercase, lowercase, number, and special character (@$!%*?&)')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password1', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, field):
        if Customer.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists. Please use a different one.')
    
    def validate_username(self, field):
        if Customer.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        length(min=MIN_PASSWORD_LENGTH),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])',
               message='Password must contain uppercase, lowercase, number, and special character')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    change_password = SubmitField('Change Password')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Product Name', validators=[
        DataRequired(),
        length(min=2, max=150),
        Regexp(r'^[a-zA-Z\s\-()&,.]+$', message='Product name must contain only letters, spaces, and basic punctuation (no numbers).')
    ])
    description = TextAreaField('Product Description', validators=[
        Optional(),
        length(max=2000)
    ])
    current_price = FloatField('Current Price (NPR)', validators=[
        DataRequired(),
        NumberRange(min=0.01, max=999999.99, message='Price must be between 0.01 and 999,999.99')
    ])
    previous_price = FloatField('Previous Price (NPR)', validators=[
        Optional(),
        NumberRange(min=0.01, max=999999.99)
    ])
    in_stock = IntegerField('Stock Quantity', validators=[
        DataRequired(),
        NumberRange(min=0, max=999999, message='Stock must be between 0 and 999,999')
    ])
    min_stock_alert = IntegerField('Low Stock Alert Level', validators=[
        Optional(),
        NumberRange(min=0, max=1000, message='Alert level must be between 0 and 1000')
    ])
    product_picture = FileField('Product Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only (jpg, jpeg, png, gif, webp)!')
    ])
    flash_sale = BooleanField('Flash Sale Product')
    is_taxable = BooleanField('Subject to 13% VAT', default=True)
    category = SelectField('Category', validators=[DataRequired()], choices=[])
    subcategory = SelectField('Subcategory', validators=[DataRequired()], choices=[])
    sku = StringField('SKU (Stock Keeping Unit)', validators=[Optional(), length(max=50)])
    
    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update Product')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c, c) for c in CATEGORIES]


class CheckoutForm(FlaskForm):
    # Delivery Information
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        length(min=2, max=100)
    ])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^(\+977)?[9][0-9]{9}$', message='Please enter a valid Nepal phone number')
    ])
    street_address = StringField('Street Address', validators=[
        DataRequired(),
        length(min=3, max=200)
    ])
    city = StringField('City', validators=[
        DataRequired(),
        length(min=2, max=100)
    ])
    zip_code = StringField('ZIP Code', validators=[
        Optional(),
        Regexp(r'^\d{5}$', message='ZIP code must be 5 digits')
    ])

    # Payment Method
    payment_method = SelectField('Payment Method', validators=[DataRequired()],
        choices=[
            ('stripe', 'Online Payment (Stripe)'),
            ('demo', 'Demo Payment'),
            ('cod', 'Cash on Delivery')
        ],
        default='stripe'
    )

    # Terms and conditions
    agree_terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])

    place_order = SubmitField('Place Order')


class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Returned', 'Returned')
    ], validators=[DataRequired()])
    update = SubmitField('Update Status')


class DeliveryInfoForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        length(min=2, max=100)
    ])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^(\+977)?[9][0-9]{9}$', message='Please enter a valid phone number')
    ])
    street_address = StringField('Street Address', validators=[
        DataRequired(),
        length(min=3, max=200)
    ])
    city = StringField('City', validators=[
        DataRequired(),
        length(min=2, max=100)
    ])
    zip_code = StringField('ZIP Code', validators=[
        Optional(),
        Regexp(r'^\d{5}$', message='ZIP code must be 5 digits')
    ])
    save = SubmitField('Save Address')


class ContactForm(FlaskForm):
    subject = StringField('Subject', validators=[
        DataRequired(),
        length(min=3, max=200)
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        length(min=10, max=2000)
    ])
    send = SubmitField('Send Message')


class SubscribeForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    subscribe = SubmitField('Subscribe')

    update_delivery = SubmitField('Update Delivery Information')


class MessageForm(FlaskForm):
    subject = StringField('Subject')
    message_text = TextAreaField('Message', validators=[DataRequired(), length(min=10)])
    send_message = SubmitField('Send Message')