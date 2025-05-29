from flask import Blueprint, request
from services.zip_packager import create_zip_from_filenames

bp = Blueprint('download', __name__)

@bp.route('/download-selected', methods=['POST'])
def download_selected():
    # Get selected filenames from frontend
    data = request.get_json()
    files = data.get('files', [])

    # Zip 'em up and send it back
    return create_zip_from_filenames(files)
