# ShopyNepal

A simple Flask-based e-commerce website for Nepal, built with SQLite, Flask-Login, and Stripe payment support.

## What this project does

- Displays products by category
- Supports guest cart and wishlist functionality
- Allows registered users to checkout and place orders
- Supports Stripe payments and cash-on-delivery
- Includes an admin dashboard for product and order management

## Key features

- Guest users can add items to cart and wishlist without login
- Customers can checkout using Stripe or COD
- Admin can manage products, orders, customers, and messages
- Stripe keys are loaded from environment variables, not stored in code

## Setup

1. Create a virtual environment and install dependencies in your workspace.
2. Copy `.env.example` to `.env` and fill in your Stripe keys plus `SECRET_KEY`.
3. Run the app with:

   ```bash
   python main.py
   ```

4. Open `http://localhost:5001` in your browser.

## Environment variables

Use a `.env` file with:

- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `SECRET_KEY`
- `FLASK_ENV=development`

  

## Important files

- `main.py` — app entrypoint
- `website/__init__.py` — Flask app factory and DB setup
- `website/views.py` — routes for cart, checkout, wishlist, Stripe, and pages
- `website/models.py` — database models
- `website/config.py` — pricing and Stripe config
- `website/templates/` — frontend templates

## Notes

- The app creates the SQLite database if it does not exist.
- Do not commit real Stripe keys to GitHub.
- Use `.env.example` as a template for local development.
