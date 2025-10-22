#!/usr/bin/env python3
"""
Complete example for Veo video generation through LiteLLM proxy.

This script demonstrates how to:
1. Generate videos using Google's Veo model
2. Poll for completion status
3. Download the generated video file

Requirements:
- LiteLLM proxy running with Google AI Studio pass-through configured
- Google AI Studio API key with Veo access

# This file is forked and adapted from: https://github.com/BerriAI/litellm/blob/main/docs/my-website/docs/proxy/veo_video_generation.md .Please refer to the original for license details.
"""

import json
import os
import time
import requests
from typing import Optional

from .settings import settings


class VeoVideoGenerator:
    """Complete Veo video generation client using LiteLLM proxy."""

    def __init__(
        self,
        base_url: str = f"{settings.ATC_BASE_URL}/gemini/v1beta",
        api_key: str = settings.ATC_API_KEY,
        *,
        duration_seconds: int = 8,
        aspect_ratio: str = "16:9",
        temperature: float = 0.7,
        generate_audio: bool = False,
        seed: Optional[int] = None,
    ):
        """
        Initialize the Veo video generator.

        Args:
            base_url: Base URL for the LiteLLM proxy with Gemini pass-through
            api_key: API key for LiteLLM proxy authentication
            duration_seconds: Length of the generated video in seconds
            aspect_ratio: Aspect ratio (e.g., "16:9", "9:16", "1:1")
            temperature: Creativity / randomness control (0.0–1.5)
            generate_audio: Whether to include generated audio
            seed: Random seed for reproducibility
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}

        # New initialization arguments
        self.duration_seconds = duration_seconds
        self.aspect_ratio = aspect_ratio
        self.seed = seed

    def generate_video(self, prompt: str) -> Optional[str]:
        """
        Initiate video generation with Veo.

        Args:
            prompt: Text description of the video to generate

        Returns:
            Operation name if successful, None otherwise
        """
        print(f"🎬 Generating video with prompt: '{prompt}'")

        url = f"{self.base_url}/models/veo-3.1-fast-generate-preview:predictLongRunning"

        # 🔧 Add parameters to payload
        parameters = {
            "aspectRatio": self.aspect_ratio,
        }
        if self.seed is not None:
            parameters["seed"] = self.seed

        # import base64

        # image_path_1 = "1.png"
        # with open(image_path_1, "rb") as f:
        #     image_content_1 = base64.b64encode(f.read()).decode("utf-8")

        # image_path_2 = "2.png"
        # with open(image_path_2, "rb") as f:
        #     image_content_2 = base64.b64encode(f.read()).decode("utf-8")

        # image_path_3 = "3.png"
        # with open(image_path_3, "rb") as f:
        #     image_content_3 = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "instances": [
                {
                    # "prompt": prompt,
                    "prompt": prompt,
                    #     "referenceImages": [
                    #         {
                    #             "image": {
                    #                 "bytesBase64Encoded": image_content_1,
                    #                 "mimeType": "image/jpeg",
                    #             },
                    #             "referenceType": "asset",
                    #         },
                    #         {
                    #             "image": {
                    #                 "bytesBase64Encoded": image_content_2,
                    #                 "mimeType": "image/jpeg",
                    #             },
                    #             "referenceType": "asset",
                    #         },
                    #         {
                    #             "image": {
                    #                 "bytesBase64Encoded": image_content_3,
                    #                 "mimeType": "image/jpeg",
                    #             },
                    #             "referenceType": "asset",
                    #         },
                    #     ],
                }
            ],
            "parameters": parameters,
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            data = response.json()
            operation_name = data.get("name")

            if operation_name:
                print(f"✅ Video generation started: {operation_name}")
                print("📦 Parameters used:")
                print(json.dumps(parameters, indent=2))
                return operation_name
            else:
                print("❌ No operation name returned")
                print(f"Response: {json.dumps(data, indent=2)}")
                return None

        except requests.RequestException as e:
            print(f"❌ Failed to start video generation: {e}")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                except Exception as e:
                    print(f"Error details: {e}")
                    print(f"Error response: {e.response.text}")
            return None

    def wait_for_completion(
        self, operation_name: str, max_wait_time: int = 600
    ) -> Optional[str]:
        """
        Poll operation status until video generation is complete.

        Args:
            operation_name: Name of the operation to monitor
            max_wait_time: Maximum time to wait in seconds (default: 10 minutes)

        Returns:
            Video URI if successful, None otherwise
        """
        print("⏳ Waiting for video generation to complete...")

        operation_url = f"{self.base_url}/{operation_name}"
        start_time = time.time()
        poll_interval = 10  # Start with 10 seconds

        while time.time() - start_time < max_wait_time:
            try:
                print(
                    f"🔍 Polling status... ({int(time.time() - start_time)}s elapsed)"
                )

                response = requests.get(operation_url, headers=self.headers)
                response.raise_for_status()

                data = response.json()

                # Check for errors
                if "error" in data:
                    print("❌ Error in video generation:")
                    print(json.dumps(data["error"], indent=2))
                    return None

                # Check if operation is complete
                is_done = data.get("done", False)

                if is_done:
                    print("🎉 Video generation complete!")

                    try:
                        # Extract video URI from nested response
                        video_uri = data["response"]["generateVideoResponse"][
                            "generatedSamples"
                        ][0]["video"]["uri"]
                        print(f"📹 Video URI: {video_uri}")
                        return video_uri
                    except KeyError as e:
                        print(f"❌ Could not extract video URI: {e}")
                        print("Full response:")
                        print(json.dumps(data, indent=2))
                        return None

                # Wait before next poll, with exponential backoff
                time.sleep(poll_interval)
                poll_interval = min(poll_interval * 1.2, 30)  # Cap at 30 seconds

            except requests.RequestException as e:
                print(f"❌ Error polling operation status: {e}")
                time.sleep(poll_interval)

        print(f"⏰ Timeout after {max_wait_time} seconds")
        return None

    def download_video(
        self, video_uri: str, output_filename: str = "outputs/generated_video.mp4"
    ) -> bool:
        """
        Download the generated video file.

        Args:
            video_uri: URI of the video to download (from Google's response)
            output_filename: Local filename to save the video

        Returns:
            True if download successful, False otherwise
        """
        print("⬇️  Downloading video...")
        print(f"Original URI: {video_uri}")

        # Convert Google URI to LiteLLM proxy URI
        # Example: https://generativelanguage.googleapis.com/v1beta/files/abc123 -> /gemini/download/v1beta/files/abc123:download?alt=media
        if video_uri.startswith("https://generativelanguage.googleapis.com/"):
            relative_path = video_uri.replace(
                "https://generativelanguage.googleapis.com/", ""
            )
        else:
            relative_path = video_uri

        # base_url: https://api.thucchien.ai/gemini/v1beta
        if self.base_url.endswith("/v1beta"):
            base_path = self.base_url.replace("/v1beta", "/download")
        else:
            base_path = self.base_url

        litellm_download_url = f"{base_path}/{relative_path}"
        print(f"Download URL: {litellm_download_url}")

        try:
            # Download with streaming and redirect handling
            response = requests.get(
                litellm_download_url,
                headers=self.headers,
                stream=True,
                allow_redirects=True,  # Handle redirects automatically
            )
            response.raise_for_status()

            # Save video file
            with open(output_filename, "wb") as f:
                downloaded_size = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Progress indicator for large files
                        if downloaded_size % (1024 * 1024) == 0:  # Every MB
                            print(
                                f"📦 Downloaded {downloaded_size / (1024*1024):.1f} MB..."
                            )

            # Verify file was created and has content
            if os.path.exists(output_filename):
                file_size = os.path.getsize(output_filename)
                if file_size > 0:
                    print("✅ Video downloaded successfully!")
                    print(f"📁 Saved as: {output_filename}")
                    print(f"📏 File size: {file_size / (1024*1024):.2f} MB")
                    return True
                else:
                    print("❌ Downloaded file is empty")
                    os.remove(output_filename)
                    return False
            else:
                print("❌ File was not created")
                return False

        except requests.RequestException as e:
            print(f"❌ Download failed: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Status code: {e.response.status_code}")
                print(f"Response headers: {dict(e.response.headers)}")
            return False

    def generate_and_download(self, prompt: str, output_filename: str = None) -> bool:
        """
        Complete workflow: generate video and download it.

        Args:
            prompt: Text description for video generation
            output_filename: Output filename (auto-generated if None)

        Returns:
            True if successful, False otherwise
        """
        # Auto-generate filename if not provided
        if output_filename is None:
            timestamp = int(time.time())
            safe_prompt = "".join(
                c for c in prompt[:30] if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            output_filename = (
                f"veo_video_{safe_prompt.replace(' ', '_')}_{timestamp}.mp4"
            )

        print("=" * 60)
        print("🎬 VEO VIDEO GENERATION WORKFLOW")
        print("=" * 60)

        # Step 1: Generate video
        operation_name = self.generate_video(prompt)
        if not operation_name:
            return False

        # Step 2: Wait for completion
        video_uri = self.wait_for_completion(operation_name)
        if not video_uri:
            return False

        # Step 3: Download video
        success = self.download_video(video_uri, output_filename)

        if success:
            print("=" * 60)
            print("🎉 SUCCESS! Video generation complete!")
            print(f"📁 Video saved as: {output_filename}")
            print("=" * 60)
        else:
            print("=" * 60)
            print("❌ FAILED! Video generation or download failed")
            print("=" * 60)

        return success
