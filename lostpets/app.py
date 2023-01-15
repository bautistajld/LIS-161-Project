from flask import Flask, render_template, request, url_for, flash, redirect, session
#Pulls functions from flask to enable certain features
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('lostpets','static', 'uploads')
#Specifies folder for uploads from file form  
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates', static_folder='static')
#Further specifies directories
app.config['SECRET_KEY'] = 'faff28ncn43y3cqn7tcn407q0c7y'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

messages = []
#Empty content

@app.route('/', methods=['GET', 'POST'])
def index(uploaded_img_file_path=None):  
    return render_template('index.html', messages=messages, uploaded_img_file_path=session['uploaded_img_file_path'])
#Uploads are saved to folder but do not show somehow

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
        #Code for file uploading and saving via file form 

        petowner = request.form['petowner']
        petowcontact = request.form['petowcontact']
        #Data is pulled from forms in create.html

        if not petname:
            flash('Name is required!')
        elif not petage:
            flash('Age is required!')
        elif not petdate:
            flash('Date is required!')
        #Only name age and date are supposed to be required
        else:
            
            messages.append({
            'petname': petname, 
            'petage': petage, 
            'petdate':petdate, 
            'petowner':petowner, 
            'petowcontact':petowcontact}) 
            #Edits empty dictionary in the beginning 

            return redirect(url_for('index'))
            #Goes back to index.html with messages edited via url_for

    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)