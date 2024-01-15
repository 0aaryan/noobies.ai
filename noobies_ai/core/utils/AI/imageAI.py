from clarifai.client.model import Model


class ImageAI:
    def __init__(
        self,
        user_id="openai",
        app_id="dall-e",
        model_id="dall-e-3",
        model_version_id="dc9dcb6ee67543cebc0b9a025861b868",
    ):
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
        # Model Predict
        model_prediction = self.llm.predict_by_bytes(
            prompt.encode(), input_type="text", inference_params=inference_params
        )

        output_base64 = model_prediction.outputs[0].data.image.base64

        with open(output_file, "wb") as f:
            f.write(output_base64)


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
