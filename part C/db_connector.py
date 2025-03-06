# db_connector.py
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# URI from .env file
uri = os.environ.get('DB_URI', 'mongodb://localhost:27017/')

# Create MongoDB server connection
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to database
db = client['yoga_spot_db']

# Collections in the project
bookings_col = db['bookings']
classes_col = db['classes']
schedule_col = db['schedule']
studios_col = db['studios']
users_col = db['users']
contact_requests_col = db['contact_requests']


# ----- User Management Functions -----

def register_user(firstName, lastName, email, phone, city, password, age=None, gender=None):
    """
    Function to register a new user
    """
    # Check if user already exists
    if users_col.find_one({'email': email}):
        return False, "User with this email already exists."

    if users_col.find_one({'phone': phone}):
        return False, "User with this phone number already exists."

    # Add new user
    new_user = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'phone': phone,
        'city': city,
        'password': password,  # In production environment, password should be encrypted
        'registrationDate': datetime.now().strftime('%Y-%m-%d'),
        'role': 'user',
        'active': True
    }

    # Add optional fields if provided
    if age:
        new_user['age'] = int(age)

    if gender:
        new_user['gender'] = gender

    # Add user to database
    user_id = users_col.insert_one(new_user).inserted_id

    # Return ID of the new user
    return True, str(user_id)


def authenticate_user(email, password):
    """
    Function to authenticate a user
    """
    user = users_col.find_one({
        'email': email,
        'password': password,  # In production environment, should verify encrypted password
        'active': True
    })

    if user:
        # Convert to regular dict (without ObjectId)
        user_dict = {k: v for k, v in user.items() if k != '_id'}
        user_dict['_id'] = str(user['_id'])
        return True, user_dict

    return False, "Invalid username or password."


def get_user_by_email(email):
    """
    Function to find a user by email
    """
    user = users_col.find_one({'email': email})
    if user:
        # Convert to regular dict (without ObjectId)
        user_dict = {k: v for k, v in user.items() if k != '_id'}
        user_dict['_id'] = str(user['_id'])
        return user_dict
    return None


def update_user(email, user_data):
    """
    Function to update user details
    """
    # Remove fields that cannot be updated
    if '_id' in user_data:
        del user_data['_id']

    # Check if the new email already exists (if email was changed)
    if 'email' in user_data and user_data['email'] != email:
        if users_col.find_one({'email': user_data['email']}):
            return False, "This email is already in use."

    # Perform update
    result = users_col.update_one(
        {'email': email},
        {'$set': user_data}
    )

    if result.modified_count > 0:
        return True, "User details updated successfully."
    else:
        return False, "No changes were made."


# ----- Class Types Management Functions -----

def initialize_class_types():
    """
    Initialize class types
    """
    class_types = [
        {
            'name': 'Vinyasa Flow',
            'description': 'Dynamic sequences linking breath with movement. Build strength, flexibility and mindfulness through flowing postures.',
            'difficulty': 'intermediate',
            'duration': 75,
            'equipment': ['Yoga mat', 'Water bottle', 'Small towel'],
            'recommendations': 'Students with some yoga experience looking to build strength and deepen their practice.'
        },
        {
            'name': 'Hatha Yoga',
            'description': 'Traditional approach focusing on basic postures, breathing techniques, and relaxation. Perfect foundation for beginners.',
            'difficulty': 'beginner',
            'duration': 60,
            'equipment': ['Yoga mat', 'Comfortable clothing', 'Optional: Yoga blocks'],
            'recommendations': 'Newcomers to yoga and those seeking a gentler, more traditional practice.'
        },
        {
            'name': 'Power Yoga',
            'description': 'High-intensity, strength-focused practice. Challenging sequences to build muscle and increase endurance.',
            'difficulty': 'advanced',
            'duration': 90,
            'equipment': ['Yoga mat', 'Water bottle', '2 towels', 'Yoga blocks'],
            'recommendations': 'Experienced practitioners looking for a challenging, athletic practice.'
        },
        {
            'name': 'Yin Yoga',
            'description': 'Slow-paced style holding poses for longer periods. Improves flexibility and promotes deep relaxation.',
            'difficulty': 'all-levels',
            'duration': 75,
            'equipment': ['Yoga mat', '2 Yoga blocks', 'Bolster or firm pillow', 'Blanket'],
            'recommendations': 'Anyone seeking deep stretch and stress relief, particularly good for athletes.'
        }
    ]

    for class_type in class_types:
        # Check if class type already exists
        if not classes_col.find_one({'name': class_type['name']}):
            classes_col.insert_one(class_type)
            print(f"Added class type: {class_type['name']}")
        else:
            print(f"Class type already exists: {class_type['name']}")


