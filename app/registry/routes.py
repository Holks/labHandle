from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.registry import bp
from app.document.routes import allowed_file
from werkzeug.utils import secure_filename
import os
from app.models import Workstation
import json



@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@bp.route('/uncertainty', methods=['GET', 'POST'])
def uncertainty():
    return render_template('registry/uncertainty.html', \
        heading='Uncertainty calculations')


@bp.route('/guide', methods=['GET', 'POST'])
def guide():

    return render_template('registry/guide.html', heading='Guides')

@bp.route('/protocol_template', methods=['GET', 'POST'])
def protocol_template():

    return render_template('registry/protocol_template.html', \
        heading='Protocol templates')

@bp.route('/workstation', methods=['GET', 'POST'])
def workstation():
    if request.method == "GET":
        args = request.args.to_dict()
        data = Workstation.query.order_by(Workstation.id).all()
        # ?data=json used for getting data as json object or other formats
        if 'data_type' in args.keys() and 'json' in args['data_type']:
            json_data = [item.to_dict() for item in data]
            return jsonify(json_data)
        return render_template('registry/workstation.html', title='', \
            data=data, header=Workstation._default_fields, \
            heading='Work stations')
    if request.method == "POST":
        json_obj = json.loads(request.args.get('form_json'))
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            render_template('registry/workstation.html', \
                heading='Work stations')
        files = request.files.getlist("file")
        for file in files:
            if file.filename == '':
                flash('No selected file')
                render_template('registry/workstation.html', \
                    heading='Work stations')
            if not allowed_file(file.filename):
                flash('Not allowed files')
                render_template('registry/workstation.html', \
                    heading='Work stations')
            if file:
                filename = secure_filename(file.filename)
                print(current_app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], \
                    filename))

        flash('Added workstation')
        return render_template('registry/workstation.html', \
            heading='Work stations')
