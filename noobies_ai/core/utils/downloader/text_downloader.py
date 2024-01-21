from abc import ABC, abstractmethod
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse


class TextDownloader(ABC):
    @abstractmethod
    def download_text(self, url):
        """
        Abstract method to download text from a given URL.
        """
        pass


class BlogDownloader(TextDownloader):
    def download_text(self, url):
        """
        Downloads text from a blog URL using WebBaseLoader.

        Args:
            url (str): The URL of the blog.

        Returns:
            tuple: A tuple containing the downloaded text and a success message.
                   If an error occurs, returns None and an error message.
        """
        try:
            loader = WebBaseLoader(url)
            text = loader.load()
            text = text[0].page_content
            return text, "Blog downloaded successfully"
        except Exception as e:
            return None, f"An error occurred while downloading blog: {e}"

    def clean_text(self, text):
        """
        Cleans the given text by replacing newlines and tabs with spaces.

        Args:
            text (str): The text to be cleaned.

        Returns:
            str: The cleaned text.
        """
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = text.replace("  ", " ")
        return text


class YouTubeTranscriptDownloader(TextDownloader):
    def video_id(self, value):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        - https://www.youtube.com/shorts/0kIhwa1e_5M
        ParseResult(scheme='https', netloc='www.youtube.com', path='/shorts/0kIhwa1e_5M', params='', query='', fragment='')
        """
        query = urlparse.urlparse(value)
        print(query)
        if query.hostname == "youtu.be":
            return query.path[1:]
        if query.hostname in ("www.youtube.com", "youtube.com"):
            if query.path == "/watch":
                p = urlparse.parse_qs(query.query)
                return p["v"][0]
            if query.path[:7] == "/embed/":
                return query.path.split("/")[2]
            if query.path[:3] == "/v/":
                return query.path.split("/")[2]
            if query.path.startswith("/shorts/"):
                return query.path.split("/")[2]
        # fail?
        return None

    def download_text(
        self, url, add_video_info=False, language=["en"], translation=None
    ):
        """
        Downloads the transcript from a YouTube video URL using YoutubeLoader.

        Args:
            url (str): The URL of the YouTube video.
            add_video_info (bool, optional): Whether to include video information in the transcript. Defaults to False.
            language (list, optional): List of languages to include in the transcript. Defaults to ["en"].
            translation (str, optional): Language code for translation. Defaults to None.

        Returns:
            tuple: A tuple containing the downloaded transcript text and a success message.
                   If an error occurs, returns None and an error message.
        """
        try:
            print(url)
            video_id = self.video_id(url)
            print("video_id", video_id)
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            print(transcript_list)
            transcript = transcript_list.find_generated_transcript(["en"])
            transcript_text = ""
            try:
                for line in transcript.fetch():
                    transcript_text += (line.get("text")) + " "
            except Exception as e:
                print(e)
                return None, f"An error occurred while downloading transcript: {e}"
            return transcript_text, "Transcript downloaded successfully"
        except Exception as e:
            print(e)
            return None, f"An error occurred while downloading transcript: {e}"


if __name__ == "__main__":
    youtube = YouTubeTranscriptDownloader()
    text, msg = youtube.download_text("https://www.youtube.com/watch?v=IN4Gftz6_ZM")
    print(text)
