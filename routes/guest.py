"""
Guest routes (dashboard, browse, booking)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.listing import Property
from models.booking import Booking
from utils.auth_helper import guest_required, login_required
from utils.validators import validate_dates, validate_guests
from utils.email_helper import send_booking_confirmation, notify_host_of_booking
from datetime import datetime

guest_bp = Blueprint('guest', __name__)

@guest_bp.route('/guest/dashboard')
@guest_required
def dashboard():
    """Guest dashboard showing bookings"""
    user_id = session['user_id']
    bookings = Booking.find_by_guest_id(user_id)

    # Get featured properties for quick booking
    featured_properties = Property.search()[:6]  # Get first 6 properties as featured

    return render_template('dashboard_guest.html', bookings=bookings, featured_properties=featured_properties)

@guest_bp.route('/browse')
@guest_required
def browse():
    """Browse available properties"""
    properties = Property.search()
    return render_template('browse.html', properties=properties)

@guest_bp.route('/search')
@guest_required
def search():
    """Search properties"""
    location = request.args.get('location', '')
    checkin = request.args.get('checkin', '')
    checkout = request.args.get('checkout', '')
    guests = int(request.args.get('guests', 1))

    properties = Property.search(location=location, max_guests=guests)

    return render_template('search_results.html',
                         properties=properties,
                         location=location,
                         checkin=checkin,
                         checkout=checkout,
                         guests=guests)

@guest_bp.route('/booking-success/<int:booking_id>')
def booking_success(booking_id):
    """Show booking success page"""
    booking = Booking.find_by_id(booking_id)
    
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('guest.dashboard'))
    
    # If user is logged in, check if booking belongs to them
    if 'user_id' in session and session.get('role') == 'guest':
        if booking.guest_id != session['user_id']:
            flash('Access denied', 'error')
            return redirect(url_for('guest.dashboard'))
    
    if not hasattr(booking, 'property_name') or not booking.property_name:
        property = Property.find_by_id(booking.property_id)
        if property:
            booking.property_name = property.title
            booking.location = property.location
    
    return render_template('booking_success.html', booking=booking)

@guest_bp.route('/property/<int:property_id>')
@guest_required
def property_detail(property_id):
    """View property details"""
    property = Property.find_by_id(property_id)

    if not property:
        flash('Property not found', 'error')
        return redirect(url_for('guest.browse'))

    return render_template('property_detail.html', property=property)

@guest_bp.route('/book/<int:property_id>', methods=['POST'])
@guest_required
def book_property(property_id):
    """Book a property"""
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    guests = int(request.form.get('guests', 1))

    # Validate dates
    valid_dates, date_error = validate_dates(check_in, check_out)
    if not valid_dates:
        flash(f'⚠️ {date_error}', 'error')
        return redirect(url_for('guest.property_detail', property_id=property_id))

    # Get property
    property = Property.find_by_id(property_id)
    if not property:
        flash('Property not found', 'error')
        return redirect(url_for('guest.browse'))

    # Validate guests
    valid_guests, guest_error = validate_guests(guests, property.max_guests)
    if not valid_guests:
        flash(f'⚠️ {guest_error}', 'error')
        return redirect(url_for('guest.property_detail', property_id=property_id))

    # Check availability
    if not Booking.validate_dates(property_id, check_in, check_out):
        flash('❌ Dates not available for this property', 'error')
        return redirect(url_for('guest.property_detail', property_id=property_id))

    try:
        # Calculate total price
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        nights = (check_out_date - check_in_date).days
        total_price = nights * float(property.price)

        # Create booking
        booking = Booking.create(
            guest_id=session['user_id'],
            property_id=property_id,
            guest_name=session['full_name'],
            guest_email=session['email'],
            guest_phone='',  # Could be added to user profile later
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total_price=total_price
        )

        # Send confirmation emails
        booking_details = {
            'id': booking.id,
            'property_title': property.title,
            'location': property.location,
            'check_in': check_in,
            'check_out': check_out,
            'guests': guests,
            'total_price': total_price,
            'host_name': property.host_name if hasattr(property, 'host_name') else 'Host',
            'host_email': property.host_email if hasattr(property, 'host_email') else 'host@smartstay.com',
            'guest_name': session['full_name'],
            'guest_email': session['email']
        }

        send_booking_confirmation(session['email'], booking_details)
        notify_host_of_booking(booking_details['host_email'], booking_details)

        flash('✅ You have successfully booked this property!', 'success')
        return redirect(url_for('guest.booking_success', booking_id=booking.id))

    except Exception as err:
        print(f"[BOOKING] Error: {err}")
        flash('❌ Booking error occurred. Please try again.', 'error')
        return redirect(url_for('guest.property_detail', property_id=property_id))