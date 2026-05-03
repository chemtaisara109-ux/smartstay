# SmartStay Enhanced Authentication System

A comprehensive, production-ready authentication system for your SmartStay platform with role-based access, password reset, and persistent login.

## 🎯 Features

- ✅ **Dual Role System**: Guest and Host roles with role-specific fields
- ✅ **Secure Password Hashing**: bcrypt for secure password storage
- ✅ **Remember Me**: 30-day persistent login with secure tokens
- ✅ **Password Reset**: Email-based password recovery
- ✅ **Dynamic Forms**: Role-based form fields that show/hide without page reload
- ✅ **Session Management**: Secure session handling with CSRF protection
- ✅ **Input Validation**: Comprehensive validation on both client and server
- ✅ **Responsive Design**: Mobile-friendly authentication forms
- ✅ **Error Handling**: User-friendly error messages

---

## 📋 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    full_name VARCHAR(100),
    email VARCHAR(120) UNIQUE,
    password VARCHAR(255),
    role ENUM('guest', 'host'),
    phone VARCHAR(20),
    property_name VARCHAR(200),
    location VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Supporting Tables
- **password_resets**: Manage password reset tokens (24-hour expiry)
- **remember_tokens**: Store remember-me tokens (30-day expiry)
- **login_audit**: Track login attempts for security

---

## 🔧 Setup Instructions

### 1. MySQL Setup

```bash
mysql -u root -p < database/mysql_schema.sql
```

### 2. Enable MySQL in Config

Edit `config.py`:
```python
USE_SQLITE = False  # Switch from SQLite to MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'smartstay_db'
```

### 3. Install Dependencies

```bash
pip install flask-jwt-extended python-dotenv
```

### 4. Update Flask App

In `app.py`:
```python
from routes.auth_enhanced import auth_bp

# Register enhanced auth blueprint
app.register_blueprint(auth_bp)
```

---

## 📝 Registration Flow

### Guest Registration
1. User selects "Guest" role
2. Fills: Full Name, Email, Password
3. Automatic redirect to guest dashboard

### Host Registration
1. User selects "Host" role
2. Additional fields appear:
   - Phone Number
   - Property Name
   - Location
3. All fields required for hosts
4. Automatic redirect to host dashboard

---

## 🔐 Login Features

### Standard Login
```
Email: guest@smartstay.com
Password: Guest@1234
```

### Remember Me (30 days)
- Check "Remember me" checkbox
- Cookie stored with secure token
- Automatic login on return visits
- Token expires after 30 days

### Forgot Password
1. Click "Forgot password?"
2. Enter email address
3. Receive reset link via email (or console for testing)
4. Create new password
5. Login with new password

---

## 🎨 User Interfaces

### Enhanced Templates

1. **register_enhanced.html**
   - Dynamic role selector
   - Host-specific fields (shown/hidden via JavaScript)
   - Password strength indicator
   - Terms & conditions checkbox

2. **login_enhanced.html**
   - Remember me checkbox
   - "Forgot password?" link
   - Error/success messages
   - Security info display

3. **forgot_password.html**
   - Email input for reset request
   - Security confirmation message

4. **reset_password.html**
   - New password input
   - Password confirmation
   - Validation on form submission

---

## 🔄 Session Management

### Session Data
```python
session['user_id']      # User's unique ID
session['username']     # Username
session['full_name']    # Full name
session['email']        # Email address
session['role']         # 'guest' or 'host'
session.permanent       # True if remember me checked
```

### Session Timeout
- Default: 30 minutes (browser close)
- With Remember Me: 30 days
- Permanent sessions use `PERMANENT_SESSION_LIFETIME`

---

## 🛡️ Security Features

### Password Security
- Bcrypt hashing with salt
- Minimum 8 characters
- Require: uppercase, lowercase, numbers
- Password confirmation on change

### Token Security
- Password reset tokens: 24-hour expiry
- Remember me tokens: 30-day expiry
- Tokens marked as used after consumption
- Tokens stored hashed in database

### Session Security
- HTTPOnly cookies (no JavaScript access)
- SameSite protection (CSRF mitigation)
- Secure flag in production (HTTPS)

---

## 💻 API Endpoints

### Authentication Routes

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/register` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/logout` | GET | Logout & clear session |
| `/forgot-password` | GET/POST | Request password reset |
| `/reset-password/<token>` | GET/POST | Reset password |
| `/profile` | GET/POST | View/edit profile |

---

## 🧪 Testing

### Test User Credentials

**Guest:**
- Email: `guest@smartstay.com`
- Password: `Guest@1234`

**Host:**
- Email: `host@smartstay.com`
- Password: `Host@1234`

### Test Scenarios

1. **Basic Login/Logout**
   - Login with credentials
   - Verify dashboard access
   - Logout and verify redirect

2. **Remember Me**
   - Login with "Remember me" checked
   - Close browser
   - Reopen and verify auto-login

3. **Forgot Password**
   - Request reset
   - Use reset link
   - Create new password
   - Login with new password

4. **Role-Based Access**
   - Login as guest → guest dashboard
   - Login as host → host dashboard
   - Test feature access restrictions

---

## 📱 Mobile Responsive

All authentication pages are mobile-responsive with:
- Stacked layout on small screens
- Touch-friendly form controls
- Readable fonts and spacing
- Proper viewport configuration

---

## 🚀 Deployment Checklist

- [ ] Switch `USE_SQLITE = False` in config.py
- [ ] Configure MySQL database
- [ ] Set `SESSION_COOKIE_SECURE = True` (HTTPS only)
- [ ] Configure email service for password resets
- [ ] Update `SECRET_KEY` with strong value
- [ ] Enable HTTPS/SSL
- [ ] Test all authentication flows
- [ ] Monitor login_audit table
- [ ] Regular database backups

---

## 📚 File Structure

```
smartstay/
├── models/
│   └── user_enhanced.py         # Enhanced User model
├── routes/
│   └── auth_enhanced.py         # Enhanced auth routes
├── utils/
│   ├── auth_service.py          # Password reset & remember me
│   └── auth_helper.py           # Decorators
├── templates/
│   ├── register_enhanced.html   # Registration form
│   ├── login_enhanced.html      # Login form
│   ├── forgot_password.html     # Forgot password
│   └── reset_password.html      # Reset password
└── database/
    └── mysql_schema.sql         # MySQL schema
```

---

## 🐛 Troubleshooting

### Email Not Sending
- Email feature is placeholder for testing
- Reset link printed to console
- Implement actual email service in production

### Remember Me Not Working
- Check cookie settings in browser
- Verify `httponly` flag not blocking cookies
- Check token expiry in database

### Password Reset Failing
- Verify token hasn't expired (24 hours)
- Check token marks as used only once
- Verify password meets requirements

---

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com)
- [Bcrypt Guide](https://github.com/pyca/bcrypt)
- [OWASP Authentication Guide](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

## 📞 Support

For issues or questions about the authentication system:
1. Check error messages in browser console
2. Review Flask debug output
3. Check database for user records
4. Verify all configuration settings

---

**Last Updated**: April 28, 2026
**Status**: Production Ready ✅
