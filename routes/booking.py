"""
Booking routes (API endpoints for booking functionality)
"""
from flask import Blueprint, request, jsonify, session, render_template, flash, redirect, url_for, send_file
from models.booking import Booking
from models.listing import Property
from utils.auth_helper import login_required
import time
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/api/search', methods=['POST'])
@login_required
def api_search():
    """API endpoint for search functionality"""
    try:
        data = request.get_json()
        location = data.get('location', '').lower()
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        guests = int(data.get('guests', 1))

        properties = Property.search(location=location, max_guests=guests)

        return jsonify({
            'success': True,
            'count': len(properties),
            'properties': [prop.to_dict() for prop in properties]
        })

    except Exception as e:
        print(f"[API_SEARCH] Error: {e}")
        return jsonify({'success': False, 'message': 'Search error'}), 500

@booking_bp.route('/api/property/<int:property_id>')
@login_required
def api_property_details(property_id):
    """Get property details as JSON"""
    try:
        property = Property.find_by_id(property_id)

        if property:
            property_dict = property.to_dict()
            # Add host name if available
            if hasattr(property, 'host_name'):
                property_dict['host_name'] = property.host_name

            return jsonify({
                'success': True,
                'property': property_dict
            })
        else:
            return jsonify({'success': False, 'message': 'Property not found'}), 404

    except Exception as e:
        print(f"[API_PROPERTY] Error: {e}")
        return jsonify({'success': False, 'message': 'Error fetching property'}), 500

@booking_bp.route('/api/validate-dates', methods=['POST'])
@login_required
def api_validate_dates():
    """Validate booking dates"""
    try:
        data = request.get_json()
        property_id = data.get('property_id')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        from datetime import datetime
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        if check_in_date >= check_out_date:
            return jsonify({'valid': False, 'message': 'Check-out must be after check-in'})

        is_available = Booking.validate_dates(property_id, check_in, check_out)

        if is_available:
            return jsonify({'valid': True, 'message': 'Dates available'})
        else:
            return jsonify({'valid': False, 'message': 'Dates not available'})

    except Exception as e:
        print(f"[API_VALIDATE_DATES] Error: {e}")
        return jsonify({'valid': False, 'message': 'Validation error'}), 500

@booking_bp.route('/api/upload-photo', methods=['POST'])
@login_required
def api_upload_photo():
    """Handle multiple photo uploads"""
    if session.get('role') != 'host':
        return jsonify({'success': False, 'message': 'Access denied'}), 401

    try:
        uploaded_files = request.files.getlist('photos')
        filenames = []

        for file in uploaded_files:
            if file and file.filename:
                # Validate file type
                if not file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                    continue

                filename = f"{session['user_id']}_{int(time.time())}_{file.filename}"
                filepath = os.path.join('static', 'uploads', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                filenames.append(filename)

        return jsonify({
            'success': True,
            'filenames': filenames,
            'message': f'{len(filenames)} photos uploaded successfully'
        })

    except Exception as e:
        print(f"[API_UPLOAD] Error: {e}")
        return jsonify({'success': False, 'message': 'Upload error'}), 500

@booking_bp.route('/submit', methods=['POST'])
def submit_booking():
    """Submit a booking request"""
    try:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # Get form data
        property_id = int(request.form.get('property_id'))
        guest_name = request.form.get('guest_name', '').strip()
        guest_email = request.form.get('guest_email', '').strip()
        guest_phone = request.form.get('guest_phone', '').strip()
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        guests = int(request.form.get('guests', 1))
        notes = request.form.get('notes', '').strip()

        # Validate required fields
        if not all([guest_name, guest_email, guest_phone, check_in, check_out]):
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields.'
            }), 400

        # Validate email format
        import re
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', guest_email):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address.'
            }), 400

        # Validate phone number (basic)
        if not re.match(r'^[\+]?[1-9][\d]{0,15}$', guest_phone):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid phone number.'
            }), 400

        # Get property details
        property = Property.find_by_id(property_id)
        if not property:
            return jsonify({
                'success': False,
                'message': 'Property not found.'
            }), 404

        # Validate dates
        from datetime import datetime
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            today = datetime.now().date()

            if check_in_date < today:
                return jsonify({
                    'success': False,
                    'message': 'Check-in date cannot be in the past.'
                }), 400

            if check_out_date <= check_in_date:
                return jsonify({
                    'success': False,
                    'message': 'Check-out date must be after check-in date.'
                }), 400

            nights = (check_out_date - check_in_date).days
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid date format.'
            }), 400

        # Validate guests
        if guests < 1 or guests > property.max_guests:
            return jsonify({
                'success': False,
                'message': f'Number of guests must be between 1 and {property.max_guests}.'
            }), 400

        # Check availability (if method exists)
        if hasattr(Booking, 'validate_dates') and not Booking.validate_dates(property_id, check_in, check_out):
            return jsonify({
                'success': False,
                'message': 'These dates are not available for this property.'
            }), 400

        # Calculate total price
        base_price = nights * float(property.price)
        service_fee = base_price * 0.12  # 12% service fee
        total_price = base_price + service_fee

        # Get guest_id if user is logged in
        guest_id = session.get('user_id') if 'user_id' in session else None

        # Create booking
        booking = Booking.create(
            guest_id=guest_id,
            property_id=property_id,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total_price=total_price,
            notes=notes
        )

        # Prepare booking details for notifications
        booking_details = {
            'id': booking.id,
            'property_id': property_id,
            'property_title': property.title,
            'property_location': property.location,
            'host_name': getattr(property, 'host_name', 'Host'),
            'host_email': getattr(property, 'host_email', 'host@smartstay.com'),
            'guest_name': guest_name,
            'guest_email': guest_email,
            'guest_phone': guest_phone,
            'check_in': check_in,
            'check_out': check_out,
            'guests': guests,
            'nights': nights,
            'total_price': total_price,
            'notes': notes,
            'created_at': booking.created_at
        }

        # Send notifications
        try:
            from utils.email_helper import send_booking_confirmation, notify_host_of_booking
            send_booking_confirmation(guest_email, booking_details)
            notify_host_of_booking(booking_details['host_email'], booking_details)

            # Create host notification in database
            create_host_notification(booking_details)
        except Exception as e:
            print(f"[BOOKING] Email notification error: {e}")
            # Don't fail the booking if email fails

        if is_ajax or request.is_json:
            return jsonify({
                'success': True,
                'message': 'Your booking request has been submitted successfully! The host will contact you shortly.',
                'booking_id': booking.id,
                'redirect_url': url_for('guest.booking_success', booking_id=booking.id)
            })

        flash('✅ Booking successful, receipt generated.', 'success')
        return redirect(url_for('guest.booking_success', booking_id=booking.id))

    except Exception as e:
        print(f"[BOOKING] Error: {e}")
        if is_ajax or request.is_json:
            return jsonify({
                'success': False,
                'message': 'An error occurred while processing your booking. Please try again.'
            }), 500
        flash('❌ An error occurred while processing your booking. Please try again.', 'error')
        return redirect(request.referrer or url_for('guest.browse'))

