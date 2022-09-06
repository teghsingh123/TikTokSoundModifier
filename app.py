from flask import Flask, render_template, redirect,url_for,request,send_file
from pydub import AudioSegment
import os
from time import sleep
import sys
import urllib.request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import shutil

#other scripts
from static.scripts.speedchange import Audio
#from static.scripts.detectfiletype import filetype

app = Flask(__name__)
SECRET_KEY = 'Tegh'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route("/", methods=['GET', 'POST'])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename("audio.wav")))
        return redirect(url_for("modify"))
    try:
        os.remove("static/files/spedupaudio.wav")
        os.remove("static/files/audio.wav")
        os.remove("static/files/sloweddownaudio.wav")
    except OSError:
        pass

    try:
        del(spedupaudio)
        del(sloweddownaudio)
    except NameError:
        pass

    return render_template("input.html",form=form)

#work on fixing the file not found issue.

@app.route("/modify")
def modify():

    spedupaudio = Audio("static\\files\\audio.wav", 1.5, "spedupaudio.wav")
    sloweddownaudio = Audio("static\\files\\audio.wav", 0.5, "sloweddownaudio.wav")

    #createaudiosegment("spedupaudio", "static\\files\\audio.wav",speed=1.5)

    #createaudiosegment("sloweddownaudio", "static\\files\\audio.wav",speed=0.5)

    return render_template("buttons.html")

@app.route("/spedup")
def spedup():
    return render_template("spedup.html")
@app.route('/downloadspedup')
def downloadspedup():
    path = "static/files\spedupaudio.wav"
    return send_file(path, as_attachment=True)



@app.route("/normal")
def normal():
    return render_template("normal.html")
@app.route('/downloadnormal')
def downloadnormal():
    path = "static/files\\audio.wav"
    return send_file(path, as_attachment=True)



@app.route("/sloweddown")
def sloweddown():
    return render_template("sloweddown.html")
@app.route('/downloadsloweddown')
def downloadsloweddown():
    path = "static/files\sloweddownaudio.wav"
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

