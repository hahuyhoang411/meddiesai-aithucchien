import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()


class ImageGenerator:
    def __init__(self):
        self.imagen_api_key = os.getenv("IMAGEN_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

    def generate_imagen_image(self, prompt: str, output_path: str):
        if not self.imagen_api_key:
            raise ValueError("IMAGEN_API_KEY not set in environment variables.")
        
        # LiteLLM call for Imagen-4
        response = completion(
            model="google/imagen-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            api_key=self.imagen_api_key
        )
        
        # Assuming the response contains a URL to the generated image
        image_url = response.choices[0].message.content # This might need adjustment based on actual LiteLLM response structure
        
        # In a real scenario, you would download the image from the URL
        # For now, we'll just print the URL
        print(f"Imagen-4 image generated: {image_url}")
        # Placeholder for saving the image
        with open(output_path, "w") as f:
            f.write(f"Generated image URL: {image_url}")
        print(f"Imagen-4 image placeholder saved to {output_path}")

    def generate_gemini_image_with_reference(self, prompt: str, reference_image_url: str, output_path: str):
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables.")
        
        # LiteLLM call for Gemini-2.5-flash-image-preview with reference
        response = completion(
            model="gemini/gemini-2.5-flash-image-preview",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": reference_image_url}}
                ]}
            ],
            api_key=self.gemini_api_key
        )
        
        # Assuming the response contains a URL to the generated image
        image_url = response.choices[0].message.content # This might need adjustment based on actual LiteLLM response structure
        
        # In a real scenario, you would download the image from the URL
        # For now, we'll just print the URL
        print(f"Gemini-2.5-flash-image-preview image generated: {image_url}")
        # Placeholder for saving the image
        with open(output_path, "w") as f:
            f.write(f"Generated image URL: {image_url}")
        print(f"Gemini-2.5-flash-image-preview image placeholder saved to {output_path}")

if __name__ == "__main__":
    generator = ImageGenerator()

    # Example for Imagen-4
    imagen_prompt = "A futuristic city at sunset, vibrant colors, high detail"
    imagen_output_path = "outputs/imagen_output.txt"
    # generator.generate_imagen_image(imagen_prompt, imagen_output_path)

    # Example for Gemini-2.5-flash-image-preview with reference
    gemini_prompt = "Generate an image in the style of the reference image, depicting a serene forest with a hidden waterfall."
    reference_image_url = "https://example.com/reference_forest.jpg" # Replace with a real image URL
    gemini_output_path = "outputs/gemini_output.txt"
    # generator.generate_gemini_image_with_reference(gemini_prompt, reference_image_url, gemini_output_path)
