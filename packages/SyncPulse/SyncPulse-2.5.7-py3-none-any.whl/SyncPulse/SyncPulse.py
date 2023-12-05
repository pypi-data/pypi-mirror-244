import sys
import argparse
from docx2pdf import convert
from pdf2docx import Converter
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from gtts import gTTS
from pyfiglet import Figlet
import click
import os

def get_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        elif query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

@click.command()
def intro_cli():
    f = Figlet(font='slant')
    print(f.renderText('Welcome to SyncPulse!'))
    print("\n")
    developer_name = "Devang Vartak"
    github_link = "https://github.com/Devang2304"
    linkedin_link = "https://www.linkedin.com/in/devang230403/"

    print("Developer Information:")
    print("\n")
    print("Developer: ", developer_name)
    click.echo(f"GitHub:     {github_link}")
    click.echo(f"LinkedIn:   {linkedin_link}")


def help():
    print("Usage: SyncPulse conversion_type input_path output_path")
    print("Valid conversion types: docx_to_pdf, pdf_to_docx, download_video, download_transcript, text_to_speech")
    sys.exit(1) 
    
def download_transcript(youtube_url,output_path='subtitles.txt'):
    video_id = get_video_id(youtube_url)
    
    if video_id:
        try:
            srt = YouTubeTranscriptApi.get_transcript(video_id)
            with open(output_path, "w") as f:
                for i in srt:
                    f.write("{}\n".format(i['text']))
            print(f"Transcript downloaded successfully. Saved at: {output_path}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid YouTube URL. Please provide a valid link.")

def docx_to_pdf(input_docx_path, output_pdf_path):
    try:
        convert(input_docx_path, output_pdf_path)
        print(f"Conversion successful. PDF saved at {output_pdf_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def pdf_to_docx(input_pdf_path, output_docx_path):
    cv = Converter(input_pdf_path)
    cv.convert(output_docx_path, start=0, end=None)
    cv.close()
    print(f"Conversion completed. Word document saved at: {output_docx_path}")

def download_video(youtube_url, output_path='.'):
    try:
        yt = YouTube(youtube_url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path)
        print("Video download successful!")

    except Exception as e:
        print(f"Error: {e}")

def text_to_speech(text, output_path='output.mp3'):
    language='en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save(output_path)
    print(f"Text-to-speech conversion successful. Audio saved at: {output_path}")

def main():
    if len(sys.argv) == 1:
        intro_cli()
        sys.exit(1)

    elif len(sys.argv) < 4 or sys.argv[1] not in ['docx_to_pdf', 'pdf_to_docx', 'download_video', 'download_transcript','text_to_speech','help']:
        print("Usage: SyncPulse conversion_type input_path output_path")
        print("Valid conversion types: docx_to_pdf, pdf_to_docx, download_video, download_transcript, text_to_speech")
        sys.exit(1) 

    conversion_type = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    if conversion_type == 'docx_to_pdf':
        docx_to_pdf(input_path, output_path)
    elif conversion_type == 'pdf_to_docx':
        pdf_to_docx(input_path, output_path)
    elif conversion_type == 'download_video':
        download_video(input_path, output_path)
    elif conversion_type == 'download_transcript':
        download_transcript(input_path,output_path)
    elif conversion_type == 'text_to_speech':
        text_to_speech(input_path, output_path)
    elif conversion_type == 'help':
        help()



