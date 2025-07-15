from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
from middleware.auth_middleware import login_required

dash = Blueprint('dash', __name__)

@dash.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@dash.route('/set-choice', methods=['POST'])
@login_required
def set_choice():
    session['choice'] = request.form.get('choice')
    print(session["choice"])
    if(session['choice'] == 'sustainability'):
        return redirect(url_for('sustain.sustainability'))
    if(session['choice'] == 'genai'):
        return redirect(url_for('AI.GenAI'))
    if(session['choice'] == 'Mechanical Engineering'):
        return redirect(url_for('mech.mech_page'))
    if(session['choice'] == 'Civil Engineering'):
        return redirect(url_for('civil.civil_page'))
    if(session['choice'] == 'Bioengineering'):
        return redirect(url_for('bio.bio_page'))
    if(session['choice'] == 'MBA'):
        return redirect(url_for('mba.mba_page'))
    if(session['choice'] == 'Chemical Engineering'):
        return redirect(url_for('chemical.chemical_page'))
    if(session['choice'] == 'eee'):
        return redirect(url_for('eee.eee_page'))