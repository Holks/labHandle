from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/uncertainty/<int:id>', methods=['GET'])
@token_auth.login_required
def get_uncertainty(id):
    return jsonify(Uncertainty.query.get_or_404(id).to_dict())
    
@bp.route('/uncertainties', methods=['GET'])
@token_auth.login_required
def get_uncertainties():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Uncertainty.to_collection_dict(Uncertainty.query, page, per_page, \
        'api.get_uncertainties')
    return jsonify(data)