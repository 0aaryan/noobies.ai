import json
from .utils.AI.imageAI import ImageAI
from .utils.AI.textAI import TextAI
from .utils.AI.prompt.video_prompt import GENERATE_VIDEO_FROM_TOPIC
from .utils.AI.syntax.video_syntax import SHORT_VIDEO_WITH_IMAGES
from .utils.AI.audioAI import AudioAI
import os
from .utils.converter.video_converter import VideoConverter

# import print error


class VideoGenerator:
    def __init__(
        self,
        model_id="gpt-4-turbo",
        prompt=GENERATE_VIDEO_FROM_TOPIC,
        syntax=SHORT_VIDEO_WITH_IMAGES,
    ):
        """
        Initializes the VideoGenerator class.

        Args:
            model_id (str, optional): The ID of the language model to be used. Defaults to "gpt-4-turbo".
            prompt (str, optional): The prompt for generating the video script. Defaults to GENERATE_VIDEO_FROM_TOPIC.
            syntax (str, optional): The syntax for generating the video script. Defaults to SHORT_VIDEO_WITH_IMAGES.
        """
        self.model_id = model_id
        self.prompt = prompt
        self.syntax = syntax
        self.languages = ["en", "hi"]

    def get_languages(self):
        """
        Returns the supported languages.

        Returns:
            list: List of supported languages.
        """
        return self.languages

    def get_voice_ids(self):
        """
        Returns the available voice IDs.

        Returns:
            dict: Dictionary of voice IDs.
        """
        audio_ai = AudioAI()
        return audio_ai.get_voice_ids()

    def get_font_list(self):
        """
        Returns the available fonts.

        Returns:
            list: List of available fonts.
        """
        video_converter = VideoConverter()
        return video_converter.get_font_list()

    def generate_script(
        self,
        topic,
        duration="30s",
        tone="casual",
        language="en",
        instructions="",
        num_of_images=5,
    ):
        """
        Generates the video script.

        Args:
            topic (str): The topic of the video.
            duration (str, optional): The duration of the video. Defaults to "30s".
            tone (str, optional): The tone of the video script. Defaults to "casual".
            language (str, optional): The language of the video script. Defaults to "en".
            instructions (str, optional): Additional instructions for generating the script. Defaults to "".
            num_of_images (int, optional): The number of images to be included in the video. Defaults to 5.

        Returns:
            dict: The generated video script.
        """
        try:
            if self.model_id is None:
                text_ai = TextAI()
            else:
                text_ai = TextAI(model_id=self.model_id)
            print("Generating script...")
            generated_script = text_ai.predict(
                self.prompt,
                topic=topic,
                duration=duration,
                tone=tone,
                language=language,
                instructions=instructions,
                num_of_images=num_of_images,
                syntax=self.syntax,
            )
            print(generated_script)

            try:
                generated_script = generated_script.replace("```json", "")
                generated_script = generated_script.replace("```", "")
            except Exception as e:
                raise Exception(
                    "Error occurred while removing json code block: " + str(e)
                )

            generated_script = json.loads(generated_script)
            video_title = generated_script["video_title"]
            video_description = generated_script["video_description"]
            video_script_json = json.dumps(generated_script["scripts"])
            script_parts = []
            image_prompts = []

            for key, script in generated_script["scripts"].items():
                script_parts.append(script["text"])
                image_prompts.append(script["image"])

            video_script = {
                "video_title": video_title,
                "video_description": video_description,
                "video_script": video_script_json,
                "script_parts": script_parts,
                "image_prompts": image_prompts,
            }
            print(video_script)

            return video_script
        except Exception as e:
            print(e)
            return None

    def generate_audio(
        self,
        script_parts=[],
        output_file="audio.wav",
        language="en",
        voice_id=None,
    ):
        """
        Generates the audio for the video.

        Args:
            script_parts (list, optional): List of script parts. Defaults to [].
            output_file (str, optional): The output file path for the audio. Defaults to "audio.wav".
            language (str, optional): The language of the audio. Defaults to "en".
            voice_id (str, optional): The voice ID for the audio. Defaults to None.
        """
        audio_ai = AudioAI()
        script = ". ".join(script_parts)
        if voice_id is None:
            voice_id = list(audio_ai.get_voice_ids().values())[0]
        audio_options = {
            "voice": voice_id,
            "speed": "1.0",
            "language": language,
        }
        audio_ai.generate(
            prompt=script,
            inference_params=audio_options,
            output_file=output_file,
        )

        print(script)

    def generate_images(self, image_prompts=[], image_path="images"):
        try:
            image_ai = ImageAI()
            image_paths = []
            for i, prompt in enumerate(image_prompts):
                path = os.path.join(image_path, f"{i}.png")
                path = os.path.abspath(path)
                try:
                    image_ai.generate(
                        prompt=prompt,
                        inference_params={
                            "quality": "standard",
                            "size": "1024x1024",
                        },
                        output_file=path,
                    )
                    image_paths.append(path)
                except Exception as e:
                    print(f"Error generating image: {e}")
                    continue
            return image_paths
        except Exception as e:
            print(e)
            return None

    def generate_subtiles(self, audio_path, word_timestamps=True):
        audio_ai = AudioAI()
        subs = audio_ai.get_transcription(audio_path, word_timestamps)
        print(subs)
        return subs

    def generate_video(
        self,
        video_dir,
        output_file="video.mp4",
        subtitle_options={
            "font_color": "yellow",
            "font_size": 60,
            "font": "liberation-sans",
        },
    ):
        """
        Generates the video.

        Args:
            video_dir (str): The directory containing the video files.
        """
        try:
            video_converter = VideoConverter()
            audio_path = os.path.join(video_dir, "voice.mp3")
            subtitles = self.generate_subtiles(audio_path)
            video_path = video_converter.create_video(
                video_dir, subtitles, subtitle_options=subtitle_options
            )

            return video_path
        except Exception as e:
            print(e)
            return None
