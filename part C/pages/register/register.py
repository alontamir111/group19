# register.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db_connector
import re

# Create Blueprint
register_bp = Blueprint('register', __name__,
                       template_folder='templates',
                       static_folder='static')

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to class search page
    if 'user_email' in session:
        return redirect(url_for('searchClasses.search'))

    if request.method == 'POST':
        # Get form data
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

        # Server-side validation
        errors = validate_registration_form(firstName, lastName, email, phone, city, password, confirmPassword, age,
                                            terms, gender)

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')

        # Register the user
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
            # Redirect to homepage after successful registration instead of login page
            return redirect(url_for('homepage.index'))
        else:
            flash(result, 'error')

    # Display registration form
    return render_template('register.html')


@register_bp.route('/register.html')
def register_html():
    # Additional route for direct HTML file access
    return redirect(url_for('register.register'))


def validate_registration_form(firstName, lastName, email, phone, city, password, confirmPassword, age, terms, gender):
    """Validation for the registration form"""
    errors = []

    # Check first name
    if not firstName or len(firstName) < 3:
        errors.append("First name must be at least 3 characters")

    # Check last name
    if not lastName or len(lastName) < 3:
        errors.append("Last name must be at least 3 characters")

    # Check email
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        errors.append("Invalid email format")

    # Check phone - דורש את המקף או מקבל גם בלעדיו
    if not re.match(r'^05\d-?\d{7}$', phone):
        errors.append("Invalid phone number")

    # Check city
    if not city:
        errors.append("City is required")

    # Check password
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters")

    # Check password confirmation
    if password != confirmPassword:
        errors.append("Passwords do not match")

    # Check age
    if age:
        try:
            age_num = int(age)
            if age_num < 16 or age_num > 120:
                errors.append("Age must be between 16 and 120")
        except ValueError:
            errors.append("Age must be a number")

    # Check terms acceptance
    if not terms:
        errors.append("You must accept the Terms and Conditions")

    # Check gender selection
    if not gender:
        errors.append("Please select a gender")

    return errors