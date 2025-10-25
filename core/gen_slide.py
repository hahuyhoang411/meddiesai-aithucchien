import datetime
import base64
from openai import OpenAI


from .settings import settings

client = OpenAI(api_key=settings.ATC_API_KEY, base_url=settings.ATC_BASE_URL)

IMAGE_MODEL = "imagen-4"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

TRIAL_FOLDER = "trial_4"
import os

os.makedirs(f"outputs/{TRIAL_FOLDER}", exist_ok=True)


def gen_slide(prompt: str, slide_number: int):
    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt
        + "\n\n **IMPORTANT:** Make sure Vietnamese text is spelled correctly. IMAGE MUST HAVE ASPECT RATIO AS 4:3 LANDSCAPE.",
        n=4,
        size="1536x1024",
    )
    for i, image_obj in enumerate(response.data):
        b64_data = image_obj.b64_json
        saved_path = f"outputs/{TRIAL_FOLDER}/slides_{slide_number}_version_{i + 1}.png"
        with open(saved_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        print(f"Saved image to {saved_path}")
