import os
from sqlite3 import connect

from flask import render_template, send_from_directory
from werkzeug.security import check_password_hash

from config import app, auth, users
from mainDIR.site.processes.endpoints.endpointAlertYoo import alertYoo
from mainDIR.site.processes.endpoints.endpointFuse import fuse
from mainDIR.site.processes.endpoints.endpointGetData import getData
from mainDIR.site.processes.endpoints.endpointMainThreadGET import handlerGET
from mainDIR.site.processes.endpoints.endpointMainThreadPOST import handlerPOST
from mainDIR.site.processes.endpoints.endpointCreate import create
from mainDIR.site.processes.endpoints.endpointRetry import retry


@auth.verify_password
async def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@app.route("/", methods = ['POST'])
async def handlerSitePOST():
    return await handlerPOST()


@app.route("/", methods = ['GET'])
async def handlerSiteGET():
    return await handlerGET()


@app.route('/getData', methods=['GET', 'POST'])
@auth.login_required
async def handlerGetData():
    return await getData()


@app.route('/retry', methods=['GET', 'POST'])
async def handlerRetry():
    return await retry()


@app.route('/create', methods=['GET', 'POST'])
async def handlerCreate():
    return await create()


@app.route('/yookassa/alert', methods=['GET', 'POST'])
async def handlerAlertYoo():
    return await alertYoo()


@app.route('/fuse', methods=['GET', 'POST'])
async def handlerFuse():
    return await fuse()


@app.route('/contacts', methods=['GET', 'POST'])
async def contacts():
    return render_template('contacts.html')


@app.route('/offer', methods=['GET', 'POST'])
async def offer():
    return render_template('publicOffer.html')


@app.route('/personal-data', methods=['GET', 'POST'])
async def personal_data():
    return render_template('policies.html')


@app.route('/admin')
@auth.login_required
async def handlerAdmin():
    return render_template('admin_panel.html')


@app.route('/icon.ico')
async def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'icon.ico', mimetype='icon.icon')


@app.route('/yookassa', methods=['GET', 'POST'])
async def yookassaCreate():
    return "yoomoney"


if __name__ == "__main__":
    with connect('databaseSITE.db') as conn:
        conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        patronymic TEXT,
        region TEXT,
        birthdate DATE,
        passport TEXT,
        passportDate DATE,
        email TEXT,
        state TEXT,
        idForOrder TEXT
        )
        """)
    app.run(debug=True)