from flask import Flask, render_template, url_for, g, request, redirect, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

DATABASE = r'.\Land_Scapes.db'
DEBUG = True
SECRET_KEY = '123456'
MAX_CONTENT_LENGTH = 1024 * 1024
UPLOAD_FOLDER = r'.\static\images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/Land_Scapes', methods=['GET', 'POST'])
def Land_Scapes():
    images = os.listdir(os.path.join(app.static_folder, "images"))
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("landscapes.html", images=images)


@app.teardown_appcontext
def close_databse(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/Land_Scapes')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)
