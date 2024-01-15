from abc import ABC, abstractmethod

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader


class TextDownloader(ABC):
    @abstractmethod
    def download_text(self, url):
        pass


class BlogDownloader(TextDownloader):
    def download_text(self, url):
        try:
            loader = WebBaseLoader(url)
            text = loader.load()
            text = text[0].page_content
            return text, "Blog downloaded successfully"
        except Exception as e:
            return None, f"An error occurred while downloading blog: {e}"

    def clean_text(self, text):
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = text.replace("  ", " ")
        return text


class YouTubeTranscriptDownloader(TextDownloader):
    def download_text(
        self, url, add_video_info=False, language=["en"], translation=None
    ):
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
    # Test YouTubeDownloader
    blog_downloader = BlogDownloader()
    text, msg = blog_downloader.download_text(
        "https://www.ndtv.com/offbeat/parle-g-replaces-iconic-girls-image-with-this-instagram-influencers-face-heres-why-4753827"
    )
    print(text, msg)
