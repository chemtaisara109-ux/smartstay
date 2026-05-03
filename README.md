# Laikipia SmartStay: A Localized Short-Term Accommodation Booking System for Laikipia County

A web-based short-term accommodation booking system tailored specifically for Laikipia County, enabling visitors to easily search, verify, and book accommodation in major towns like Nanyuki, Nyahururu, and Rumuruti.

## 🎯 Core Features

### Authentication & Authorization
- ✅ Secure user registration and authentication system
- ✅ Role-based access control (Guest & Host roles)
- ✅ Session-based login with bcrypt password hashing

### Guest Features
- ✅ Search accommodation by town, price range, and purpose of stay
- ✅ Browse verified property listings in Laikipia County
- ✅ Book short-term accommodation with instant confirmation
- ✅ View booking history and manage reservations

### Host Features
- ✅ List available short-term rental properties
- ✅ Manage property details and availability
- ✅ View and confirm booking requests
- ✅ Track earnings from rentals

### Booking & Reservation System
- ✅ Secure booking and reservation management
- ✅ Date conflict detection and validation
- ✅ Automatic pricing calculation

### Rating & Review Mechanism
- ✅ Verified property ratings (1-5 stars)
- ✅ Detailed review comments from guests
- ✅ Average rating display for properties
- ✅ Review count tracking

### Administrative Panel
- ✅ Admin dashboard for monitoring
- ✅ Property listing verification system
- ✅ User and property management
- ✅ Verification status tracking

## 📋 Development Methodology

The system was developed following the Agile Software Development Methodology, an iterative and flexible approach that promotes continuous stakeholder involvement, incremental delivery of system features, and regular feedback throughout the project lifecycle.

### Development Stages
1. **Requirements Gathering and Planning**
   - System requirements collected from stakeholders
   - Project tasks organized into short development cycles (sprints)

2. **Iterative System Design and Development**
   - System designed and developed in small, manageable increments
   - Each sprint focused on implementing specific features using Python Flask, MySQL, and XAMPP

3. **Continuous Testing**
   - Testing conducted throughout each sprint
   - Features validated to meet specified requirements

4. **Review and Feedback**
   - Developed components reviewed by stakeholders at sprint end
   - Feedback incorporated into subsequent iterations

5. **Final Integration and Deployment**
   - All sprints completed and requirements satisfied
   - System fully integrated, tested, and deployed

The Agile methodology ensured flexibility, improved system quality, continuous improvement, and active stakeholder participation throughout the development process.

### Installation

