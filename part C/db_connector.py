# db_connector.py
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime, timedelta

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# URI מקובץ .env
uri = os.environ.get('DB_URI', 'mongodb://localhost:27017/')

# יצירת התחברות לשרת MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))

# התחברות למסד הנתונים
db = client['yoga_spot_db']

# אוספים (collections) בפרויקט - לפי מה שראינו בתמונות
bookings_col = db['bookings']
classes_col = db['classes']
schedule_col = db['schedule']
studios_col = db['studios']
users_col = db['users']
contact_requests_col = db['contact_requests']


# ----- פונקציות ניהול משתמשים -----

def register_user(firstName, lastName, email, phone, city, password, age=None, gender=None):
    """
    פונקציה להרשמת משתמש חדש - לפי המבנה המדויק שראינו ב-users בתמונה
    """
    # בדיקה אם המשתמש כבר קיים
    if users_col.find_one({'email': email}):
        return False, "משתמש עם אימייל זה כבר קיים."

    if users_col.find_one({'phone': phone}):
        return False, "משתמש עם מספר טלפון זה כבר קיים."

    # הוספת משתמש חדש
    new_user = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'phone': phone,
        'city': city,
        'password': password,  # בסביבת פיתוח, סיסמה ללא הצפנה. בסביבת ייצור יש להצפין
        'registrationDate': datetime.now().strftime('%Y-%m-%d'),
        'role': 'user',
        'active': True
    }

    # הוספת שדות אופציונליים אם סופקו
    if age:
        new_user['age'] = int(age)

    if gender:
        new_user['gender'] = gender

    # הוספת המשתמש למסד הנתונים
    user_id = users_col.insert_one(new_user).inserted_id

    # החזרת ID של המשתמש החדש
    return True, str(user_id)


def authenticate_user(email, password):
    """
    פונקציה לאימות משתמש
    """
    user = users_col.find_one({
        'email': email,
        'password': password,  # בסביבת ייצור יש לבדוק את הסיסמה המוצפנת
        'active': True
    })

    if user:
        # המרה ל-dict רגיל (ללא ObjectId)
        user_dict = {k: v for k, v in user.items() if k != '_id'}
        user_dict['_id'] = str(user['_id'])
        return True, user_dict

    return False, "שם משתמש או סיסמה שגויים."


def get_user_by_email(email):
    """
    פונקציה למציאת משתמש לפי אימייל
    """
    user = users_col.find_one({'email': email})
    if user:
        # המרה ל-dict רגיל (ללא ObjectId)
        user_dict = {k: v for k, v in user.items() if k != '_id'}
        user_dict['_id'] = str(user['_id'])
        return user_dict
    return None


def update_user(email, user_data):
    """
    פונקציה לעדכון פרטי משתמש
    """
    # הסרת שדות שלא ניתן לעדכן
    if '_id' in user_data:
        del user_data['_id']

    # בדיקה אם האימייל החדש כבר קיים (אם האימייל השתנה)
    if 'email' in user_data and user_data['email'] != email:
        if users_col.find_one({'email': user_data['email']}):
            return False, "אימייל זה כבר בשימוש."

    # ביצוע העדכון
    result = users_col.update_one(
        {'email': email},
        {'$set': user_data}
    )

    if result.modified_count > 0:
        return True, "פרטי המשתמש עודכנו בהצלחה."
    else:
        return False, "לא בוצעו שינויים."


# ----- פונקציות לניהול סוגי שיעורים -----

def initialize_class_types():
    """
    אתחול סוגי שיעורים - לפי המבנה המדויק שראינו ב-classes בתמונה
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
        # בדיקה אם סוג השיעור כבר קיים
        if not classes_col.find_one({'name': class_type['name']}):
            classes_col.insert_one(class_type)
            print(f"נוסף סוג שיעור: {class_type['name']}")
        else:
            print(f"סוג שיעור כבר קיים: {class_type['name']}")


def get_all_class_types():
    """
    פונקציה לקבלת כל סוגי השיעורים
    """
    return list(classes_col.find())


def get_class_type_by_id(class_id):
    """
    פונקציה לקבלת סוג שיעור לפי מזהה
    """
    if isinstance(class_id, str):
        class_id = ObjectId(class_id)
    return classes_col.find_one({'_id': class_id})


# ----- פונקציות לניהול סטודיו -----

def initialize_studios():
    """
    אתחול סטודיו - לפי המבנה המדויק שראינו ב-studios בתמונה
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
        # בדיקה אם הסטודיו כבר קיים
        if not studios_col.find_one({'name': studio['name']}):
            studios_col.insert_one(studio)
            print(f"נוסף סטודיו: {studio['name']}")
        else:
            print(f"סטודיו כבר קיים: {studio['name']}")


