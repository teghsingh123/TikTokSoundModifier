from unicodedata import name
from pydub import AudioSegment
import shutil
import os

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


class Audio:
    def __init__(self,baseaudio,speed,nameforaudio):
        self.audio = baseaudio
        self.speed = speed
        self.name = nameforaudio
        self.detectfiletype()
        self.createaudiosegment()

    def detectfiletype(self):
        self.filetype = os.path.splitext(self.audio)[1]
        return self.filetype

    def speedchange(self,soundsegment):
            # Manually override the frame_rate. This tells the computer how many
        # samples to play per second

        sound_with_altered_frame_rate = soundsegment._spawn(soundsegment.raw_data, overrides={
         "frame_rate": int(soundsegment.frame_rate * self.speed)
        })
         # convert the sound with altered frame rate to a standard frame rate
        # so that regular playback programs will work right. They often only
        # know how to play audio at standard frame rate (like 44.1k)
        return sound_with_altered_frame_rate.set_frame_rate(soundsegment.frame_rate)

    def createaudiosegment(self):
        if self.filetype == ".wav":
            nameforaudiosegment = AudioSegment.from_wav(self.audio)
            nameforaudiosegment = self.speedchange(nameforaudiosegment)
            nameforaudiosegment.export(self.name,format=str(os.path.splitext(self.name)[1]).replace(".",""))
            shutil.move(self.name, "static\\files")

