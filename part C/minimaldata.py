# minimal_initialize.py - סקריפט אתחול מינימלי לתצוגת פונקציונליות
import os
import pymongo
from bson import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# URI מקובץ .env
uri = os.environ.get('DB_URI', 'mongodb://localhost:27017/')

try:
    # יצירת התחברות לשרת MongoDB
    client = pymongo.MongoClient(uri)

    # בדיקת חיבור
    client.admin.command('ping')
    print("✅ חיבור למסד הנתונים נוצר בהצלחה!")
except Exception as e:
    print(f"❌ שגיאה בחיבור למסד הנתונים: {e}")
    sys.exit(1)

# שאלה לפני מחיקת מסד הנתונים
answer = input("⚠️ האם אתה בטוח שברצונך למחוק את מסד הנתונים הקיים וליצור חדש? (כן/לא): ")
if answer.lower() not in ['כן', 'yes', 'y']:
    print("פעולת האתחול בוטלה.")
    sys.exit(0)

# מחיקת מסד הנתונים הקיים (אם הוא קיים) ויצירת אחד חדש
db_name = 'yoga_spot_db'
client.drop_database(db_name)
db = client[db_name]

# יצירת אוספים
users_col = db['users']
classes_col = db['classes']
studios_col = db['studios']
schedule_col = db['schedule']
bookings_col = db['bookings']
contact_requests_col = db['contact_requests']

print("\n🚀 אתחול בסיס הנתונים החל...")

# === יצירת סוגי שיעורים (מינימום) ===
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
    },
    {
        'name': 'Morning Flow',
        'description': 'Energizing morning practice to awaken body and mind. Gentle movements building to more dynamic sequences.',
        'difficulty': 'all-levels',
        'duration': 60,
        'equipment': ['Yoga mat', 'Water bottle'],
        'recommendations': 'Perfect start to the day for all practitioners.'
    }
]

class_type_ids = {}
for class_type in class_types:
    result = classes_col.insert_one(class_type)
    class_type_ids[class_type['name']] = result.inserted_id
    print(f"➕ נוסף סוג שיעור: {class_type['name']}")

# === יצירת סטודיו (מינימום) ===
studios = [
    {
        'name': 'Tel Aviv Main Studio',
        'address': '123 Dizengoff Street, Tel Aviv',
        'phone': '03-1234567',
        'email': 'telaviv@theyogaspot.com',
        'description': 'Our flagship location with state-of-the-art facilities.',
        'amenities': ['Spacious Practice Rooms', 'Changing Rooms', 'Showers']
    },
    {
        'name': 'Tel Aviv Lounge Studio',
        'address': '45 Rothschild Boulevard, Tel Aviv',
        'phone': '03-7654321',
        'email': 'lounge@theyogaspot.com',
        'description': 'A cozy and intimate space for small group sessions.',
        'amenities': ['Cozy Practice Room', 'Tea Station']
    }
]

studio_ids = {}
for studio in studios:
    result = studios_col.insert_one(studio)
    studio_ids[studio['name']] = result.inserted_id
    print(f"➕ נוסף סטודיו: {studio['name']}")