def get_all_studios():
    """
    פונקציה לקבלת כל הסטודיו
    """
    return list(studios_col.find())


def get_studio_by_id(studio_id):
    """
    פונקציה לקבלת סטודיו לפי מזהה
    """
    if isinstance(studio_id, str):
        studio_id = ObjectId(studio_id)
    return studios_col.find_one({'_id': studio_id})


# ----- פונקציות לניהול לוח זמנים -----

def initialize_schedule(days_ahead=30):
    """
    אתחול לוח זמנים - לפי המבנה המדויק שראינו ב-schedule בתמונה
    """
    # קבלת סוגי השיעורים והסטודיו
    class_types = list(classes_col.find())
    studios = list(studios_col.find())

    # רשימת מדריכים
    instructors = [
        {'_id': ObjectId(), 'name': 'Sarah Cohen'},
        {'_id': ObjectId(), 'name': 'Danny Levy'},
        {'_id': ObjectId(), 'name': 'Michelle Golan'},
        {'_id': ObjectId(), 'name': 'Emma Wilson'}
    ]

    # וידוא שיש מפתחות של classId לכל סוג שיעור
    class_map = {}
    for class_type in class_types:
        class_map[class_type['name']] = class_type['_id']

    # משתני עזר
    from datetime import datetime, timedelta
    start_date = datetime.now()

    classes_to_add = []

    # יצירת שיעורים לפי הימים
    for i in range(days_ahead):
        current_date = start_date + timedelta(days=i)

        # מידע על השיעורים היומיים
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

    # הוספת כל השיעורים
    if classes_to_add:
        for class_item in classes_to_add:
            existing = schedule_col.find_one({
                'startTime': class_item['startTime'],
                'instructorId': class_item['instructorId']
            })

            if not existing:
                schedule_col.insert_one(class_item)

        print(f"נוספו {len(classes_to_add)} שיעורי יוגה")


def get_upcoming_classes(filters=None):
    """
    פונקציה לקבלת שיעורים עתידיים עם אפשרות סינון
    """
    # שאילתת בסיס - עם סינון לפי תאריך תחילה עתידי בלבד
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    query = {
        'active': True,
        'startTime': {'$gt': current_time}  # רק שיעורים עתידיים
    }

    # איסוף תנאים לשדה classId
    class_id_conditions = []

    # הוספת פילטרים נוספים
    if filters:
        # פילטר סוג שיעור
        if 'classType' in filters and filters['classType']:
            class_type = filters['classType']
            # מציאת ה-ID של סוג השיעור לפי שם
            class_type_doc = classes_col.find_one({'name': class_type})
            if class_type_doc:
                class_id = class_type_doc['_id']
                class_id_conditions.append({'classId': class_id})

        # פילטר רמת קושי
        if 'level' in filters and filters['level']:
            # מציאת ID של סוגי שיעורים ברמה המבוקשת
            level_classes = classes_col.find({'difficulty': filters['level']})
            class_ids = [cls['_id'] for cls in level_classes]
            if class_ids:
                class_id_conditions.append({'classId': {'$in': class_ids}})

        # פילטר סטודיו
        if 'studioId' in filters and filters['studioId']:
            query['studioId'] = ObjectId(filters['studioId'])

        # פילטר מדריך
        if 'instructorName' in filters and filters['instructorName']:
            # מציאת המדריך לפי שם
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
                # חיפוש חופשי בשם המדריך (שם מלא או חלקי)
                instructors = users_col.find({'role': 'instructor'})
                instructor_ids = []
                search_name = filters['instructorName'].lower()

                for instructor in users_col.find({'role': 'instructor'}):
                    full_name = f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}".lower()
                    if search_name in full_name:
                        instructor_ids.append(instructor['_id'])

                if instructor_ids:
                    query['instructorId'] = {'$in': instructor_ids}

        # אפשרות לסינון לפי שעות היום
        if 'time_of_day' in filters and filters['time_of_day']:
            time_of_day = filters['time_of_day']
            time_query = None

            if time_of_day == 'morning':
                # שיעורי בוקר (6:00-12:00)
                time_query = {
                    '$or': [
                        {'startTime': {'$regex': 'T0[6-9]'}},
                        {'startTime': {'$regex': 'T1[0-1]'}}
                    ]
                }
            elif time_of_day == 'afternoon':
                # שיעורי צהריים (12:00-17:00)
                time_query = {
                    '$or': [
                        {'startTime': {'$regex': 'T12'}},
                        {'startTime': {'$regex': 'T1[3-6]'}}
                    ]
                }
            elif time_of_day == 'evening':
                # שיעורי ערב (17:00-23:00)
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

    # שילוב כל התנאים של classId
    if class_id_conditions:
        if len(class_id_conditions) == 1:
            # אם יש רק תנאי אחד, אפשר להוסיף אותו ישירות
            query.update(class_id_conditions[0])
        else:
            # אם יש כמה תנאים, צריך להשתמש ב-$and
            if '$and' not in query:
                query['$and'] = []
            query['$and'].extend(class_id_conditions)

    # שליפת הנתונים וסידור לפי זמן
    return list(schedule_col.find(query).sort('startTime', 1))

