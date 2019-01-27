from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.admin import bp
from app.models import Department, Document, User, Instrument
from app.email import send_user_created
import json
from app import ext_modules

"""
Users
"""
@bp.route('/users', methods=['GET'])
def get_user_list():
    args = request.args.to_dict()
    data = User.query.order_by(User.id).all()
    # ?data=json used for getting data as json object or other formats
    if 'data_type' in args.keys() and 'json' in args['data_type']:
        json_data = [item.to_dict() for item in data]
        print(json_data)
        return jsonify(json_data)
    return render_template('admin/users.html', title='Users', \
        data=data, header=User._default_fields, heading='Users')

@bp.route('/user', methods=['PUT'])
def edit_user():
    return render_template('admin/department_view.html', title='')

@bp.route('/user/<int:id>', methods=['GET', 'POST'])
def get_user(id):
    return render_template('admin/department_view.html', title='')


@bp.route('/user', methods=['POST'])
def add_user():
    json_obj = json.loads(request.form.get('form_json'))
    if 'username' not in json_obj or 'email' not in json_obj \
        or 'password' not in json_obj:
        flash('must include username, email and password fields')
        print('must include username, email and password fields')
    elif User.query.filter_by(username=json_obj['username']).first():
        flash('please use a different username')
        print('please use a different username')
    else:
        user = User()
        user.from_dict(**json_obj)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=json_obj['username']).first()
        if user:
            flash('Added user {0}'.format(json_obj['username']))
        else:
            print('Unable to add new user {0}'.format(json_obj['username']))
            flash('Unable to add new user {0}'.format(json_obj['username']))
        #return redirect(url_for('admin.get_user_list'))
    data = User.query.order_by(User.id).all()
    return render_template('admin/users.html', title='Users', \
        data=data, header=User._default_fields, heading='Users')
"""
Departments
"""
@bp.route('/department', methods=['GET'])
def get_department_list():
    args = request.args.to_dict()
    data = Department.query.order_by(Department.id).all()
    # ?data=json used for getting data as json object or other formats
    if 'data_type' in args.keys() and 'json' in args['data_type']:
        json_data = [item.to_dict() for item in data]
        return jsonify(json_data)
    return render_template('admin/departments.html', title='Departments', \
        data=data, header=Department._default_fields, heading='Departments')

@bp.route('/department', methods=['POST'])
def add_department():
    return render_template('admin/add_department.html', title='')

@bp.route('/department', methods=['DELETE'])
def archive_department():
    return render_template('admin/departments.html', title='')

@bp.route('/department', methods=['PUT'])
def edit_department():
    return render_template('admin/department_view.html', title='')

@bp.route('/department/<int:id>', methods=['GET', 'POST'])
def get_department(id):
    return render_template('admin/department_view.html', title='')

"""
Documents
"""
@bp.route('/document', methods=['GET', 'POST'])
def add_document():
    return render_template('admin/document.html', title='')

"""
Instruments
"""
def update_instrument_list(auth):
    return ext_modules.api_get_instruments(auth_credentials=auth)

@bp.route('/instruments', methods=['GET', 'POST'])
def get_instrument_list():
    if request.method in 'GET':
        data = Instrument.query.order_by(Instrument.id).all()
        return render_template('admin/instruments.html', title='Instruments', \
            data=data, header=Instrument._default_fields, heading='Instruments')
    if request.method in 'POST':
        auth = request.get_json()
        resp = update_instrument_list(auth)
        if resp['data']:
            for instrument in resp['data']:
                inst = Instrument(
                    mois_id=instrument['id'],
                    description=instrument['manufacturer'] + ';' \
                        + instrument['name'] + ';' \
                        + instrument['serial_number'],
                    data_fields_json=instrument['data_fields'],
                    last_maintenance_interval=instrument[ \
                        'last_maintenance_interval'])
                if instrument['last_maintenance_date']:
                    inst.last_maintenance_date = datetime.fromtimestamp( \
                        float(instrument['last_maintenance_date']))
                try:
                    db.session.add(inst)
                    db.session.commit()
                except:
                    db.session.rollback()

            return '', 200
        else:
            return '', 403
