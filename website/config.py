"
Application Configuration and Constants
"
import os

# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Stripe API Keys - Use environment variables for security
STRIPE_SECRET_KEY = os.environ.get(
    'STRIPE_SECRET_KEY',
    
)
STRIPE_PUBLISHABLE_KEY = os.environ.get(
    'STRIPE_PUBLISHABLE_KEY',
    
)

# ─────────────────────────────────────────────────────────────────────────────
# PRICING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

DELIVERY_CHARGE = 200  # NPR (Nepali Rupees)
VAT_RATE = 0.13  # 13% VAT for Nepal
DEFAULT_TAX_APPLICABLE = True

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Password requirements
MIN_PASSWORD_LENGTH = 8  # Increased from 6 for better security
PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
PASSWORD_HINT = "Password must contain uppercase, lowercase, number, and special character (@$!%*?&)"

# File upload configuration
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_FOLDER = 'media'

# Aliases for backward compatibility
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS
MAX_FILE_SIZE = MAX_IMAGE_SIZE

# Form validation
MAX_PRODUCT_NAME_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
MAX_USERNAME_LENGTH = 50
MIN_USERNAME_LENGTH = 3
MAX_EMAIL_LENGTH = 100

# Rate limiting (requests per minute)
RATE_LIMIT_AUTH = 5  # Login attempts per minute
RATE_LIMIT_SUBSCRIBE = 10  # Subscribe requests per minute per IP
RATE_LIMIT_CONTACT = 3  # Contact form per minute per user

# ─────────────────────────────────────────────────────────────────────────────
# PHONE NUMBER VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

VALID_PHONE_PATTERN = r'^(\+977)?[9][0-9]{9}$'  # Nepal phone format

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Admin role control (no longer hardcoded to user_id == 1)
REQUIRE_ADMIN_ROLE = True

# ─────────────────────────────────────────────────────────────────────────────
# PAGINATION CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

ITEMS_PER_PAGE = 12
SEARCH_RESULTS_PER_PAGE = 20
ORDERS_PER_PAGE = 10

# ─────────────────────────────────────────────────────────────────────────────
# CACHE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

CACHE_TIMEOUT_HOME = 300  # 5 minutes
CACHE_TIMEOUT_PRODUCT = 600  # 10 minutes
CACHE_TIMEOUT_CATEGORY = 300  # 5 minutes
