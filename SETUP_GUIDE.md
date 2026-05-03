# SmartStay Setup & Deployment Guide

## Complete Step-by-Step Setup Instructions

### Phase 1: Environment Setup (15 minutes)

#### Step 1.1: Install Python 3.8+
```bash
# Windows: Download from python.org or use:
choco install python

# Verify installation
python --version
```

#### Step 1.2: Navigate to Project Directory
```bash
cd "c:\Users\DANNY\Documents\smartstay h"
```

#### Step 1.3: Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

#### Step 1.4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Verify all packages:**
```bash
pip list
```

Should show:
- Flask 2.3.3
- PyMySQL 1.1.0
- bcrypt 4.0.1
- ReportLab 4.0.7
- Pillow 10.0.1

---

### Phase 2: Database Setup (20 minutes)

#### Step 2.1: Start MySQL Service

**Option A: XAMPP (Easiest)**
1. Open XAMPP Control Panel
2. Click "Start" button next to MySQL
3. Wait for it to show "Running" with green indicator
4. Open phpMyAdmin: http://localhost/phpmyadmin

**Option B: Windows Services**
1. Open Services (services.msc)
2. Find "MySQL80" or similar
3. Right-click → Start

**Option C: Command Line (if installed standalone)**
```bash
mysql.server start
```

#### Step 2.2: Verify MySQL Connection
```bash
python test_connection.py
```

Expected output:
```
🔍 Testing MySQL Connection...
Port 3306 is OPEN
✅ MySQL server is running!
```

#### Step 2.3: Create Database
```bash
mysql -u root -p
```

If prompted for password, press Enter (default is empty for XAMPP).

```sql
-- Create database
CREATE DATABASE smartstay_test;

-- Use the database
USE smartstay_test;

-- Import schema
SOURCE database/schema.sql;

-- Verify tables created
SHOW TABLES;

-- Exit
EXIT;
```

Or use phpMyAdmin:
1. Login to phpMyAdmin: http://localhost/phpmyadmin
2. Click "New" database
3. Name: `smartstay_test`
4. Charset: `utf8mb4_unicode_ci`
5. Click "Create"
6. Click on `smartstay_test` database
7. Go to "Import" tab
8. Select `database/schema.sql`
9. Click "Go"

#### Step 2.4: Verify Database Setup
```bash
python -c "
from database import init_db
init_db()
"
```

Expected output:
```
✅ Database initialized successfully!
```

---

### Phase 3: Application Configuration (5 minutes)

#### Step 3.1: Update config.py (if needed)
```python
# config.py
class Config:
    # Database
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Empty for XAMPP default
    MYSQL_DATABASE = 'smartstay_test'
    MYSQL_CHARSET = 'utf8mb4'
    MYSQL_TIMEOUT = 10
    
    # Flask
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DEBUG = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60
```

#### Step 3.2: Create uploads folder
```bash
mkdir static/uploads
```

---

### Phase 4: Launch Application (5 minutes)

#### Step 4.1: Start Flask Development Server
```bash
python app.py
```

**Expected output:**
```
✅ Database initialized successfully!
Starting SmartStay...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

#### Step 4.2: Access the Application
- **Homepage**: http://127.0.0.1:5000
- **Login**: http://127.0.0.1:5000/login
- **Register**: http://127.0.0.1:5000/register

---

### Phase 5: Test with Sample Accounts (10 minutes)

#### Sample Account 1: Guest
```
Email: guest@example.com
Password: password123
```

Actions to test:
1. Login with guest account
2. Browse properties
3. Search for properties
4. View property details
5. Make a booking
6. View bookings in dashboard

#### Sample Account 2: Host
```
Email: host@example.com
Password: password123
```

Actions to test:
1. Login with host account
2. View host dashboard
3. Add new property (with details & optional images)
4. View bookings on your properties
5. Confirm pending bookings
6. Generate PDF receipt

#### Create New Guest Account
1. Click "Sign Up"
2. Select "Guest" role
3. Fill in details:
   - Full Name: `[Your Name]`
   - Email: `[Your Email]`
   - Password: `[Secure Password]`
4. Confirm password
5. Click "Register"

#### Create New Host Account
1. Click "Become a Host"
2. Fill in details:
   - Full Name: `[Your Name]`
   - Email: `[Your Email]`
   - Password: `[Secure Password]`
3. Confirm password
4. Click "Register as Host"

---

## User Workflows

### Guest Booking Flow
```
1. Login → Guest Dashboard
2. Click "Browse" or search on homepage
3. Select property from list
4. Click property card → View Details
5. Select check-in & check-out dates
6. Select number of guests
7. Click "Book Now"
8. Confirm booking
9. View in dashboard → "My Bookings"
```

### Host Property Management Flow
```
1. Login → Host Dashboard
2. Click "Add Property" button
3. Fill in:
   - Title: "Beautiful Downtown Loft"
   - Description: "Modern, spacious, great views"
   - Location: "Downtown"
   - Price: "150"
   - Max Guests: "4"
   - Upload images (optional)
