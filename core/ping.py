import datetime
import click
import base64
from openai import OpenAI


from .settings import settings
from .gen_video import VeoVideoGenerator

client = OpenAI(api_key=settings.ATC_API_KEY, base_url=settings.ATC_BASE_URL)

TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "imagen-4"
TEXT_TO_SPEECH_MODEL = "gemini-2.5-pro-preview-tts"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")


@click.command()
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["text", "image", "video", "text2speech"]),
    default="text",
)
def main(mode: str):
    if mode == "text":
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[{"role": "user", "content": "PING!"}],
        )
        print(response.choices[0].message.content)
    elif mode == "image":
        prompt = "A vibrant and festive Lunar New Year 2026 (Year of the Horse) cover image. Dominant colors are auspicious red and gold. Features traditional Vietnamese Tết elements like blooming peach blossoms (hoa đào), kumquat trees (cây quất), and decorative red envelopes (lì xì). In the foreground, subtly integrated with modern elegance, is the Techcombank logo. The overall mood is prosperous, hopeful, and celebratory, with a touch of modern financial sophistication. Text overlay: 'TẾT AN KHANG, SINH LỜI VÀNG CÙNG TECHCOMBANK' (large, prominent), 'Techcombank Sinh Lời Tự Động' (medium), 'Chào đón Tết Nguyên Đán 2026' (smaller)."
        response = client.images.generate(
            model=IMAGE_MODEL,
            # prompt="A beautiful image of a cat",
            prompt=prompt,
            n=1,
        )
        for i, image_obj in enumerate(response.data):
            b64_data = image_obj.b64_json
            saved_path = f"outputs/generated_image_{timestamp}_{i + 1}.png"
            with open(saved_path, "wb") as f:
                f.write(base64.b64decode(b64_data))
            print(f"Saved image to {saved_path}")
    elif mode == "video":
        video_generator = VeoVideoGenerator()
        result = video_generator.generate_and_download(
            prompt="A cat is playing in the garden with a dog",
            output_filename=f"outputs/generated_video_{timestamp}.mp4",
        )
        print(f"Video generation {'successful' if result else 'failed'}")
    elif mode == "text2speech":
        voice = "alloy"
        response = client.audio.speech.create(
            model=TEXT_TO_SPEECH_MODEL,
            input="Chúng tôi sẽ tiến vào vòng 3 của chương trình Thực Chiến AI 2025!",
            voice=voice,
        )
        speech_file_path = f"outputs/generated_speech_{timestamp}_{voice}.mp3"
        response.write_to_file(speech_file_path)
        print(f"Saved speech to {speech_file_path}")


if __name__ == "__main__":
    main()
