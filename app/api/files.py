from flask import jsonify, request, url_for, current_app
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    """
    Check whether file is inallowd extension list
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           current_app.config['ALLOWED_EXTENSIONS']  

@bp.route('/files/<int:id>', methods=['GET'])
@token_auth.login_required
def get_file(id):
    return jsonify(Document.query.get_or_404(id).to_dict())
    
@bp.route('/files', methods=['GET'])
@token_auth.login_required
def get_files():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Document.to_collection_dict(Document.query, page, per_page, \
        'api.get_files')
    return jsonify(data)
    
@bp.route('/files', methods=['POST'])
#@token_auth.login_required
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return bad_request("field \'file\' not found")    
    files = request.files.getlist("file")
    for file in files:
        if file.filename == '':
            return bad_request('filename empty string')
        if not allowed_file(file.filename):
            return bad_request('not allowed file type')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'status':'ok'})