4. Click "Create Property"
5. View in dashboard → Property list
6. Click property → View bookings
7. Manage bookings (confirm, view details)
```

---

## Troubleshooting Guide

### Issue: "Port 3306 is CLOSED"
```
Error: MySQL is not running

Solution:
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait 10 seconds
4. Try again
```

### Issue: "Unknown database 'smartstay_test'"
```
Error: Database doesn't exist

Solution:
1. Go to phpMyAdmin: http://localhost/phpmyadmin
2. Click "New" database
3. Create database named: smartstay_test
4. Import schema.sql
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
```
Error: Flask not installed

Solution:
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
```
Error: Another app using port 5000

Solution (Windows):
netstat -ano | findstr :5000
taskkill /PID [PID] /F

Or use different port:
python app.py --port 5001
```

### Issue: "Cannot upload images"
```
Error: Upload fails silently

Solution:
1. Check static/uploads/ folder exists
2. Verify file permissions
3. Check file is image (jpg, jpeg, png, gif)
4. Check file size < 5MB
```

### Issue: "Password incorrect but I'm sure it's right"
```
Note: Sample accounts use password: password123
But passwords are case-sensitive

Solution:
Try resetting:
1. Use phpMyAdmin to update password
2. Or create new test account
```

---

## Development Tips

### Enable Debug Mode
In `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Debug features:
- Auto-reload on file changes
- Interactive debugger on errors
- Request/response logging

### Check Database
```bash
# Open MySQL CLI
mysql -u root

# View all data
USE smartstay_test;
SELECT * FROM users;
SELECT * FROM properties;
SELECT * FROM bookings;

# Check table structure
DESC users;
DESC properties;
DESC bookings;
```

### Monitor Logs
Flask will show requests in terminal:
```
GET / HTTP/1.1 - 200
POST /login HTTP/1.1 - 302
POST /book/1 HTTP/1.1 - 201
```

### Test Without Browser
```bash
# Using curl
curl http://127.0.0.1:5000/

# Using Python
import requests
r = requests.get('http://127.0.0.1:5000/')
print(r.status_code)
```

---

## Production Deployment

### Before Going Live

1. **Security**
   - Change `DEBUG = False`
   - Set strong `SECRET_KEY`
   - Use environment variables
   - Enable HTTPS/SSL
   - Validate all inputs

2. **Database**
   - Use dedicated MySQL server (not XAMPP)
   - Set strong database password
   - Enable backups
   - Use connection pooling

3. **Performance**
   - Use production WSGI (Gunicorn, uWSGI)
   - Enable caching
   - Compress static files
   - Use CDN for images

### Deploy to Server
```bash
# Using Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With Nginx reverse proxy (advanced)
# See deployment documentation
```

### Environment Variables
```bash
# .env file
FLASK_ENV=production
MYSQL_HOST=your-server.com
MYSQL_USER=prod_user
MYSQL_PASSWORD=strong_password
SECRET_KEY=random_long_string_here
```

---

## Support & Resources

### Files to Reference
- `README.md` - Overview & features
- `MYSQL_CONNECTION_GUIDE.md` - Detailed MySQL setup
- `VISUAL_GUIDE.md` - UI walkthrough
- `XAMPP_MYSQL_GUIDE.md` - XAMPP-specific help
- `DOCUMENTATION_INDEX.md` - Feature documentation

### Common Commands
```bash
# Start app
python app.py

# Start in virtual environment
venv\Scripts\activate && python app.py

# Stop app
CTRL+C

# Test database connection
python test_connection.py

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version

# Check installed packages
pip list
```

### Getting Help
1. Check error message carefully
2. Look at terminal output for clues
3. Check browser console (F12)
4. Review relevant documentation file
5. Check database logs in phpMyAdmin

---

## Verification Checklist

Before considering setup complete, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] MySQL running
- [ ] Database `smartstay_test` created
- [ ] Tables created (users, properties, bookings)
- [ ] Sample data loaded
- [ ] App starts without errors
- [ ] Can access http://127.0.0.1:5000
- [ ] Can login with guest@example.com
- [ ] Can login with host@example.com
- [ ] Can browse properties as guest
- [ ] Can manage properties as host
- [ ] Can make bookings
- [ ] Can view bookings in dashboard

Once all items are checked ✅, the application is ready to use!

---

**Last Updated**: April 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