1. **Clone/Download the project**
   ```bash
   cd "c:\Users\DANNY\Documents\smartstay h"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

### Sample Login Credentials

**Guest Account:**
- Email: `guest@smartstay.com`
- Password: `Password123`

**Host Account:**
- Email: `host@smartstay.com`
- Password: `Password123`

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python Flask |
| **Database** | MySQL (via XAMPP) |
| **Development Environment** | XAMPP |
| **Authentication** | Session-based with bcrypt |
| **Additional Libraries** | ReportLab (PDF), Pillow (Images) |

## 📁 Project Structure

```
smartstay/
├── app.py                              # Flask app initialization & entry point
├── config.py                           # Configuration (database, secrets)
├── requirements.txt                    # Python dependencies
│
├── database/
│   ├── __init__.py                     # DB connection utilities & schema init
│   └── schema.sql                      # MySQL table definitions
│
├── models/                             # Data models (ORM-style)
│   ├── user.py                         # User model (auth, roles)
│   ├── listing.py                      # Property model (CRUD, search)
│   └── booking.py                      # Booking model (validation, management)
│
├── routes/                             # API endpoints & views
│   ├── auth.py                         # Authentication (login, register, logout)
│   ├── guest.py                        # Guest operations (browse, book, dashboard)
│   ├── host.py                         # Host operations (manage properties, bookings)
│   └── booking.py                      # Booking API (search, validate, upload)
│
├── static/                             # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── style.css                   # Main stylesheet (500+ lines)
│   │   ├── landing.css                 # Landing page styles (Airbnb-inspired)
│   │   └── ...
│   ├── js/
│   │   ├── script.js                   # Frontend logic (validation, UI)
│   │   └── ...
│   ├── uploads/                        # User-uploaded property images
│   └── favicon.ico
│
├── templates/                          # Jinja2 HTML templates
│   ├── base.html                       # Base template (navbar, footer)
│   ├── index.html                      # Landing page (Laikipia-focused)
│   ├── login.html                      # Login form
│   ├── register.html                   # Registration form (Guest & Host)
│   ├── host_register.html              # Host-specific registration
│   ├── browse.html                     # Property listings (grid)
│   ├── search_results.html             # Search results (filtered)
│   ├── property_detail.html            # Single property details
│   ├── dashboard_guest.html            # Guest bookings & history
│   ├── dashboard_host.html             # Host properties & earnings
│   └── ...
│
├── utils/                              # Utility functions
│   ├── auth_helper.py                  # Authentication decorators
│   └── validators.py                   # Input validation functions
│
├── DOCUMENTATION_INDEX.md              # Feature documentation
├── MYSQL_CONNECTION_GUIDE.md           # MySQL setup guide
├── VISUAL_GUIDE.md                     # UI walkthrough
└── README.md                           # This file
```

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: 3.8 or higher
- **MySQL**: XAMPP or standalone MySQL server
- **Git**: For cloning repository

### Step 1: Install Python Dependencies

```bash
cd "c:\Users\DANNY\Documents\smartstay h"
pip install -r requirements.txt
```

**Expected packages:**
- Flask 2.3.3
- PyMySQL 1.1.0
- bcrypt 4.0.1
- ReportLab 4.0.7
- Pillow 10.0.1

### Step 2: Set Up MySQL Database

#### Option A: Using XAMPP (Recommended for Windows)

1. **Start XAMPP**
   - Open XAMPP Control Panel
   - Click "Start" next to MySQL

2. **Create Database**
   - Open phpMyAdmin: http://localhost/phpmyadmin
   - Click "New" to create new database
   - Database name: `smartstay_test` (or your choice)
   - Charset: `utf8mb4_unicode_ci`
   - Click "Create"

3. **Import Schema**
   - Select the `smartstay_test` database
   - Go to "Import" tab
   - Choose `database/schema.sql`
   - Click "Go"

#### Option B: Using MySQL CLI

```bash
mysql -u root -p
CREATE DATABASE smartstay_test;
USE smartstay_test;
SOURCE database/schema.sql;
```

### Step 3: Configure Application

Edit `config.py`:

```python
# Database Configuration
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''          # Leave blank if no password set
MYSQL_DATABASE = 'smartstay_test'
MYSQL_CHARSET = 'utf8mb4'
MYSQL_TIMEOUT = 10

# Flask Configuration
SECRET_KEY = 'your-secret-key-here'
DEBUG = True
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60  # 7 days
```

### Step 4: Run the Application

```bash
python app.py
```

**Expected output:**
```
✅ Database initialized successfully!
Starting SmartStay...
 * Running on http://127.0.0.1:5000
```

### Step 5: Access the Application

- **Homepage**: http://127.0.0.1:5000
- **Login**: http://127.0.0.1:5000/login
- **Register**: http://127.0.0.1:5000/register

## 👤 Sample Test Accounts

After database initialization, two sample accounts are automatically created:

### Guest Account
```
Email: guest@example.com
Password: password123
Role: Guest
```

### Host Account
```
Email: host@example.com
Password: password123
Role: Host
```

## 🔐 Authentication Flow

### Registration (Guests & Hosts)
```
User Input Form
    ↓
Validate Email & Password
    ↓
Hash Password (bcrypt)
    ↓
Create User Record
    ↓
Auto-login & Session
    ↓
Redirect to Dashboard
```

### Login
```
Email & Password Input
    ↓
Find User by Email
    ↓
Verify Password Hash
    ↓
Create Session
    ↓
