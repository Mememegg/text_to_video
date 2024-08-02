from flask import Flask, request, jsonify
from moviepy.editor import *
import requests
from gtts import gTTS
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your API keys
PEXELS_API_KEY = '7a1QSeN2vQqje97Tij77Gbwh6lmAgyhiTlzrxmTYIJgKe0TFWyXP33Wm'
OPENAI_API_KEY = 'sk-proj-QsvcUFIhi6mRx08RMqLHT3BlbkFJsj23VsJOYwDCNPFO3ht3'

# Fetch media from Pexels
def fetch_media(query):
    url = f'https://api.pexels.com/videos/search?query={query}&per_page=1'
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        video_url = response.json()['videos'][0]['video_files'][0]['link']
        return video_url
    else:
        return None

# Generate text-to-speech
def text_to_speech(text, filename='voice.mp3'):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# Generate video
def generate_video(text, output_file='output.mp4'):
    # Fetch a video snippet from Pexels
    video_url = fetch_media('nature')
    if not video_url:
        return None

    # Download the video snippet
    video_filename = 'snippet.mp4'
    video_response = requests.get(video_url)
    with open(video_filename, 'wb') as f:
        f.write(video_response.content)

    # Generate audio from text
    audio_filename = text_to_speech(text)

    # Load video and audio
    video_clip = VideoFileClip(video_filename)
    audio_clip = AudioFileClip(audio_filename)

    # Set audio to video
    final_clip = video_clip.set_audio(audio_clip)

    # Write the final video file
    final_clip.write_videofile(output_file, codec='libx264', fps=24)

    # Cleanup
    os.remove(video_filename)
    os.remove(audio_filename)

    return output_file

@app.route('/generate_video', methods=['POST'])
def generate_video_endpoint():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    output_file = generate_video(text)
    if not output_file:
        return jsonify({"error": "Failed to generate video"}), 500

    return jsonify({"message": "Video generated successfully!", "video_path": output_file})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