def get_class_details(schedule_id):
    """
    פונקציה לקבלת פרטי שיעור מורחבים
    """
    if isinstance(schedule_id, str):
        schedule_id = ObjectId(schedule_id)

    # שליפת הנתונים על השיעור
    schedule_item = schedule_col.find_one({'_id': schedule_id})
    if not schedule_item:
        return None

    # שליפת סוג השיעור
    class_type = classes_col.find_one({'_id': schedule_item['classId']})

    # שליפת הסטודיו
    studio = studios_col.find_one({'_id': schedule_item['studioId']})

    # יצירת אובייקט מידע מורחב
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


# ----- פונקציות לניהול הזמנות -----

def book_class(user_id, schedule_id):
    """
    פונקציה להרשמה לשיעור
    """
    print(f"DB: Booking class for user_id: {user_id}, schedule_id: {schedule_id}")
    print(f"Types - user_id: {type(user_id)}, schedule_id: {type(schedule_id)}")

    # המרה למזהים
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    if isinstance(schedule_id, str):
        schedule_id = ObjectId(schedule_id)

    # וידוא שהשיעור קיים
    schedule_item = schedule_col.find_one({'_id': schedule_id})
    if not schedule_item:
        return False, "השיעור לא נמצא"

    print(f"Schedule found: {schedule_item.get('name')}")

    # בדיקה אם השיעור מלא
    if schedule_item.get('bookedCount', 0) >= schedule_item.get('capacity', 0):
        return False, "השיעור מלא"

    # בדיקה אם כבר קיימת הזמנה
    existing_booking = bookings_col.find_one({
        'userId': user_id,
        'scheduleId': schedule_id,
        'status': 'confirmed'
    })

    if existing_booking:
        return False, "כבר קיימת הזמנה לשיעור זה"

    # יצירת הזמנה חדשה
    booking_data = {
        'userId': user_id,
        'scheduleId': schedule_id,
        'bookingDate': datetime.now().strftime('%Y-%m-%d'),
        'status': 'confirmed',
        'paymentStatus': 'paid',
        'price': schedule_item.get('price', 0)
    }

    # שמירת ההזמנה
    booking_id = bookings_col.insert_one(booking_data).inserted_id

    # עדכון מספר המקומות המוזמנים
    schedule_col.update_one(
        {'_id': schedule_id},
        {'$inc': {'bookedCount': 1}}
    )

    print(f"Booking created with ID: {booking_id}")
    return True, str(booking_id)


def cancel_booking(booking_id):
    """
    פונקציה לביטול הזמנה
    """
    if isinstance(booking_id, str):
        booking_id = ObjectId(booking_id)

    # וידוא שההזמנה קיימת
    booking = bookings_col.find_one({'_id': booking_id})
    if not booking:
        return False, "ההזמנה לא נמצאה"

    # עדכון ההזמנה
    bookings_col.update_one(
        {'_id': booking_id},
        {'$set': {
            'status': 'cancelled',
            'paymentStatus': 'refunded'
        }}
    )

    # עדכון מספר המקומות המוזמנים
    schedule_col.update_one(
        {'_id': booking['scheduleId']},
        {'$inc': {'bookedCount': -1}}
    )

    return True, "ההזמנה בוטלה בהצלחה"


