"""
Booking model for SmartStay
"""
from database import get_db_connection, get_placeholder
from datetime import datetime

class Booking:
    def __init__(self, id=None, guest_id=None, property_id=None, guest_name=None, guest_email=None,
                 guest_phone=None, check_in=None, check_out=None, guests=None, total_price=None,
                 notes=None, status='pending', created_at=None, confirmed_at=None, **kwargs):
        self.id = id
        self.guest_id = guest_id
        self.property_id = property_id
        self.guest_name = guest_name
        self.guest_email = guest_email
        self.guest_phone = guest_phone
        self.check_in = check_in
        self.check_out = check_out
        self.guests = guests
        self.total_price = total_price
        self.notes = notes
        self.status = status
        self.created_at = created_at
        self.confirmed_at = confirmed_at

        # Store additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create(guest_id, property_id, guest_name, guest_email, guest_phone, check_in, check_out, guests, total_price, notes=None):
        """Create a new booking"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'''INSERT INTO bookings (guest_id, property_id, guest_name, guest_email, guest_phone,
                                        check_in, check_out, guests, total_price, notes)
                   VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder},
                           {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})''',
                (guest_id, property_id, guest_name, guest_email, guest_phone, check_in, check_out, guests, total_price, notes)
            )

            conn.commit()

            booking_id = cursor.lastrowid
            return Booking(id=booking_id, guest_id=guest_id, property_id=property_id,
                         guest_name=guest_name, guest_email=guest_email, guest_phone=guest_phone,
                         check_in=check_in, check_out=check_out, guests=guests,
                         total_price=total_price, notes=notes)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_guest_id(guest_id):
        """Find all bookings by guest ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(f'''
            SELECT b.id, b.guest_id, b.property_id, b.check_in, b.check_out, b.guests, b.total_price, b.status, b.created_at, b.confirmed_at,
                   p.title, p.location, u.username as host_name
            FROM bookings b
            JOIN properties p ON b.property_id = p.id
            JOIN users u ON p.host_id = u.id
            WHERE b.guest_id = {placeholder}
        ''', (guest_id,))

        bookings_data = cursor.fetchall()
        cursor.close()
        conn.close()

        bookings = []
        for booking in bookings_data:
            if hasattr(booking, 'keys'):
                booking = dict(booking)
            bookings.append(Booking(**{k: v for k, v in booking.items() if k in ['id', 'guest_id', 'property_id', 'check_in', 'check_out', 'guests', 'total_price', 'status', 'created_at', 'confirmed_at']},
                           **{'title': booking.get('title'), 'location': booking.get('location'), 'host_name': booking.get('host_name')}))
        return bookings

    @staticmethod
    def find_by_host_id(host_id):
        """Find all bookings for properties owned by host"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(f'''
            SELECT b.*, p.title as property_title, p.location
            FROM bookings b
            JOIN properties p ON b.property_id = p.id
            WHERE p.host_id = {placeholder}
            ORDER BY b.created_at DESC
        ''', (host_id,))

        bookings_data = cursor.fetchall()
        cursor.close()
        conn.close()

        bookings = []
        for booking in bookings_data:
            if hasattr(booking, 'keys'):
                booking = dict(booking)
            bookings.append(Booking(**{k: v for k, v in booking.items()
                             if k in ['id', 'guest_id', 'property_id', 'guest_name', 'guest_email',
                                     'guest_phone', 'check_in', 'check_out', 'guests', 'total_price',
                                     'notes', 'status', 'created_at', 'confirmed_at']},
                           **{'property_title': booking.get('property_title'), 'location': booking.get('location')}))
        return bookings

    @staticmethod
    def find_by_property_id(property_id):
        """Find all bookings for a single property."""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(f'''
            SELECT b.*, u.username as guest_username
            FROM bookings b
            LEFT JOIN users u ON b.guest_id = u.id
            WHERE b.property_id = {placeholder}
            ORDER BY b.check_in ASC
        ''', (property_id,))

        bookings_data = cursor.fetchall()
        cursor.close()
        conn.close()

        bookings = []
        for booking in bookings_data:
            if hasattr(booking, 'keys'):
                booking = dict(booking)
            bookings.append(Booking(**{k: v for k, v in booking.items()
                             if k in ['id', 'guest_id', 'property_id', 'guest_name', 'guest_email',
                                     'guest_phone', 'check_in', 'check_out', 'guests', 'total_price',
                                     'notes', 'status', 'created_at', 'confirmed_at']},
                           **{'guest_username': booking.get('guest_username')}))
        return bookings

    @staticmethod
    def find_by_id(booking_id):
        """Find booking by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(f'''
            SELECT b.*, p.title as property_name, p.location, u.username as guest_username,
                   h.username as host_name, h.email as host_email
            FROM bookings b
            JOIN properties p ON b.property_id = p.id
            LEFT JOIN users u ON b.guest_id = u.id
            JOIN users h ON p.host_id = h.id
            WHERE b.id = {placeholder}
        ''', (booking_id,))

        booking_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if booking_data:
            if hasattr(booking_data, 'keys'):
                booking_data = dict(booking_data)
            booking = Booking(**{k: v for k, v in booking_data.items()
                               if k in ['id', 'guest_id', 'property_id', 'guest_name', 'guest_email',
                                       'guest_phone', 'check_in', 'check_out', 'guests', 'total_price',
                                       'notes', 'status', 'created_at', 'confirmed_at']})
            booking.property_name = booking_data.get('property_name')
            booking.location = booking_data.get('location')
            booking.guest_username = booking_data.get('guest_username')
            booking.host_name = booking_data.get('host_name')
            booking.host_email = booking_data.get('host_email')
            return booking
        return None

    def confirm(self):
        """Confirm the booking"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'UPDATE bookings SET status = {placeholder}, confirmed_at = {placeholder} WHERE id = {placeholder}',
                ('confirmed', datetime.now(), self.id)
            )

            conn.commit()

            self.status = 'confirmed'
            self.confirmed_at = datetime.now()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def validate_dates(property_id, check_in, check_out):
        """Validate booking dates for availability"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(f'''
            SELECT COUNT(*) as count FROM bookings
            WHERE property_id = {placeholder} AND status != 'cancelled'
            AND NOT (
                check_out <= {placeholder}
                OR check_in >= {placeholder}
            )
        ''', (property_id, check_in, check_out))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return True

        if isinstance(result, dict):
            count = result.get('count') or list(result.values())[0]
        elif isinstance(result, tuple):
            count = result[0]
        else:
            count = 0

        return int(count) == 0

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'guest_id': self.guest_id,
            'property_id': self.property_id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'guest_phone': self.guest_phone,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'guests': self.guests,
            'total_price': self.total_price,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at,
            'confirmed_at': self.confirmed_at
        }