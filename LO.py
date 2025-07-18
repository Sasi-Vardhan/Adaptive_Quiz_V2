from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
import json
from middleware.auth_middleware import login_required
LO = Blueprint('LO', __name__)



@LO.route("/Learning")
@login_required
def Learning():
    NC = ['email', 'choice', 'user_id', 'key']
    for key, _ in list(session.items()):  # Convert to list to avoid RuntimeError
        if key not in NC:
            session.pop(key, None)

    f=open("subjects.json")

    data=json.load(f)
    choice = session['choice']
    data=data['subjects']
    if(choice == 'sustainability'):
        # print("camee here")
        data=data[0]
    elif (choice == 'genai') :
        data=data[1]
    elif (choice == 'Mechanical Engineering') :
        data=data[2]
    elif (choice == 'Civil Engineering') :
        data=data[3]
    elif (choice == "Bioengineering"):
        data=data[4]
    elif (choice == "Chemical Engineering"):
        data=data[5]
    elif(choice == "MBA"):
        data=data[6]
    elif(choice == "eee"):
        data=data[7]
    # print(data)
    # course_data = data[choice]
    name = data["name"]
    filepath = data["filepath"]
    details = []

    for i, lo in enumerate(data["learning_outcomes"]):
        details.append([
            f"LO{i+1}",
            lo['level'],
            lo['outcome']
        ])
    print(details)
    return render_template(
        'LB.html',
        course_name=name,
        course_path=filepath,
        learning_details=details
    )