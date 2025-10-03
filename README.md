
# Fashion Store - E-commerce Website

A comprehensive full-stack e-commerce website focused on clothing and accessories, built with Django and Django REST Framework.

## 🚀 Features

### ✅ **Core E-commerce Features**
- **User Authentication**: Registration, login, logout with JWT tokens
- **Password Reset**: Email-based password reset with secure tokens
- **Product Management**: Full CRUD operations for products with images
- **Shopping Cart**: Add, update, remove items with size/color selection
- **Order Management**: Complete order processing with tracking
- **Product Reviews**: User reviews and ratings system
- **Admin Panel**: Full admin interface for managing the store

### 🎯 **Advanced Features**
- **Outfit Recommendations**: AI-powered outfit suggestions based on occasion, season, and preferences
- **Personalized Shopping**: Custom outfit creation and personalized recommendations
- **Discount System**: Flexible discount codes with percentage and fixed amount options
- **Product Variants**: Size and color selection with stock management
- **Responsive Design**: Mobile-friendly interface with Bootstrap
- **RESTful APIs**: Complete API for all operations

### 🛍️ **Shopping Experience**
- **Product Filtering**: Filter by category, gender, price range, size, color
- **Product Search**: Advanced search with multiple criteria
- **Image Galleries**: Multiple product images with zoom functionality
- **Cart Persistence**: Shopping cart maintained across sessions
- **Order Tracking**: Real-time order status updates
- **User Profiles**: Personal information and order history

## 🛠️ **Tech Stack**

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **MySQL**: Database
- **JWT Authentication**: Secure token-based auth
- **Django CORS Headers**: Cross-origin resource sharing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Styling and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons

### Database
- **MySQL**: Primary database
- **Django ORM**: Database abstraction layer

## 📦 **Installation & Setup**

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
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE fashion_store_db;
```

### 5. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=fashion_store_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

### 6. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Populate Sample Data
```bash
# Create sample products and images
python manage.py populate_sample_data

# Create outfit recommendations
python manage.py populate_outfits
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🏗️ **Project Structure**

```
fashion-store-project/
├── authentication/          # User authentication app
│   ├── models.py           # User and password reset models
│   ├── views.py            # Authentication views
│   ├── serializers.py      # API serializers
│   └── urls.py             # Authentication URLs
├── products/               # Product management app
│   ├── models.py           # Product, category, review models
│   ├── views.py            # Product views
│   ├── outfit_views.py     # Outfit recommendation views
│   ├── serializers.py      # Product serializers
│   └── management/         # Management commands
├── cart/                   # Shopping cart app
│   ├── models.py           # Cart and cart item models
│   ├── views.py            # Cart views
│   └── serializers.py      # Cart serializers
├── orders/                 # Order management app
│   ├── models.py           # Order, order item, discount models
│   ├── views.py            # Order views
│   └── serializers.py      # Order serializers
├── frontend/               # Frontend views
│   ├── views.py            # Template views
│   └── urls.py             # Frontend URLs
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── frontend/           # Page templates
├── static/                 # Static files
├── media/                  # User uploaded files
├── fashion_store/          # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
└── manage.py               # Django management script
```

## 🔌 **API Endpoints**

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - User profile
- `POST /api/auth/request-password-reset/` - Request password reset
- `POST /api/auth/reset-password/` - Reset password

### Products
- `GET /api/products/` - List products
- `GET /api/products/{id}/` - Product details
- `POST /api/products/` - Create product (admin)
- `PUT /api/products/{id}/` - Update product (admin)
- `DELETE /api/products/{id}/` - Delete product (admin)
- `GET /api/products/search/` - Search products
- `GET /api/products/trending/` - Trending products

### Outfit Recommendations
- `GET /api/products/outfits/` - List outfit recommendations
- `GET /api/products/outfits/{id}/` - Outfit details
- `GET /api/products/outfits/personalized/` - Personalized outfits
- `POST /api/products/outfits/create/` - Create custom outfit
- `GET /api/products/outfits/suggestions/` - Get outfit suggestions
- `GET /api/products/outfits/occasion/` - Occasion-based outfits

### Cart
- `GET /api/cart/` - Get cart contents
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove cart item

### Orders
- `GET /api/orders/` - List user orders
- `GET /api/orders/{id}/` - Order details
- `POST /api/orders/create/` - Create order from cart
- `PUT /api/orders/{id}/` - Update order (admin)

## 🎨 **Frontend Pages**

### Public Pages
- **Home** (`/`) - Landing page with hero section and categories
- **Products** (`/products/`) - Product listing with filters
- **Product Detail** (`/products/{id}/`) - Individual product page
- **Outfits** (`/outfits/`) - Outfit recommendations
- **Login** (`/login/`) - User login
- **Register** (`/register/`) - User registration
- **Forgot Password** (`/forgot-password/`) - Password reset request

### Authenticated Pages
- **Cart** (`/cart/`) - Shopping cart
- **Checkout** (`/checkout/`) - Order placement
- **Orders** (`/orders/`) - Order history
- **Profile** (`/profile/`) - User profile

## 🔐 **Security Features**

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Django's built-in password hashing
- **CSRF Protection**: Cross-site request forgery protection
- **CORS Configuration**: Controlled cross-origin requests
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM protection

## 🚀 **Deployment**

### Production Settings
1. Set `DEBUG = False` in settings.py
2. Configure production database
3. Set up static file serving
4. Configure email backend
5. Set up SSL certificates
6. Configure domain and allowed hosts

### Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=mysql://user:password@host:port/database
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 **Database Models**

### Core Models
- **User**: Extended user model with additional fields
- **Product**: Product information with variants
- **Category**: Product categorization
- **ProductImage**: Multiple images per product
- **ProductVariant**: Size and color variants
- **ProductReview**: User reviews and ratings

### E-commerce Models
- **Cart**: User shopping cart
- **CartItem**: Individual cart items
- **Order**: Order information
- **OrderItem**: Order line items
- **DiscountCode**: Promotional codes

### Outfit Models
- **OutfitRecommendation**: Outfit suggestions
- **OutfitItem**: Items in an outfit
- **UserOutfitPreference**: User style preferences

## 🧪 **Testing**

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📈 **Performance Optimization**

- **Database Indexing**: Optimized database queries
- **Image Optimization**: Compressed product images
- **Caching**: Redis caching for frequently accessed data
- **CDN Integration**: Content delivery network for static files
- **Database Connection Pooling**: Efficient database connections

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 **Changelog**

### Version 1.0.0
- Initial release
- Complete e-commerce functionality
- Outfit recommendation system
- User authentication and authorization
- Admin panel
- Responsive design
- RESTful API

---

**Built with ❤️ using Django and modern web technologies**
# fashion_store