def get_user_bookings(user_id):
    """
    פונקציה לקבלת הזמנות של משתמש
    """
    print(f"Fetching bookings for user_id: {user_id}, type: {type(user_id)}")

    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
        print(f"Converted to ObjectId: {user_id}")

    # שליפת ההזמנות
    bookings = list(bookings_col.find({
        'userId': user_id,
        'status': 'confirmed'
    }))

    print(f"Found {len(bookings)} bookings")

    result = []
    current_time = datetime.now()

    for booking in bookings:
        print(f"Processing booking: {booking.get('_id')}")

        # שליפת פרטי השיעור
        schedule_item = schedule_col.find_one({'_id': booking['scheduleId']})
        if not schedule_item:
            print(f"Schedule item not found for scheduleId: {booking['scheduleId']}")
            continue  # דילוג על הזמנות ללא שיעור מתאים

        print(f"Schedule item found: {schedule_item.get('_id')}")
        print(
            f"Schedule item instructorId: {schedule_item.get('instructorId')}, type: {type(schedule_item.get('instructorId'))}")

        # שליפת פרטי סוג השיעור
        class_type = classes_col.find_one({'_id': schedule_item['classId']})

        # שליפת פרטי הסטודיו
        studio = studios_col.find_one({'_id': schedule_item['studioId']})

        # פורמט תאריך ושעה
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

        # בדיקה האם השיעור כבר עבר
        is_past = False
        if class_datetime:
            is_past = class_datetime < current_time

        # שליפת שם המדריך
        instructor_name = get_instructor_name(schedule_item.get('instructorId'))

        # יצירת אובייקט מידע על ההזמנה
        booking_info = {
            'id': str(booking['_id']),
            'className': schedule_item.get('name', 'Unknown Class'),
            'date': formatted_date,
            'time': formatted_time,
            'duration': class_type.get('duration', 60) if class_type else 60,
            'studio': studio.get('name', 'Unknown') if studio else 'Unknown',
            'price': booking.get('price', 0),
            'scheduleId': str(schedule_item['_id']),
            'isPast': is_past,  # סימון אם השיעור כבר התקיים
            'classType': class_type.get('name', 'Unknown') if class_type else 'Unknown',
            'instructor': instructor_name,
            'level': class_type.get('difficulty', 'all-levels') if class_type else 'all-levels'
        }

        result.append(booking_info)

    # מיון התוצאות - שיעורים עתידיים קודם, ואז שיעורים שעברו
    return sorted(result, key=lambda x: (x['isPast'], x['date'], x['time']))

