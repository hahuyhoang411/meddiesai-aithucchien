import json
import time
from core.gen_slide import gen_slide


def generate_slides_from_prompts(json_file_path: str):
    with open(json_file_path, "r", encoding="utf-8") as f:
        prompts_data = json.load(f)

    for slide_info in prompts_data:
        prompt = slide_info["prompt"]
        slide_number = slide_info["slide"]
        topic = slide_info["topic"]

        print(f"Generating image for Slide {slide_number}: {topic}")

        retries = 0
        max_retries = 5
        success = False

        while retries < max_retries and not success:
            try:
                gen_slide(prompt, slide_number)  # Pass slide_number here
                success = True
                print(f"Successfully generated image for Slide {slide_number}.")
            except Exception as e:
                retries += 1
                print(
                    f"Error generating image for Slide {slide_number} (Attempt {retries}/{max_retries}): {e}"
                )
                if retries < max_retries:
                    time.sleep(10)  # Wait for 5 seconds before retrying
                else:
                    print(
                        f"Failed to generate image for Slide {slide_number} after {max_retries} attempts."
                    )
        print("-" * 50)


if __name__ == "__main__":
    generate_slides_from_prompts("prompt_no_text.json")
