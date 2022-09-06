import os
from pydub import AudioSegment
import shutil

class Audio:
    def __init__(self,baseAudio:str,speed:float,nameForAudio:str):
        self.baseaudio = baseAudio
        self.speed = speed
        self.name = nameForAudio
        self.detectfiletype()
        self.createAudioSegment()

    def detectfiletype(self):
        self.basefiletype = os.path.splitext(self.baseaudio)[1]
        return self.basefiletype
    
    def speedchange(self,soundsegment):
        sound_with_altered_frame_rate = soundsegment._spawn(soundsegment.raw_data, overrides = {
            "frame_rate": int(soundsegment.frame_rate * self.speed)
        })

        return sound_with_altered_frame_rate.set_frame_rate(soundsegment.frame_rate)

    def createAudioSegment(self):
        if self.basefiletype == ".wav":
            nameforaudiosegment = AudioSegment.from_wav(self.baseaudio)
            nameforaudiosegment = self.speedchange(nameforaudiosegment)
            nameforaudiosegment.export(self.name, format = str(os.path.splitext(self.name)[1]).replace(".",""))
            shutil.move(self.name, "static/files")
