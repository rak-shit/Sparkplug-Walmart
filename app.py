#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
from htmllib import HTML
import logging
import json
from logging import Formatter, FileHandler
from forms import *
import os
import pandas as pd
from sparkplug import Dashboard
from helpers import send_mail, essential_items
from flask_cors import CORS
import boto3
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
CORS(app)

client = boto3.client('lambda')
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
catalog_managers = ["bim2016002@iiita.ac.in"]
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
    year = int(year)
    if request.args.get(commodity_name) and request.args.get(year) and request.args.get(country):
        sellers = find_sellers(request.args.get(commodity_name), request.args.get(country))
        mkt_dict = map_mkt(request.args.get(commodity_name), request.args.get(country))
    else:
        dashboard = Dashboard(commodity_name, country, year)
        sellers = dashboard.find_sellers(commodity_name, country)
        mkt_dict = dashboard.map_mkt(commodity_name, country)

    anomaly_obj = dashboard.anomaly_detection(mkt_dict, year, commodity_name, country)

    anomaly_obj_json = anomaly_obj[0]
    outliers_list = anomaly_obj[1]

    mkt_dict_reverse =  {_id: marketer for marketer, _id in mkt_dict.items()}
    print(mkt_dict)
    outlier_set = set()
    for outlier in outliers_list:
        try:
            seller_info = mkt_dict_reverse[outlier[0]]
            outlier_set.add(seller_info)
        except Exception as e:
            print(e)
    outlier_list = list(outlier_set)

    seller_histories = []
    
    # data reduced to commodity, year and country
    reduced_data = dashboard.data[(dashboard.data["mkt_name"].isin(outlier_list)) & (dashboard.data["adm0_name"] == country) & (dashboard.data["mp_year"] == year)]

    print(reduced_data)
    print("TH", dashboard.threshold_all(commodity_name, year, country))

    # send emails asynchronously, AWS Lambda
    for manager in catalog_managers:
        outlier_lists = reduced_data[["adm1_id","cm_name","mp_price","mp_month","mp_year"]].values.tolist()
        outlier_lists = [["Seller/Marketer ID","Commodity Name","Selling Price","Month","Year"]] + outlier_lists
        html_content = HTML.table(outlier_lists)
        html_content = "<html><h1>Price Gouging Sellers & Historical Data</h1><body>{}</body></html>".format(html_content)
        payload = {'to_email': manager, 'subject':"Potential Price Gouging Alert",
                  'html_content': html_content}
        response = client.invoke(
            FunctionName='lambda-sparkplug',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
    return anomaly_obj_json


    # Blocking task of emails(takes a lot of time, laid off asynchronously above)
    # try:
        # outlier_lists = reduced_data[["adm1_id","cm_name","mp_price","mp_month","mp_year"]].values.tolist()
        # outlier_lists = [["Seller/Marketer ID","Commodity Name","Selling Price","Month","Year"]] + outlier_lists
        # html_content = HTML.table(outlier_lists)
        # html_content = "<html><h1>Price Gouging Sellers & Historical Data</h1><body>{}</body></html>".format(html_content)
        # send_mail(catalog_managers, "Potential Price Gouging Alert", html_content)
    # except Exception as e:
    #     print(str(e))
    #     print("Email Alerts pertaining to price gouging has not been sent to catalog manager...")
    #     print("Continuing to relay data...")

    # return anomaly_obj_json


# #----------------------------------------------------------------------------#
# # Launch.
# #----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# # Or specify port manually:
# '''
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
# '''
