from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.document import bp
from werkzeug.utils import secure_filename
import os
from app.models import Document
import json

def allowed_file(filename, extensions):
    """
    Check whether file is inallowd extension list
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           extensions

@staticmethod
def upload(request, upload_folder, extensions):
    if 'file' not in request.files:
        flash('No file part')
    files = request.files.getlist("file")
    for file in files:
        if file.filename == '':
            flash('No selected file(s)')
        elif not allowed_file(file.filename, extensions):
            flash('Not allowed file(s)')
        elif file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, \
                filename))

@bp.route('/archive', methods=['GET', 'POST'])
def archive():
    pass

@bp.route('', methods=['GET'])
def document():
    args = request.args.to_dict()
    data = Document.query.order_by(Document.id).all()
    # ?data=json used for getting data as json object or other formats
    if 'data_type' in args.keys() and 'json' in args['data_type']:
        json_data = [item.to_dict() for item in data]
        return jsonify(json_data)
    return render_template('document/view.html', title='Documents', \
        data=data, header=Document._default_fields, heading='Documents')

@bp.route('', methods=['POST'])
def add_document():
    json_obj = json.loads(request.form.get('form_json'))
    print(json_obj)
    if 'designation' not in json_obj or 'description' not in json_obj \
        or 'version' not in json_obj:
        flash('must include designation, description and version')
    elif Document.query\
            .filter_by(designation==json_obj['designation'], \
            version=data['version']).first():
        flash('please use a different designation')
    else:
        doc = Document()
        doc.from_dict(**json_obj)
        db.session.add(doc)
        db.session.commit()
        doc = Document.query.\
            filter_by(Designation=json_obj['designation']).first()
        if doc:
            flash('Added document {0}'.format(json_obj['designation']))
        else:
            flash('Unable to add new docuement {0}'.\
                format(json_obj['designation']))
        upload(request, current_app.config['UPLOAD_FOLDER'], \
            current_app.config['ALLOWED_FILE_EXTENSIONS'])
    return redirect(url_for('document.document'))

@bp.route('protocol_template', methods=['GET'])
def protocol_template():
    args = request.args.to_dict()
    data = Document.query.order_by(Document.id).all()
    # ?data=json used for getting data as json object or other formats
    if 'data_type' in args.keys() and 'json' in args['data_type']:
        json_data = [item.to_dict() for item in data]
        return jsonify(json_data)
    return render_template('document/view.html', title='Documents', \
        data=data, header=Document._default_fields, heading='Documents')

@bp.route('protocol_template', methods=['POST'])
def add_protocol_template():
    json_obj = json.loads(request.form.get('form_json'))
    print(json_obj)
    if 'designation' not in json_obj or 'description' not in json_obj \
        or 'version' not in json_obj:
        flash('must include designation, description and version')
    elif Document.query\
            .filter_by(designation==json_obj['designation'], \
            version=data['version']).first():
        flash('please use a different designation')
    else:
        doc = Document()
        doc.from_dict(**json_obj)
        db.session.add(doc)
        db.session.commit()
        doc = Document.query.\
            filter_by(Designation=json_obj['designation']).first()
        if doc:
            flash('Added document {0}'.format(json_obj['designation']))
        else:
            flash('Unable to add new docuement {0}'.\
                format(json_obj['designation']))
        upload(request, current_app.config['UPLOAD_FOLDER'], \
            current_app.config['ALLOWED_FILE_EXTENSIONS'])
    return redirect(url_for('document.document'))

@bp.route('/configuration', methods=['GET', 'POST'])
def configuration():
    return render_template('document/configuration.html', \
        title='Document configuration')
