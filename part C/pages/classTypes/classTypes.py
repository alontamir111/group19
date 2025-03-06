# classTypes.py
from flask import Blueprint, render_template
import db_connector

# יצירת Blueprint עם השם הנכון - classTypes
classTypes = Blueprint('classTypes', __name__,
                       template_folder='templates',
                       static_folder='static')


@classTypes.route('/')
def index():
    # קבלת כל סוגי השיעורים ממסד הנתונים
    classes = db_connector.get_all_class_types()

    # מיפוי שמות שיעורים לקבצי תמונות
    image_mapping = {
        'Vinyasa Flow': 'vinyasa-yoga.jpg',
        'Hatha Yoga': 'hatha-yoga.jpg',
        'Power Yoga': 'power-yoga.jpg',
        'Yin Yoga': 'yin-yoga.jpg',
        'Prenatal Yoga': 'YogaStudio.jpg',  # תמונה זמנית לשיעור הריון
        'Meditation': 'YogaStudio.jpg'  # תמונה זמנית למדיטציה
    }

    # הוספת שדה תמונה לכל שיעור
    for class_type in classes:
        class_name = class_type.get('name', '')

        if class_name in image_mapping:
            class_type['image'] = image_mapping[class_name]
        else:
            # ברירת מחדל אם אין התאמה מדויקת
            class_type['image'] = 'YogaStudio.jpg'

    return render_template('classTypes.html', classes=classes)