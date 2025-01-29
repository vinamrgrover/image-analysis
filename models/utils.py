from pydantic import BaseModel, Field
import json
import os
from dotenv import load_dotenv
import base64
import openai
from urllib.parse import urlparse
from openai.types.chat.chat_completion import ChatCompletion


class ImageAnalysis(BaseModel):
    description: str = Field(description="Short Description of the image")
    objects: list[str] = Field(
        description="All the detected objects in the image"
    )
    colors: list[str] = Field(description="All the colors used in the image")


class ImageDescription(BaseModel):
    description: str = Field(description="A lengthly description of the image")
    tags: list[str] = Field(description="Tags or description about the image")


class ImageSentiment(BaseModel):
    description: str = Field(
        description="Description of the image's sentiment"
    )
    score: int = Field(description="Image's sentiment score out of 100")


class Image:
    def __init__(self, image: str):
        load_dotenv()
        self.base_url = os.getenv("GROQ_BASE_URL")
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("GROQ_MODEL_NAME")
        self.client = openai.Client(
            api_key=self.api_key, base_url=self.base_url
        )
        self.image = image  # can be either a url or path

    def img_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def validate_response(self, response: dict, ImageClass) -> bool:
        try:
            ImageClass(**response)
            return True
        except Exception as e:
            return False

    def is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def generate_response(self, prompt: str) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": self.image,
                            },
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
        )
        return response

    def get_image_analysis(self) -> ImageAnalysis:
        if not self.is_valid_url(self.image):
            base64_string = self.img_to_base64(self.image)

        with open("prompts/analysis_prompt.txt", "r") as file:
            prompt = file.read()
            file.close()

        response = self.generate_response(prompt=prompt)

        object = json.loads(response.choices[0].message.content)
        if self.validate_response(object, ImageAnalysis):
            return ImageAnalysis(**object)
        return None

    def get_image_description(self) -> ImageDescription:
        if not self.is_valid_url(self.image):
            base64_string = self.img_to_base64(self.image)

        with open("prompts/description_prompt.txt", "r") as file:
            prompt = file.read()
            file.close()

        response = self.generate_response(prompt=prompt)

        object = json.loads(response.choices[0].message.content)
        if self.validate_response(object, ImageDescription):
            return ImageDescription(**object)
        return None

    def get_image_sentiment(self) -> ImageSentiment:
        if not self.is_valid_url(self.image):
            base64_string = self.img_to_base64(self.image)

        with open("prompts/sentiment_prompt.txt", "r") as file:
            prompt = file.read()
            file.close()

        response = self.generate_response(prompt=prompt)

        object = json.loads(response.choices[0].message.content)
        if self.validate_response(object, ImageSentiment):
            return ImageSentiment(**object)
        return None
