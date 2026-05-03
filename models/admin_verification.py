"""
Admin Verification model for Laikipia SmartStay listing verification
"""
from database import get_db_connection, get_placeholder


class AdminVerification:
    def __init__(self, id=None, property_id=None, admin_id=None, status='pending',
                 notes=None, verified_at=None, created_at=None, **kwargs):
        self.id = id
        self.property_id = property_id
        self.admin_id = admin_id
        self.status = status or 'pending'
        self.notes = notes
        self.verified_at = verified_at
        self.created_at = created_at

        # Store additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create(property_id, admin_id, status='pending', notes=None):
        """Create a new admin verification record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'INSERT INTO admin_verifications (property_id, admin_id, status, notes) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})',
                (property_id, admin_id, status, notes)
            )

            conn.commit()
            verification_id = cursor.lastrowid
            return AdminVerification(id=verification_id, property_id=property_id,
                                   admin_id=admin_id, status=status, notes=notes)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_property_id(property_id):
        """Find verification record for a property"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            cursor.execute(
                f'SELECT av.id, av.property_id, av.admin_id, av.status, av.notes, av.verified_at, av.created_at, u.full_name as admin_name FROM admin_verifications av JOIN users u ON av.admin_id = u.id WHERE av.property_id = {placeholder} ORDER BY av.created_at DESC LIMIT 1',
                (property_id,)
            )

            result = cursor.fetchone()
            if not result:
                return None

            if isinstance(result, dict):
                return AdminVerification(**dict(result))
            else:
                return AdminVerification(
                    id=result[0],
                    property_id=result[1],
                    admin_id=result[2],
                    status=result[3],
                    notes=result[4],
                    verified_at=result[5],
                    created_at=result[6],
                    admin_name=result[7]
                )
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_verifications():
        """Get all pending verifications for admin review"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT av.id, av.property_id, av.admin_id, av.status, av.notes, av.verified_at, av.created_at,
                       p.title as property_title, p.location, u.full_name as host_name, u.email as host_email
                FROM admin_verifications av
                JOIN properties p ON av.property_id = p.id
                JOIN users u ON p.host_id = u.id
                WHERE av.status = 'pending'
                ORDER BY av.created_at ASC
            ''')

            results = cursor.fetchall()
            verifications = []
            for row in results:
                if isinstance(row, dict):
                    verification_data = dict(row)
                else:
                    verification_data = {
                        'id': row[0],
                        'property_id': row[1],
                        'admin_id': row[2],
                        'status': row[3],
                        'notes': row[4],
                        'verified_at': row[5],
                        'created_at': row[6],
                        'property_title': row[7],
                        'location': row[8],
                        'host_name': row[9],
                        'host_email': row[10]
                    }
                verifications.append(AdminVerification(**verification_data))
            return verifications
        finally:
            cursor.close()
            conn.close()

    def update_status(self, status, admin_id, notes=None):
        """Update verification status"""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = get_placeholder()

        try:
            if status in ['verified', 'rejected']:
                cursor.execute(
                    f'UPDATE admin_verifications SET status = {placeholder}, admin_id = {placeholder}, notes = {placeholder}, verified_at = CURRENT_TIMESTAMP WHERE id = {placeholder}',
                    (status, admin_id, notes, self.id)
                )
            else:
                cursor.execute(
                    f'UPDATE admin_verifications SET status = {placeholder}, admin_id = {placeholder}, notes = {placeholder} WHERE id = {placeholder}',
                    (status, admin_id, notes, self.id)
                )

            conn.commit()
            self.status = status
            self.admin_id = admin_id
            self.notes = notes
            if status in ['verified', 'rejected']:
                self.verified_at = 'CURRENT_TIMESTAMP'  # This would be set by the DB
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()