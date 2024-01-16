from clarifai.client.model import Model

# USER_ID = "stability-ai"

# APP_ID = "stable-diffusion-2"


# Change these to whatever model
class ImageAI:
    def __init__(
        self,
        user_id="openai",
        app_id="dall-e",
        model_id="dall-e-3",
        model_version_id="dc9dcb6ee67543cebc0b9a025861b868",
    ):
        """
        Initializes the ImageAI class.

        Args:
            user_id (str): User ID for the model (default: "openai").
            app_id (str): App ID for the model (default: "dall-e").
            model_id (str): Model ID for the model (default: "dall-e-3").
            model_version_id (str): Model version ID for the model (default: "dc9dcb6ee67543cebc0b9a025861b868").
        """
        self.user_id = user_id
        self.app_id = app_id
        self.model_id = model_id
        self.model_version_id = model_version_id
        self.llm = Model(
            user_id=self.user_id,
            app_id=self.app_id,
            model_id=self.model_id,
        )

    def generate(
        self,
        prompt,
        inference_params={
            "quality": "standard",
            "size": "1024x1024",
        },
        output_file="image.png",
    ):
        """
        Generates an image based on the given prompt.

        Args:
            prompt (str): The prompt for generating the image.
            inference_params (dict): Inference parameters for the model (default: {"quality": "standard", "size": "1024x1024"}).
            output_file (str): Output file name for the generated image (default: "image.png").
        """
        try:
            # Model Predict
            inference_params["bacth_size"] = 1
            model_prediction = self.llm.predict_by_bytes(
                prompt.encode(), input_type="text", inference_params=inference_params
            )

            output_base64 = model_prediction.outputs[0].data.image.base64

            with open(output_file, "wb") as f:
                f.write(output_base64)
        except Exception as e:
            print(f"Error generating image: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    image_ai = ImageAI()
    image_ai.generate(
        prompt="A painting of a cat",
        inference_params={
            "quality": "standard",
            "size": "1024x1024",
        },
        output_file="image.png",
    )
