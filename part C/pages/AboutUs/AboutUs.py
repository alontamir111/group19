from flask import Blueprint, render_template

about_us = Blueprint(
    'about_us',
    __name__,
    static_folder='static',
    static_url_path='/about_us',
    template_folder='templates'
)

@about_us.route('/')
def index():
    return render_template('AboutUs.html')