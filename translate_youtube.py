import subprocess
import speech_recognition as sr
import nltk
from nltk.tokenize import sent_tokenize
import os
import yt_dlp as yd

VIDEO_ID = '6Hewb1wlOlo'
# Download the audio from the YouTube video using youtube-dl
video_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yd.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])

download_audio(video_url)

cwd = os.getcwd()
print(f"Current working directory: {cwd}")
print(f"Contents of directory: {os.listdir(cwd)}")

# Convert the audio to text using Google Speech Recognition
r = sr.Recognizer()
audio_file = f"{VIDEO_ID}.mp3"
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)
text = r.recognize_google(audio, language="en-US")

# Tokenize the text into sentences
sentences = sent_tokenize(text)

# Map each sentence to a timestamp in the audio track
timestamps = []
for i, sentence in enumerate(sentences):
    duration = len(sentence)  # Assume 1 character per millisecond
    start_time = sum([len(sentences[j]) for j in range(i)])
    end_time = start_time + duration
    timestamps.append((start_time, end_time))

# Translate the text to Hungarian using Google Translate
from googletrans import Translator
translator = Translator()
hungarian_sentences = [translator.translate(sentence, dest="hu").text for sentence in sentences]

# Generate a new video with Hungarian subtitles using MoviePy
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
video_clip = VideoFileClip(audio_file)
subtitles = [TextClip(sentence, fontsize=24, color="white", bg_color="black").set_start(start).set_duration(duration) 
             for (start, end), sentence, duration in zip(timestamps, hungarian_sentences, video_clip.duration)]
composite_clip = CompositeVideoClip([video_clip, *subtitles])
composite_clip.write_videofile("hungarian_video.mp4")
