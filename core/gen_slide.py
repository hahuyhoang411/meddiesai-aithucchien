import datetime
import base64
from openai import OpenAI


from .settings import settings

client = OpenAI(api_key=settings.ATC_API_KEY, base_url=settings.ATC_BASE_URL)

TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "imagen-4"
TEXT_TO_SPEECH_MODEL = "gemini-2.5-pro-preview-tts"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")


def gen_slide(prompt: str):
    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        n=1,
    )
    for i, image_obj in enumerate(response.data):
        b64_data = image_obj.b64_json
        saved_path = f"outputs/generated_image_{timestamp}_{i + 1}.png"
        with open(saved_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        print(f"Saved image to {saved_path}")
