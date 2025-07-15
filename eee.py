from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
from middleware.auth_middleware import login_required

eee=Blueprint("eee",__name__)

@eee.route('/eee',methods=['get','post'])
@login_required
def eee_page():
    return render_template("eee.html")