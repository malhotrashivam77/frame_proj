from flask import Flask, render_template, request, send_file
import os
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['photo']
    if file.filename == '':
        return 'No file selected', 400

    # Save the uploaded file
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.png')
    file.save(filename)
    return {'status': 'success', 'filename': 'temp.png'}

@app.route('/download', methods=['POST'])
def download():
    # Get the canvas data URL from the request
    image_data = request.json['imageData']
    # Remove the data URL prefix
    image_data = image_data.split(',')[1]
    
    # Convert base64 to image
    import base64
    img_data = base64.b64decode(image_data)
    
    # Create a response with the image
    return send_file(
        io.BytesIO(img_data),
        mimetype='image/png',
        as_attachment=True,
        download_name='framed_photo.png'
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

