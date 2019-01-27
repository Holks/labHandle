from flask import jsonify, request, url_for
from app import db
from app.models import Usercategory, Documentcategory
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
import json

@bp.route('/file_category/<int:id>', methods=['GET'])
@token_auth.login_required
def get_file_category(id):
    return jsonify(Document.query.get_or_404(id).to_dict())
    
@bp.route('/file_categories', methods=['GET'])
@token_auth.login_required
def get_file_categories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Document.to_collection_dict(Document.query, page, per_page, \
        'api.get_file_categories')
    return jsonify(data)
    
@bp.route('/user_category', methods=['POST'])
@token_auth.login_required
def add_user_category():
    data = request.get_json() or {}
    if data['name']:
        user_cat_exist = Usercategory.query.filter_by(name=data['name']).first()
        if user_cat_exist:
            return bad_request('provided category already exists')
        user_cat = Usercategory()
        user_cat.from_dict(**data)
        
        db.session.add(user_cat)
        db.session.commit()
        
        user_cat = Usercategory.query.filter_by(name=data['name']).first()
        
        return jsonify(user_cat.to_dict())
    else:
        return bad_request('Category name not provided')
        
        
@bp.route('/file_category', methods=['POST'])
@token_auth.login_required
def file_category():
    data = request.get_json() or {}
    if data['name']:
        file_cat_exist = Documentcategory.query.filter_by(name=data['name']).first()
        if file_cat_exist:
            return bad_request('provided category already exists')
        file_cat = Documentcategory()
        file_cat.from_dict(**data)
        
        db.session.add(file_cat)
        db.session.commit()
        
        file_cat = Documentcategory.query.filter_by(name=data['name']).first()
        
        return jsonify(file_cat.to_dict())
    else:
        return bad_request('Category name not provided')

@bp.route('/status_category', methods=['POST'])
@token_auth.login_required
def status_category():
    data = request.get_json() or {}
    if data['name']:
        status_cat_exist = Documentstatus.query.filter_by(name=data['name']).first()
        if status_cat_exist:
            return bad_request('provided category already exists')
        status_cat = Documentstatus()
        status_cat.from_dict(**data)
        
        db.session.add(status_cat)
        db.session.commit()
        
        status_cat = Documentstatus.query.filter_by(name=data['name']).first()
        
        return jsonify(status_cat.to_dict())
    else:
        return bad_request('Category name not provided')