from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/department/<int:id>', methods=['GET'])
@token_auth.login_required
def get_department(id):
    return jsonify(Document.query.get_or_404(id).to_dict())
    
@bp.route('/department', methods=['GET'])
@token_auth.login_required
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Document.to_collection_dict(Document.query, page, per_page, \
        'api.get_files')
    return jsonify(data)
    
    