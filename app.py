from flask import Flask, request, send_file, render_template
import os
import secrets

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secrets.token_hex(8) + '_' + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        download_url = request.host_url + 'download/' + filename
        return render_template('upload_success.html', download_url=download_url)
    return 'Upload failed'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)