from abc import ABC, abstractmethod
from pytube import YouTube
import instaloader


class VideoDownloader(ABC):
    @abstractmethod
    def download_video(self, url, download_path):
        pass


class YouTubeDownloader(VideoDownloader):
    """
    A class that provides functionality to download YouTube videos.
    """

    def download_video(self, url, download_path, **kwargs):
        resolution = kwargs.get("resolution", "highest")
        try:
            yt = YouTube(url)
            if resolution == "highest":
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.filter(res=resolution).first()
                if stream is None:
                    return f"No stream available at resolution: {resolution}."
            try:
                stream.download(download_path)
                return "YouTube video downloaded successfully"
            except OSError as e:
                return f"An error occurred while accessing the file system: {e}"
        except Exception as e:
            return f"An error occurred while downloading YouTube video: {e}"


class InstagramDownloader(VideoDownloader):
    def download_video(self, url, download_path):
        try:
            L = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
            try:
                L.download_post(post, target=download_path)
                return "Instagram video downloaded successfully"
            except OSError as e:
                return f"An error occurred while accessing the file system: {e}"
        except Exception as e:
            return f"An error occurred while downloading Instagram video: {e}"


if __name__ == "__main__":
    # Test YouTubeDownloader
    youtube_downloader = YouTubeDownloader()
    print(
        youtube_downloader.download_video(
            "https://www.youtube.com/watch?v=9bZkp7q19f0", "downloads"
        )
    )
