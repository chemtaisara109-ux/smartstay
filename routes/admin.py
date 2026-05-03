"""
Admin routes for Laikipia SmartStay administrative panel
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from models.admin_verification import AdminVerification
from models.listing import Property
from models.user import User
from utils.auth_helper import login_required, admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    try:
        # Get pending verifications
        pending_verifications = AdminVerification.get_pending_verifications()

        # Get statistics
        total_properties = len(Property.search())  # This could be optimized
        total_users = len(User.find_all()) if hasattr(User, 'find_all') else 0
        pending_count = len(pending_verifications)

        return render_template('admin_dashboard.html',
                             pending_verifications=pending_verifications,
                             total_properties=total_properties,
                             total_users=total_users,
                             pending_count=pending_count)

    except Exception as e:
        print(f"Admin dashboard error: {e}")
        flash('Error loading admin dashboard', 'error')
        return redirect(url_for('guest.index'))

@admin_bp.route('/api/admin/verification/<int:verification_id>', methods=['POST'])
@login_required
@admin_required
def update_verification(verification_id):
    """Update verification status"""
    try:
        data = request.get_json()
        status = data.get('status')
        notes = data.get('notes', '')

        if status not in ['verified', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400

        # Find verification
        verification = AdminVerification.find_by_property_id(verification_id)
        if not verification or verification.id != verification_id:
            return jsonify({'error': 'Verification not found'}), 404

        # Update status
        verification.update_status(status, session.get('user_id'), notes)

        return jsonify({'message': f'Property {status} successfully'}), 200

    except Exception as e:
        print(f"Update verification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@admin_bp.route('/api/admin/verifications/pending', methods=['GET'])
@login_required
@admin_required
def get_pending_verifications():
    """Get pending verifications"""
    try:
        verifications = AdminVerification.get_pending_verifications()
        verification_data = []
        for v in verifications:
            verification_data.append({
                'id': v.id,
                'property_id': v.property_id,
                'property_title': getattr(v, 'property_title', ''),
                'location': getattr(v, 'location', ''),
                'host_name': getattr(v, 'host_name', ''),
                'host_email': getattr(v, 'host_email', ''),
                'created_at': v.created_at
            })

        return jsonify({'verifications': verification_data}), 200

    except Exception as e:
        print(f"Get pending verifications error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@admin_bp.route('/api/admin/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """Get all users for admin management"""
    try:
        # This would need a User.find_all() method - for now return empty
        users = []
        return jsonify({'users': users}), 200

    except Exception as e:
        print(f"Get users error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@admin_bp.route('/api/admin/properties', methods=['GET'])
@login_required
@admin_required
def get_properties():
    """Get all properties for admin management"""
    try:
        properties = Property.search()
        property_data = []
        for p in properties:
            property_data.append({
                'id': p.id,
                'title': p.title,
                'location': p.location,
                'price': p.price,
                'host_name': getattr(p, 'host_name', ''),
                'verification_status': p.verification_status,
                'average_rating': p.average_rating,
                'review_count': p.review_count
            })

        return jsonify({'properties': property_data}), 200

    except Exception as e:
        print(f"Get properties error: {e}")
        return jsonify({'error': 'Internal server error'}), 500