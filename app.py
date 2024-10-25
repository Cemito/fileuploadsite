from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'  # Necessary for flashing messages

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file", "error")
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash("File successfully uploaded", "success")
            return redirect(url_for('index'))

    # List all files in the upload folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"File '{filename}' successfully deleted", "success")
    else:
        flash(f"File '{filename}' not found", "error")
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))


if __name__ == '__main__':
    app.run(debug=True)
