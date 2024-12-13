import re
from flask import Flask, jsonify, request
from secrets import token_urlsafe
from random import randint
from os import environ
from flask_cors import CORS

from db import *
from util import *

GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = environ.get('GOOGLE_CLIENT_SECRET')

app = Flask(__name__)
CORS(app)
app.secret_key = "GIET, best university in eastern odisha"

@app.route("/get_otp", methods = ["POST"])
def get_otp():
    body = request.get_json()
    email = body['email']
    if not email.endswith("@giet.edu"):
        return "giet@edu mail is required", 401
    token = token_urlsafe(16)
    otp = randint(1000, 9999)
    send_otp(email, otp)
    insert_otp(token + email, otp)
    return jsonify({ 'token': token })

required_info = ('email', 'name', 'type', 'password', 'otp', 'token')
@app.route("/create_user", methods = ["POST"])
def create_user():
    body = request.get_json()
    for info in required_info:
        if info not in body:
            return "missing " + info, 400
    is_student_mail = bool(re.match(r"^[1-9]+[a-z]+[1-9]+\.", body['email']))
    if (body['type'] == "student") != is_student_mail:
        return "mail type doesnot match with login type", 401
    if not validate_otp(body['token'] + body['email'], body['otp']):
        return "invalid otp", 401
    key = token_urlsafe(64)
    if body['type'] == "faculty":
        create_faculty(body, key)
    elif body['type'] == "student":
        create_student(body, key)
    else:
        return "invalid login type", 400
    return jsonify({ 'key': key })

@app.route("/fetch_key", methods = ['POST'])
def fetch_key():
    body = request.get_json()
    for info in ('email', 'password', "type"):
        if info not in body:
            print(info, "missing")
            return "missing " + info, 400
    res = select_key(body['email'], body['password'], body['type'])
    if res:
        return jsonify({ 'key': res })
    else:
        return "invalid credentials", 401

@app.route("/faculty_details", methods = ['GET'])
def faculty_details():
    if not validate_authorization(request.headers.get("Authorization")):
        return "invalid Authorization", 401
    return select_faculty_status()

@app.route("/update_status", methods = ['PATCH'])
def update_status():
    token = validate_authorization(request.headers.get("Authorization"))
    if token == None:
        return "invalid Authorization", 401
    body = request.json
    if token[0] != "faculty":
        return "type should be faculty", 401
    if 'incampus' not in body:
        return "incampus not found", 400
    update_faculty_status(token[1], body['incampus'])
    return {}, 200
app.run()
