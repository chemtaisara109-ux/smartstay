"""
Host routes (dashboard, property management, bookings)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models.listing import Property
from models.booking import Booking
from models.admin_verification import AdminVerification
from models.property_availability import AvailabilityBlock
from utils.auth_helper import host_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from datetime import datetime
import os

host_bp = Blueprint('host', __name__)

@host_bp.route('/host/dashboard')
@host_required
def dashboard():
    """Host dashboard showing properties and bookings"""
    user_id = session['user_id']

    properties = Property.find_by_host_id(user_id)
    bookings = Booking.find_by_host_id(user_id)

    monthly_earnings = sum(booking.total_price or 0 for booking in bookings)
    recent_bookings = bookings[:5]
    occupancy_rate = 0.0
    avg_rating = 0.0

    return render_template(
        'dashboard_host.html',
        properties=properties,
        bookings=bookings,
        recent_bookings=recent_bookings,
        monthly_earnings=monthly_earnings,
        occupancy_rate=occupancy_rate,
        avg_rating=avg_rating
    )

@host_bp.route('/add_property', methods=['POST'])
@host_required
def add_property():
    """Add a new property"""
    title = request.form.get('title', '').strip()
    location = request.form.get('location', '').strip()
    price = request.form.get('price')
    max_guests = request.form.get('max_guests')
    description = request.form.get('description', '').strip()

    # Validation
    if not all([title, location, price, max_guests]):
        flash('⚠️ All fields are required', 'error')
        return redirect(url_for('host.dashboard'))

    try:
        price = float(price)
        max_guests = int(max_guests)

        if price <= 0:
            flash('⚠️ Price must be greater than 0', 'error')
            return redirect(url_for('host.dashboard'))

        if max_guests < 1:
            flash('⚠️ Maximum guests must be at least 1', 'error')
            return redirect(url_for('host.dashboard'))

    except ValueError:
        flash('⚠️ Invalid price or guest count', 'error')
        return redirect(url_for('host.dashboard'))

    # Handle file uploads
    photos = request.files.getlist('photos')
    image_urls = []
    for photo in photos:
        if photo and photo.filename:
            # Basic file validation
            if not photo.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                continue

            filename = f"{session['user_id']}_{title.replace(' ', '_')}_{len(image_urls)}.jpg"
            filepath = os.path.join('static', 'uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            photo.save(filepath)
            image_urls.append(filename)

    image_url = ','.join(image_urls) if image_urls else None

    try:
        property = Property.create(
            host_id=session['user_id'],
            title=title,
            location=location,
            price=price,
            max_guests=max_guests,
            description=description,
            image_url=image_url
        )

        # Create admin verification request
        try:
            AdminVerification.create(
                property_id=property.id,
                admin_id=1,  # Default admin ID, should be updated to actual admin
                status='pending',
                notes='New property listing submitted for verification'
            )
        except Exception as verification_err:
            print(f"[ADD_PROPERTY] Verification creation error: {verification_err}")
            # Don't fail the property creation if verification fails

        flash('✅ Property added successfully! It will be visible after admin verification.', 'success')
    except Exception as err:
        print(f"[ADD_PROPERTY] Error: {err}")
        flash('❌ Error adding property. Please try again.', 'error')

    return redirect(url_for('host.dashboard'))

@host_bp.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
@host_required
def edit_property(property_id):
    """View and update a property listing."""
    property = Property.find_by_id(property_id)
    if not property or property.host_id != session['user_id']:
        flash('❌ Access denied', 'error')
        return redirect(url_for('host.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        location = request.form.get('location', '').strip()
        price = request.form.get('price')
        max_guests = request.form.get('max_guests')
        description = request.form.get('description', '').strip()

        if not all([title, location, price, max_guests, description]):
            flash('⚠️ All fields are required', 'error')
            return redirect(url_for('host.edit_property', property_id=property_id))

        try:
            price = float(price)
            max_guests = int(max_guests)

            if price <= 0:
                flash('⚠️ Price must be greater than 0', 'error')
                return redirect(url_for('host.edit_property', property_id=property_id))

            if max_guests < 1:
                flash('⚠️ Maximum guests must be at least 1', 'error')
                return redirect(url_for('host.edit_property', property_id=property_id))
        except ValueError:
            flash('⚠️ Invalid price or guest count', 'error')
            return redirect(url_for('host.edit_property', property_id=property_id))

        # Handle optional file uploads
        photos = request.files.getlist('photos')
        existing_images = property.image_url.split(',') if property.image_url else []
        new_images = []
        for photo in photos:
            if photo and photo.filename:
                if not photo.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                    continue

                filename = f"{session['user_id']}_{title.replace(' ', '_')}_{len(existing_images) + len(new_images)}.jpg"
                filepath = os.path.join('static', 'uploads', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                photo.save(filepath)
                new_images.append(filename)

        image_url = ','.join(existing_images + new_images) if existing_images or new_images else None

        try:
            property.update(
                title=title,
                location=location,
                price=price,
                max_guests=max_guests,
                description=description,
                image_url=image_url
            )
            flash('✅ Property updated successfully!', 'success')
        except Exception as err:
            print(f"[EDIT_PROPERTY] Error: {err}")
            flash('❌ Error updating property. Please try again.', 'error')

        return redirect(url_for('host.dashboard'))

    return render_template('edit_property.html', property=property)


@host_bp.route('/property/<int:property_id>/calendar')
@host_required
def property_calendar(property_id):
    """Display bookings and blocked dates for a property."""
    property = Property.find_by_id(property_id)
    if not property or property.host_id != session['user_id']:
        flash('❌ Access denied', 'error')
        return redirect(url_for('host.dashboard'))

    bookings = Booking.find_by_property_id(property_id)
    blocked_dates = AvailabilityBlock.find_by_property_id(property_id)

    return render_template('property_calendar.html', property=property, bookings=bookings, blocked_dates=blocked_dates)


@host_bp.route('/property/<int:property_id>/calendar/block', methods=['POST'])
@host_required
def block_property_dates(property_id):
    """Create a blocked date range for the property."""
    property = Property.find_by_id(property_id)
    if not property or property.host_id != session['user_id']:
        flash('❌ Access denied', 'error')
        return redirect(url_for('host.dashboard'))

    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    notes = request.form.get('notes', '').strip()

    if not start_date or not end_date:
        flash('⚠️ Start and end dates are required', 'error')
        return redirect(url_for('host.property_calendar', property_id=property_id))

    if start_date > end_date:
        flash('⚠️ End date must be after or equal to start date', 'error')
        return redirect(url_for('host.property_calendar', property_id=property_id))

    try:
        AvailabilityBlock.create(property_id, start_date, end_date, notes)
        flash('✅ Availability updated. The dates are now blocked.', 'success')
    except Exception as err:
        print(f"[BLOCK_PROPERTY_DATES] Error: {err}")
        flash('❌ Could not block these dates. Please try again.', 'error')

    return redirect(url_for('host.property_calendar', property_id=property_id))


@host_bp.route('/confirm_booking/<int:booking_id>', methods=['POST'])
@host_required
def confirm_booking(booking_id):
    """Confirm a booking"""
    try:
        booking = Booking.find_by_id(booking_id)

        if not booking:
            flash('❌ Booking not found', 'error')
            return redirect(url_for('host.dashboard'))

        # Check if host owns this property
        property = Property.find_by_id(booking.property_id)
        if not property or property.host_id != session['user_id']:
            flash('❌ Access denied', 'error')
            return redirect(url_for('host.dashboard'))

        booking.confirm()
        flash('✅ Booking confirmed!', 'success')

    except Exception as err:
        print(f"[CONFIRM_BOOKING] Error: {err}")
        flash('❌ Error confirming booking. Please try again.', 'error')

    return redirect(url_for('host.dashboard'))

@host_bp.route('/receipt/<int:booking_id>')
@host_required
def generate_receipt(booking_id):
    """Generate PDF receipt for booking"""
    try:
        booking = Booking.find_by_id(booking_id)

        if not booking:
            flash('❌ Booking not found', 'error')
            return redirect(url_for('host.dashboard'))

        # Check if host owns this property
        property = Property.find_by_id(booking.property_id)
        if not property or property.host_id != session['user_id']:
            flash('❌ Access denied', 'error')
            return redirect(url_for('host.dashboard'))

        # Generate PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "SmartStay Booking Receipt")

        # Booking details
        c.setFont("Helvetica", 12)
        y = height - 100
        c.drawString(100, y, f"Booking ID: {booking.id}")
        y -= 20
        c.drawString(100, y, f"Guest Name: {booking.guest_name}")
        y -= 20
        c.drawString(100, y, f"Property: {booking.property_name}")
        y -= 20
        c.drawString(100, y, f"Location: {booking.location}")
        y -= 20
        c.drawString(100, y, f"Check-in: {booking.check_in}")
        y -= 20
        c.drawString(100, y, f"Check-out: {booking.check_out}")
        y -= 20
        c.drawString(100, y, f"Number of Guests: {booking.guests}")
        y -= 20
        c.drawString(100, y, f"Total Cost: ${booking.total_price:.2f}")
        y -= 20
        if booking.confirmed_at:
            c.drawString(100, y, f"Confirmed on: {booking.confirmed_at}")

        c.save()
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name=f'receipt_{booking_id}.pdf', mimetype='application/pdf')

    except Exception as err:
        print(f"[RECEIPT] Error: {err}")
        flash('❌ Error generating receipt. Please try again.', 'error')
        return redirect(url_for('host.dashboard'))