# def get_user_bookings(user_id):
#     """
#     פונקציה לקבלת הזמנות של משתמש
#     """
#     print(f">>> get_user_bookings - התחלה: user_id={user_id}, type={type(user_id)}")
#
#     if isinstance(user_id, str):
#         user_id = ObjectId(user_id)
#         print(f">>> המרת מזהה משתמש ל-ObjectId: {user_id}")
#
#     # שליפת ההזמנות
#     bookings = list(bookings_col.find({
#         'userId': user_id,
#         'status': 'confirmed'
#     }))
#
#     print(f">>> נמצאו {len(bookings)} הזמנות מאושרות")
#
#     result = []
#     current_time = datetime.now()
#
#     for booking in bookings:
#         print(f"\n>>> מעבד הזמנה: {booking.get('_id')}")
#
#         # בדיקה אם scheduleId קיים
#         if 'scheduleId' not in booking:
#             print(f"!!! שגיאה: scheduleId חסר בהזמנה {booking.get('_id')}")
#             continue
#
#         # שליפת פרטי השיעור
#         schedule_item = schedule_col.find_one({'_id': booking['scheduleId']})
#         if not schedule_item:
#             print(f"!!! שגיאה: שיעור לא נמצא עבור scheduleId: {booking['scheduleId']}")
#             continue
#
#         print(f">>> שיעור נמצא: {schedule_item.get('_id')}")
#
#         # בדיקה אם classId קיים
#         if 'classId' not in schedule_item:
#             print(f"!!! שגיאה: classId חסר בשיעור {schedule_item.get('_id')}")
#             continue
#
#         # שליפת פרטי סוג השיעור
#         class_type = classes_col.find_one({'_id': schedule_item['classId']})
#         if not class_type:
#             print(f"!!! שגיאה: סוג שיעור לא נמצא עבור classId: {schedule_item['classId']}")
#             continue
#
#         # בדיקה אם studioId קיים
#         if 'studioId' not in schedule_item:
#             print(f"!!! שגיאה: studioId חסר בשיעור {schedule_item.get('_id')}")
#             continue
#
#         # שליפת פרטי הסטודיו
#         studio = studios_col.find_one({'_id': schedule_item['studioId']})
#         if not studio:
#             print(f"!!! שגיאה: סטודיו לא נמצא עבור studioId: {schedule_item['studioId']}")
#             continue
#
#         # בדיקה אם startTime קיים
#         if 'startTime' not in schedule_item:
#             print(f"!!! שגיאה: startTime חסר בשיעור {schedule_item.get('_id')}")
#             continue
#
#         # פורמט תאריך ושעה
#         start_time = schedule_item['startTime']
#         try:
#             class_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.000Z')
#             formatted_date = class_datetime.strftime('%d/%m/%Y')
#             formatted_time = class_datetime.strftime('%H:%M')
#         except ValueError:
#             try:
#                 class_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
#                 formatted_date = class_datetime.strftime('%d/%m/%Y')
#                 formatted_time = class_datetime.strftime('%H:%M')
#             except ValueError:
#                 print(f"!!! שגיאה: לא ניתן לנתח את פורמט התאריך: {start_time}")
#                 continue
#
#         # בדיקה האם השיעור כבר עבר
#         is_past = class_datetime < current_time
#
#         # בדיקה אם instructorId קיים
#         if 'instructorId' not in schedule_item:
#             print(f"!!! שגיאה: instructorId חסר בשיעור {schedule_item.get('_id')}")
#             continue
#
#         # שליפת שם המדריך
#         instructor = users_col.find_one({'_id': schedule_item['instructorId']})
#         if not instructor:
#             print(f"!!! שגיאה: מדריך לא נמצא עבור instructorId: {schedule_item['instructorId']}")
#             continue
#
#         instructor_name = f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}"
#         if not instructor_name.strip():
#             print(f"!!! שגיאה: שם המדריך ריק עבור instructorId: {schedule_item['instructorId']}")
#             continue
#
#         # יצירת אובייקט מידע על ההזמנה
#         booking_info = {
#             'id': str(booking['_id']),
#             'className': schedule_item['name'],
#             'date': formatted_date,
#             'time': formatted_time,
#             'duration': class_type['duration'],
#             'studio': studio['name'],
#             'price': booking['price'],
#             'scheduleId': str(schedule_item['_id']),
#             'isPast': is_past,
#             'classType': class_type['name'],
#             'instructor': instructor_name,
#             'level': class_type['difficulty']
#         }
#
#         result.append(booking_info)
#         print(f">>> הזמנה נוספה לתוצאות: {booking_info['className']} בתאריך {booking_info['date']}")
#
#     # מיון התוצאות - שיעורים עתידיים קודם, ואז שיעורים שעברו
#     sorted_result = sorted(result, key=lambda x: (x['isPast'], x['date'], x['time']))
#     print(f"\n>>> סה\"כ {len(sorted_result)} הזמנות נמצאו ומוחזרות")
#
#     return sorted_result

# פונקציית עזר לקבלת שם המדריך
def get_instructor_name(instructor_id):
    """קבלת שם המדריך לפי מזהה"""
    print(f"get_instructor_name called with ID: {instructor_id}, type: {type(instructor_id)}")

    if not instructor_id:
        return "Unknown Instructor"

    instructor = users_col.find_one({'_id': instructor_id})
    print(f"Instructor search result: {instructor}")

    if instructor:
        return f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}"
    return "Unknown Instructor"

def initialize_database():
    """
    פונקציה לאתחול מסד הנתונים
    """
    initialize_class_types()
    initialize_studios()
    initialize_schedule()

    print("מסד הנתונים אותחל בהצלחה!")


# פונקציה לבדיקת חיבור
def test_connection():
    try:
        # בדיקת חיבור
        client.admin.command('ping')
        print("חיבור למסד הנתונים נוצר בהצלחה!")
        return True
    except Exception as e:
        print(f"שגיאה בחיבור למסד הנתונים: {e}")
        return False


