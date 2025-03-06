# pages/signin/signin.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db_connector

# Create blueprint
signin = Blueprint('signin', __name__,
                   template_folder='templates',
                   static_folder='static')


@signin.route('/', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to class search page
    if 'user_email' in session:
        return redirect(url_for('searchClasses.search'))  # Note the Blueprint name

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Basic validation checks
        if not email:
            flash('Please enter your email', 'error')
            return render_template('signin.html')

        if not password:
            flash('Please enter your password', 'error')
            return render_template('signin.html')

        # Authenticate user against database
        success, result = db_connector.authenticate_user(email, password)

        if success:
            # Store user details in session
            session['user_email'] = email
            session['user_id'] = result['_id']
            session['user_name'] = f"{result['firstName']} {result['lastName']}"

            # Redirect to class search page
            return redirect('/searchClasses')
        else:
            # Display error message
            flash('Invalid email or password', 'error')

    # Display login page
    return render_template('signin.html')


@signin.route('/signin.html')
def signin_html():
    # Additional route for direct HTML file access
    return redirect(url_for('signin.login'))