Redirect Based on Role
    (Guest → Guest Dashboard)
    (Host → Host Dashboard)
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),          -- bcrypt hash
    role ENUM('guest', 'host'),
    created_at TIMESTAMP
);
```

### Properties Table
```sql
CREATE TABLE properties (
    id INT PRIMARY KEY AUTO_INCREMENT,
    host_id INT,                    -- Foreign key to users
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    price DECIMAL(10,2),
    max_guests INT,
    image_url VARCHAR(500),         -- Comma-separated URLs
    created_at TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id)
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    guest_id INT,                   -- Foreign key to users
    property_id INT,                -- Foreign key to properties
    check_in DATE,
    check_out DATE,
    guests INT,
    total_price DECIMAL(10,2),
    status ENUM('pending', 'confirmed', 'cancelled'),
    created_at TIMESTAMP,
    confirmed_at TIMESTAMP,
    FOREIGN KEY (guest_id) REFERENCES users(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
);
```

## 🎨 User Interface

### Landing Page
- Hero section with background image
- 3-field search bar (Where, When, Who)
- Featured Laikipia stays (horizontal scroll)
- Category tiles (Safari Lodges, Mountain Cabins, Farm Stays, Luxury Villas)
- Weekend deals section
- Features highlights
- Host CTA banner
- Responsive mobile design

### Navigation
- **Authenticated Users**: Dashboard, Browse, User Menu (Logout)
- **Unauthenticated Users**: Login, Register, Browse (if guest-accessible)
- **Hosts**: My Properties, Add Property, My Bookings
- **Guests**: My Bookings, Browse, Search

### Guest Dashboard
- Booking history with status badges
- View booking details
- Cancel bookings
- Upcoming stays
- Past stays

### Host Dashboard
- Property overview cards
- Quick stats (monthly earnings, occupancy rate, ratings)
- Recent bookings
- Add property button
- Manage properties (edit, delete, view bookings)
- Confirm/reject pending bookings
- Generate receipts

## 🔗 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Guest Routes
- `GET /` - Landing page
- `GET /browse` - Browse all properties
- `GET /search` - Search properties with filters
- `GET /property/<id>` - View property details
- `POST /book/<id>` - Create booking
- `GET /dashboard` - Guest dashboard (bookings)

### Host Routes
- `GET /dashboard` - Host dashboard (properties & bookings)
- `POST /add_property` - Create new property
- `POST /confirm_booking/<id>` - Confirm booking
- `GET /receipt/<id>` - Generate PDF receipt

### Booking API
- `POST /api/search` - JSON search endpoint
- `GET /api/property/<id>` - Property details JSON
- `POST /api/validate-dates` - Date validation
- `POST /api/upload-photo` - Upload property images

## ✨ Key Features Explained

### Double Booking Prevention
```python
# Validate dates before booking
is_available = Booking.validate_dates(property_id, check_in, check_out)
# Checks against ALL existing bookings for that property
```

### Password Security
```python
# Passwords are hashed using bcrypt
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# Verified during login
is_correct = bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

### Role-Based Access
```python
# Protected routes with decorators
@guest_required      # Only logged-in guests
@host_required       # Only logged-in hosts
@login_required      # Any authenticated user
```

### Image Upload
```python
# Hosts can upload multiple property images
# Images stored in /static/uploads/
# File names: {user_id}_{timestamp}_{original_name}
```

## 🐛 Troubleshooting

### MySQL Connection Error
```
Error: Port 3306 is CLOSED
Solution: Start MySQL in XAMPP Control Panel
```

### Database Not Found
```
Error: Unknown database 'smartstay_test'
Solution: Create database in phpMyAdmin (Step 2)
```

### Module Not Found
```
Error: ModuleNotFoundError: No module named 'flask'
Solution: pip install -r requirements.txt
```

### Port 5000 Already in Use
```
Error: Address already in use
Solution: Kill process using port 5000 or use different port
   Windows: netstat -ano | findstr :5000
```

## 📚 Documentation

- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Complete feature documentation
- [MYSQL_CONNECTION_GUIDE.md](MYSQL_CONNECTION_GUIDE.md) - Detailed MySQL setup
- [VISUAL_GUIDE.md](VISUAL_GUIDE.md) - UI/UX walkthrough
- [XAMPP_MYSQL_GUIDE.md](XAMPP_MYSQL_GUIDE.md) - XAMPP-specific setup

## 🔄 Development Workflow

### Making Changes
1. Edit Python files (routes, models, etc.)
2. Changes auto-reload with Flask debug mode
3. Refresh browser to see changes

### Testing
```bash
# Test without database
python -m pytest tests/

# Test specific route
python -c "from app import app; client = app.test_client(); print(client.get('/').status_code)"

# Check database
python test_connection.py
```

### Deployment
1. Set `DEBUG = False` in config.py
2. Use production WSGI server (Gunicorn, uWSGI)
3. Set strong `SECRET_KEY`
4. Use environment variables for sensitive data
5. Enable HTTPS/SSL

## 📄 License

