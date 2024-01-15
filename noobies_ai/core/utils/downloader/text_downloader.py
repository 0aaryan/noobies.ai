from abc import ABC, abstractmethod
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader


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
            loader = YoutubeLoader.from_youtube_url(
                url,
                add_video_info=add_video_info,
                language=language,
                translation=translation,
            )
            transcript = loader.load()
            text = " ".join([t["text"] for t in transcript])
            return text, "YouTube transcript downloaded successfully"
        except Exception as e:
            return None, f"An error occurred while downloading YouTube transcript: {e}"


if __name__ == "__main__":
    # Test BlogDownloader
    blog_downloader = BlogDownloader()
    text, msg = blog_downloader.download_text(
        "https://www.ndtv.com/offbeat/parle-g-replaces-iconic-girls-image-with-this-instagram-influencers-face-heres-why-4753827"
    )
    print(text, msg)
