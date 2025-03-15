#!/usr/bin/env python3
"""
LLM utility module for the political analysis system.
Provides functions for interacting with the Mistral API.
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

# Load environment variables
load_dotenv()

# Mistral configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    logger.warning("MISTRAL_API_KEY not found in environment.")

# Import Mistral client
try:
    from mistralai.client import MistralClient

    logger.info("Successfully imported Mistral client")
except ImportError as e:
    logger.error(f"Failed to import Mistral client: {e}")
    sys.exit(1)


class LLMService:
    """Service for interacting with LLM APIs."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM service."""
        self.api_key = api_key or MISTRAL_API_KEY
        if not self.api_key:
            raise ValueError(
                "Mistral API key not provided or found in environment variables"
            )

        self.client = MistralClient(api_key=self.api_key)
        self.default_model = "mistral-large-latest"

    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
    ) -> Dict[str, Any]:
        """
        Send a query to the Mistral API.

        Args:
            prompt: The prompt to send
            model: The model to use (default: mistral-large-latest)
            temperature: Temperature setting (default: 0.1)
            max_tokens: Maximum tokens in response (default: 4000)

        Returns:
            Dict containing the response text and usage statistics
        """
        model = model or self.default_model
        logger.info(
            f"Querying Mistral API (model: {model}, temperature: {temperature})"
        )

        try:
            # For Mistral client 0.0.7, we need to use ChatMessage
            from mistralai.models.chat_completion import ChatMessage

            messages = [ChatMessage(role="user", content=prompt)]

            # Log what we're doing
            logger.info(f"Using ChatMessage format with version 0.0.7")

            response = self.client.chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response_text = response.choices[0].message.content
            usage = response.usage

            logger.info(
                f"Token usage - Input: {usage.prompt_tokens}, Output: {usage.completion_tokens}, Total: {usage.total_tokens}"
            )

            return {
                "text": response_text,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error(f"Error calling Mistral API: {e}")
            return {"error": str(e)}

    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse a JSON response from the LLM.

        Args:
            response_text: The text response from the LLM

        Returns:
            Parsed JSON object or error dict
        """
        try:
            # Attempt to find JSON in the response (handling cases where LLM adds extra text)
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)

            # Try parsing the entire response as JSON
            return json.loads(response_text)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return {
                "error": "Failed to parse response as JSON",
                "raw_response": response_text,
            }


def main():
    """Test the LLM service with simple test strings."""
    print("Testing the Mistral LLM service with simple examples")

    # Create the LLM service
    try:
        llm_service = LLMService()

        # Test 1: Basic joke
        joke_prompt = "Tell me a short joke about politics"
        print("\n--- TEST 1: Basic Joke ---")
        print(f"Prompt: {joke_prompt}")

        result = llm_service.query(
            prompt=joke_prompt,
            model="mistral-tiny",  # Using a smaller model for faster/cheaper testing
            temperature=0.7,  # Higher temperature for more creative responses
            max_tokens=100,
        )

        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("\n--- RESPONSE ---")
            print(result["text"])
            print(
                f"\nToken usage - Input: {result['usage']['prompt_tokens']}, Output: {result['usage']['completion_tokens']}, Total: {result['usage']['total_tokens']}"
            )

        # Test 2: Political analysis
        analysis_prompt = (
            "Summarize the main political issues in the EU in 2-3 sentences"
        )
        print("\n\n--- TEST 2: Political Analysis ---")
        print(f"Prompt: {analysis_prompt}")

        result = llm_service.query(
            prompt=analysis_prompt,
            model="mistral-tiny",  # Using a smaller model for faster/cheaper testing
            temperature=0.1,  # Lower temperature for more focused analysis
            max_tokens=100,
        )

        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("\n--- RESPONSE ---")
            print(result["text"])
            print(
                f"\nToken usage - Input: {result['usage']['prompt_tokens']}, Output: {result['usage']['completion_tokens']}, Total: {result['usage']['total_tokens']}"
            )

        print("\n--- Testing complete ---")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