@booking_bp.route('/receipt/<int:booking_id>')
def download_receipt(booking_id):
    """Generate and download booking receipt as PDF"""
    try:
        booking = Booking.find_by_id(booking_id)
        
        if not booking:
            flash('Booking not found', 'error')
            return redirect(url_for('guest.dashboard') if session.get('role') == 'guest' else url_for('landing'))

        # Log access attempt
        session_user_id = session.get('user_id')
        session_role = session.get('role')
        print(f"[RECEIPT] Accessing booking {booking_id}: booking.guest_id={booking.guest_id}, session_user_id={session_user_id}, session_role={session_role}")

        # Generate PDF (allow for now, can add access control later)
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "SmartStay Booking Receipt")

        # Date
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Receipt Date: {datetime.now().strftime('%B %d, %Y')}")

        # Horizontal line
        c.setLineWidth(1)
        c.line(50, height - 80, width - 50, height - 80)

        # Booking details
        c.setFont("Helvetica-Bold", 12)
        y = height - 110

        details = [
            f"Booking ID: #{booking.id}",
            f"Property: {booking.property_name or 'N/A'}",
            f"Location: {booking.location or 'N/A'}",
            "",
            f"Guest Name: {booking.guest_name}",
            f"Guest Email: {booking.guest_email}",
            f"Guest Phone: {booking.guest_phone}",
            "",
            f"Check-in: {booking.check_in}",
            f"Check-out: {booking.check_out}",
            f"Number of Guests: {booking.guests}",
            f"Status: {booking.status.title()}",
        ]

        c.setFont("Helvetica", 11)
        for detail in details:
            if detail:
                c.drawString(50, y, detail)
            y -= 20

        # Price breakdown
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Price Breakdown")
        y -= 20

        c.setFont("Helvetica", 11)
        from datetime import datetime as dt
        check_in_date = dt.strptime(str(booking.check_in), '%Y-%m-%d').date()
        check_out_date = dt.strptime(str(booking.check_out), '%Y-%m-%d').date()
        nights = (check_out_date - check_in_date).days

        property_obj = Property.find_by_id(booking.property_id)
        base_price = nights * (property_obj.price if property_obj else 0)
        service_fee = booking.total_price - base_price

        c.drawString(50, y, f"Base Price ({nights} nights × KES {property_obj.price if property_obj else 0}): KES {base_price:.2f}")
        y -= 20
        c.drawString(50, y, f"Service Fee (12%): KES {service_fee:.2f}")
        y -= 20

        # Total
        c.setLineWidth(1)
        c.line(50, y - 5, width - 50, y - 5)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y - 20, f"Total Amount: KES {booking.total_price:.2f}")

        # Footer
        y -= 60
        c.setFont("Helvetica", 9)
        c.drawString(50, y, "Thank you for your booking! The host will contact you shortly to confirm your reservation.")
        y -= 15
        c.drawString(50, y, "For support, visit www.smartstay.com or contact support@smartstay.com")

        c.save()
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'receipt_{booking_id}.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"[RECEIPT] Error: {e}")
        flash('Error generating receipt. Please try again.', 'error')
        return redirect(request.referrer or url_for('landing'))

def create_host_notification(booking_details):
    """Create a notification for the host in the database"""
    try:
        from database import get_db_connection, get_placeholder

        # Get host_id from property
        property = Property.find_by_id(booking_details['property_id'])
        if not property or not hasattr(property, 'host_id'):
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        message = f"New booking request from {booking_details['guest_name']} for {booking_details['property_title']} ({booking_details['check_in']} to {booking_details['check_out']})"

        cursor.execute(
            f"INSERT INTO host_notifications (host_id, booking_id, message) VALUES ({placeholder}, {placeholder}, {placeholder})",
            (property.host_id, booking_details['id'], message)
        )

        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[NOTIFICATION] Error creating host notification: {e}")