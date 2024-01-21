from clarifai.client.model import Model


from clarifai.client.model import Model


class AudioAI:
    def __init__(
        self,
        model_url="https://clarifai.com/eleven-labs/audio-generation/models/speech-synthesis",
    ):
        """
        Initializes the AudioAI class.

        Args:
            model_url (str): URL of the audio generation model (default: "https://clarifai.com/eleven-labs/audio-generation/models/speech-synthesis").
        """
        self.model_url = model_url
        self.llm = Model(
            model_url,
        )
        self.voice_ids = {
            "male1": "2EiwWnXFnvU5JabPnv8n",
            "female1": "LcfcDJNUP1GQjkzn1xUU",
        }

    def generate(
        self,
        prompt,
        inference_params={
            "voice-id": "2EiwWnXFnvU5JabPnv8n",
            "model_id": "eleven_multilingual_v2",
            "stability": 0.5,
            "similarity_boost": 0.5,
            "style": 0,
            "use_speaker_boost": True,
            "language": "hi",
        },
        output_file="audio.wav",
    ):
        """
        Generate an audio file based on the given prompt.

        Args:
            prompt (str): The prompt for generating the audio.
            inference_params (dict): Inference parameters for the audio generation (default: {"voice-id": "2EiwWnXFnvU5JabPnv8n", "model_id": "eleven_multilingual_v2", "stability": 0.5, "similarity_boost": 0.5, "style": 0, "use_speaker_boost": True, "language": "hi"}).
            output_file (str): The output file path for saving the generated audio (default: "audio.wav").

        Returns:
            bool: True if the audio generation is successful, False otherwise.
        """
        try:
            prediction = self.llm.predict_by_bytes(
                prompt.encode(), input_type="text", inference_params=inference_params
            )
            output_base64 = prediction.outputs[0].data.audio.base64
            with open(output_file, "wb") as f:
                f.write(output_base64)
            return True
        except Exception as e:
            print(e)
            return False

    def get_voice_ids(self):
        """
        Get the available voice IDs.

        Returns:
            dict: A dictionary containing the available voice IDs.
        """
        return self.voice_ids

    def get_transcription(self, audio_path, word_timestamps=True):
        """
        Get the transcription of an audio file.

        Args:
            audio_path (str): The path to the audio file.
            word_timestamps (bool): Whether to include word timestamps in the transcription (default: True).

        Returns:
            list: A list of words in the transcription.
        """
        import whisper

        model = whisper.load_model("base.en")
        result = model.transcribe(audio_path, word_timestamps=word_timestamps)
        words = []
        for res in result["segments"]:
            words.extend(res["words"])
        return words


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    audio_ai = AudioAI()
    audio_ai.generate(
        prompt="weather is very good today. let's go to the beach",
        output_file="audio.wav",
    )

    transcript = audio_ai.get_transcription("/Data/aryanCodes3/noobies.ai/voice.mp3")
    for word in transcript:
        print(word["word"], word["start"], word["end"])
