import io, os
from zipfile import ZipFile
from flask import send_file
from config import UPLOAD_FOLDER

# Bundle up images into one sweet zip
def create_zip_from_filenames(filenames):
    buffer = io.BytesIO()

    with ZipFile(buffer, 'w') as zipf:
        for fname in filenames:
            full_path = os.path.join(UPLOAD_FOLDER, fname)
            if os.path.exists(full_path):
                zipf.write(full_path, arcname=fname)

    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='selected_frames.zip'
    )
