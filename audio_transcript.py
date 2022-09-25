import speech_recognition as sr
from os import path
import os 
import pydub
from pydub import AudioSegment

pydub.AudioSegment.converter = os.getcwd()+ "\\ffmpeg.exe"                    
pydub.AudioSegment.ffprobe   = os.getcwd()+ "\\ffprobe.exe"

def convert_to_wav(src):                                                                         
    dst = "captcha.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

def transcript(src):
    convert_to_wav(src)
    r = sr.Recognizer()

    convert_to_wav(src)
    with sr.AudioFile('captcha.wav') as source:
        audio = r.record(source)

    return r.recognize_google(audio, language='en-US')

if __name__ == "__main__":
    print(transcript('captcha.mp3'))