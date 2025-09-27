# fashion-store

# Fashion Store - E-commerce Website

A full-stack e-commerce website for clothing and accessories built with Django, Django REST Framework, and Bootstrap.

## Features

### User Authentication
- User registration and login
- Password reset via email
- JWT token-based authentication
- User profile management

### Product Management
- Product CRUD operations (Admin only)
- Product categories and variants (size, color)
- Product images and reviews
- Advanced search and filtering
- Product ratings and reviews

### Shopping Cart
- Add/remove items from cart
- Update quantities
- Size and color selection
- Cart persistence

### Order Management
- Place orders from cart
- Order tracking
- Order history
- Admin order management
- Discount codes

### Responsive Design
- Mobile-friendly Bootstrap UI
- Modern and clean design
- Responsive navigation

## Tech Stack

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: JWT tokens
- **Image Handling**: Pillow

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fashion-store-project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
1. Create MySQL database:
```sql
CREATE DATABASE fashion_store_db;
```

2. Update database settings in `fashion_store/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fashion_store_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/request-password-reset/` - Request password reset
- `POST /api/auth/reset-password/` - Reset password

### Products
- `GET /api/products/` - List products
- `GET /api/products/{id}/` - Get product details
- `POST /api/products/` - Create product (Admin)
- `PUT /api/products/{id}/` - Update product (Admin)
- `DELETE /api/products/{id}/` - Delete product (Admin)
- `GET /api/products/categories/` - List categories
- `GET /api/products/search/` - Search products
- `GET /api/products/trending/` - Get trending products

### Cart
- `GET /api/cart/` - Get cart items
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/remove/` - Remove item from cart
- `DELETE /api/cart/clear/` - Clear cart

### Orders
- `GET /api/orders/` - List orders
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/create-from-cart/` - Create order from cart
- `PUT /api/orders/{id}/update-status/` - Update order status (Admin)
- `GET /api/orders/{id}/tracking/` - Get order tracking

## Usage

### Admin Panel
1. Access admin panel at `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Manage products, categories, orders, and users

### Frontend
1. Visit `http://localhost:8000/` for the homepage
2. Browse products and categories
3. Register/login to add items to cart
4. Proceed to checkout to place orders

### API Testing
Use tools like Postman or curl to test API endpoints:

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123", "password_confirm": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Get products (no auth required)
curl http://localhost:8000/api/products/
```

## Project Structure

```
fashion-store-project/
├── fashion_store/          # Django project settings
├── authentication/         # User authentication app
├── products/              # Product management app
├── cart/                  # Shopping cart app
├── orders/                # Order management app
├── frontend/              # Frontend views and templates
├── templates/             # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── requirements.txt       # Python dependencies
└── manage.py              # Django management script
```

## Security Features

- JWT token-based authentication
- Password hashing with Django's built-in validators
- CSRF protection
- Secure password reset with tokens
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@fashionstore.com or create an issue in the repository.
