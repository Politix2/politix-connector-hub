import json
from typing import Any, Dict, List, Optional

from loguru import logger
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from app.config import MISTRAL_API_KEY


class MistralAI:
    """Client for interacting with Mistral AI's API."""

    def __init__(self):
        self.client = MistralClient(api_key=MISTRAL_API_KEY)
        self.model = "mistral-large-latest"  # Using the latest model
        logger.info("Mistral AI client initialized")

    def analyze_topics(self, text: str) -> Dict[str, Any]:
        """Analyze topics in the given text using Mistral AI."""
        system_prompt = """
        You are an expert political analyst. Analyze the following text and identify the main political topics,
        sentiment, and key political entities mentioned. Format your response as JSON with the following structure:
        {
            "topics": ["topic1", "topic2", ...],
            "sentiment": "positive|negative|neutral",
            "keywords": ["keyword1", "keyword2", ...],
            "summary": "A brief summary of the content"
        }
        Only respond with the JSON, no other text.
        """

        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=text),
        ]

        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Lower temperature for more deterministic results
                max_tokens=500,
            )

            # Extract and parse the JSON response
            json_text = response.choices[0].message.content
            # Clean up the response in case it has markdown formatting
            json_text = json_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_result = json.loads(json_text)
                return analysis_result
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response: {json_text}")
                return {
                    "topics": [],
                    "sentiment": "neutral",
                    "keywords": [],
                    "summary": "Failed to analyze content",
                }

        except Exception as e:
            logger.error(f"Error calling Mistral AI: {e}")
            return {
                "topics": [],
                "sentiment": "neutral",
                "keywords": [],
                "summary": "Error analyzing content",
            }

    def compare_topics(self, text1: str, text2: str) -> Dict[str, Any]:
        """Compare topics between two texts."""
        system_prompt = """
        You are an expert political analyst. Compare the following two texts and identify the similarities and differences 
        in the political topics discussed. Format your response as JSON with the following structure:
        {
            "common_topics": ["topic1", "topic2", ...],
            "unique_to_text1": ["topic1", "topic2", ...],
            "unique_to_text2": ["topic1", "topic2", ...],
            "summary": "A brief summary of the comparison"
        }
        Only respond with the JSON, no other text.
        """

        prompt = f"""
        TEXT 1:
        {text1}
        
        TEXT 2:
        {text2}
        """

        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=prompt),
        ]

        try:
            response = self.client.chat(
                model=self.model, messages=messages, temperature=0.1, max_tokens=500
            )

            # Extract and parse the JSON response
            json_text = response.choices[0].message.content
            # Clean up the response in case it has markdown formatting
            json_text = json_text.replace("```json", "").replace("```", "").strip()

            try:
                comparison_result = json.loads(json_text)
                return comparison_result
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response: {json_text}")
                return {
                    "common_topics": [],
                    "unique_to_text1": [],
                    "unique_to_text2": [],
                    "summary": "Failed to compare content",
                }

        except Exception as e:
            logger.error(f"Error calling Mistral AI: {e}")
            return {
                "common_topics": [],
                "unique_to_text1": [],
                "unique_to_text2": [],
                "summary": "Error comparing content",
            }


# Singleton Mistral AI client
llm = MistralAI()
