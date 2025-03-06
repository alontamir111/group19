# studios.py
from flask import Blueprint, render_template

studios = Blueprint('studios', __name__,
                    template_folder='templates',
                    static_folder='static')


@studios.route('/')
def index():
    # דוגמה של סטודיו - בפרויקט אמיתי זה יגיע ממסד הנתונים
    studios_data = [
        {
            'name': 'Tel Aviv Main Studio',
            'address': '123 Dizengoff Street, Tel Aviv',
            'phone': '03-1234567',
            'email': 'telaviv@theyogaspot.com',
            'description': 'Our flagship location featuring state-of-the-art facilities and ocean views.',
            'amenities': ['Spacious Practice Rooms', 'Changing Rooms', 'Showers', 'Free Wifi', 'Water Station',
                          'Equipment Rental'],
            'image': 'telaviv-main.jpg'
        },
        {
            'name': 'Tel Aviv Lounge Studio',
            'address': '45 Rothschild Boulevard, Tel Aviv',
            'phone': '03-7654321',
            'email': 'lounge@theyogaspot.com',
            'description': 'A cozy and intimate space perfect for small group sessions and personal practice.',
            'amenities': ['Cozy Practice Room', 'Changing Area', 'Tea Station', 'Equipment Provided',
                          'Meditation Corner'],
            'image': 'telaviv-lounge.jpg'
        }
    ]

    # מיפוי של תמונות התקני סטודיו
    facilities = [
        {
            'name': 'Quality Props',
            'description': 'We provide high-quality yoga props to support your practice and help you achieve proper alignment.',
            'image': 'telaviv-props.jpg'
        },
        {
            'name': 'Welcoming Reception',
            'description': 'Our friendly staff is always ready to assist you and answer any questions you might have.',
            'image': 'telaviv-reception.jpg'
        },
        {
            'name': 'Relaxing Lounge',
            'description': 'Unwind before or after your class in our comfortable lounge area with complimentary tea.',
            'image': 'telaviv-lounge.jpg'
        },
        {
            'name': 'Modern Shower Facilities',
            'description': 'Our clean, modern shower facilities make it easy to freshen up after your practice.',
            'image': 'shower-cubicles.jpg'  # שם התמונה המתוקן
        }
    ]

    return render_template('studios.html', studios=studios_data, facilities=facilities)