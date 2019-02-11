from flask_wtf.file import FileField, FileRequired
from flask.ext.wtf import Form
from wtforms import TextField, validators

class UploadFile(Form):
    filePath = FileField(label="Add CSV here", description="db_upload", validators=[FileRequired(message="A file must be selected.")])

class EnterDBInfo(Form):
    dbNotes = TextField(label='Items to add to DB', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])    

class RetrieveDBInfo(Form):
    numRetrieve = TextField(label='Number of DB Items to Get', description="db_get", validators=[validators.required(), validators.Regexp('^\d{1}$',message=u'Enter a number between 1 and 10')])
