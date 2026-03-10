from flask import Flask, jsonify, request, session
from flask_cors import CORS
import json
import os
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import pooling
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key in production
CORS(app, supports_credentials=True)


# Connect to db
# db = mysql.connector.connect(
#     host="localhost",
#     user="kaliosky",
#     password="toor",
#     database="generalCRM")

dbconfig = {
    "host": os.environ["MYSQL_HOST"],
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "database": os.environ["MYSQL_DATABASE"]
}
 


db = pooling.MySQLConnectionPool(pool_name="mypool",
                                      pool_size=10,
                                      pool_reset_session=True,
                                      **dbconfig)
 

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


#adaugare cross_request_api spre un alt service inafara de e in sessiune 

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    users={}
    first_name = data.get('First_name')
    last_name = data.get("Last_name")
    service_name = data.get("Service_name")
    email = data.get("email")
    password = data.get("password")


    print(first_name)
    print(last_name)
    print(service_name)
    print(email)
    print(password)
    if not first_name or not last_name or not service_name or not email or not password:
        return jsonify({"message": "Data forms are required"}), 400

    #need to check if service_name/email exist

    cur = db.cursor(buffered=True)
    cur.execute("INSERT INTO users (First_Name, Last_Name, Email, Service_Name, Password) VALUES (%s, %s, %s, %s, %s);", (first_name, last_name, email, service_name, password))
    db.commit()
    cur.execute(f"SELECT id from users WHERE Email='{email}';")
    user_id = cur.fetchone()
    cur.close()
    conn.close()
    session['user_id'] = user_id
    session['email'] = email
    session['First_name'] = first_name
    session['Last_name'] = last_name
    session['serviceName'] = service_name
    print(data)
    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user_id,
            "email": email,
            "First_name": first_name,
            "Last_name": last_name,
            "serviceName": service_name
        }
    }), 201


      
# @app.route('/api/auth/register', methods=['POST'])
# def register_debug():
#     # Încercăm să preluăm JSON-ul
#     data = request.get_json(silent=True) # Folosim silent=True pentru a nu crăpa dacă nu e JSON
    
#     # Printăm în consolă pentru verificare
#     print("-----------------------------------------")
#     print("HEADER-UL 'Content-Type':", request.headers.get('Content-Type'))
#     print("DATELE BRUTE PRIMITE (JSON):", data)
#     print("-----------------------------------------")

#     # Verificăm cauza problemei
#     if data is None:
#         # Aceasta este cea mai frecventă problemă!
#         # Înseamnă fie că nu s-a trimis JSON, fie a lipsit header-ul 'Content-Type'.
#         return jsonify({
#             "EROARE": "Serverul NU a primit date în format JSON.",
#             "message": "request.get_json() a returnat None. Verifică header-ul 'Content-Type: application/json' în cererea fetch din frontend."
#         }), 400 # 400 Bad Request

#     # Dacă am primit date, le trimitem înapoi pentru a le inspecta în browser
#     return jsonify({
#         "status": "Date primite cu succes pentru depanare.",
#         "tipul_datelor_primite": str(type(data)),
#         "cheile_gasite_in_date": list(data.keys()), # Listăm TOATE cheile găsite
#         "datele_complete_primite": data
#     }), 200

    
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('First_name')
    last_name = data.get("Last_name")
    service_name = data.get("Service_name")

    if not email or not password: 
        return jsonify({
            "message": "Email or password it's invalid",
        }), 401

    conn = db.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)
    cur.execute("SELECT * FROM users WHERE Email=%s AND Password=%s;", (email, password))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"message": "User doesn't exist"}), 401

    session['user_id'] = user["id"]
    session['email'] = user["Email"]
    session['First_name'] = user["First_Name"]
    session['Last_name'] = user["Last_Name"]
    session['serviceName'] = user["Service_Name"]
    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "email": user["Email"],
            "First_name": user["First_Name"],
            "Last_name": user["Last_Name"],
            "serviceName": user["Service_Name"]
        }
    }),201

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 201


# @app.route("/api/me", methods=["POST"])
# def me():



@app.route('/api/auth/status', methods=['GET'])
def status():
    if 'user_id' in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "id": session['user_id'],
                "email": session['email'],
                "First_name": session['First_name'],
                "Last_name": session['Last_name'],
                "serviceName": session['serviceName']
                
            }
        }), 201
    else:
        return jsonify({"authenticated": False}), 401


