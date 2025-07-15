from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
from middleware.auth_middleware import login_required

mech=Blueprint("mech",__name__)

@mech.route('/mech',methods=['get','post'])
@login_required
def mech_page():
    return render_template("mech.html")