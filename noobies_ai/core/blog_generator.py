from utils import *
from utils.downloader.text_downloader import BlogDownloader
from utils.AI.textAI import TextAI
from utils.AI.prompt.text_prompt import GENERATE_BLOG_FROM_BLOG
from utils.AI.syntax.blog_syntax import HUGO
from datetime import date


class BlogGenerator:
    def __init__(self, model_id=None, prompt=GENERATE_BLOG_FROM_BLOG, syntax=HUGO):
        self.model_id = model_id
        self.prompt = prompt
        self.syntax = syntax

    def blog_to_blog(
        self,
        url,
        generate_ai_image=False,
        summary=False,
        instructions="",
    ):
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


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    url = "https://economictimes.indiatimes.com/industry/renewables/tesla-gets-a-94-billion-reality-check-as-ev-winter-sets-in/articleshow/106817487.cms"

    blog_generator = BlogGenerator(model_id="gpt-4-turbo")
    generated_blog = blog_generator.blog_to_blog(url)

    print(generated_blog)