@app.route("/api/addStock", methods=['POST'])
@login_required
def addStock():
    data = request.get_json() 
    partname = data.get("partName")
    parttype = data.get("partType")
    quantity = data.get("quantity")
    vCompatibility = data.get("vehicleCompatibility")
    price = data.get("price")
    bServiceName = session["serviceName"]

    print(partname)
    print(parttype)
    print(quantity)
    print(vCompatibility)
    print(price)
    print(bServiceName)
    if not partname and not parttype and not quantity and not vCompatibility and not price:
        return jsonify({"message": "All forms need to be processed"}), 400
    conn = db.get_connection()
    cur = conn.cursor(buffered=True)
    cur.execute("INSERT INTO stocks (partName, partType, quantity, vehicleCompatibility, price, bServiceName) VALUES (%s, %s, %s, %s, %s, %s);", (partname, parttype, quantity, vCompatibility, price, bServiceName))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Add new stock with success",
    }), 201
    


@app.route("/api/fetchStock")
@login_required
def viewStock():
    print(session["serviceName"])
    bServiceName = session["serviceName"]
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT id, partName, partType, quantity, vehicleCompatibility, price FROM stocks WHERE bServiceName=%s", (bServiceName,))
        stocks_data = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    # for stock in stocks_data:
    #     return jsonify({
    #         "partName": stock["PartName"],
    #         "partType": stock["PartType"],
    #         "quantity": stock["Quantity"],
    #         "vehicleCompatibility": stock["vCompatibility"],
    #         "price": stock["Price"]
    #     }), 200
    print("viewStock called API CRM")
    print(stocks_data)
    return jsonify(stocks_data)


@app.route("/api/removeStock", methods=["POST"])
@login_required
def removeStock():
    bServiceName = session["serviceName"]
    data = request.get_json()
    partName = data.get("partName")

    if not partName:
        return jsonify({"message":"All params required"}), 400

    print("PartName is " + partName)
    conn = db.get_connection()
    cur = conn.cursor(buffered=True)
    cur.execute("DELETE FROM stocks WHERE bServiceName=%s AND partName=%s ", (bServiceName, partName))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(
        {
            "message":"Stock removed succesfully"
        }
    ), 201

@app.route("/api/editStock", methods=["POST"])
@login_required
def editStock():
    #trebuie sa verific dupa ce ii dau where, daca modific partname va cauta dupa partname-ul nou, si nu vreau asta 
    data = request.get_json()
    ids = data.get("id")
    bServiceName = session["serviceName"]
    partname = data.get("partName")
    parttype = data.get("partType")
    quantity = data.get("quantity")
    vCompatibility = data.get("vehicleCompatibility")
    price = data.get("price")
    
    print(ids)
    if not partname or not parttype or not quantity or not vCompatibility or not price:
        return jsonify({
            "message":"All params will be needed"
        }), 401
    
    conn = db.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)
    cur.execute("UPDATE stocks SET partName=%s, partType=%s, quantity=%s, vehicleCompatibility=%s, price=%s WHERE bServiceName=%s AND id=%s", (partname, parttype, quantity, vCompatibility, price, bServiceName, ids))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(
        {
            "message":"The stock data was edited succesfully"
        }
    ), 201

@app.route("/api/addClient", methods=['POST'])
@login_required
def addClient():
    data = request.get_json() 
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    phone = data.get("phone")
    carMake = data.get("carMake")
    carModel = data.get("carModel")
    carYear = data.get("carYear")
    licensePlate = data.get("licensePlate")
    bServiceName = session["serviceName"]

    print(firstName)
    print(lastName)
    print(email)
    print(phone)
    print(carMake)
    print(carModel)
    print(carYear)
    print(licensePlate)
    print(bServiceName)

    if not firstName and not lastName and not email and not phone and not carMake and not carModel and not carYear and not carYear and not licensePlate:
        return jsonify({"message": "All forms need to be processed"}), 400
    
    conn = db.get_connection()
    cur = conn.cursor(buffered=True)
    cur.execute("INSERT INTO clients (firstName, lastName, email, phone, carMake, carModel, carYear, licensePlate, bServiceName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (firstName, lastName, email, phone, carMake, carModel, carYear, licensePlate, bServiceName))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Add new client with success",
    }), 201
    
