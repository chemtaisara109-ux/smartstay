"""
Review model for Laikipia SmartStay rating and review system
"""
from database import get_db_connection, get_placeholder


class Review:
    def __init__(self, id=None, booking_id=None, guest_id=None, property_id=None,
                 rating=None, review_text=None, created_at=None, **kwargs):
        self.id = id
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.property_id = property_id
        self.rating = rating
        self.review_text = review_text
        self.created_at = created_at

        # Store additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create(booking_id, guest_id, property_id, rating, review_text=None):
        """Create a new review"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'INSERT INTO reviews (booking_id, guest_id, property_id, rating, review_text) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})',
                (booking_id, guest_id, property_id, rating, review_text)
            )

            conn.commit()
            review_id = cursor.lastrowid
            return Review(id=review_id, booking_id=booking_id, guest_id=guest_id,
                         property_id=property_id, rating=rating, review_text=review_text)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_property_id(property_id):
        """Find all reviews for a property"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'SELECT r.id, r.booking_id, r.guest_id, r.property_id, r.rating, r.review_text, r.created_at, u.full_name as guest_name FROM reviews r JOIN users u ON r.guest_id = u.id WHERE r.property_id = {placeholder} ORDER BY r.created_at DESC',
                (property_id,)
            )

            results = cursor.fetchall()
            reviews = []
            for row in results:
                if isinstance(row, dict):
                    review_data = dict(row)
                else:
                    review_data = {
                        'id': row[0],
                        'booking_id': row[1],
                        'guest_id': row[2],
                        'property_id': row[3],
                        'rating': row[4],
                        'review_text': row[5],
                        'created_at': row[6],
                        'guest_name': row[7]
                    }
                reviews.append(Review(**review_data))
            return reviews
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_average_rating(property_id):
        """Get average rating for a property"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'SELECT AVG(rating) as avg_rating, COUNT(*) as review_count FROM reviews WHERE property_id = {placeholder}',
                (property_id,)
            )

            result = cursor.fetchone()
            if result:
                if isinstance(result, dict):
                    return result.get('avg_rating', 0), result.get('review_count', 0)
                else:
                    return result[0] or 0, result[1] or 0
            return 0, 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_booking_id(booking_id):
        """Find review for a specific booking"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'SELECT id, booking_id, guest_id, property_id, rating, review_text, created_at FROM reviews WHERE booking_id = {placeholder}',
                (booking_id,)
            )

            result = cursor.fetchone()
            if not result:
                return None

            if isinstance(result, dict):
                return Review(**dict(result))
            else:
                return Review(
                    id=result[0],
                    booking_id=result[1],
                    guest_id=result[2],
                    property_id=result[3],
                    rating=result[4],
                    review_text=result[5],
                    created_at=result[6]
                )
        finally:
            cursor.close()
            conn.close()