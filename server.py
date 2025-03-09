from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Neural Network Model
class Model(nn.Module):
    def __init__(self, in_features=6, h1=8, h2=8, out_features=4):
        super().__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.output = nn.Linear(h2, out_features)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.output(x)
        return x

# Initialize model
model = Model()

@app.route('/analyze_learning_style', methods=['POST', 'OPTIONS'])
def analyze_learning_style():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
        
    try:
        # Get input data from request
        data = request.get_json()
        input_data = data['input_data']
        
        # Convert input to tensor
        x = torch.FloatTensor(input_data)
        
        # Get model prediction
        with torch.no_grad():
            output = model(x)
            
        # Apply softmax to get probabilities
        probabilities = F.softmax(output, dim=0).numpy()
        
        # Get the predicted class (learning style)
        predicted_style = int(np.argmax(probabilities))
        
        return jsonify({
            'learning_style': predicted_style,
            'probabilities': probabilities.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Serve static files from the current directory
    app.static_folder = '.'
    app.static_url_path = ''
    
    # Run the server on port 5500
    app.run(debug=True, port=5500) 