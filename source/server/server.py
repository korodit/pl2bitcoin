# coding: utf-8
import logic
import logging
from flask import Flask,url_for,request,make_response
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def play():
    cook = None
    if "session_id" in request.cookies:
        cook = request.cookies["session_id"]

    req_type = request.method

    req_formdict = None
    try:
        req_formdict = request.form
    except:
        pass
    
    body,cook = logic.handle_play(req_type,cook,req_formdict)
    
    resp = make_response(body)
    resp.set_cookie("session_id",cook)
    return resp