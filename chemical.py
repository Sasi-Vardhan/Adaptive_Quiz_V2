from flask import Flask, render_template, request, redirect, url_for, session,blueprints,Blueprint
import random
import csv
import os
import math
import requests
from middleware.auth_middleware import login_required

chemical=Blueprint("chemical",__name__)

@chemical.route('/chemical',methods=['get','post'])
@login_required
def chemical_page():
    return render_template("chemical.html")