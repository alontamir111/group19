# pages/profile/profile.py
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
import db_connector
import re
from bson import ObjectId

# יצירת Blueprint
profile_bp = Blueprint('profile', __name__,
                       template_folder='templates',
                       static_folder='static')


# דקורטור לבדיקת משתמש מחובר
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
    # קבלת פרטי המשתמש מהסשן
    user_email = session.get('user_email')

    # קבלת פרטי המשתמש ממסד הנתונים
    user = db_connector.get_user_by_email(user_email)
    if not user:
        # אם המשתמש לא נמצא, מחיקת הסשן והפנייה להתחברות
        session.clear()
        flash('User not found. Please sign in again.', 'error')
        return redirect(url_for('signin.login'))

    # קבלת ההזמנות של המשתמש
    user_bookings = db_connector.get_user_bookings(user['_id'])
    print(f"Retrieved {len(user_bookings)} bookings for user")
    for booking in user_bookings:
        print(
            f"Booking: {booking.get('id')}, Class: {booking.get('className')}, Instructor: {booking.get('instructor')}, isPast: {booking.get('isPast')}")

    # קבלת פניות צור קשר של המשתמש
    contact_requests = db_connector.get_user_contact_requests(user_email)
    print(f"Retrieved {len(contact_requests)} contact requests for user")

    # הכנת אובייקט המשתמש לתצוגה
    user_display = {
        'name': f"{user.get('firstName', '')} {user.get('lastName', '')}",
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        'city': user.get('city', '')
    }

    # הצגת דף הפרופיל
    return render_template('profile.html', user=user_display, booked_classes=user_bookings,
                           contact_requests=contact_requests)


@profile_bp.route('/update', methods=['POST'])
@login_required
def update_profile():
    # קבלת המשתמש הנוכחי מהסשן
    user_email = session.get('user_email')

    # קבלת נתונים מהטופס
    name = request.form.get('nameInput', '').strip()
    email = request.form.get('emailInput', '').strip()
    phone = request.form.get('phoneInput', '').strip()
    city = request.form.get('cityInput', '').strip()

    # חלוקת השם לשם פרטי ומשפחה
    name_parts = name.split(' ', 1)
    firstName = name_parts[0]
    lastName = name_parts[1] if len(name_parts) > 1 else ''

    # ולידציה בסיסית
    if not validate_profile_inputs(firstName, lastName, email, phone, city):
        return jsonify({'success': False, 'message': 'Please fill in all fields correctly'})

    # הכנת נתוני המשתמש לעדכון
    user_data = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'phone': phone,
        'city': city
    }

    # עדכון הנתונים במסד הנתונים
    success, message = db_connector.update_user(user_email, user_data)

    # אם האימייל השתנה, יש לעדכן גם בסשן
    if success and email != user_email:
        session['user_email'] = email

    # החזרת תשובה
    return jsonify({'success': success, 'message': message})


@profile_bp.route('/cancel-booking', methods=['POST'])
@login_required
def cancel_booking():
    # קבלת מזהה ההזמנה מהטופס
    booking_id = request.form.get('bookingId')

    if not booking_id:
        return jsonify({'success': False, 'message': 'Booking ID is required'})

    # ביטול ההזמנה
    success, message = db_connector.cancel_booking(booking_id)

    # החזרת תשובה
    return jsonify({'success': success, 'message': message})


@profile_bp.route('/delete-contact-request', methods=['POST'])
@login_required
def delete_contact_request():
    # קבלת מזהה הפנייה מהטופס
    request_id = request.form.get('requestId')

    if not request_id:
        return jsonify({'success': False, 'message': 'Request ID is required'})

    # קבלת האימייל של המשתמש
    user_email = session.get('user_email')

    # בדיקה שהפנייה שייכת למשתמש הנוכחי (אבטחה)
    contact_requests = db_connector.get_user_contact_requests(user_email)
    is_owner = any(req['id'] == request_id for req in contact_requests)

    if not is_owner:
        return jsonify({'success': False, 'message': 'Permission denied'})

    # מחיקת הפנייה
    success, message = db_connector.delete_contact_request(request_id)

    # החזרת תשובה
    return jsonify({'success': success, 'message': message})


@profile_bp.route('/profile.html')
def profile_html():
    # ניתוב נוסף עבור קבצי HTML ישירים
    return redirect(url_for('profile.show_profile'))


def validate_profile_inputs(firstName, lastName, email, phone, city):
    """ולידציה של נתוני הפרופיל"""
    # בדיקת שם פרטי ומשפחה
    if not firstName or not lastName:
        return False

    # בדיקת אימייל
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return False

    # בדיקת טלפון (הסרת מקף אם קיים)
    clean_phone = phone.replace('-', '')
    if not re.match(r'^05\d{8}$', clean_phone):
        return False

    # בדיקת עיר
    if not city:
        return False

    return True