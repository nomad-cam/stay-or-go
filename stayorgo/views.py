from flask import render_template, request, jsonify

from stayorgo import app
from bom_ftp import wx_obs

from datetime import datetime

@app.route('/') #, methods=['GET','POST'])
def stayorgo():
    # default page
    return render_template('index.html')


@app.route('/api/wx/current/<station_id>')#, methods=['POST'])
def api_wx_current(station_id):
    # fetch the current weather for a given weather station id.
    # ftp://ftp.bom.gov.au/anon/gen/fwo/IDV60920.xml
    #if request.method == "POST":
        #wx = {}
        #wx['station_id'] = station_id

        obs = wx_obs("IDV60920", station_id)

        return jsonify(obs)


@app.route('/api/wx/forecast/<station_id>')
def api_wx_forecast(station_id):
    # fetch the current weather for a given weather station id.
    #
    wx = {}
    wx['station_id'] = station_id

    return jsonify(wx)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404