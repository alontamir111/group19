# searchClasses.py
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from functools import wraps
from bson import ObjectId
import db_connector
from datetime import datetime

# Create Blueprint
searchClasses_bp = Blueprint('searchClasses', __name__,
                             template_folder='templates',
                             static_folder='static')


# Login check decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('signin.login'))
        return f(*args, **kwargs)

    return decorated_function


@searchClasses_bp.route('/')
@login_required
def search():
    """Display class search page"""
    # Get all class types and studios for filtering options
    class_types = db_connector.get_all_class_types()
    studios = db_connector.get_all_studios()

    return render_template('searchClasses.html',
                           class_types=class_types,
                           studios=studios)


@searchClasses_bp.route('/api/instructors')
@login_required
def api_instructors():
    """API to return instructor list"""
    # Get all instructors from database
    instructors = db_connector.users_col.find({"role": "instructor"})

    # Convert to JSON format
    instructor_list = []
    for instructor in instructors:
        instructor_list.append({
            "id": str(instructor.get('_id')),
            "name": f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}".strip()
        })

    return jsonify(instructor_list)


@searchClasses_bp.route('/api/classes')
@login_required
def api_classes():
    """API to return filtered class list"""
    # Get filter parameters from query string
    class_type = request.args.get('class_type')
    level = request.args.get('level')
    time = request.args.get('time')
    location = request.args.get('location')
    instructor = request.args.get('instructor')

    # Prepare parameters dictionary for filter function
    filters = {}
    if class_type:
        filters['classType'] = class_type  # Note: key name matches db_connector function
    if level:
        filters['level'] = level
    if time:
        filters['time_of_day'] = time
    if location:
        filters['studioId'] = location  # Note: key name matches db_connector function
    if instructor:
        filters['instructorName'] = instructor  # Note: key name matches db_connector function

    # Get filtered classes from database
    schedule_items = db_connector.get_upcoming_classes(filters)

    # Convert to client-side friendly format
    user_email = session.get('user_email')
    user = db_connector.get_user_by_email(user_email)

    results = []
    for item in schedule_items:
        # Get additional information about the class
        class_type_obj = db_connector.get_class_type_by_id(item.get('classId'))
        studio = db_connector.get_studio_by_id(item.get('studioId'))
        instructor_id = item.get('instructorId')
        instructor = db_connector.users_col.find_one({'_id': instructor_id}) if instructor_id else None

        # Check if user is registered for this class
        is_booked = False
        if user:
            booking = db_connector.bookings_col.find_one({
                'userId': ObjectId(user.get('_id')) if isinstance(user.get('_id'), str) else user.get('_id'),
                'scheduleId': item.get('_id'),
                'status': 'confirmed'
            })
            is_booked = booking is not None

        # Format date and time display
        start_time = item.get('startTime')
        formatted_date = start_time
        try:
            # Convert to more user-friendly format - depends on original format
            dt = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            formatted_date = dt.strftime('%A, %B %d, %Y %I:%M %p')
        except:
            try:
                # Try alternative format
                dt = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.000Z')
                formatted_date = dt.strftime('%A, %B %d, %Y %I:%M %p')
            except:
                pass

        # Create class information object
        result = {
            'id': str(item.get('_id')),
            'name': item.get('name', 'Unknown Class'),
            'classType': class_type_obj.get('name', 'Unknown Type') if class_type_obj else 'Unknown Type',  # Note: Added class type field
            'level': class_type_obj.get('difficulty', 'All Levels') if class_type_obj else 'All Levels',
            'datetime': formatted_date,
            'duration': class_type_obj.get('duration', 60) if class_type_obj else 60,
            'instructorName': f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}" if instructor else 'Unknown',
            'location': studio.get('name', 'Unknown Location') if studio else 'Unknown Location',
            'maxParticipants': item.get('capacity', 0),
            'availableSpots': item.get('capacity', 0) - item.get('bookedCount', 0),
            'description': class_type_obj.get('description', '') if class_type_obj else '',
            'is_booked': is_booked,
            'is_full': item.get('bookedCount', 0) >= item.get('capacity', 0),
            'price': item.get('price', 0)
        }

        results.append(result)

    # Sort by date and time
    results.sort(key=lambda x: x['datetime'])

    return jsonify(results)


@searchClasses_bp.route('/book', methods=['POST'])
@login_required
def book_class():
    """Book a class"""
    class_id = request.form.get('classId')
    user_email = session.get('user_email')

    print(f"Booking class_id: {class_id} for user: {user_email}")

    if not class_id:
        return jsonify({'success': False, 'message': 'Class ID is required'})

    user = db_connector.get_user_by_email(user_email)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    print(f"User found: {user.get('_id')}, type: {type(user.get('_id'))}")

    # Use function from db_connector
    success, result = db_connector.book_class(user.get('_id'), class_id)

    if success:
        return jsonify({'success': True, 'message': 'Class booked successfully', 'bookingId': result})
    else:
        return jsonify({'success': False, 'message': result})


@searchClasses_bp.route('/cancel', methods=['POST'])
@login_required
def cancel_class():
    """Cancel class registration"""
    class_id = request.form.get('classId')
    user_email = session.get('user_email')

    if not class_id:
        return jsonify({'success': False, 'message': 'Class ID is required'})

    user = db_connector.get_user_by_email(user_email)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    # Find the booking
    booking = db_connector.bookings_col.find_one({
        'userId': ObjectId(user.get('_id')) if isinstance(user.get('_id'), str) else user.get('_id'),
        'scheduleId': ObjectId(class_id),
        'status': 'confirmed'
    })

    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found'})

    # Update booking status
    db_connector.bookings_col.update_one(
        {'_id': booking.get('_id')},
        {'$set': {'status': 'cancelled', 'paymentStatus': 'refunded'}}
    )

    # Update occupied spots count in the class
    db_connector.schedule_col.update_one(
        {'_id': ObjectId(class_id)},
        {'$inc': {'bookedCount': -1}}
    )

    return jsonify({'success': True, 'message': 'Booking cancelled successfully'})