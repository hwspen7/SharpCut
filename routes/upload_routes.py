from flask import Blueprint, request, jsonify
from services.frame_extractor import extract_clear_frames
from services.video_utils import make_video_from_frames
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
    make_video = request.form.get('make_video') == 'on'

    # Run the frame extraction logic
    frames, metadata = extract_clear_frames(filepath, threshold, step, resize)

    response = { 'frames': metadata }

    # If user asked for a video, generate it
    if make_video and frames:
        video_name = make_video_from_frames(frames)
        response['video'] = video_name

    # Boom. Done.
    return jsonify(response)
