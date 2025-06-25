import requests
from pytube import YouTube

def download_youtube_short(url: str, output_path: str) -> str:
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if video:
            video.download(output_path)
            return f"Downloaded: {video.title}"
        else:
            return "No suitable video stream found."
    except Exception as e:
        return f"An error occurred: {str(e)}"