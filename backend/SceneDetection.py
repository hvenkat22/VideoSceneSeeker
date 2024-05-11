import cv2
import numpy as np
import requests

# Function to generate caption for an image using OpenAI API
def generate_caption(image):
    url = "https://open-ai21.p.rapidapi.com/imagecaptioning"
    files = {'file': image}
    headers = {
        "X-RapidAPI-Key": "XXXXXXXXXXXXXXX",
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }
    response = requests.post(url, files=files, headers=headers)
    return response.json()

# Function to perform motion detection using background subtraction
def detect_motion(prev_frame, frame):
    # Convert frames to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Compute absolute difference between current and previous frame
    frame_diff = cv2.absdiff(prev_gray, gray)
    
    # Apply thresholding to get binary mask of regions with significant differences
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    
    # Count non-zero pixels in the thresholded image
    motion_pixels = cv2.countNonZero(thresh)
    
    # Calculate percentage of motion in the frame
    total_pixels = thresh.shape[0] * thresh.shape[1]
    motion_percentage = (motion_pixels / total_pixels) * 100
    
    return motion_percentage

# Function to process video and collect summaries from frames
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    summaries = []
    prev_frame = None
    framenum=0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Skip first frame
        if prev_frame is None:
            prev_frame = frame
            continue
        
        # Detect motion in the frame
        motion_percentage = detect_motion(prev_frame, frame)
        
        # If motion percentage is above a threshold, generate summary for the frame
        if motion_percentage > 5:  # Adjust the threshold as needed
            framenum+=1
            
            # Convert frame to byte array
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            
            # Generate caption for the frame
            caption = generate_caption(img_bytes)
            print(f"Frame Number {framenum}'s caption: {caption}")
            summaries.append(caption['result'])
        
        prev_frame = frame
        
    cap.release()
    cv2.destroyAllWindows()

    return summaries

# Example usage
video_path = '../MilletAdvertisementVideo.mp4'
summaries = process_video(video_path)
print(summaries)
