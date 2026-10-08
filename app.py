from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)  
@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json()
    cnx = mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123")
    
    name = req['name']
    login = req['email']
    password = generate_password_hash(req['password'])
    date = (name, login, password)
    cur = cnx.cursor()
    rows = cur.execute('INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
    cnx.commit()
    cnx.close()

    return 'vse ok'
@app.route('/login', methods=['POST'])
def user_login():
    req = request.get_json(silent=True) or request.form

    email = req.get('email', '')
    password = req.get('password', '')

    cnx = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        port=3306,
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

    try:
        cur = cnx.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()
        finally:
            cur.close()
    finally:
        cnx.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Неверная почта или пароль'}), 401

    session.clear()
    session['user_id'] = user['id']

    return jsonify({
        'message': 'Успешный вход',
        'redirect': '/lk'
    })
# # Fetch one result
# row = cur.fetchone()
# print("Current date is: {0}".format(row[0]))

# # Close connection
# cnx.close()

@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/login")
def login():
    return render_template('login.html')
app.run()