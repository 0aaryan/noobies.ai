from moviepy.editor import *
import numpy as np
import os


class VideoConverter:
    def __init__(self):
        self.folder_path = None

    def zoom_in_out(self, t):
        """Defines a zoom in and out function based on a sin wave"""
        return 1.7 + 0.3 * np.sin(t / 3)

    def create_video(self, folder_path, output_file="video.mp4"):
        """Creates a video from a folder of images and an audio file"""
        self.folder_path = folder_path
        image_folder = os.path.join(self.folder_path, "images")
        image_files = sorted(
            [
                os.path.join(image_folder, img)
                for img in os.listdir(image_folder)
                if img.endswith(".png")
            ]
        )
        audio_file = os.path.join(self.folder_path, "voice.mp3")

        # Check if audio file exists
        if not os.path.exists(audio_file):
            print(f"Audio file {audio_file} does not exist.")
            return

        # Load audio file
        audio = AudioFileClip(audio_file)
        audio_duration = audio.duration

        # Check if audio duration is valid
        if audio_duration is None:
            print("Could not determine audio duration.")
            return

        # Calculate duration for each image
        image_duration = audio_duration / len(image_files)

        clips = []
        height = 1280
        width = 720
        # if width % 2 != 0:
        #     width = width - 1
        # width = int(width)
        print(width, height)
        for i in range(len(image_files)):
            print("processing image", i)
            clip = ImageClip(image_files[i]).set_duration(image_duration)
            clip = clip.resize((width, height))
            clip = clip.resize(self.zoom_in_out)
            clips.append(clip)

        print("concatenating")
        video_clip = concatenate_videoclips(clips, method="compose")
        video_clip = video_clip.set_audio(audio)
        # final_video.write_videofile(output_file, fps=30, threads=8, audio=True, codec='libx264')
        print("writing")
        video_clip.write_videofile(
            os.path.join(self.folder_path, output_file),
            fps=24,
            threads=8,
            audio=True,
            codec="libx264",
            audio_codec="aac",
        )

        return os.path.join(self.folder_path, output_file)


if __name__ == "__main__":
    video_converter = VideoConverter()
    video_converter.create_video("/Data/aryanCodes3/noobies.ai/video")
