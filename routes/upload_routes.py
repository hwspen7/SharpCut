from flask import Blueprint, request, jsonify
from services.frame_extractor import extract_clear_frames
import os, uuid
from config import UPLOAD_FOLDER

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=['POST'])
def upload():
    # Grab the file and drop it in uploads/
    file = request.files['video']
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Get options from the form
    threshold = float(request.form.get('threshold', 100))
    step = int(request.form.get('step', 1))
    resize = request.form.get('resize') == 'on'

    # Run the frame extraction logic
    frames, metadata = extract_clear_frames(filepath, threshold, step, resize)

    response = { 'frames': metadata }

    # Boom. Done.
    return jsonify(response)
