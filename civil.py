from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
from middleware.auth_middleware import login_required

civil=Blueprint("civil",__name__)

@civil.route('/civil',methods=['get','post'])
@login_required
def civil_page():
    return render_template("civil.html")