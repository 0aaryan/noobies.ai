from utils import *
from utils.downloader.text_downloader import BlogDownloader
from utils.AI.textAI import TextAI
from utils.AI.imageAI import ImageAI
from utils.AI.prompt.text_prompt import GENERATE_BLOG_FROM_BLOG
from utils.AI.syntax.blog_syntax import HUGO
from utils.converter.blog_converter import BlogConverter
from utils.converter.image_converter import ImageConverter
from datetime import date
import os
import json


class BlogGenerator:
    """
    Class responsible for generating blogs.
    """

    def __init__(self, model_id=None, prompt=GENERATE_BLOG_FROM_BLOG, syntax=HUGO):
        """
        Initialize the BlogGenerator class.

        Args:
            model_id (str): The ID of the text AI model to use. Defaults to None.
            prompt (str): The prompt template for generating the blog. Defaults to GENERATE_BLOG_FROM_BLOG.
            syntax (str): The syntax to use for the generated blog. Defaults to HUGO.
        """
        self.model_id = model_id
        self.prompt = prompt
        self.syntax = syntax

    def generate_text(
        self,
        url,
        summary=False,
        instructions="",
    ):
        """
        Generate text for the blog.

        Args:
            url (str): The URL of the blog.
            summary (bool): Whether to include a summary in the generated blog. Defaults to False.
            instructions (str): Additional instructions for the text AI model. Defaults to "".

        Returns:
            str: The generated blog text.
        """
        try:
            blog_downloader = BlogDownloader()
            blog, error = blog_downloader.download_text(url)
            blog = blog_downloader.clean_text(blog)
            if self.model_id is None:
                text_ai = TextAI()
            else:
                text_ai = TextAI(model_id=self.model_id)
            generated_blog = text_ai.predict(
                prompt_template=self.prompt,
                topic=blog,
                instructions=instructions,
                syntax=self.syntax,
                date=date.today().strftime("%B %d, %Y"),
            )
            return generated_blog
        except Exception as e:
            # Handle the exception here
            print(f"Error generating text: {e}")
            return None

    def generate_images(
        self,
        prompts,
        image_path="images",
        infrence_params=None,
    ):
        """
        Generate images for the blog.

        Args:
            prompts (list): List of prompts for generating images.
            image_path (str): The path to save the generated images. Defaults to "images".
            infrence_params (dict): Inference parameters for generating images. Defaults to None.

        Returns:
            bool: True if images are generated successfully, False otherwise.
        """
        try:
            image_converter = ImageConverter()
            if infrence_params is None:
                infrence_params = {
                    "quality": "standard",
                    "size": "512x512",
                }
            for i, prompt in enumerate(prompts):
                image_ai = ImageAI()
                path = os.path.join(image_path, f"{i}.png")
                path = os.path.abspath(path)

                image_ai.generate(
                    prompt=prompt,
                    inference_params=infrence_params,
                    output_file=path,
                )

                image_converter.resize([path])

            return True
        except Exception as e:
            # Handle the exception here
            print(f"Error generating images: {e}")
            return False

    def get_prompts(self, blog_json):
        """
        Get the prompts for generating images from the blog JSON.

        Args:
            blog_json (dict): The JSON data of the blog.

        Returns:
            list: List of prompts for generating images.
        """
        prompts = []
        try:
            title_image = blog_json["title_image"]
            prompts.append(title_image)

            for content in blog_json["content"]:
                prompts.append(content["image"])

            return prompts
        except Exception as e:
            # Handle the exception here
            print(f"Error getting prompts: {e}")
            return []

    def convert_to_markdown(self, blog_dir):
        """
        Convert the blog JSON to markdown format.

        Args:
            blog_dir (str): The directory path of the blog.

        Returns:
            str: The markdown content of the blog.
        """
        try:
            converter = BlogConverter(blog_dir)
            markdown_content = converter.json_to_hugo()
            converter.save_markdown(markdown_content)
            return markdown_content
        except Exception as e:
            # Handle the exception here
            print(f"Error converting to markdown: {e}")
            return None

    def generate_blog(
        self,
        url,
        summary=False,
        instructions="",
        generate_images=False,
        infrence_params=None,
        debug=False,
        base_dir="./",
    ):
        """
        Generate the complete blog.

        Args:
            url (str): The URL of the blog.
            summary (bool): Whether to include a summary in the generated blog. Defaults to False.
            instructions (str): Additional instructions for the text AI model. Defaults to "".
            generate_images (bool): Whether to generate images for the blog. Defaults to False.
            infrence_params (dict): Inference parameters for generating images. Defaults to None.
            debug (bool): Whether to print debug information. Defaults to False.
            base_dir (str): The base directory to save the generated blog. Defaults to "./".

        Returns:
            dict: The generated blog data.
        """
        try:
            if debug:
                print("Generating Blog")
                print(f"URL: {url}")
                print(f"Summary: {summary}")
                print(f"Instructions: {instructions}")
                print(f"Generate Images: {generate_images}")
                print(f"Infrence Params: {infrence_params}")
                print(f"Debug: {debug}")

            blog_generator = BlogGenerator()
            generated_blog = blog_generator.generate_text(
                url,
                summary=summary,
                instructions=instructions,
            )
            if generated_blog is None:
                return None

            blog_title = generated_blog["title"]
            blog_dir = blog_title.replace(" ", "_")

            # remove all special characters keep _
            blog_dir = "".join(
                [char if char.isalnum() or char == "_" else "" for char in blog_dir]
            )
            # lowercase
            blog_dir = blog_dir.lower()

            os.path.join(base_dir, blog_dir)
            os.makedirs(blog_dir, exist_ok=True)
            blog_dir = os.path.abspath(blog_dir)

            # save blog.json
            with open(os.path.join(blog_dir, "blog.json"), "w") as f:
                json.dump(generated_blog, f)

            if debug:
                print(f"Blog Title: {blog_title}")
                print(f"Blog Dir: {blog_dir}")
                print("Generating Images")

            # generate images
            if generate_images:
                prompts = blog_generator.get_prompts(generated_blog)
                success = blog_generator.generate_images(
                    prompts,
                    image_path=blog_dir,
                    infrence_params=infrence_params,
                )
                if not success:
                    return None

            if debug:
                print("Generating Blog Complete")

            # convert to markdown
            markdown_content = blog_generator.convert_to_markdown(blog_dir)
            if markdown_content is None:
                return None

            return generated_blog
        except Exception as e:
            # Handle the exception here
            print(f"Error generating blog: {e}")
            return None


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    url = "https://economictimes.indiatimes.com/tech/newsletters/tech-top-5/invesco-raises-swiggys-valuation-by-9-fmcg-items-a-hit-on-ecommerce-platforms/articleshow/106548171.cms"

    base_dir = "./blogs"
    base_dir = os.path.abspath(base_dir)

    blog_generator = BlogGenerator(model_id="GPT-4")
    blog_generator.generate_blog(
        url,
        summary=False,
        instructions="",
        generate_images=True,
        infrence_params={
            "quality": "standard",
            "size": "1024x1024",
        },
        debug=True,
        base_dir=base_dir,
    )
