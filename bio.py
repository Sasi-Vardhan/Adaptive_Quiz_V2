from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
from middleware.auth_middleware import login_required

bio=Blueprint("bio",__name__)

@bio.route('/bio',methods=['get','post'])
@login_required
def bio_page():
    return render_template("bio.html")