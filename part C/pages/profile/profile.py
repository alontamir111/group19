# pages/profile/profile.py
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
import db_connector
import re
from bson import ObjectId

# Create Blueprint
profile_bp = Blueprint('profile', __name__,
                       template_folder='templates',
                       static_folder='static')


# Decorator to check for logged in user
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('signin.login'))
        return f(*args, **kwargs)

    return decorated_function


@profile_bp.route('/')
@login_required
def show_profile():
    # Get user details from session
    user_email = session.get('user_email')

    # Get user details from database
    user = db_connector.get_user_by_email(user_email)
    if not user:
        # If user not found, clear session and redirect to login
        session.clear()
        flash('User not found. Please sign in again.', 'error')
        return redirect(url_for('signin.login'))

    # Get user bookings
    user_bookings = db_connector.get_user_bookings(user['_id'])
    print(f"Retrieved {len(user_bookings)} bookings for user")
    for booking in user_bookings:
        print(
            f"Booking: {booking.get('id')}, Class: {booking.get('className')}, Instructor: {booking.get('instructor')}, isPast: {booking.get('isPast')}")

    # Get user contact requests
    contact_requests = db_connector.get_user_contact_requests(user_email)
    print(f"Retrieved {len(contact_requests)} contact requests for user")

    # Prepare user object for display
    user_display = {
        'name': f"{user.get('firstName', '')} {user.get('lastName', '')}",
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        'city': user.get('city', '')
    }

    # Display profile page
    return render_template('profile.html', user=user_display, booked_classes=user_bookings,
                           contact_requests=contact_requests)


@profile_bp.route('/update', methods=['POST'])
@login_required
def update_profile():
    # Get current user from session
    user_email = session.get('user_email')

    # Get data from form
    name = request.form.get('nameInput', '').strip()
    email = request.form.get('emailInput', '').strip()
    phone = request.form.get('phoneInput', '').strip()
    city = request.form.get('cityInput', '').strip()

    # Split name into first and last name
    name_parts = name.split(' ', 1)
    firstName = name_parts[0]
    lastName = name_parts[1] if len(name_parts) > 1 else ''

    # Basic validation
    if not validate_profile_inputs(firstName, lastName, email, phone, city):
        return jsonify({'success': False, 'message': 'Please fill in all fields correctly'})

    # Prepare user data for update
    user_data = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'phone': phone,
        'city': city
    }

    # Update data in database
    success, message = db_connector.update_user(user_email, user_data)

    # If email changed, update in session as well
    if success and email != user_email:
        session['user_email'] = email

    # Return response
    return jsonify({'success': success, 'message': message})


@profile_bp.route('/cancel-booking', methods=['POST'])
@login_required
def cancel_booking():
    # Get booking ID from form
    booking_id = request.form.get('bookingId')

    if not booking_id:
        return jsonify({'success': False, 'message': 'Booking ID is required'})

    # Cancel the booking
    success, message = db_connector.cancel_booking(booking_id)

    # Return response
    return jsonify({'success': success, 'message': message})


@profile_bp.route('/delete-contact-request', methods=['POST'])
@login_required
def delete_contact_request():
    # Get request ID from form
    request_id = request.form.get('requestId')

    if not request_id:
        return jsonify({'success': False, 'message': 'Request ID is required'})

    # Get user email
    user_email = session.get('user_email')

    # Check that request belongs to current user (security)
    contact_requests = db_connector.get_user_contact_requests(user_email)
    is_owner = any(req['id'] == request_id for req in contact_requests)

    if not is_owner:
        return jsonify({'success': False, 'message': 'Permission denied'})

    # Delete the request
    success, message = db_connector.delete_contact_request(request_id)

    # Return response
    return jsonify({'success': success, 'message': message})


@profile_bp.route('/profile.html')
def profile_html():
    # Additional route for direct HTML files
    return redirect(url_for('profile.show_profile'))


def validate_profile_inputs(firstName, lastName, email, phone, city):
    """Validation of profile data"""
    # Check first and last name
    if not firstName or not lastName:
        return False

    # Check email
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return False

    # Check phone (remove dash if exists)
    clean_phone = phone.replace('-', '')
    if not re.match(r'^05\d{8}$', clean_phone):
        return False

    # Check city
    if not city:
        return False

    return True