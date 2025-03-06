from flask import Flask, render_template, url_for, request, session, flash, redirect
# App setup
app = Flask(__name__,
           template_folder='templates',
           static_folder='static')

# Secret key for sessions
app.secret_key = 'your_secret_key_here'  # Important for form security

# Import Blueprints
from pages.profile.profile import profile_bp
from pages.homepage.Home import homepage
from pages.searchClasses.searchClasses import searchClasses_bp
from pages.AboutUs.AboutUs import about_us
from pages.ContactUs.ContactUs import contact_us
from pages.register.register import register_bp
from pages.signin.signin import signin as signin
from pages.studios.studios import studios
from pages.classTypes.classTypes import classTypes


# Register Blueprints
app.register_blueprint(homepage)
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(about_us, url_prefix='/about')
app.register_blueprint(contact_us, url_prefix='/contact')
app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(signin, url_prefix='/signin')  # New name and new path
app.register_blueprint(studios, url_prefix='/studios')
app.register_blueprint(classTypes, url_prefix='/classes')
app.register_blueprint(searchClasses_bp, url_prefix='/searchClasses')

# Context processor to add functions to all templates
@app.context_processor
def utility_processor():
    def is_active(path):
        # Function that checks if the path is the current path
        return path == request.path
    return dict(is_active=is_active)

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found - 404", 404

@app.errorhandler(500)
def internal_error(e):
    return "Internal server error - 500", 500

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Send logout message to user
    flash('You have been logged out successfully', 'success')
    # Redirect to homepage
    return redirect(url_for('homepage.index'))


if __name__ == '__main__':
    app.run(debug=True)