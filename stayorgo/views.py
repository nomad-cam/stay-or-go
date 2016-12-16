from flask import render_template, request

from stayorgo import app

from datetime import datetime

@app.route('/') #, methods=['GET','POST'])
def stayorgo():
    # default page
    return render_template('index.html')





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404