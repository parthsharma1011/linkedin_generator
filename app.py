from flask import Flask, request, jsonify
from linkedin_generator import LinkedInPostGenerator
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "LinkedIn Post Generator API", "version": "1.0"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('topic')
        tone = data.get('tone', 'professional')
        post_type = data.get('post_type', 'thought-leader')
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        generator = LinkedInPostGenerator()
        result = generator.generate_post(topic, tone, post_type)
        
        if result:
            return jsonify(result)
        return jsonify({"error": "Failed to generate post"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
