from flask import Flask, request, jsonify
from flask_cors import CORS
from bedrock_client import get_financial_advice

app = Flask(__name__)
CORS(app)

@app.route('/api/advice', methods=['POST'])
def get_advice():
    data = request.json
    question = data.get('question', '')
    
    try:
        answer = get_financial_advice(question)
        return jsonify({'success': True, 'answer': answer})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)