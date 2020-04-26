#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from sparkplug import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods=['POST', 'GET'])
def index():
    commodity_name = 'Wheat'
    year = 2013
    country = 'India'
    return redirect(url_for('home',commodity_name=commodity_name, year=year, country=country))

@app.route('/monitor/<commodity_name>/<year>/<country>', methods=['POST', 'GET'])
def home(commodity_name, year, country):
    if 'commodity_name' in request.form.keys() and 'year' in request.form.keys() and 'country' and request.form.keys():
        sellers = find_sellers(request.form['commodity_name'], request.form['country'])
        mkt_dict = map_mkt(request.form['commodity_name'], request.form['country'])
        # thresh = threshold(commodity_name, year, country)
        cluster_obj = cluster(mkt_dict, request.form['year'], request.form['commodity_name'], request.form['country'])
        return cluster_obj
    
    year = int(year)
    sellers = find_sellers(commodity_name, country)
    mkt_dict = map_mkt(commodity_name, country)
    # thresh = threshold(commodity_name, year, country)
    cluster_obj = cluster(mkt_dict, year, commodity_name, country)
    return cluster_obj 


# @app.route('/about')
# def about():
#     return render_template('pages/placeholder.about.html')


# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     return render_template('forms/login.html', form=form)


# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# # Error handlers.


# @app.errorhandler(500)
# def internal_error(error):
#     #db_session.rollback()
#     return render_template('errors/500.html'), 500


# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('errors/404.html'), 404

# if not app.debug:
#     file_handler = FileHandler('error.log')
#     file_handler.setFormatter(
#         Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
#     )
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('errors')

# #----------------------------------------------------------------------------#
# # Launch.
# #----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# # Or specify port manually:
# '''
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
# '''