def get_all_class_types():
    """
    Function to get all class types
    """
    return list(classes_col.find())


def get_class_type_by_id(class_id):
    """
    Function to get class type by ID
    """
    if isinstance(class_id, str):
        class_id = ObjectId(class_id)
    return classes_col.find_one({'_id': class_id})


# ----- Studio Management Functions -----

def initialize_studios():
    """
    Initialize studios
    """
    studios = [
        {
            'name': 'Tel Aviv Main Studio',
            'address': '123 Dizengoff Street, Tel Aviv',
            'phone': '03-1234567',
            'email': 'telaviv@theyogaspot.com',
            'description': 'Our flagship location featuring state-of-the-art facilities and ocean views.',
            'amenities': ['Spacious Practice Rooms', 'Changing Rooms', 'Showers', 'Free Wifi', 'Water Station',
                          'Equipment Rental']
        },
        {
            'name': 'Tel Aviv Lounge Studio',
            'address': '45 Rothschild Boulevard, Tel Aviv',
            'phone': '03-7654321',
            'email': 'lounge@theyogaspot.com',
            'description': 'A cozy and intimate space perfect for small group sessions and personal practice.',
            'amenities': ['Cozy Practice Room', 'Changing Area', 'Tea Station', 'Equipment Provided',
                          'Meditation Corner']
        }
    ]

    for studio in studios:
        # Check if studio already exists
        if not studios_col.find_one({'name': studio['name']}):
            studios_col.insert_one(studio)
            print(f"Added studio: {studio['name']}")
        else:
            print(f"Studio already exists: {studio['name']}")


def get_all_studios():
    """
    Function to get all studios
    """
    return list(studios_col.find())


def get_studio_by_id(studio_id):
    """
    Function to get studio by ID
    """
    if isinstance(studio_id, str):
        studio_id = ObjectId(studio_id)
    return studios_col.find_one({'_id': studio_id})


# ----- Schedule Management Functions -----

