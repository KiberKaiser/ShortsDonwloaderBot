import requests
from bs4 import BeautifulSoup

def download_instagram_reel(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video')
        
        if video_tag and 'src' in video_tag.attrs:
            video_url = video_tag['src']
            return video_url
        else:
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def fetch_and_download_reel(url):
    video_url = download_instagram_reel(url)
    if video_url:
        # Logic to download the video from video_url
        # This can be implemented using requests or any other method
        return video_url
    else:
        return None