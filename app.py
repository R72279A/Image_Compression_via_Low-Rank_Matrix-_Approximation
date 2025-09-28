from flask import Flask, request, render_template, jsonify
import numpy as np
from PIL import Image
import io
import base64
from Backend.main import compress_image

# Initialize the Flask application with CORRECT paths
app = Flask(__name__, template_folder='Front_end/Templates', static_folder='Front_end/Static')

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('Index.html')

@app.route('/compress', methods=['POST'])
def handle_compression():
    """Handles the image compression request."""
    
    try:
        # Get the data from the request
        image_file = request.files.get('image')
        k = int(request.form.get('k', 50))
        
        if not image_file:
            return jsonify({'error': 'No image file provided'}), 400
        
        # Prepare the image for compression
        image = Image.open(image_file.stream)
        grayscale_image = image.convert('L')
        image_matrix = np.array(grayscale_image)
        normalized_image_matrix = image_matrix / 255.0
        
        # Ensure k is within valid bounds
        m, n = normalized_image_matrix.shape
        k = max(1, min(k, min(m, n)))
        
        # Call the compression function
        compressed_matrix = compress_image(normalized_image_matrix, k)
        
        # Convert back to image
        unnormalized_matrix = np.clip(compressed_matrix * 255, 0, 255)
        image_array = unnormalized_matrix.astype(np.uint8)
        compressed_pil_image = Image.fromarray(image_array)
        
        # Encode as Base64
        buffered = io.BytesIO()
        compressed_pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        compressed_size_kb = (len(img_str) * 3 / 4) / 1024
        
        return jsonify({
            'image_data': f'data:image/png;base64,{img_str}',
            'compressed_size_kb': round(compressed_size_kb, 2)
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask Application...")
    print("🌐 Available at: http://127.0.0.1:5000")
    app.run(debug=True)
