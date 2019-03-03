from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.main import bp
from werkzeug.utils import secure_filename
from app.models import User
import json

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route('/calendar', methods=['GET'])
def calendar():
    return render_template('main/calendar.html')

@bp.route('/tasks', methods=['GET'])
def tasks():
    return render_template('main/tasks.html')
