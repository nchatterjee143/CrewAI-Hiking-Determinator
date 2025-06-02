from langchain_core.tools import tool
from re import search
from youtube_transcript_api import YouTubeTranscriptApi

@tool
def get_transcript(video_url) -> str:
    """Fetch the transcript text from a given YouTube video URL."""

    def get_video_id(url):
        match = search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        return match.group(1) if match else None
    
    video_id = get_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL"
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"

tools = [get_transcript]
