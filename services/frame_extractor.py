import cv2, os, uuid
from config import UPLOAD_FOLDER

# Super simple clarity calculator using Laplacian variance
def calculate_clarity(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

# Compare histograms to detect scene changes
def scene_change(prev, curr):
    if prev is None:
        return True
    hist1 = cv2.calcHist([cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
    diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    return diff > 0.3  # tweak this if needed

# Extract sharp frames only
def extract_clear_frames(video_path, threshold=100, step=1, resize=False):
    cap = cv2.VideoCapture(video_path)
    frame_index = 0
    saved_frames = []
    metadata = []
    prev_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % step == 0:
            if resize:
                frame = cv2.resize(frame, (640, 360))

            clarity = calculate_clarity(frame)
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # in seconds

            if clarity > threshold and scene_change(prev_frame, frame):
                filename = f"{uuid.uuid4().hex}.jpg"
                path = os.path.join(UPLOAD_FOLDER, filename)
                cv2.imwrite(path, frame)
                saved_frames.append(path)
                metadata.append({
                    'filename': filename,
                    'clarity': round(clarity, 2),
                    'timestamp': round(timestamp, 2)
                })
                prev_frame = frame  # track for scene change

        frame_index += 1

    cap.release()
    return saved_frames, metadata