@app.route("/api/fetchClients", methods=["GET"])
@login_required
def fetchClients():
    print(session["serviceName"])
    bServiceName = session["serviceName"]
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT id, firstName, lastName, email, phone, carMake, carModel, carYear, licensePlate FROM clients WHERE bServiceName=%s", (bServiceName,))
        stocks_data = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    # for stock in stocks_data:
    #     return jsonify({
    #         "partName": stock["PartName"],
    #         "partType": stock["PartType"],
    #         "quantity": stock["Quantity"],
    #         "vehicleCompatibility": stock["vCompatibility"],
    #         "price": stock["Price"]
    #     }), 200
    print("viewClients called API CRM")
    print(stocks_data)
    return jsonify(stocks_data)

@app.route("/api/removeClient", methods=["POST"])
@login_required
def removeClient():
    bServiceName = session["serviceName"]
    conn = db.get_connection()
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message":"All params required"}), 400

    cur = conn.cursor(buffered=True)
    cur.execute("DELETE FROM clients WHERE bServiceName=%s AND email=%s ", (bServiceName, email))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(
        {
            "message":"Client removed succesfully"
        }
    ), 201

@app.route("/api/editClient", methods=['POST'])
@login_required
def editClient():
    data = request.get_json() 
    ids = data.get("id")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    phone = data.get("phone")
    carMake = data.get("carMake")
    carModel = data.get("carModel")
    carYear = data.get("carYear")
    licensePlate = data.get("licensePlate")
    bServiceName = session["serviceName"]

    print(firstName)
    print(lastName)
    print(email)
    print(phone)
    print(carMake)
    print(carModel)
    print(carYear)
    print(licensePlate)
    print(bServiceName)

    if not firstName and not lastName and not email and not phone and not carMake and not carModel and not carYear and not carYear and not licensePlate:
        return jsonify({"message": "All forms need to be processed"}), 400
    
    #trebuie sa verific cum editam, la fel si pentru stocuri, ca noi postam cu noile informatii, si n-avem de unde sa luam informatia de legatura
    #am rezolvat ceva dar nu se editeaza in clients, mai trebuie testat in stocks
    #posibil rezolvat editingClient / formdata in Pages
    conn = db.get_connection()
    cur = conn.cursor(buffered=True)
    cur.execute("UPDATE clients SET firstName=%s, lastName=%s, email=%s, phone=%s, carMake=%s, carModel=%s, carYear=%s, licensePlate=%s WHERE bServiceName=%s AND id=%s;", (firstName, lastName, email, phone, carMake, carModel, carYear, licensePlate, bServiceName, ids))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Edit client with success",
    }), 201

@app.route("/api/addHistory", methods=['POST'])
@login_required
def addHistory():
    data = request.get_json() 
    email = data.get("email")
    clientName = data.get("clientName")
    carInfo = data.get("carInfo")
    problem = data.get("problem")
    solution = data.get("solution")
    date = data.get("date")
    cost = data.get("cost")
    status = data.get("status")
    bServiceName = session["serviceName"]


    if not email and not clientName and not carInfo and not problem and not solution and not date and not cost:
        return jsonify({"message": "All forms need to be processed"}), 400
    
    #trebuie sa verific cum editam, la fel si pentru stocuri, ca noi postam cu noile informatii, si n-avem de unde sa luam informatia de legatura
    #am rezolvat ceva dar nu se editeaza in clients, mai trebuie testat in stocks
    #posibil rezolvat editingClient / formdata in Pages
    
    conn = db.get_connection()
    cur = conn.cursor(buffered=True)
    cur.execute("INSERT INTO history (email, clientName, carInfo, problem, solution, date, cost, status, bServiceName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (email, clientName, carInfo, problem, solution, date, cost, status, bServiceName))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Add new client with success",
    }), 201
    
@app.route("/api/fetchHistory", methods=["GET"])
@login_required
def fetchHistory():
    print(session["serviceName"])
    bServiceName = session["serviceName"]
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT email, clientName, carInfo, problem, solution, cost, date, status FROM history WHERE bServiceName=%s", (bServiceName,))
        stocks_data = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    # for stock in stocks_data:
    #     return jsonify({
    #         "partName": stock["PartName"],
    #         "partType": stock["PartType"],
    #         "quantity": stock["Quantity"],
    #         "vehicleCompatibility": stock["vCompatibility"],
    #         "price": stock["Price"]
    #     }), 200
    print("viewHistory called API CRM")
    print(stocks_data)
    return jsonify(stocks_data)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
