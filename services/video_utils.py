import cv2, os, uuid
from config import UPLOAD_FOLDER

# Slap all frames together into a video
def make_video_from_frames(frame_paths):
    if not frame_paths:
        return None

    # Use first frame for size reference
    h, w = cv2.imread(frame_paths[0]).shape[:2]

    video_name = f"output_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(UPLOAD_FOLDER, video_name)

    # 10 FPS is a nice vibe
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (w, h))

    for path in frame_paths:
        out.write(cv2.imread(path))

    out.release()
    return video_name
