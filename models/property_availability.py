"""
Property availability model for blocked and unavailable date ranges.
"""
from database import get_db_connection, get_placeholder

class AvailabilityBlock:
    def __init__(self, id=None, property_id=None, start_date=None, end_date=None, notes=None, created_at=None, **kwargs):
        self.id = id
        self.property_id = property_id
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.created_at = created_at

        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create(property_id, start_date, end_date, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'''INSERT INTO property_availability (property_id, start_date, end_date, notes) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})''',
                (property_id, start_date, end_date, notes)
            )
            conn.commit()
            block_id = cursor.lastrowid
            return AvailabilityBlock(id=block_id, property_id=property_id, start_date=start_date, end_date=end_date, notes=notes)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_property_id(property_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        cursor.execute(
            f'''SELECT id, property_id, start_date, end_date, notes, created_at FROM property_availability WHERE property_id = {placeholder} ORDER BY start_date ASC''',
            (property_id,)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        blocks = []
        for row in rows:
            if hasattr(row, 'keys'):
                row = dict(row)
            blocks.append(AvailabilityBlock(**row))
        return blocks
