# pages/signin/signin.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db_connector

# יצירת blueprint
signin = Blueprint('signin', __name__,
                   template_folder='templates',
                   static_folder='static')


@signin.route('/', methods=['GET', 'POST'])
def login():
    # אם המשתמש כבר מחובר, הפנייה לדף חיפוש שיעורים
    if 'user_email' in session:
        return redirect(url_for('searchClasses.search'))  # שים לב לשם Blueprint

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # בדיקות ולידציה בסיסיות
        if not email:
            flash('Please enter your email', 'error')
            return render_template('signin.html')

        if not password:
            flash('Please enter your password', 'error')
            return render_template('signin.html')

        # אימות המשתמש מול מסד הנתונים
        success, result = db_connector.authenticate_user(email, password)

        if success:
            # שמירת פרטי המשתמש בסשן
            session['user_email'] = email
            session['user_id'] = result['_id']
            session['user_name'] = f"{result['firstName']} {result['lastName']}"

            # הפנייה לדף חיפוש שיעורים
            return redirect('/searchClasses')
        else:
            # הצגת הודעת שגיאה
            flash('Invalid email or password', 'error')

    # הצגת דף ההתחברות
    return render_template('signin.html')


@signin.route('/signin.html')
def signin_html():
    # ניתוב נוסף עבור קבצי HTML ישירים
    return redirect(url_for('signin.login'))