# === יצירת משתמשים (מדריכים ומשתמש בדיקה) ===
instructors = [
    {
        'firstName': 'Sarah',
        'lastName': 'Cohen',
        'email': 'sarah@theyogaspot.com',
        'phone': '050-1234567',
        'city': 'Tel Aviv',
        'password': 'password123',
        'registrationDate': (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'),
        'role': 'instructor',
        'bio': 'Certified yoga instructor specializing in Vinyasa and Hatha.',
        'active': True
    },
    {
        'firstName': 'Emma',
        'lastName': 'Wilson',
        'email': 'emma@theyogaspot.com',
        'phone': '050-9876543',
        'city': 'Tel Aviv',
        'password': 'password123',
        'registrationDate': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
        'role': 'instructor',
        'bio': 'Yin Yoga specialist with meditation training.',
        'active': True
    }
]

instructor_ids = {}
for instructor in instructors:
    result = users_col.insert_one(instructor)
    instructor_ids[f"{instructor['firstName']} {instructor['lastName']}"] = result.inserted_id
    print(f"➕ נוסף מדריך: {instructor['firstName']} {instructor['lastName']}")

# משתמש בדיקה אחד
test_user = {
    'firstName': 'Test',
    'lastName': 'User',
    'email': 'test@example.com',
    'phone': '050-0000000',
    'city': 'Tel Aviv',
    'password': 'password',
    'registrationDate': datetime.now().strftime('%Y-%m-%d'),
    'role': 'user',
    'active': True
}

test_user_id = users_col.insert_one(test_user).inserted_id
print(f"➕ נוסף משתמש בדיקה: {test_user['firstName']} {test_user['lastName']}")

# === יצירת שיעורים (מינימום) ===
schedule_items = []

# תאריכים קבועים לפשטות
past_dates = [
    datetime.now() - timedelta(days=10),  # לפני 10 ימים
    datetime.now() - timedelta(days=7),  # לפני שבוע
    datetime.now() - timedelta(days=3)  # לפני 3 ימים
]

future_dates = [
    datetime(2025, 5, 1),  # 1 במאי 2025
    datetime(2025, 5, 5),  # 5 במאי 2025
    datetime(2025, 5, 10),  # 10 במאי 2025
    datetime(2025, 5, 15),  # 15 במאי 2025
    datetime(2025, 5, 20)  # 20 במאי 2025
]

# שיעורים שכבר עברו
for i, past_date in enumerate(past_dates):
    # Vinyasa Flow בבוקר (עם Sarah Cohen)
    morning_class = {
        'name': 'Morning Flow',
        'classId': class_type_ids['Vinyasa Flow'],
        'studioId': studio_ids['Tel Aviv Main Studio'],
        'instructorId': instructor_ids['Sarah Cohen'],
        'startTime': past_date.replace(hour=8, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'endTime': past_date.replace(hour=9, minute=15).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'capacity': 10,
        'bookedCount': 8,
        'price': 65,
        'active': True
    }
    schedule_items.append(morning_class)

    # Yin Yoga בערב (עם Emma Wilson)
    evening_class = {
        'name': 'Evening Yin',
        'classId': class_type_ids['Yin Yoga'],
        'studioId': studio_ids['Tel Aviv Lounge Studio'],
        'instructorId': instructor_ids['Emma Wilson'],
        'startTime': past_date.replace(hour=18, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'endTime': past_date.replace(hour=19, minute=15).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'capacity': 8,
        'bookedCount': 6,
        'price': 65,
        'active': True
    }
    schedule_items.append(evening_class)

# שיעורים עתידיים
for i, future_date in enumerate(future_dates):
    # Vinyasa Flow בבוקר (עם Sarah Cohen)
    morning_class = {
        'name': 'Morning Flow',
        'classId': class_type_ids['Vinyasa Flow'],
        'studioId': studio_ids['Tel Aviv Main Studio'],
        'instructorId': instructor_ids['Sarah Cohen'],
        'startTime': future_date.replace(hour=8, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'endTime': future_date.replace(hour=9, minute=15).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'capacity': 10,
        'bookedCount': 0,
        'price': 65,
        'active': True
    }
    schedule_items.append(morning_class)

    # Hatha Yoga בצהריים (עם Sarah Cohen)
    noon_class = {
        'name': 'Gentle Hatha',
        'classId': class_type_ids['Hatha Yoga'],
        'studioId': studio_ids['Tel Aviv Lounge Studio'],
        'instructorId': instructor_ids['Sarah Cohen'],
        'startTime': future_date.replace(hour=12, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'endTime': future_date.replace(hour=13, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'capacity': 5 if i == 0 else 8,  # השיעור הראשון עם קיבולת קטנה לבדיקת שיעור מלא
        'bookedCount': 0,
        'price': 60,
        'active': True
    }
    schedule_items.append(noon_class)

    # Yin Yoga בערב (עם Emma Wilson)
    evening_class = {
        'name': 'Evening Yin',
        'classId': class_type_ids['Yin Yoga'],
        'studioId': studio_ids['Tel Aviv Main Studio'],
        'instructorId': instructor_ids['Emma Wilson'],
        'startTime': future_date.replace(hour=18, minute=0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'endTime': future_date.replace(hour=19, minute=15).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'capacity': 10,
        'bookedCount': 0,
        'price': 65,
        'active': True
    }
    schedule_items.append(evening_class)

# הוספת שיעורים למסד הנתונים
schedule_ids = {}
for item in schedule_items:
    result = schedule_col.insert_one(item)
    key = f"{item['name']}_{item['startTime']}"
    schedule_ids[key] = result.inserted_id

print(f"➕ נוספו {len(schedule_ids)} שיעורים ללוח הזמנים")

# === יצירת הזמנות ===
bookings = []

# הזמנות לשיעורים שעברו
past_items = [item for item in schedule_items if
              datetime.strptime(item['startTime'], '%Y-%m-%dT%H:%M:%S.000Z') < datetime.now()]
for i, past_class in enumerate(past_items[:3]):
    booking = {
        'userId': test_user_id,
        'scheduleId': schedule_ids[f"{past_class['name']}_{past_class['startTime']}"],
        'bookingDate': (
                    datetime.strptime(past_class['startTime'], '%Y-%m-%dT%H:%M:%S.000Z') - timedelta(days=3)).strftime(
            '%Y-%m-%d'),
        'status': 'confirmed',
        'paymentStatus': 'paid',
        'price': past_class['price']
    }
    bookings.append(booking)

# הזמנות לשיעורים עתידיים
future_items = [item for item in schedule_items if
                datetime.strptime(item['startTime'], '%Y-%m-%dT%H:%M:%S.000Z') >= datetime.now()]
for i, future_class in enumerate(future_items[:2]):
    booking = {
        'userId': test_user_id,
        'scheduleId': schedule_ids[f"{future_class['name']}_{future_class['startTime']}"],
        'bookingDate': datetime.now().strftime('%Y-%m-%d'),
        'status': 'confirmed',
        'paymentStatus': 'paid',
        'price': future_class['price']
    }
    bookings.append(booking)

    # עדכון מספר המקומות התפוסים בשיעור
    schedule_col.update_one(
        {'_id': schedule_ids[f"{future_class['name']}_{future_class['startTime']}"]},
        {'$inc': {'bookedCount': 1}}
    )

# שיעור מבוטל
if len(future_items) > 2:
    cancelled_class = future_items[2]
    booking = {
        'userId': test_user_id,
        'scheduleId': schedule_ids[f"{cancelled_class['name']}_{cancelled_class['startTime']}"],
        'bookingDate': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'status': 'cancelled',
        'paymentStatus': 'refunded',
        'price': cancelled_class['price']
    }
    bookings.append(booking)

# שיעור עם תפוסה מלאה (הראשון מהעתידיים)
full_class = future_items[0]
full_class_id = schedule_ids[f"{full_class['name']}_{full_class['startTime']}"]
# הוסף 4 הזמנות נוספות (יחד עם זו של משתמש הבדיקה = 5, מלא)
for i in range(4):
    dummy_user = {
        'firstName': f'Dummy{i}',
        'lastName': 'User',
        'email': f'dummy{i}@example.com',
        'phone': f'050-000000{i}',
        'city': 'Tel Aviv',
        'password': 'password',
        'registrationDate': datetime.now().strftime('%Y-%m-%d'),
        'role': 'user',
        'active': True
    }
    dummy_user_id = users_col.insert_one(dummy_user).inserted_id

    dummy_booking = {
        'userId': dummy_user_id,
        'scheduleId': full_class_id,
        'bookingDate': datetime.now().strftime('%Y-%m-%d'),
        'status': 'confirmed',
        'paymentStatus': 'paid',
        'price': full_class['price']
    }
    bookings_col.insert_one(dummy_booking)

# עדכון מספר המקומות בשיעור המלא
schedule_col.update_one(
    {'_id': full_class_id},
    {'$set': {'bookedCount': 5}}  # מלא (קיבולת 5)
)

# הוספת ההזמנות למסד הנתונים
for booking in bookings:
    bookings_col.insert_one(booking)

print(f"➕ נוספו {len(bookings)} הזמנות למשתמש התבנית, וסה\"כ {len(bookings) + 4} הזמנות")

print("\n✅ אתחול בסיס הנתונים הושלם בהצלחה!")
print("\n📱 פרטי התחברות למשתמש לדוגמה:")
print(f"Email: test@example.com")
print(f"Password: password")