This project is open source and available for educational and commercial use.

## 👥 Contributing

Contributions are welcome! Areas for enhancement:
- Payment integration (Stripe, PayPal)
- Email notifications
- Reviews & ratings system
- Wishlist functionality
- Chat messaging between hosts & guests
- Admin dashboard
- Analytics & reporting

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review error messages in browser console
3. Check Flask debug output in terminal
4. Review database logs

---

**Version**: 1.0.0 | **Last Updated**: April 2026 | **Status**: Production Ready ✅

### Step 6: Access the Application
- Open http://127.0.0.1:5000
- Register as guest or host
- Start exploring properties!

## Sample Data

The application includes sample users and properties for testing:

**Test Users:**
- Guest: guest@example.com / password123
- Host: host@example.com / password123

**Sample Properties:**
- Modern Downtown Apartment
- Cozy Beach House
- Mountain Cabin Retreat

## API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Guest Features
- `GET /` - Landing page
- `GET /browse` - Browse all listings
- `GET /property/<id>` - Property details
- `POST /search` - Search properties
- `POST /book/<property_id>` - Make booking
- `GET /dashboard/guest` - Guest dashboard

### Host Features
- `GET /dashboard/host` - Host dashboard
- `GET/POST /host/add-property` - Add new property
- `GET/POST /host/edit/<property_id>` - Edit property
- `DELETE /host/delete/<property_id>` - Delete property

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('guest', 'host') DEFAULT 'guest',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Properties Table
```sql
CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    max_guests INT DEFAULT 1,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT NOT NULL,
    property_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    guests INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP NULL,
    FOREIGN KEY (guest_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);
```

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- CSRF protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## Development

### Running Tests
```bash
python test_connection.py
```

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

## Deployment

For production deployment:

1. Set `DEBUG = False` in config
2. Use a production WSGI server (Gunicorn)
3. Set up proper database credentials
4. Enable HTTPS
5. Configure proper session secrets
6. Set up logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.
- ✅ **Add properties with detailed descriptions**
- ✅ **Upload multiple property photos**
- ✅ **View all incoming guest bookings**
- ✅ **Confirm/manage bookings**
- ✅ **Generate PDF receipts**
- ✅ **Role-based dashboard**

### System Features
- ✅ User authentication (guest & host roles)
- ✅ Secure password hashing
- ✅ Session management
- ✅ Property browsing and booking
- ✅ Booking confirmation system
- ✅ PDF receipt generation
- ✅ Mobile-responsive design
- ✅ Real-time flash messages
- ✅ Comprehensive error handling

## 🔐 Security

- **Password Hashing**: Werkzeug's `generate_password_hash()` and `check_password_hash()`
- **Session Management**: Flask secure sessions
- **Access Control**: Role-based routing (host/guest)
- **SQL Injection Prevention**: Parameterized queries
- **Input Validation**: All user inputs validated
- **Error Handling**: No sensitive data exposure

## 📋 User Accounts

### Guest Account
- Register as "Guest (Looking for accommodation)"
- Browse and book properties
- View your bookings
- Download receipts

### Host Account
- Register as "Host (Listing properties)"
- Add and manage properties
- View guest bookings
- Confirm reservations
- Generate receipts

## 🏗️ System Architecture

```
SmartStay Platform
├── Frontend (HTML/CSS/JS)
│   ├── Login & Register
│   ├── Property Browsing
│   ├── Guest Dashboard
│   └── Host Dashboard
├── Backend (Flask/Python)
│   ├── Authentication Routes
│   ├── Property Management
│   ├── Booking System
│   └── Receipt Generation
└── Database (MySQL)
    ├── Users (guests & hosts)
    ├── Properties (listings)
    └── Bookings (reservations)
```

## 📁 File Structure

```
smartstay/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database.sql/
│   └── database.sql           # Database schema
├── templates/                  # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html         # Guest dashboard
│   ├── host_dashboard.html    # Host dashboard
│   ├── browse.html
│   └── property_detail.html
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── landing.css
│   ├── js/
│   │   └── script.js
│   └── uploads/               # Property images
└── docs/
    ├── HOST_QUICK_START.md
    ├── HOST_SETUP_GUIDE.md
    ├── HOST_TEST_SCENARIOS.md
    └── IMPLEMENTATION_COMPLETE.md
```

## 🔗 Routes Overview

