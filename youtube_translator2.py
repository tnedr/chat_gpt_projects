import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from pytube import YouTube
import time
from translate import Translator


def get_video_info(video_url):
    try:
        yt = YouTube(video_url)
        video_info = {
            'id': yt.video_id,
            'title': yt.title,
            'thumbnail_url': yt.thumbnail_url,
            'length': yt.length,
            'views': yt.views,
            'rating': yt.rating,
        }
        return video_info
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None


def export_subtitles_to_indexed_srt(subtitles, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, subtitle in enumerate(subtitles):
            f.write(f"{i + 1}\n")
            f.write(f"{subtitle['text']}\n")
            f.write("\n")


def get_subtitles(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        subtitles = transcript.fetch()
        export_subtitles_to_srt(subtitles, 'subtitles.srt')
        export_subtitles_to_indexed_srt(subtitles, 'subtitles_reduced.srt')

        return subtitles
    except Exception as e:
        print(f"Error fetching subtitles: {e}")
        return None

def export_subtitles_to_srt(subtitles, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, subtitle in enumerate(subtitles):
            f.write(f"{i + 1}\n")
            start_time = format_timestamp(subtitle['start'])
            end_time = format_timestamp(subtitle['start'] + subtitle['duration'])
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{subtitle['text']}\n\n")

def format_timestamp(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def translate_subtitles(subtitles, target_language='hu'):
    translator = Translator(to_lang=target_language)
    translated_subtitles = []

    for i, subtitle in enumerate(subtitles):
        try:
            translated_text = translator.translate(subtitle['text'])
            translated_subtitles.append({
                'start': subtitle['start'],
                'duration': subtitle['duration'],
                'text': translated_text,
            })
            print(f"Translated subtitle {i + 1}/{len(subtitles)}")
        except Exception as e:
            print(f"Error translating subtitle {i + 1}/{len(subtitles)}: {e}")

    return translated_subtitles

if __name__ == "__main__":


    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    video_url = 'https://www.youtube.com/watch?v=cab-58TyBd0'
    video_url = 'https://www.youtube.com/watch?v=tV1dN20e_vY'
    video_url = 'https://www.youtube.com/watch?v=pHCb3bpBxW0'
    video_info = get_video_info(video_url)

    if video_info is not None:
        video_id = video_info['id']
        print(video_id)
        subtitles = get_subtitles(video_id)
        print(subtitles)
        if subtitles:
            translated_subtitles = translate_subtitles(subtitles)
            print(translated_subtitles)
            for subtitle in translated_subtitles:
                print(f"{subtitle['start']:.2f} - {subtitle['text']}")
        else:
            print("No subtitles found.")
    else:
        print("Video information could not be retrieved.")
