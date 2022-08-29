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

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'static/files'

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


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
    except OSError:
        pass
    try:
        os.remove("static/files/sloweddownaudio.wav")
    except OSError:
        pass
    try:
        os.remove("static/files/audio.wav")
    except OSError:
        pass
    return render_template("input.html",form=form )

#work on fixing the file not found issue.

@app.route("/modify")
def modify():

    spedup = AudioSegment.from_wav("./static/files/audio.wav")
    spedup = speed_change(spedup, 1.5)
    spedup.export("spedupaudio.wav", format="wav")
    spedup = "spedupaudio.wav"
    shutil.move("spedupaudio.wav", "static/files")


    sloweddown = AudioSegment.from_wav("./static/files/audio.wav")
    sloweddown = speed_change(sloweddown, 0.75)
    sloweddown.export("sloweddownaudio.wav", format="wav")
    sloweddown = "sloweddownaudio.wav"
    shutil.move("sloweddownaudio.wav", "static/files")

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

