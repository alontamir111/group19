# pages/register/register.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db_connector
import re

# יצירת Blueprint
register_bp = Blueprint('register', __name__,
                       template_folder='templates',
                       static_folder='static')

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    # אם המשתמש כבר מחובר, הפנייה לדף חיפוש שיעורים
    if 'user_email' in session:
        return redirect(url_for('searchClasses.search'))

    if request.method == 'POST':
        # קבלת נתוני הטופס
        firstName = request.form.get('firstName', '').strip()
        lastName = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        city = request.form.get('city', '').strip()
        password = request.form.get('password', '')
        confirmPassword = request.form.get('confirmPassword', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        terms = request.form.get('terms') == 'on'

        # ולידציה שרת
        errors = validate_registration_form(firstName, lastName, email, phone, city, password, confirmPassword, age,
                                            terms, gender)

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')

        # הרשמת המשתמש
        success, result = db_connector.register_user(
            firstName=firstName,
            lastName=lastName,
            email=email,
            phone=phone,
            city=city,
            password=password,
            age=age,
            gender=gender
        )

        if success:
            flash('Registration successful!', 'success')
            # הפנייה לדף הבית לאחר הרשמה מוצלחת במקום לדף התחברות
            return redirect(url_for('homepage.index'))
        else:
            flash(result, 'error')

    # הצגת טופס ההרשמה
    return render_template('register.html')


@register_bp.route('/register.html')
def register_html():
    # ניתוב נוסף עבור קבצי HTML ישירים
    return redirect(url_for('register.register'))


def validate_registration_form(firstName, lastName, email, phone, city, password, confirmPassword, age, terms, gender):
    """ולידציה של טופס ההרשמה"""
    errors = []

    # בדיקת שם פרטי
    if not firstName or len(firstName) < 3:
        errors.append("First name must be at least 3 characters")

    # בדיקת שם משפחה
    if not lastName or len(lastName) < 3:
        errors.append("Last name must be at least 3 characters")

    # בדיקת אימייל
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        errors.append("Invalid email format")

    # בדיקת טלפון
    if not re.match(r'^05\d{8}$', phone):
        errors.append("Invalid phone number")

    # בדיקת עיר
    if not city:
        errors.append("City is required")

    # בדיקת סיסמה
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters")

    # בדיקת התאמת סיסמאות
    if password != confirmPassword:
        errors.append("Passwords do not match")

    # בדיקת גיל
    if age:
        try:
            age_num = int(age)
            if age_num < 16 or age_num > 120:
                errors.append("Age must be between 16 and 120")
        except ValueError:
            errors.append("Age must be a number")

    # בדיקת תנאי שימוש
    if not terms:
        errors.append("You must accept the Terms and Conditions")

    # בדיקת מגדר
    if not gender:
        errors.append("Please select a gender")

    return errors