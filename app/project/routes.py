from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.project import bp
import json
from datetime import datetime


@bp.route('', methods=['GET'])
def projects():
    return render_template('project/projects.html', title='')
