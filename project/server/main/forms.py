# project/server/main/forms.py


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    file1 = FileField('inputFile1',
        validators=[
            FileRequired(),
            FileAllowed(['csv', 'CSV only!'])
        ])
    file2 = FileField('inputFile2',
        validators=[
            FileRequired(),
            FileAllowed(['csv', 'CSV only!'])
        ])
