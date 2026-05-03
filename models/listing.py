"""
Property/Listing model for Laikipia SmartStay
"""
from database import get_db_connection, get_placeholder
from models.review import Review
from models.admin_verification import AdminVerification

class Property:
    def __init__(self, id=None, host_id=None, title=None, description=None, location=None,
                 price=None, max_guests=1, image_url=None, created_at=None,
                 verification_status='pending', average_rating=0, review_count=0, **kwargs):
        self.id = id
        self.host_id = host_id
        self.title = title
        self.description = description
        self.location = location
        self.price = price
        self.max_guests = max_guests
        self.image_url = image_url
        self.created_at = created_at
        self.verification_status = verification_status or 'pending'
        self.average_rating = average_rating or 0
        self.rating = average_rating or 0
        self.review_count = review_count or 0

        # Store additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create(host_id, title, location, price, max_guests=1, description=None, image_url=None):
        """Create a new property"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'INSERT INTO properties (host_id, title, location, price, max_guests, description, image_url) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})',
                (host_id, title, location, price, max_guests, description, image_url)
            )

            conn.commit()

            property_id = cursor.lastrowid
            return Property(id=property_id, host_id=host_id, title=title, location=location,
                          price=price, max_guests=max_guests, description=description, image_url=image_url)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def update(self, title, location, price, max_guests, description, image_url=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            if image_url is not None:
                cursor.execute(
                    f'UPDATE properties SET title = {placeholder}, location = {placeholder}, price = {placeholder}, max_guests = {placeholder}, description = {placeholder}, image_url = {placeholder} WHERE id = {placeholder}',
                    (title, location, price, max_guests, description, image_url, self.id)
                )
                self.image_url = image_url
            else:
                cursor.execute(
                    f'UPDATE properties SET title = {placeholder}, location = {placeholder}, price = {placeholder}, max_guests = {placeholder}, description = {placeholder} WHERE id = {placeholder}',
                    (title, location, price, max_guests, description, self.id)
                )

            conn.commit()
            self.title = title
            self.location = location
            self.price = price
            self.max_guests = max_guests
            self.description = description
            return self
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_id(property_id):
        """Find property by ID with verification and rating info"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(
            f'SELECT p.id, p.host_id, p.title, p.description, p.location, p.price, p.max_guests, p.image_url, p.created_at, u.username as host_name, u.email as host_email FROM properties p JOIN users u ON p.host_id = u.id WHERE p.id = {placeholder}',
            (property_id,)
        )

        property_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if property_data:
            property_obj = Property(**property_data)
            # Add verification status
            verification = AdminVerification.find_by_property_id(property_id)
            property_obj.verification_status = verification.status if verification else 'pending'
            # Add rating info
            avg_rating, review_count = Review.get_average_rating(property_id)
            property_obj.average_rating = avg_rating
            property_obj.rating = avg_rating
            property_obj.review_count = review_count
            return property_obj
        return None

    @staticmethod
    def find_by_host_id(host_id):
        """Find all properties by host ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(
            f'SELECT id, host_id, title, description, location, price, max_guests, image_url, created_at FROM properties WHERE host_id = {placeholder}',
            (host_id,)
        )

        properties_data = cursor.fetchall()
        cursor.close()
        conn.close()

        properties = [Property(**prop) for prop in properties_data]
        for property_obj in properties:
            verification = AdminVerification.find_by_property_id(property_obj.id)
            property_obj.verification_status = verification.status if verification else 'pending'
            avg_rating, review_count = Review.get_average_rating(property_obj.id)
            property_obj.average_rating = avg_rating
            property_obj.rating = avg_rating
            property_obj.review_count = review_count
        return properties

    @staticmethod
    def search(location=None, max_guests=1):
        """Search properties by location and guest count"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        query = f'SELECT p.id, p.host_id, p.title, p.description, p.location, p.price, p.max_guests, p.image_url, p.created_at, u.username as host_name FROM properties p JOIN users u ON p.host_id = u.id LEFT JOIN admin_verifications av ON p.id = av.property_id WHERE (av.status != "rejected" OR av.id IS NULL)'

        params = []

        if location:
            query += f' AND LOWER(p.location) LIKE {placeholder}'
            params.append(f'%{location.lower()}%')

        if max_guests:
            query += f' AND p.max_guests >= {placeholder}'
            params.append(max_guests)

        cursor.execute(query, params)
        properties_data = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert to Property objects with host_name, verification, and rating
        properties = []
        for prop in properties_data:
            prop_dict = prop if isinstance(prop, dict) else dict(prop)
            property_obj = Property(**{k: v for k, v in prop_dict.items() if k != 'host_name'})
            property_obj.host_name = prop_dict.get('host_name')
            
            # Add verification status
            verification = AdminVerification.find_by_property_id(property_obj.id)
            property_obj.verification_status = verification.status if verification else 'pending'
            
            # Add rating info
            avg_rating, review_count = Review.get_average_rating(property_obj.id)
            property_obj.average_rating = avg_rating
            property_obj.review_count = review_count
            
            properties.append(property_obj)

        return properties

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'host_id': self.host_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'price': self.price,
            'max_guests': self.max_guests,
            'image_url': self.image_url,
            'created_at': self.created_at
        }