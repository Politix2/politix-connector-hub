#!/usr/bin/env python3
"""
Topic analyzer service for extracting relevant content from plenary sessions and tweets.
This service uses an LLM to find, extract, and summarize content related to specific topics.
"""

import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from loguru import logger

from supabase import create_client

# Import Mistral client
try:
    from mistralai.client import MistralClient

    logger.info("Successfully imported Mistral client")
except ImportError as e:
    logger.error(f"Failed to import Mistral client: {e}")
    sys.exit(1)

# Configure Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Configure Mistral client
mistral_api_key = os.getenv("MISTRAL_API_KEY")
mistral_client = MistralClient(api_key=mistral_api_key)


class TopicAnalyzer:
    """Service for analyzing plenary sessions and tweets for relevant topic content."""

    def __init__(self):
        """Initialize the topic analyzer service."""
        self.model_name = "mistral-large-latest"
        self.max_tokens = 4096
        self.temperature = 0.1  # Low temperature for more focused, analytical responses

    def fetch_topic_details(self, topic_id: str) -> Dict[str, Any]:
        """Fetch details about a specific topic."""
        response = supabase.table("topics").select("*").eq("id", topic_id).execute()

        if not response.data:
            raise ValueError(f"Topic with ID {topic_id} not found")

        return response.data[0]

    def fetch_plenary_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch plenary sessions from the database."""
        response = supabase.table("plenary_sessions").select("*").limit(limit).execute()
        return response.data

    def fetch_tweets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch tweets from the database."""
        response = supabase.table("tweets").select("*").limit(limit).execute()
        return response.data

    def create_analysis_prompt(
        self,
        topic: Dict[str, Any],
        sessions: List[Dict[str, Any]],
        tweets: List[Dict[str, Any]],
    ) -> str:
        """
        Create a prompt for the LLM to analyze content related to a specific topic.
        """
        # Format the topic information
        topic_info = f"Topic: {topic['name']}\nDescription: {topic['description'] or 'N/A'}\nKeywords: {', '.join(topic['keywords'])}\n\n"

        # Format plenary sessions
        sessions_text = "--- PLENARY SESSIONS ---\n"
        for i, session in enumerate(sessions):
            sessions_text += (
                f"[Session {i + 1}] {session['title']} ({session['date']})\n"
            )
            sessions_text += f"Content: {session['content'][:1000]}...\n\n"

        # Format tweets
        tweets_text = "--- TWEETS ---\n"
        for i, tweet in enumerate(tweets):
            tweets_text += (
                f"[Tweet {i + 1}] @{tweet['user_handle']} ({tweet['posted_at']})\n"
            )
            tweets_text += f"Content: {tweet['content']}\n\n"

        # Create the instruction prompt
        instruction = f"""
You are a political analyst assistant tasked with finding and analyzing content related to specific political topics.

TASK:
1. Find and extract ALL relevant text from the plenary sessions and tweets that is connected to the given topic.
2. For each relevant extract, provide the source (session or tweet ID).
3. Analyze what political opinions, positions, and sentiments are expressed about this topic.
4. Summarize the overall discourse around this topic.
5. Provide context about why this topic is politically significant based on the content.

Format your response as a structured JSON with the following keys:
- "relevant_extracts": List of found relevant text segments with source IDs
- "opinions": Analysis of different political opinions expressed
- "summary": Overall summary of discourse
- "context": Political context and significance
- "sentiment": Overall sentiment (positive, negative, neutral, mixed)
- "key_stakeholders": Key politicians or parties mentioned in relation to the topic

{topic_info}

THE CONTENT TO ANALYZE:

{sessions_text}

{tweets_text}
"""
        return instruction

    def analyze_topic(self, topic_id: str) -> Dict[str, Any]:
        """
        Analyze content related to a specific topic and store the result.
        """
        # Fetch data
        topic = self.fetch_topic_details(topic_id)
        sessions = self.fetch_plenary_sessions()
        tweets = self.fetch_tweets()

        # Create prompt
        prompt = self.create_analysis_prompt(topic, sessions, tweets)

        # Call LLM
        logger.info(f"Analyzing topic: {topic['name']}")

        # Use ChatMessage for Mistral client 0.0.7
        from mistralai.models.chat_completion import ChatMessage

        response = mistral_client.chat(
            model=self.model_name,
            messages=[ChatMessage(role="user", content=prompt)],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        analysis_text = response.choices[0].message.content

        # Process the response (assuming it's properly formatted JSON)
        # In a production system, we should add error handling for malformed responses
        import json

        try:
            analysis_data = json.loads(analysis_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, save the raw response
            analysis_data = {"raw_response": analysis_text}

        # Store result in database
        analysis_record = {
            "topic_id": topic_id,
            "analysis_data": analysis_data,
            "relevant_extracts": analysis_data.get("relevant_extracts", []),
            "summary": analysis_data.get("summary", ""),
            "sentiment": analysis_data.get("sentiment", ""),
            "analyzed_at": datetime.now().isoformat(),
        }

        # Store in database
        response = supabase.table("topic_analyses").insert(analysis_record).execute()

        if response.data:
            logger.info(f"Analysis stored successfully for topic: {topic['name']}")
            return analysis_record
        else:
            logger.error(f"Failed to store analysis for topic: {topic['name']}")
            return None

    def get_analyses_for_topic(self, topic_id: str) -> List[Dict[str, Any]]:
        """Get all analyses for a specific topic."""
        response = (
            supabase.table("topic_analyses")
            .select("*")
            .eq("topic_id", topic_id)
            .execute()
        )
        return response.data


def main():
    """
    Run the topic analyzer directly from command line.
    """
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Run the topic analyzer")
    parser.add_argument("topic_id", help="ID of the topic to analyze")
    parser.add_argument(
        "--sessions",
        type=int,
        default=5,
        help="Number of plenary sessions to analyze (default: 5)",
    )
    parser.add_argument(
        "--tweets",
        type=int,
        default=10,
        help="Number of tweets to analyze (default: 10)",
    )
    parser.add_argument(
        "--show-prompt", action="store_true", help="Display the generated prompt"
    )
    parser.add_argument(
        "--show-extracts",
        type=int,
        default=3,
        help="Number of extracts to display (default: 3)",
    )
    parser.add_argument(
        "--only-prompt",
        action="store_true",
        help="Only generate and show the prompt, don't run analysis",
    )

    args = parser.parse_args()

    try:
        # Initialize the analyzer
        analyzer = TopicAnalyzer()

        # Fetch the topic details
        try:
            topic = analyzer.fetch_topic_details(args.topic_id)
            print(f"\nTopic: {topic['name']}")
            print(f"Description: {topic['description'] or 'N/A'}")
            print(f"Keywords: {', '.join(topic['keywords'])}")
        except ValueError as e:
            print(f"Error: Topic not found - {e}")
            return 1

        # Fetch the data for analysis
        sessions = analyzer.fetch_plenary_sessions(limit=args.sessions)
        print(f"\nFetched {len(sessions)} plenary sessions")

        tweets = analyzer.fetch_tweets(limit=args.tweets)
        print(f"Fetched {len(tweets)} tweets")

        # Generate the prompt
        prompt = analyzer.create_analysis_prompt(topic, sessions, tweets)

        # Show the prompt if requested
        if args.show_prompt or args.only_prompt:
            print("\n--- ANALYSIS PROMPT ---\n")
            print(prompt)
            print("\n--- END PROMPT ---\n")

        # Exit if only showing the prompt
        if args.only_prompt:
            return 0

        # Run the analysis
        print("\nRunning analysis...")

        result = analyzer.analyze_topic(args.topic_id)

        if not result:
            print("Error: Analysis failed")
            return 1

        # Display the results
        print("\n=== ANALYSIS RESULTS ===\n")

        print(f"Analysis ID: {result.get('id', 'Unknown')}")
        print(f"Analyzed at: {result.get('analyzed_at', 'Unknown')}")

        print("\n--- SUMMARY ---")
        print(result.get("summary", "No summary available"))

        print("\n--- SENTIMENT ---")
        print(result.get("sentiment", "No sentiment available"))

        # Show the detailed analysis data
        if "analysis_data" in result:
            analysis_data = result["analysis_data"]

            # Show key stakeholders
            if "key_stakeholders" in analysis_data:
                print("\n--- KEY STAKEHOLDERS ---")
                for stakeholder in analysis_data["key_stakeholders"]:
                    print(f"- {stakeholder}")

            # Show opinions
            if "opinions" in analysis_data:
                print("\n--- OPINIONS ---")
                print(analysis_data["opinions"])

            # Show political context
            if "context" in analysis_data:
                print("\n--- POLITICAL CONTEXT ---")
                print(analysis_data["context"])

            # Show extracts
            if "relevant_extracts" in analysis_data:
                extracts = analysis_data["relevant_extracts"]
                limit = min(len(extracts), args.show_extracts)

                print(
                    f"\n--- RELEVANT EXTRACTS ({len(extracts)} found, showing {limit}) ---"
                )
                for i, extract in enumerate(extracts[:limit]):
                    print(f"\nExtract {i + 1} from {extract.get('source', 'unknown')}")
                    print("-" * 40)
                    print(extract.get("text", "No text"))
                    print("-" * 40)

            # Show the full JSON if there are other keys
            other_keys = set(analysis_data.keys()) - {
                "key_stakeholders",
                "opinions",
                "context",
                "relevant_extracts",
                "summary",
                "sentiment",
            }
            if other_keys:
                print("\n--- OTHER DATA ---")
                other_data = {k: analysis_data[k] for k in other_keys}
                print(json.dumps(other_data, indent=2))

        print("\nAnalysis completed and stored in database.")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
