from unicodedata import name
from pydub import AudioSegment
import shutil

def checkfiletype(sound):
    filetype = sound.split(".")[1]
    return filetype

def speed_change(soundsegment, speed):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second

    sound_with_altered_frame_rate = soundsegment._spawn(soundsegment.raw_data, overrides={
         "frame_rate": int(soundsegment.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(soundsegment.frame_rate)

def createaudiosegment(nameforaudiowithoutfiletype,path,speed):
    nameforaudiosegment = AudioSegment.from_wav(path)
    nameforaudiosegment = speed_change(nameforaudiosegment,speed)
    nameforaudiosegment.export(nameforaudiowithoutfiletype + ".wav",format = "wav")
    shutil.move(nameforaudiowithoutfiletype + ".wav", "static/files")