### Authentication
- `GET/POST /register` - User registration (guest or host)
- `GET/POST /login` - User login
- `GET /logout` - Logout

### Guest Routes
- `GET /dashboard` - Guest bookings dashboard
- `GET /browse` - Browse properties
- `GET /property/<id>` - Property details
- `POST /book/<id>` - Book a property

### Host Routes
- `GET /host_dashboard` - Host control panel
- `POST /add_property` - Add new property
- `POST /confirm_booking/<id>` - Confirm booking
- `GET /generate_receipt/<id>` - Download PDF receipt

## 🧪 Testing

### Test Host Registration
1. Go to `/register`
2. Fill form, select **"Host (Listing properties)"**
3. Click Sign Up
4. Login with your credentials
5. Should see Host Dashboard

### Test Host Features
1. Go to "Add New Property"
2. Fill property details including **description**
3. Upload photos (optional)
4. Click "Add Property"
5. Property appears in "Your Properties"

### Test Booking Management
1. Guest books a property
2. Host sees booking in "Incoming Bookings"
3. Host clicks "Confirm Booking"
4. Host clicks "Download Receipt"

## ⚙️ Configuration

### Database Connection
Edit in `app.py`:
```python
def get_db_connection():
    return pymysql.connect(
        host='localhost',      # MySQL host
        user='root',          # MySQL user
        password='',          # MySQL password
        database='smartstay',  # Database name
        cursorclass=pymysql.cursors.DictCursor
    )
```

### Flask Settings
```python
app.secret_key = 'smartstay_secret_key_2024'  # Change this!
```

## 📚 Database Schema

### Users Table
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- user_type (guest or host)
- created_at (Timestamp)
```

### Properties Table
```sql
- id (Primary Key)
- host_id (Foreign Key → users)
- title
- description
- location
- price
- max_guests
- image_url
- created_at
```

### Bookings Table
```sql
- id (Primary Key)
- guest_id (Foreign Key → users)
- property_id (Foreign Key → properties)
- check_in
- check_out
- guests
- total_price
- status (pending/confirmed/cancelled)
- created_at
```

## 🐛 Troubleshooting

### Can't Login
- Check username/email is correct
- Verify password (case-sensitive)
- Ensure you registered as the correct role

### No Properties Showing
- Refresh the page
- Verify you're logged in as a host
- Check MySQL connection

### Bookings Not Appearing
- Ensure guests have made bookings
- Verify you're logged in as the correct host
- Check database connection

### More Help
See:
- [HOST_QUICK_START.md](HOST_QUICK_START.md) - Quick fixes
- [HOST_SETUP_GUIDE.md](HOST_SETUP_GUIDE.md) - Setup help
- [HOST_TEST_SCENARIOS.md](HOST_TEST_SCENARIOS.md) - Testing guide

## 👥 User Roles

### Guest User
- Search and browse properties
- Book properties
- View booking status
- Download receipts
- Cannot list properties or confirm bookings

### Host User
- List and manage properties
- Add property descriptions and photos
- View all guest bookings for their properties
- Confirm pending bookings
- Generate booking receipts
- Cannot browse as a guest or book properties

## 🎨 UI/UX Features

- **Responsive Design**: Works on mobile, tablet, desktop
- **Modern Styling**: Clean, professional interface
- **Flash Messages**: Real-time notifications for actions
- **Form Validation**: Prevents errors before submission
- **Error Handling**: Clear, helpful error messages
- **Loading States**: Visual feedback during operations
- **Accessibility**: Semantic HTML and proper labels

## 📱 Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## 🚀 Performance

- Optimized database queries
- Caching for property listings
- Efficient session management
- Responsive images
- Minified CSS and JavaScript

## 📄 License

SmartStay © 2024. All rights reserved.

## 🤝 Contributing

For issues or improvements, please refer to the documentation files.

## 📞 Support

For support:
1. Check the relevant documentation file
2. Review error messages carefully
3. Verify MySQL server is running
4. Ensure all dependencies are installed

---

**Ready to use SmartStay?**

1. Start with [HOST_QUICK_START.md](HOST_QUICK_START.md) if you're a host
2. Refer to documentation files above for detailed help
3. Test the system with the test scenarios
4. Deploy to production when ready

Enjoy! 🏠
✅ Input validation
✅ Error handling
✅ Session security#   s m a r t s t a y  
 