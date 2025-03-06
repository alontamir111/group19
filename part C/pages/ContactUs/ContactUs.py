from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
import db_connector
from datetime import datetime

contact_us = Blueprint(
    'contact_us',
    __name__,
    static_folder='static',
    static_url_path='/contact_us',
    template_folder='templates'
)


@contact_us.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # קבלת נתונים מהטופס
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone', '')  # אופציונלי
            subject = request.form.get('subject')
            message = request.form.get('message')

            # בדיקת שדות חובה
            if not name or not email or not subject or not message:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': False,
                        'message': 'Please fill in all required fields'
                    })
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('contact_us.index'))

            # יצירת אובייקט פנייה
            contact_request = {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'new',
                'user_id': None
            }

            # אם המשתמש מחובר למערכת, נשמור את המזהה שלו
            if 'user_email' in session:
                user = db_connector.get_user_by_email(session['user_email'])
                if user:
                    contact_request['user_id'] = user.get('_id')

            # הוספת הפנייה למסד הנתונים
            result = db_connector.contact_requests_col.insert_one(contact_request)

            if result.inserted_id:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': True,
                        'message': 'Your message has been sent successfully!'
                    })
                flash('Your message has been sent successfully!', 'success')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': False,
                        'message': 'Failed to send message. Please try again.'
                    })
                flash('Failed to send message. Please try again.', 'error')

            return redirect(url_for('contact_us.index'))

        except Exception as e:
            print(f"Error submitting contact form: {e}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'An error occurred while processing your request.'
                })
            flash('An error occurred while processing your request.', 'error')
            return redirect(url_for('contact_us.index'))

    return render_template('ContactUs.html')