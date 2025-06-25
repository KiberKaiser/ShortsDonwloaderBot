def is_valid_url(url):
    return url.startswith(("http://", "https://"))

def extract_video_id(url):
    return url.split("/")[-1] if url else None
def handle_error(error_message):
    print(f"Error: {error_message}")