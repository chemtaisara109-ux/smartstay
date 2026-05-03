"""
Simple Authentication Routes for SmartStay
Handles registration, login, logout, and profile
"""
import re
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models.user_enhanced import User
from utils.validators import validate_email, validate_password
from utils.auth_helper import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    """Simple registration with role selection"""
    selected_role = 'guest'
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'guest')
        selected_role = role
        phone = request.form.get('phone', '').strip() if role == 'host' else None
        property_name = request.form.get('property_name', '').strip() if role == 'host' else None
        location = request.form.get('location', '').strip() if role == 'host' else None

        if not full_name or not email or not password or not confirm_password:
            return render_template('register_enhanced.html', error='Please fill in all required fields.', selected_role=role)

        if password != confirm_password:
            return render_template('register_enhanced.html', error='Passwords do not match.', selected_role=role)

        if not validate_email(email):
            return render_template('register_enhanced.html', error='Invalid email format.', selected_role=role)

        if not validate_password(password):
            return render_template('register_enhanced.html', error='Password must be at least 8 characters with uppercase, lowercase, and numbers.', selected_role=role)

        if User.email_exists(email):
            return render_template('register_enhanced.html', error='Email already registered.', selected_role=role)

        username = re.sub(r'[^A-Za-z0-9_]+', '_', full_name.lower()).strip('_')
        if len(username) < 3:
            username = email.split('@')[0]
        if len(username) > 50:
            username = username[:50]

        base_username = username
        suffix = 1
        while User.username_exists(username):
            username = f"{base_username}_{suffix}"
            if len(username) > 50:
                username = username[:50]
            suffix += 1

        if role == 'host' and (not phone or not property_name or not location):
            return render_template('register_enhanced.html', error='Please fill in all host information fields.', selected_role=role)

        user = User.create(username, full_name, email, password, role, phone, property_name, location)

        session['user_id'] = user.id
        session['username'] = user.username
        session['full_name'] = user.full_name
        session['email'] = user.email
        session['role'] = user.role

        flash(f'Account created successfully! Welcome, {full_name}!', 'success')

        return redirect(url_for('host.dashboard') if role == 'host' else url_for('guest.dashboard'))

    return render_template('register_enhanced.html', selected_role=selected_role)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """Simple login with session management"""
    if 'user_id' in session:
        return redirect(url_for('host.dashboard') if session.get('role') == 'host' else url_for('guest.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login_enhanced.html', error='Email and password are required.')

        user = User.find_by_email(email)
        if not user or not User.check_password(user.password, password):
            return render_template('login_enhanced.html', error='Invalid email or password.')

        session['user_id'] = user.id
        session['username'] = user.username
        session['full_name'] = user.full_name
        session['email'] = user.email
        session['role'] = user.role

        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('host.dashboard') if user.role == 'host' else url_for('guest.dashboard'))

    return render_template('login_enhanced.html')


@auth_bp.route('/dashboard')
@login_required
def dashboard_route():
    """Redirect /dashboard to the correct role-specific dashboard."""
    role = session.get('role')
    if role == 'host':
        return redirect(url_for('host.dashboard'))
    if role == 'guest':
        return redirect(url_for('guest.dashboard'))
    if role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))

    flash('Unknown user role. Please log in again.', 'error')
    session.clear()
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/auth/host-register', methods=['GET', 'POST'])
def host_register_alias():
    return host_register()


@auth_bp.route('/host-register', methods=['GET', 'POST'])
def host_register():
    """Host registration page and submit handler"""
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'host')
        phone = request.form.get('phone', '').strip()
        property_name = request.form.get('property_name', '').strip() or request.form.get('property_title', '').strip()
        location = request.form.get('location', '').strip()

        if not full_name or not email or not password or not confirm_password or not phone or not property_name or not location:
            return render_template('host_register.html', error='Please fill in all required host registration fields.', selected_role='host')

        if password != confirm_password:
            return render_template('host_register.html', error='Passwords do not match.', selected_role='host')

        if not validate_email(email):
            return render_template('host_register.html', error='Invalid email format.', selected_role='host')

        if not validate_password(password):
            return render_template('host_register.html', error='Password must be at least 8 characters with uppercase, lowercase, and numbers.', selected_role='host')

        if User.email_exists(email):
            return render_template('host_register.html', error='Email already registered.', selected_role='host')

        username = re.sub(r'[^A-Za-z0-9_]+', '_', full_name.lower()).strip('_')
        if len(username) < 3:
            username = email.split('@')[0]
        if len(username) > 50:
            username = username[:50]

        base_username = username
        suffix = 1
        while User.username_exists(username):
            username = f"{base_username}_{suffix}"
            if len(username) > 50:
                username = username[:50]
            suffix += 1

        user = User.create(username, full_name, email, password, role='host', phone=phone, property_name=property_name, location=location)

        session['user_id'] = user.id
        session['username'] = user.username
        session['full_name'] = user.full_name
        session['email'] = user.email
        session['role'] = user.role

        flash(f'Host account created successfully! Welcome, {full_name}!', 'success')
        return redirect(url_for('host.dashboard'))

    return render_template('host_register.html', selected_role='host')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('landing'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    user = User.find_by_id(session['user_id'])

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()

        if user.role == 'host':
            property_name = request.form.get('property_name', '').strip()
            location = request.form.get('location', '').strip()
            user.update_profile(full_name=full_name, phone=phone, property_name=property_name, location=location)
        else:
            user.update_profile(full_name=full_name, phone=phone)

        session['full_name'] = full_name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile.html', user=user)
from database import get_db_connection, get_placeholder
