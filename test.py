from static.scripts.speedchange import checkfiletype, speed_change,createaudiosegment
from pydub import AudioSegment
import shutil

sound = checkfiletype("audio.wav")

if checkfiletype("audio.wav") == "wav":
    print("the file type is a wav file")

createaudiosegment("spedupaudio", "static\\files\\audio.wav",speed=1.5)