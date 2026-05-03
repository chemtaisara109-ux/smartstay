         # XAMPP MySQL Setup & Troubleshooting

## ✅ Quick Start for XAMPP Users

### Step 1: Start MySQL in XAMPP

1. Open XAMPP Control Panel (`C:\xampp\xampp-control.exe`)
2. Look for "MySQL" module
3. Click the "Start" button
4. Wait for status to show "Running"

### Step 2: Verify MySQL is Running

```bash
netstat -an | findstr 3306
```

**Expected output:** Should show `LISTENING` on 127.0.0.1:3306

### Step 3: Create Database

Option A - Quick Python Command:
```bash
python -c "import pymysql; c = pymysql.connect(host='localhost', user='root'); c.cursor().execute('CREATE DATABASE IF NOT EXISTS smartstay_db'); c.close(); print('✅ Done')"
```

Option B - Using phpMyAdmin:
1. Open http://localhost/phpmyadmin
2. Click "Databases"
3. Create: `smartstay_db`

---

## 🔍 Diagnostic Commands

### Check MySQL Service
```bash
sc query MySQL80
```
Or for MariaDB:
```bash
sc query MariaDB
```

### Start MySQL Service (if installed as service)
```bash
net start MySQL80
```

### Check Port 3306
```bash
netstat -an | findstr 3306
```

### List MySQL Databases
```bash
mysql -u root -e "SHOW DATABASES;"
```

### Connect to MySQL
```bash
mysql -u root -h localhost
```

---

## 🐛 Common XAMPP Issues

### Issue: MySQL won't start

**Solution:**
1. Check XAMPP logs: `C:\xampp\mysql\data\*.err`
2. Try stopping other MySQL instances:
   ```bash
   taskkill /IM mysqld.exe /F
   ```
3. Restart XAMPP
4. Check if port 3306 is in use:
   ```bash
   netstat -ano | findstr :3306
   ```

### Issue: Port 3306 already in use

**Solution:**
```bash
# Find what's using port 3306
netstat -ano | findstr :3306

# Get the PID from output, then kill it
taskkill /PID <PID> /F
```

### Issue: Can't connect with empty password

**Solution:**
```python
# Make sure password is empty string or None:
pymysql.connect(
    host='localhost',
    user='root',
    password='',  # Empty string
    database='smartstay_db'
)
```

### Issue: MySQL keeps crashing

**Solution:**
1. Back up your data
2. Uninstall MySQL from XAMPP
3. Delete `C:\xampp\mysql\data\` folder
4. Reinstall MySQL in XAMPP Control Panel
5. Recreate database

---

## 📝 config.py Settings for XAMPP

```python
# For XAMPP MySQL
MYSQL_HOST = 'localhost'      # Or '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''           # Empty for XAMPP default
MYSQL_DATABASE = 'smartstay_db'
MYSQL_PORT = 3306
MYSQL_CHARSET = 'utf8mb4'
MYSQL_TIMEOUT = 10
```

---

## 🚀 Complete Testing Workflow

```bash
# 1. Make sure XAMPP MySQL is running (via Control Panel)

# 2. Run the connection test
python test_connection.py

# 3. Review any errors and fix them

# 4. Once test passes, run the Flask app
python app.py

# 5. Open in browser
http://localhost:5000
```

---

## 📊 XAMPP MySQL Locations

| Item | Location |
|------|----------|
| XAMPP Install | C:\xampp\ |
| MySQL Binary | C:\xampp\mysql\bin\mysql.exe |
| MySQL Data | C:\xampp\mysql\data\ |
| MySQL Logs | C:\xampp\mysql\data\*.err |
| phpMyAdmin | http://localhost/phpmyadmin |
| Config | C:\xampp\mysql\bin\my.ini |

---

## ✅ Verification Commands

```bash
# 1. Check MySQL is installed
dir C:\xampp\mysql\bin\mysql.exe

# 2. Check XAMPP is running
netstat -an | findstr 3306

# 3. Test MySQL connection
mysql -u root -e "SELECT VERSION();"

# 4. List databases
mysql -u root -e "SHOW DATABASES;"

# 5. Check if smartstay_db exists
mysql -u root -e "SHOW DATABASES LIKE 'smartstay_db';"

# 6. Show tables in database
mysql -u root -e "USE smartstay_db; SHOW TABLES;"
```

---

## 🎯 When Everything Works

You should see:
```
✅ MySQL connected successfully to 'smartstay_db'
✅ Database initialized successfully!
Starting SmartStay...
 * Running on http://localhost:5000
```

Then open http://localhost:5000 in your browser!
