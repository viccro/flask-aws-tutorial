'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo, UploadFile
from werkzeug.utils import secure_filename
import os
import csv

UPLOAD_FOLDER = '/Users/206790/Documents/OtherStuff/flask-aws-tutorial/data'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'i74zA0NSWhlMTk@EJ@z9'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    fileForm = UploadFile(request.form)
    form1 = EnterDBInfo(request.form) 
    form2 = RetrieveDBInfo(request.form) 

    if request.method == 'POST' and fileForm.validate_on_submit():
        fileContents = fileForm.filePath.data
        filename = secure_filename(fileContents.filename)

        try:
            filePath = os.path.join(application.instance_path, 'photos', filename)
            fileContents.save(filePath, fileContents)
            print(filePath)
            print(fileContents)
            with open(filePath, newline='') as csvfile:
                filereader = csv.DictReader(csvfile)

            for row in filereader:
                print(row)
                db.session.add(row)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=fileForm.filePath.data)

    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:     
            db.session.add(data_entered)
            db.session.commit()        
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data)
        
    if request.method == 'POST' and form2.validate():
        try:   
            num_return = int(form2.numRetrieve.data)
            query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
            for q in query_db:
                print(q.notes)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('results.html', results=query_db, num_return=num_return)                
    
    return render_template('index.html', fileForm=fileForm, form1=form1, form2=form2)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    application.run(host='0.0.0.0')
