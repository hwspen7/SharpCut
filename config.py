import os

# Base path
BASE_DIR = os.path.dirname(__file__)

# Where we store uploaded videos and output frames
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Allowed file types (you can tweak this)
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

# Default values (fallbacks)
DEFAULT_THRESHOLD = 100  # Laplacian variance threshold
DEFAULT_STEP = 1         # Check every frame by default
