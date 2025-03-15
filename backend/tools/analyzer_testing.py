#!/usr/bin/env python3
"""
Test script for the topic analyzer and Mistral API.
This script provides functions to quickly test different parts of the analysis system.

Usage:
  python analyzer_testing.py mistral "Your prompt here"
  python analyzer_testing.py topic <topic_id>
  python analyzer_testing.py help
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from loguru import logger
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Add the parent directory to the Python path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.topic_analyzer import TopicAnalyzer

# Configure logger
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

# Load environment variables
load_dotenv()

# Mistral configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    logger.error(
        "MISTRAL_API_KEY not found in environment. Please check your .env file."
    )
    sys.exit(1)


def test_mistral_query(
    prompt: str,
    model: str = "mistral-large-latest",
    temperature: float = 0.1,
    max_tokens: int = 1000,
) -> Dict[str, Any]:
    """
    Test a direct query to the Mistral API.

    Args:
        prompt: The prompt to send to Mistral
        model: The model to use (default: mistral-large-latest)
        temperature: Temperature setting (default: 0.1)
        max_tokens: Maximum tokens in response (default: 1000)

    Returns:
        The response from Mistral
    """
    logger.info(
        f"Sending prompt to Mistral API (model: {model}, temperature: {temperature})"
    )

    mistral_client = MistralClient(api_key=MISTRAL_API_KEY)

    # Simple wrapping of the prompt in a chat message
    messages = [ChatMessage(role="user", content=prompt)]

    # Call the API
    try:
        response = mistral_client.chat(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Extract the response text and return more useful info
        response_text = response.choices[0].message.content
        usage = response.usage

        # Log token usage
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


def test_topic_analyzer(
    topic_id: str,
    limit_sessions: int = 5,
    limit_tweets: int = 10,
    display_prompt: bool = False,
) -> Dict[str, Any]:
    """
    Test the topic analyzer on a specific topic.

    Args:
        topic_id: The UUID of the topic to analyze
        limit_sessions: Limit of plenary sessions to include (default: 5)
        limit_tweets: Limit of tweets to include (default: 10)
        display_prompt: Whether to display the generated prompt (default: False)

    Returns:
        The analysis result
    """
    logger.info(f"Testing topic analyzer for topic ID: {topic_id}")

    try:
        # Initialize the analyzer
        analyzer = TopicAnalyzer()

        # Try to get topic details
        try:
            topic = analyzer.fetch_topic_details(topic_id)
            logger.info(f"Found topic: {topic['name']}")
            logger.info(f"Description: {topic['description'] or 'N/A'}")
            logger.info(f"Keywords: {', '.join(topic['keywords'])}")
        except ValueError as e:
            logger.error(f"Topic not found: {e}")
            try:
                from app.db import db

                topics = db.get_topics()
                if topics:
                    logger.info("Available topics:")
                    for t in topics:
                        logger.info(f"- ID: {t.id}, Name: {t.name}")
                else:
                    logger.info("No topics found in the database.")
            except Exception as list_err:
                logger.error(f"Could not list topics: {list_err}")
            return {"error": str(e)}

        # Fetch data for analysis
        sessions = analyzer.fetch_plenary_sessions(limit=limit_sessions)
        logger.info(f"Fetched {len(sessions)} plenary sessions")

        tweets = analyzer.fetch_tweets(limit=limit_tweets)
        logger.info(f"Fetched {len(tweets)} tweets")

        # Generate the prompt
        prompt = analyzer.create_analysis_prompt(topic, sessions, tweets)

        # Optionally display the prompt
        if display_prompt:
            logger.info("\n--- PROMPT ---\n")
            logger.info(prompt)
            logger.info("\n--- END PROMPT ---\n")

        # Run the analysis
        logger.info("Running analysis...")
        result = analyzer.analyze_topic(topic_id)

        if result:
            logger.info("Analysis completed successfully!")
            logger.info(f"Summary: {result.get('summary', 'No summary available')}")
            logger.info(
                f"Sentiment: {result.get('sentiment', 'No sentiment available')}"
            )
            logger.info(f"Analysis stored with ID: {result.get('id', 'Unknown')}")

            # Pretty print the analysis data
            if "analysis_data" in result:
                analysis_data = result["analysis_data"]
                logger.info("\nAnalysis Data:")

                # Print key stakeholders
                if "key_stakeholders" in analysis_data:
                    logger.info("\nKey Stakeholders:")
                    for stakeholder in analysis_data["key_stakeholders"]:
                        logger.info(f"- {stakeholder}")

                # Print relevant extracts (first 3)
                if "relevant_extracts" in analysis_data:
                    extracts = analysis_data["relevant_extracts"]
                    logger.info(
                        f"\nRelevant Extracts: ({len(extracts)} found, showing first 3)"
                    )
                    for i, extract in enumerate(extracts[:3]):
                        logger.info(
                            f"Extract {i + 1} from {extract.get('source', 'unknown')}:"
                        )
                        logger.info(f"{extract.get('text', 'No text')}")
                        logger.info("---")

                # Print opinions
                if "opinions" in analysis_data:
                    logger.info("\nOpinions:")
                    logger.info(analysis_data["opinions"])

                # Print context
                if "context" in analysis_data:
                    logger.info("\nContext:")
                    logger.info(analysis_data["context"])

            return result
        else:
            logger.error("Analysis failed")
            return {"error": "Analysis failed"}

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return {"error": str(e)}


def main():
    """
    Main function to parse arguments and run the appropriate test.
    """
    parser = argparse.ArgumentParser(description="Test the topic analyzer system")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Mistral command
    mistral_parser = subparsers.add_parser(
        "mistral", help="Test a direct Mistral query"
    )
    mistral_parser.add_argument("prompt", help="The prompt to send to Mistral")
    mistral_parser.add_argument(
        "--model", default="mistral-large-latest", help="Model to use"
    )
    mistral_parser.add_argument(
        "--temperature", type=float, default=0.1, help="Temperature setting"
    )
    mistral_parser.add_argument(
        "--max-tokens", type=int, default=1000, help="Maximum tokens in response"
    )

    # Topic analyzer command
    topic_parser = subparsers.add_parser("topic", help="Test the topic analyzer")
    topic_parser.add_argument("topic_id", help="The UUID of the topic to analyze")
    topic_parser.add_argument(
        "--sessions", type=int, default=5, help="Limit of plenary sessions"
    )
    topic_parser.add_argument("--tweets", type=int, default=10, help="Limit of tweets")
    topic_parser.add_argument(
        "--show-prompt", action="store_true", help="Display the generated prompt"
    )

    # Parse the arguments
    args = parser.parse_args()

    # If no command is given, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Run the appropriate test
    if args.command == "mistral":
        result = test_mistral_query(
            prompt=args.prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )

        # Display the Mistral response
        if "error" in result:
            logger.error(f"Error: {result['error']}")
        else:
            logger.info("\n--- MISTRAL RESPONSE ---\n")
            logger.info(result["text"])
            logger.info("\n--- END RESPONSE ---\n")

    elif args.command == "topic":
        result = test_topic_analyzer(
            topic_id=args.topic_id,
            limit_sessions=args.sessions,
            limit_tweets=args.tweets,
            display_prompt=args.show_prompt,
        )

        # Result handling is done in the function
        if "error" in result:
            logger.error(f"Error: {result['error']}")

    else:
        logger.error(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
