from flask import Flask, request, jsonify
import openai
import os
import requests

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'sk-proj-QsvcUFIhi6mRx08RMqLHT3BlbkFJsj55VsJOYwDCNPFO3ht3'

# Set up Pexels API key
PEXELS_API_KEY = '7a1QSeN2vQqje97Tij55Gbwh6lmAgyhiTlzrxmTYIJgKe0TFWyXP55Wm'

@app.route('/')
def home():
    return "Welcome to the Video Generation API!"

@app.route('/generate_script', methods=['POST'])
def generate_script():
    data = request.json
    topic = data['topic']
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Write a detailed script about {topic}."}
        ]
    )
    
    script = response['choices'][0]['message']['content']
    return jsonify({'script': script})

@app.route('/fetch_media', methods=['POST'])
def fetch_media():
    data = request.json
    query = data['query']
    
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    
    response = requests.get(
        f'https://api.pexels.com/v1/search?query={query}&per_page=10',
        headers=headers
    )
    
    media = response.json()
    return jsonify(media)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
