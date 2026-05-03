"""
Review routes for Laikipia SmartStay rating and review system
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from models.review import Review
from models.booking import Booking
from utils.auth_helper import login_required

review_bp = Blueprint('review', __name__)

@review_bp.route('/api/review/<int:booking_id>', methods=['POST'])
@login_required
def submit_review(booking_id):
    """Submit a review for a completed booking"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        review_text = data.get('review_text', '')

        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        # Check if booking exists and belongs to current user
        booking = Booking.find_by_id(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        if booking.guest_id != session.get('user_id'):
            return jsonify({'error': 'Unauthorized'}), 403

        # Check if booking is completed
        if booking.status != 'completed':
            return jsonify({'error': 'Can only review completed bookings'}), 400

        # Check if review already exists
        existing_review = Review.find_by_booking_id(booking_id)
        if existing_review:
            return jsonify({'error': 'Review already submitted for this booking'}), 400

        # Create review
        review = Review.create(
            booking_id=booking_id,
            guest_id=booking.guest_id,
            property_id=booking.property_id,
            rating=rating,
            review_text=review_text
        )

        return jsonify({
            'message': 'Review submitted successfully',
            'review': {
                'id': review.id,
                'rating': review.rating,
                'review_text': review.review_text,
                'created_at': review.created_at
            }
        }), 201

    except Exception as e:
        print(f"Review submission error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@review_bp.route('/api/property/<int:property_id>/reviews', methods=['GET'])
def get_property_reviews(property_id):
    """Get all reviews for a property"""
    try:
        reviews = Review.find_by_property_id(property_id)
        review_data = []
        for review in reviews:
            review_data.append({
                'id': review.id,
                'rating': review.rating,
                'review_text': review.review_text,
                'created_at': review.created_at,
                'guest_name': getattr(review, 'guest_name', 'Anonymous')
            })

        return jsonify({'reviews': review_data}), 200

    except Exception as e:
        print(f"Get reviews error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@review_bp.route('/api/property/<int:property_id>/rating', methods=['GET'])
def get_property_rating(property_id):
    """Get average rating and count for a property"""
    try:
        avg_rating, review_count = Review.get_average_rating(property_id)
        return jsonify({
            'average_rating': round(avg_rating, 1) if avg_rating else 0,
            'review_count': review_count
        }), 200

    except Exception as e:
        print(f"Get rating error: {e}")
        return jsonify({'error': 'Internal server error'}), 500