from flask import Flask, render_template
from config import Config
from database import init_db
from routes.auth_enhanced import auth_bp
from routes.guest import guest_bp
from routes.host import host_bp
from routes.booking import booking_bp
from routes.review import review_bp
from routes.admin import admin_bp
import sys

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def landing():
    return render_template('index.html')

# Initialize database and create sample data
init_db()

# Import and run sample data setup (only if tables are empty)
try:
    from models.user_enhanced import User
    from models.listing import Property

    # Check if we have any users
    if not User.find_by_email('guest@smartstay.com'):
        print("📝 Creating sample data...")
        import subprocess
        subprocess.run([sys.executable, 'setup_sample_data.py'], check=True)
except Exception as e:
    print(f"⚠️ Sample data setup skipped: {e}")

app.register_blueprint(auth_bp)
app.register_blueprint(guest_bp)
app.register_blueprint(host_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(review_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    print("Starting SmartStay...")
    print("Visit http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
