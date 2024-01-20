from moviepy.editor import *
import numpy as np
import os


class VideoConverter:
    def __init__(self):
        self.folder_path = None

    def zoom_in_out(self, t):
        """Defines a zoom in and out function based on a sin wave"""
        return 1.3 + 0.3 * np.sin(t / 3)

    def get_font_list(self):
        """Returns a list of fonts available on the system"""
        font_list = TextClip.list("font")
        return font_list

    def create_text_clips(self, subtitles, subtitle_options):
        """Creates a list of text clips from a list of subtitles"""
        font_size = subtitle_options.get("font_size", 40)
        font_color = subtitle_options.get("font_color", "yellow")
        font = subtitle_options.get("font", "./static/fonts/Corben-Bold.ttf")
        stroke_width = subtitle_options.get("stroke_width", 0)
        stroke_color = subtitle_options.get("stroke_color", "black")
        positionX = subtitle_options.get("positionX", "center")
        positionY = subtitle_options.get("positionY", "center")
        clips = []
        for word in subtitles:
            word_text = word["word"]
            word_start = word["start"]
            word_end = word["end"]
            word_duration = word_end - word_start

            clip = TextClip(
                word_text,
                fontsize=font_size,
                color=font_color,
                font=font,
                method="caption",
            )
            clip = clip.set_start(word_start).set_end(word_end)
            print(clip.start, clip.end)
            clip = clip.set_position((positionX, positionY))

            clips.append(clip)

        return clips

    def create_video(
        self,
        folder_path,
        subtitles,
        subtitle_options={},
        output_file="video.mp4",
    ):
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
        # height = 480
        # width = 270
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

        print("adding subtitles")
        text_clips = self.create_text_clips(subtitles, subtitle_options)
        print("adding text clips")
        video_clip = CompositeVideoClip([video_clip] + text_clips)
        print(video_clip.duration)
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
    folder = "/Data/aryanCodes3/noobies.ai/video"
    subtiles = [
        {"word": "Hello", "start": 0, "end": 1},
        {"word": "World", "start": 1, "end": 2},
        {"word": "This", "start": 2, "end": 3},
        {"word": "is", "start": 3, "end": 4},
        {"word": "a", "start": 4, "end": 5},
        {"word": "test", "start": 5, "end": 6},
    ]

    real_subs = [
        {
            "word": " Imagine",
            "start": 0.0,
            "end": 0.42,
            "probability": 0.9495607018470764,
        },
        {"word": " an", "start": 0.42, "end": 0.68, "probability": 0.9909719228744507},
        {
            "word": " intelligence",
            "start": 0.68,
            "end": 1.16,
            "probability": 0.9867811799049377,
        },
        {
            "word": " that",
            "start": 1.16,
            "end": 1.52,
            "probability": 0.9986353516578674,
        },
        {"word": " can", "start": 1.52, "end": 1.68, "probability": 0.9992653727531433},
        {
            "word": " create,",
            "start": 1.68,
            "end": 2.16,
            "probability": 0.9969281554222107,
        },
        {
            "word": " learn,",
            "start": 2.6,
            "end": 3.0,
            "probability": 0.9969039559364319,
        },
        {"word": " and", "start": 3.36, "end": 3.64, "probability": 0.9989809393882751},
        {
            "word": " evolve.",
            "start": 3.64,
            "end": 4.06,
            "probability": 0.9964007139205933,
        },
        {
            "word": " That's",
            "start": 4.66,
            "end": 5.06,
            "probability": 0.9965402781963348,
        },
        {
            "word": " generative",
            "start": 5.06,
            "end": 5.64,
            "probability": 0.8473568260669708,
        },
        {"word": " AI,", "start": 5.64, "end": 6.1, "probability": 0.9672739505767822},
        {"word": " the", "start": 6.72, "end": 6.86, "probability": 0.9965164661407471},
        {
            "word": " artist",
            "start": 6.86,
            "end": 7.24,
            "probability": 0.99111407995224,
        },
        {"word": " and", "start": 7.24, "end": 7.66, "probability": 0.7845732569694519},
        {"word": " the", "start": 7.66, "end": 7.82, "probability": 0.996756374835968},
        {
            "word": " architect",
            "start": 7.82,
            "end": 8.24,
            "probability": 0.9990252256393433,
        },
        {"word": " of", "start": 8.24, "end": 8.54, "probability": 0.997698962688446},
        {"word": " the", "start": 8.54, "end": 8.68, "probability": 0.9914013743400574},
        {
            "word": " digital",
            "start": 8.68,
            "end": 9.06,
            "probability": 0.9732556343078613,
        },
        {"word": " age.", "start": 9.06, "end": 9.5, "probability": 0.9988310933113098},
        {
            "word": " It's",
            "start": 10.02,
            "end": 10.24,
            "probability": 0.9981632232666016,
        },
        {
            "word": " not",
            "start": 10.24,
            "end": 10.38,
            "probability": 0.9991229176521301,
        },
        {
            "word": " just",
            "start": 10.38,
            "end": 10.66,
            "probability": 0.9984221458435059,
        },
        {
            "word": " code.",
            "start": 10.66,
            "end": 11.04,
            "probability": 0.9868582487106323,
        },
        {
            "word": " It's",
            "start": 11.68,
            "end": 11.86,
            "probability": 0.9986642301082611,
        },
        {"word": " a", "start": 11.86, "end": 11.92, "probability": 0.9969289898872375},
        {
            "word": " creative",
            "start": 11.92,
            "end": 12.38,
            "probability": 0.9986819624900818,
        },
        {
            "word": " force,",
            "start": 12.38,
            "end": 12.98,
            "probability": 0.9969018697738647,
        },
        {
            "word": " designing",
            "start": 13.36,
            "end": 13.78,
            "probability": 0.996785044670105,
        },
        {
            "word": " realities",
            "start": 13.78,
            "end": 14.46,
            "probability": 0.9845792055130005,
        },
        {
            "word": " so",
            "start": 14.46,
            "end": 14.88,
            "probability": 0.9432005882263184,
        },
        {
            "word": " vivid,",
            "start": 14.88,
            "end": 15.28,
            "probability": 0.9978920817375183,
        },
        {
            "word": " they",
            "start": 15.7,
            "end": 15.92,
            "probability": 0.9975051283836365,
        },
        {
            "word": " blur",
            "start": 15.92,
            "end": 16.18,
            "probability": 0.9904258847236633,
        },
        {
            "word": " the",
            "start": 16.18,
            "end": 16.42,
            "probability": 0.9981439113616943,
        },
        {
            "word": " lines",
            "start": 16.42,
            "end": 16.74,
            "probability": 0.9973652958869934,
        },
        {
            "word": " between",
            "start": 16.74,
            "end": 17.14,
            "probability": 0.9981424808502197,
        },
        {
            "word": " our",
            "start": 17.14,
            "end": 17.48,
            "probability": 0.9941266775131226,
        },
        {
            "word": " world",
            "start": 17.48,
            "end": 17.88,
            "probability": 0.9993662238121033,
        },
        {
            "word": " and",
            "start": 17.88,
            "end": 18.14,
            "probability": 0.9929147958755493,
        },
        {
            "word": " the",
            "start": 18.14,
            "end": 18.26,
            "probability": 0.9977834820747375,
        },
        {
            "word": " virtual.",
            "start": 18.26,
            "end": 18.68,
            "probability": 0.9944720268249512,
        },
        {
            "word": " And",
            "start": 19.34,
            "end": 19.56,
            "probability": 0.9890609979629517,
        },
        {
            "word": " as",
            "start": 19.56,
            "end": 19.74,
            "probability": 0.9629661440849304,
        },
        {
            "word": " it",
            "start": 19.74,
            "end": 19.88,
            "probability": 0.9993637204170227,
        },
        {
            "word": " learns",
            "start": 19.88,
            "end": 20.14,
            "probability": 0.9955398440361023,
        },
        {"word": " at", "start": 20.14, "end": 20.44, "probability": 0.800445556640625},
        {"word": " an", "start": 20.44, "end": 20.6, "probability": 0.9963018894195557},
        {
            "word": " unnerving",
            "start": 20.6,
            "end": 21.1,
            "probability": 0.9803441365559896,
        },
        {
            "word": " speed,",
            "start": 21.1,
            "end": 21.56,
            "probability": 0.9980301260948181,
        },
        {
            "word": " one",
            "start": 21.94,
            "end": 22.14,
            "probability": 0.9932966828346252,
        },
        {
            "word": " question",
            "start": 22.14,
            "end": 22.6,
            "probability": 0.9939630627632141,
        },
        {
            "word": " looms.",
            "start": 22.6,
            "end": 23.1,
            "probability": 0.9829591512680054,
        },
        {
            "word": " Are",
            "start": 23.66,
            "end": 23.76,
            "probability": 0.9181776642799377,
        },
        {
            "word": " we",
            "start": 23.76,
            "end": 23.94,
            "probability": 0.9989944100379944,
        },
        {
            "word": " in",
            "start": 23.94,
            "end": 24.04,
            "probability": 0.9989493489265442,
        },
        {
            "word": " control?",
            "start": 24.04,
            "end": 24.38,
            "probability": 0.9993775486946106,
        },
        {
            "word": " Or",
            "start": 24.94,
            "end": 25.06,
            "probability": 0.9858685731887817,
        },
        {
            "word": " are",
            "start": 25.06,
            "end": 25.26,
            "probability": 0.9755246639251709,
        },
        {
            "word": " we",
            "start": 25.26,
            "end": 25.42,
            "probability": 0.9894877672195435,
        },
        {
            "word": " the",
            "start": 25.42,
            "end": 25.52,
            "probability": 0.9949535727500916,
        },
        {
            "word": " ones",
            "start": 25.52,
            "end": 25.74,
            "probability": 0.998132050037384,
        },
        {
            "word": " being",
            "start": 25.74,
            "end": 26.04,
            "probability": 0.9990202188491821,
        },
        {
            "word": " reprogrammed?",
            "start": 26.04,
            "end": 27.02,
            "probability": 0.9919383327166239,
        },
    ]

    subtitle_option = {
        "font": "liberation-sans",
    }

    video_converter.create_video(
        "/Data/aryanCodes3/noobies.ai/video",
        subtitles=real_subs,
    )