# def get_upcoming_classes(filters=None):
#     """
#     פונקציה לקבלת שיעורים עתידיים עם אפשרות סינון
#     """
#     # שאילתת בסיס - עם סינון לפי תאריך תחילה עתידי בלבד
#     current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
#     query = {
#         'active': True,
#         'startTime': {'$gt': current_time}  # רק שיעורים עתידיים
#     }
#
#     # הוספת פילטרים נוספים
#     if filters:
#         if 'classType' in filters and filters['classType']:
#             class_type = filters['classType']
#             class_id = None
#             # מציאת ה-ID של סוג השיעור לפי שם
#             class_type_doc = classes_col.find_one({'name': class_type})
#             if class_type_doc:
#                 class_id = class_type_doc['_id']
#             if class_id:
#                 query['classId'] = class_id
#
#         if 'studioId' in filters and filters['studioId']:
#             query['studioId'] = ObjectId(filters['studioId'])
#
#         if 'instructorName' in filters and filters['instructorName']:
#             # מציאת המדריך לפי שם
#             instructor_name_parts = filters['instructorName'].split()
#             if len(instructor_name_parts) == 2:
#                 first_name, last_name = instructor_name_parts
#                 instructor = users_col.find_one({
#                     'firstName': first_name,
#                     'lastName': last_name,
#                     'role': 'instructor'
#                 })
#                 if instructor:
#                     query['instructorId'] = instructor['_id']
#             else:
#                 # חיפוש חופשי בשם המדריך (שם מלא או חלקי)
#                 instructors = users_col.find({'role': 'instructor'})
#                 instructor_ids = []
#                 search_name = filters['instructorName'].lower()
#
#                 for instructor in users_col.find({'role': 'instructor'}):
#                     full_name = f"{instructor.get('firstName', '')} {instructor.get('lastName', '')}".lower()
#                     if search_name in full_name:
#                         instructor_ids.append(instructor['_id'])
#
#                 if instructor_ids:
#                     query['instructorId'] = {'$in': instructor_ids}
#
#         # אפשרות לסינון לפי שעות היום
#         if 'time_of_day' in filters and filters['time_of_day']:
#             time_of_day = filters['time_of_day']
#             time_query = None
#
#             if time_of_day == 'morning':
#                 # שיעורי בוקר (6:00-12:00)
#                 time_query = {
#                     '$or': [
#                         {'startTime': {'$regex': 'T0[6-9]'}},
#                         {'startTime': {'$regex': 'T1[0-1]'}}
#                     ]
#                 }
#             elif time_of_day == 'afternoon':
#                 # שיעורי צהריים (12:00-17:00)
#                 time_query = {
#                     '$or': [
#                         {'startTime': {'$regex': 'T12'}},
#                         {'startTime': {'$regex': 'T1[3-6]'}}
#                     ]
#                 }
#             elif time_of_day == 'evening':
#                 # שיעורי ערב (17:00-23:00)
#                 time_query = {
#                     '$or': [
#                         {'startTime': {'$regex': 'T1[7-9]'}},
#                         {'startTime': {'$regex': 'T2[0-3]'}}
#                     ]
#                 }
#
#             if time_query:
#                 if '$and' not in query:
#                     query['$and'] = []
#                 query['$and'].append(time_query)
#
#         # אם יש סינון לפי רמת קושי
#         if 'level' in filters and filters['level']:
#             # מציאת ID של סוגי שיעורים ברמה המבוקשת
#             level_classes = classes_col.find({'difficulty': filters['level']})
#             class_ids = [cls['_id'] for cls in level_classes]
#             if class_ids:
#                 query['classId'] = {'$in': class_ids}
#
#     # שליפת הנתונים וסידור לפי זמן
#     return list(schedule_col.find(query).sort('startTime', 1))


def initialize_contact_requests():
    """
    אתחול קולקשן של פניות צור קשר
    """
    # בדיקה אם קיימות פניות לדוגמה
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
        print(f"נוספו {len(sample_requests)} פניות לדוגמה")


def get_user_contact_requests(user_email):
    """
    קבלת פניות צור קשר של משתמש לפי אימייל

    Args:
        user_email: האימייל של המשתמש

    Returns:
        list: רשימת פניות צור קשר של המשתמש
    """
    try:
        requests = contact_requests_col.find({'email': user_email}).sort('date', -1)
        contact_requests_list = []

        for req in requests:
            # המרת תאריך אם קיים
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
    מחיקת פניית צור קשר לפי מזהה

    Args:
        request_id: המזהה של הפנייה למחיקה

    Returns:
        tuple: (הצלחה, הודעה)
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

# הפעלת בדיקת חיבור אם הקובץ מופעל ישירות
if __name__ == "__main__":
    if test_connection():
        initialize_database()