def initialize_schedule(days_ahead=30):
    """
    Initialize schedule
    """
    # Get class types and studios
    class_types = list(classes_col.find())
    studios = list(studios_col.find())

    # List of instructors
    instructors = [
        {'_id': ObjectId(), 'name': 'Sarah Cohen'},
        {'_id': ObjectId(), 'name': 'Danny Levy'},
        {'_id': ObjectId(), 'name': 'Michelle Golan'},
        {'_id': ObjectId(), 'name': 'Emma Wilson'}
    ]

    # Create map of class types
    class_map = {}
    for class_type in class_types:
        class_map[class_type['name']] = class_type['_id']

    # Helper variables
    start_date = datetime.now()

    classes_to_add = []

    # Create classes by days
    for i in range(days_ahead):
        current_date = start_date + timedelta(days=i)

        # Daily class information
        day_classes = [
            {
                'name': 'Morning Flow',
                'classId': class_map.get('Vinyasa Flow'),
                'studioId': studios[0]['_id'],
                'instructorId': instructors[0]['_id'],
                'startTime': current_date.replace(hour=8, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'endTime': current_date.replace(hour=9, minute=15).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'capacity': 20,
                'bookedCount': 0,
                'price': 65,
                'active': True
            },
            {
                'name': 'Power Yoga',
                'classId': class_map.get('Power Yoga'),
                'studioId': studios[0]['_id'],
                'instructorId': instructors[1]['_id'],
                'startTime': current_date.replace(hour=12, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'endTime': current_date.replace(hour=13, minute=30).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'capacity': 15,
                'bookedCount': 0,
                'price': 70,
                'active': True
            },
            {
                'name': 'Yin Yoga',
                'classId': class_map.get('Yin Yoga'),
                'studioId': studios[0]['_id'],
                'instructorId': instructors[3]['_id'],
                'startTime': current_date.replace(hour=17, minute=30).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'endTime': current_date.replace(hour=19, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'capacity': 20,
                'bookedCount': 0,
                'price': 65,
                'active': True
            }
        ]

        classes_to_add.extend(day_classes)

    # Add all classes
    if classes_to_add:
        for class_item in classes_to_add:
            existing = schedule_col.find_one({
                'startTime': class_item['startTime'],
                'instructorId': class_item['instructorId']
            })

            if not existing:
                schedule_col.insert_one(class_item)

        print(f"Added {len(classes_to_add)} yoga classes")


def get_upcoming_classes(filters=None):
    """
    Function to get upcoming classes with filtering options
    """
    # Base query - filter by future start date only
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    query = {
        'active': True,
        'startTime': {'$gt': current_time}  # Only future classes
    }

    # Collect conditions for classId field
    class_id_conditions = []

    # Add additional filters
    if filters:
        # Class type filter
        if 'classType' in filters and filters['classType']:
            class_type = filters['classType']
            # Find class type ID by name
            class_type_doc = classes_col.find_one({'name': class_type})
            if class_type_doc:
                class_id = class_type_doc['_id']
                class_id_conditions.append({'classId': class_id})

        # Difficulty level filter
        if 'level' in filters and filters['level']:
            # Find IDs of class types with requested level
            level_classes = classes_col.find({'difficulty': filters['level']})
            class_ids = [cls['_id'] for cls in level_classes]
            if class_ids:
                class_id_conditions.append({'classId': {'$in': class_ids}})

        # Studio filter
        if 'studioId' in filters and filters['studioId']:
            query['studioId'] = ObjectId(filters['studioId'])

        # Instructor filter
        if 'instructorName' in filters and filters['instructorName']:
            # Find instructor by name
            instructor_name_parts = filters['instructorName'].split()
            if len(instructor_name_parts) == 2:
                first_name, last_name = instructor_name_parts
                instructor = users_col.find_one({
                    'firstName': first_name,
                    'lastName': last_name,
                    'role': 'instructor'
                })
                if instructor:
                    query['instructorId'] = instructor['_id']
            else:
                # Free search in instructor name (full or partial name)
                instructors = users_col.find({'role': 'instructor'})
                instructor_ids = []
                search_name = filters['instructorName'].lower()

                for instructor in users_col.find({'role': 'instructor'}):
                    full_name = f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}".lower()
                    if search_name in full_name:
                        instructor_ids.append(instructor['_id'])

                if instructor_ids:
                    query['instructorId'] = {'$in': instructor_ids}

        # Time of day filter
        if 'time_of_day' in filters and filters['time_of_day']:
            time_of_day = filters['time_of_day']
            time_query = None

            if time_of_day == 'morning':
                # Morning classes (6:00-12:00)
                time_query = {
                    '$or': [
                        {'startTime': {'$regex': 'T0[6-9]'}},
                        {'startTime': {'$regex': 'T1[0-1]'}}
                    ]
                }
            elif time_of_day == 'afternoon':
                # Afternoon classes (12:00-17:00)
                time_query = {
                    '$or': [
                        {'startTime': {'$regex': 'T12'}},
                        {'startTime': {'$regex': 'T1[3-6]'}}
                    ]
                }
            elif time_of_day == 'evening':
                # Evening classes (17:00-23:00)
                time_query = {
                    '$or': [
                        {'startTime': {'$regex': 'T1[7-9]'}},
                        {'startTime': {'$regex': 'T2[0-3]'}}
                    ]
                }

            if time_query:
                if '$and' not in query:
                    query['$and'] = []
                query['$and'].append(time_query)

    # Combine all classId conditions
    if class_id_conditions:
        if len(class_id_conditions) == 1:
            # If there's only one condition, add it directly
            query.update(class_id_conditions[0])
        else:
            # If there are multiple conditions, use $and
            if '$and' not in query:
                query['$and'] = []
            query['$and'].extend(class_id_conditions)

    # Retrieve data and sort by time
    return list(schedule_col.find(query).sort('startTime', 1))


def get_class_details(schedule_id):
    """
    Function to get detailed class information
    """
    if isinstance(schedule_id, str):
        schedule_id = ObjectId(schedule_id)

    # Get class information
    schedule_item = schedule_col.find_one({'_id': schedule_id})
    if not schedule_item:
        return None

    # Get class type information
    class_type = classes_col.find_one({'_id': schedule_item['classId']})

    # Get studio information
    studio = studios_col.find_one({'_id': schedule_item['studioId']})

    # Create detailed information object
    class_details = {
        'id': str(schedule_item['_id']),
        'name': schedule_item['name'],
        'startTime': schedule_item['startTime'],
        'endTime': schedule_item['endTime'],
        'capacity': schedule_item['capacity'],
        'bookedCount': schedule_item['bookedCount'],
        'price': schedule_item['price'],
        'class': class_type,
        'studio': studio
    }

    return class_details


# ----- Booking Management Functions -----

def book_class(user_id, schedule_id):
    """
    Function to book a class
    """
    # print(f"DB: Booking class for user_id: {user_id}, schedule_id: {schedule_id}")
    # print(f"Types - user_id: {type(user_id)}, schedule_id: {type(schedule_id)}")

    # Convert to IDs
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    if isinstance(schedule_id, str):
        schedule_id = ObjectId(schedule_id)

    # Verify class exists
    schedule_item = schedule_col.find_one({'_id': schedule_id})
    if not schedule_item:
        return False, "Class not found"

    # print(f"Schedule found: {schedule_item.get('name')}")

    # Check if class is full
    if schedule_item.get('bookedCount', 0) >= schedule_item.get('capacity', 0):
        return False, "Class is full"

    # Check if booking already exists
    existing_booking = bookings_col.find_one({
        'userId': user_id,
        'scheduleId': schedule_id,
        'status': 'confirmed'
    })

    if existing_booking:
        return False, "Booking already exists for this class"

    # Create new booking
    booking_data = {
        'userId': user_id,
        'scheduleId': schedule_id,
        'bookingDate': datetime.now().strftime('%Y-%m-%d'),
        'status': 'confirmed',
        'paymentStatus': 'paid',
        'price': schedule_item.get('price', 0)
    }

    # Save booking
    booking_id = bookings_col.insert_one(booking_data).inserted_id

    # Update booked count
    schedule_col.update_one(
        {'_id': schedule_id},
        {'$inc': {'bookedCount': 1}}
    )

    # print(f"Booking created with ID: {booking_id}")
    return True, str(booking_id)


def cancel_booking(booking_id):
    """
    Function to cancel a booking
    """
    if isinstance(booking_id, str):
        booking_id = ObjectId(booking_id)

    # Verify booking exists
    booking = bookings_col.find_one({'_id': booking_id})
    if not booking:
        return False, "Booking not found"

    # Update booking
    bookings_col.update_one(
        {'_id': booking_id},
        {'$set': {
            'status': 'cancelled',
            'paymentStatus': 'refunded'
        }}
    )

    # Update booked count
    schedule_col.update_one(
        {'_id': booking['scheduleId']},
        {'$inc': {'bookedCount': -1}}
    )

    return True, "Booking cancelled successfully"


def get_user_bookings(user_id):
    """
    Function to get user bookings
    """
    # print(f"Fetching bookings for user_id: {user_id}, type: {type(user_id)}")

    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
        # print(f"Converted to ObjectId: {user_id}")

    # Get bookings
    bookings = list(bookings_col.find({
        'userId': user_id,
        'status': 'confirmed'
    }))

    # print(f"Found {len(bookings)} bookings")

    result = []
    current_time = datetime.now()

    for booking in bookings:
        # print(f"Processing booking: {booking.get('_id')}")

        # Get class information
        schedule_item = schedule_col.find_one({'_id': booking['scheduleId']})
        if not schedule_item:
            # print(f"Schedule item not found for scheduleId: {booking['scheduleId']}")
            continue  # Skip bookings without matching class

        # print(f"Schedule item found: {schedule_item.get('_id')}")
        # print(f"Schedule item instructorId: {schedule_item.get('instructorId')}, type: {type(schedule_item.get('instructorId'))}")

        # Get class type information
        class_type = classes_col.find_one({'_id': schedule_item['classId']})

        # Get studio information
        studio = studios_col.find_one({'_id': schedule_item['studioId']})

        # Format date and time
        start_time = schedule_item.get('startTime', '')
        formatted_date = start_time
        class_datetime = None

        try:
            class_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.000Z')
            formatted_date = class_datetime.strftime('%d/%m/%Y')
            formatted_time = class_datetime.strftime('%H:%M')
        except:
            try:
                class_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                formatted_date = class_datetime.strftime('%d/%m/%Y')
                formatted_time = class_datetime.strftime('%H:%M')
            except:
                formatted_date = "Unknown date"
                formatted_time = "Unknown time"

        # Check if class is in the past
        is_past = False
        if class_datetime:
            is_past = class_datetime < current_time

        # Get instructor name
        instructor_name = get_instructor_name(schedule_item.get('instructorId'))

        # Create booking information object
        booking_info = {
            'id': str(booking['_id']),
            'className': schedule_item.get('name', 'Unknown Class'),
            'date': formatted_date,
            'time': formatted_time,
            'duration': class_type.get('duration', 60) if class_type else 60,
            'studio': studio.get('name', 'Unknown') if studio else 'Unknown',
            'price': booking.get('price', 0),
            'scheduleId': str(schedule_item['_id']),
            'isPast': is_past,  # Mark if class has already occurred
            'classType': class_type.get('name', 'Unknown') if class_type else 'Unknown',
            'instructor': instructor_name,
            'level': class_type.get('difficulty', 'all-levels') if class_type else 'all-levels'
        }

        result.append(booking_info)

    # Sort results - future classes first, then past classes
    return sorted(result, key=lambda x: (x['isPast'], x['date'], x['time']))


# Helper function to get instructor name
def get_instructor_name(instructor_id):
    """Get instructor name by ID"""
    # print(f"get_instructor_name called with ID: {instructor_id}, type: {type(instructor_id)}")

    if not instructor_id:
        return "Unknown Instructor"

    instructor = users_col.find_one({'_id': instructor_id})
    # print(f"Instructor search result: {instructor}")

    if instructor:
        return f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}"
    return "Unknown Instructor"


def initialize_database():
    """
    Function to initialize the database
    """
    initialize_class_types()
    initialize_studios()
    initialize_schedule()

    # print("Database initialized successfully!")


# Function to test connection
def test_connection():
    try:
        # Test connection
        client.admin.command('ping')
        print("Database connection established successfully!")
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False


def initialize_contact_requests():
    """
    Initialize contact requests collection
    """
    # Check if sample requests exist
    if contact_requests_col.count_documents({}) == 0:
        sample_requests = [
            {
                'name': 'David Cohen',
                'email': 'david@example.com',
                'phone': '050-1234567',
                'subject': 'membership',
                'message': 'I would like more information about your membership plans.',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'new',
                'user_id': None
            },
            {
                'name': 'Sarah Levy',
                'email': 'sarah@example.com',
                'phone': '054-7654321',
                'subject': 'class-inquiry',
                'message': 'Are your Vinyasa classes suitable for beginners?',
                'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'responded',
                'user_id': None
            }
        ]

        contact_requests_col.insert_many(sample_requests)
        # print(f"Added {len(sample_requests)} sample requests")


def get_user_contact_requests(user_email):
    """
    Get user contact requests by email

    Args:
        user_email: User's email

    Returns:
        list: List of user's contact requests
    """
    try:
        requests = contact_requests_col.find({'email': user_email}).sort('date', -1)
        contact_requests_list = []

        for req in requests:
            # Convert date if exists
            date_str = "Unknown"
            if 'date' in req and req['date']:
                if isinstance(req['date'], datetime):
                    date_str = req['date'].strftime('%d/%m/%Y %H:%M')
                else:
                    date_str = str(req['date'])

            contact_requests_list.append({
                'id': str(req.get('_id')),
                'subject': req.get('subject', 'No Subject'),
                'message': req.get('message', ''),
                'date': date_str,
                'status': req.get('status', 'Pending')
            })

        return contact_requests_list
    except Exception as e:
        print(f"Error getting user contact requests: {e}")
        return []


def delete_contact_request(request_id):
    """
    Delete contact request by ID

    Args:
        request_id: ID of the request to delete

    Returns:
        tuple: (success, message)
    """
    try:
        result = contact_requests_col.delete_one({'_id': ObjectId(request_id)})

        if result.deleted_count > 0:
            return True, "Contact request deleted successfully"
        else:
            return False, "Contact request not found"
    except Exception as e:
        print(f"Error deleting contact request: {e}")
        return False, f"Error: {str(e)}"


# Run connection test if file is executed directly
if __name__ == "__main__":
    if test_connection():
        initialize_database()