from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Clarifai
import os
import json
from langchain_core.output_parsers import StrOutputParser


class TextAI:
    def __init__(
        self,
        user_id="openai",
        app_id="chat-completion",
        model_id="GPT-3_5-turbo",
        model_version_id="5d7a50b44aec4a01a9c492c5a5fcf387",
    ):
        self.user_id = user_id
        self.app_id = app_id
        self.model_id = model_id
        self.model_version_id = model_version_id
        self.llm = Clarifai(
            user_id=self.user_id,
            app_id=self.app_id,
            model_id=self.model_id,
        )

    def predict(self, prompt_template, **kwargs):
        prompt = PromptTemplate(
            template=prompt_template["template"],
            input_variables=prompt_template["input_variables"],
        )
        input_variables = prompt_template["input_variables"]
        inputs = {}
        for variable in input_variables:
            inputs[variable] = kwargs[variable]

        chain = prompt | llm | StrOutputParser()
        blog_text = chain.invoke(inputs)
        # save response in text file

        # remove json code block from markdown response
        blog_text = blog_text.replace("```json", "")
        blog_text = blog_text.replace("```", "")

        with open("response.txt", "w") as f:
            f.write(blog_text)

        # save response in json file
        with open("response.json", "w") as f:
            json.dump(json.loads(blog_text), f, indent=4)

        return json.loads(blog_text)


if __name__ == "__main__":
    from prompt.text_prompt import GENERATE_BLOG_FROM_BLOG
    from syntax.blog_syntax import HUGO
    import datetime
    from dotenv import load_dotenv

    load_dotenv()
    text_ai = TextAI()
    print(
        text_ai.predict(
            GENERATE_BLOG_FROM_BLOG,
            topic="How to write a blog post",
            syntax=HUGO,
            date=datetime.datetime.now().strftime("%Y-%m-%d"),
        )
    )
