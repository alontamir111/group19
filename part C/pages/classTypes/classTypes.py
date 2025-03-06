# classTypes.py
from flask import Blueprint, render_template
import db_connector

# Create Blueprint with the correct name - classTypes
classTypes = Blueprint('classTypes', __name__,
                       template_folder='templates',
                       static_folder='static')


@classTypes.route('/')
def index():
    # Get all class types from the database
    classes = db_connector.get_all_class_types()

    # Map class names to image files
    image_mapping = {
        'Vinyasa Flow': 'vinyasa-yoga.jpg',
        'Hatha Yoga': 'hatha-yoga.jpg',
        'Power Yoga': 'power-yoga.jpg',
        'Yin Yoga': 'yin-yoga.jpg',
        'Prenatal Yoga': 'YogaStudio.jpg',  # Temporary image for prenatal class
        'Meditation': 'YogaStudio.jpg'  # Temporary image for meditation
    }

    # Add image field to each class
    for class_type in classes:
        class_name = class_type.get('name', '')

        if class_name in image_mapping:
            class_type['image'] = image_mapping[class_name]
        else:
            # Default if no exact match
            class_type['image'] = 'YogaStudio.jpg'

    return render_template('classTypes.html', classes=classes)