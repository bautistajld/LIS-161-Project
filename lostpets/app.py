from flask import Flask, render_template, request, url_for, flash, redirect, session
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('messages','static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'faff28ncn43y3cqn7tcn407q0c7y'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

messages = []

@app.route('/', methods=['GET', 'POST'])
def index(uploaded_img_file_path=None):  
    return render_template('index.html', messages=messages, uploaded_img_file_path=session['uploaded_img_file_path'])

# DIVIDER

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        petname = request.form['petname']
        petage = request.form['petage']
        petdate = request.form['petdate']

        uploaded_img = request.files['uploaded-file']
        img_filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        
        petowner = request.form['petowner']
        petowcontact = request.form['petowcontact']

        if not petname:
            flash('Name is required!')
        elif not petage:
            flash('Age is required!')
        elif not petdate:
            flash('Date is required!')
        else:
            
            messages.append({
            'petname': petname, 
            'petage': petage, 
            'petdate':petdate, 
            'petowner':petowner, 
            'petowcontact':petowcontact}) 

            return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)