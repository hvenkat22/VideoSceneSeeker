from flask import Flask, request, jsonify
import cv2
import numpy as np
import requests
import assemblyai as aai

app = Flask(__name__)

# Set up AssemblyAI API key
aai.settings.api_key = "3d562e41f9c045b591814f2243585398"

# Function to generate caption for an image using OpenAI API
def generate_caption(image):
    url = "https://open-ai21.p.rapidapi.com/imagecaptioning"
    files = {'file': image}
    headers = {
        "X-RapidAPI-Key": "5e80c89a7fmsh2ce45fb89d4b858p15da95jsn525b7230bc83",
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }
    response = requests.post(url, files=files, headers=headers)
    return response.json()

# Function to transcribe audio using AssemblyAI
def transcribe_audio(video_path):
    transcript = aai.Transcriber().transcribe(video_path)
    return transcript

# Function to search for a query in video captions
def search_in_captions(captions, query):
    for caption in captions:
        if query.lower() in caption['text'].lower():
            return caption['timestamp']
    return None

# Function to process video and collect captions from frames
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    captions = []
    prev_frame = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Skip first frame
        if prev_frame is None:
            prev_frame = frame
            continue
        
        # Convert frame to byte array
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        
        # Generate caption for the frame
        caption = generate_caption(img_bytes)
        captions.append(caption['result'])
        
        prev_frame = frame
    
    cap.release()
    cv2.destroyAllWindows()

    return captions

@app.route('/video/search', methods=['POST', 'GET'])
def search_video():
    # Get the search query from the request
    search_query = request.json.get('query', '')

    # Get the video file from the request
    video_file = request.files.get('file')

    # Save the video file temporarily
    video_path = 'temp_video.mp4'
    video_file.save(video_path)

    # Transcribe audio from the video
    transcript = transcribe_audio(video_path)

    # Search for the query in the video captions
    captions = transcript['captions']
    timestamp = search_in_captions(captions, search_query)

    if timestamp:
        return jsonify({'timestamp': timestamp})
    else:
        # Process the video to generate image captions
        captions = process_video(video_path)
        timestamp = search_in_captions(captions, search_query)
        if timestamp:
            return jsonify({'timestamp': timestamp})
        else:
            return jsonify({'message': 'Query not found'})

if __name__ == '__main__':
    app.run(debug=True)
